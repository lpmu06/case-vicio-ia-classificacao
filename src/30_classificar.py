"""Etapa 3: classificação por LLM, uma chamada por questão, com árvore + metadados no system prompt (cacheado).

Uso: python src/30_classificar.py --provedor openai --modelo gpt-5.5 [--effort medium] [--limite 3] [--ids Q0001,Q0002]
     python src/30_classificar.py --provedor claude_cli --modelo opus
Saída: runs/<rotulo>/<id>.json (uma por questão; reexecução pula as já feitas) e runs/<rotulo>/_usage.json
"""
import argparse, importlib, json, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from llm import chamar_json
arv = importlib.import_module("10_arvore")

RAIZ = Path(__file__).resolve().parents[1]

ESQUEMA = {
    "type": "object",
    "properties": {
        "fora": {"type": "boolean"},
        "tema_n1_id": {"type": ["string", "null"]},
        "subtema_n2_id": {"type": ["string", "null"]},
        "confianca_ramo": {"type": "number"},
        "confianca_subtema": {"type": "number"},
        "segunda_opcao_id": {"type": ["string", "null"]},
        "extras_ids": {"type": "array", "items": {"type": "string"}},
        "multi_tema": {"type": "boolean"},
        "justificativa": {"type": "string"},
    },
    "required": ["fora", "tema_n1_id", "subtema_n2_id", "confianca_ramo", "confianca_subtema",
                 "segunda_opcao_id", "extras_ids", "multi_tema", "justificativa"],
    "additionalProperties": False,
}

def montar_sistema(temas):
    enr_path = RAIZ / "data" / "temas_enriquecidos.json"
    enr = json.loads(enr_path.read_text(encoding="utf-8")) if enr_path.exists() else {}
    blocos = []
    for t in temas.values():
        if t["nivel"] == 0 or t["status"] != "active" or t["bucket"]:
            continue
        e = enr.get(t["tema_id"])
        if not e:
            continue
        blocos.append(
            f"[{t['tema_id']}] {t['caminho']}\n"
            f"  descrição: {e.get('descricao', '')}\n"
            f"  palavras-chave: {', '.join(e.get('palavras_chave', []))}\n"
            f"  dispositivos: {', '.join(e.get('dispositivos', []))}\n"
            f"  não confundir: {e.get('nao_confundir', '')}")
    modelo = (RAIZ / "prompts" / "classificar_sistema.md").read_text(encoding="utf-8")
    return modelo.replace("{arvore}", arv.arvore_texto(temas)).replace("{metadados}", "\n\n".join(blocos)), len(enr)

def montar_pedido(q):
    return (f"Questão {q['id']}\n"
            f"disciplina_origem (pista fraca): {q['disciplina_origem'] or '-'}\n"
            f"assunto_origem (pista fraca): {q['assunto_origem'] or '-'}\n"
            f"tipo: {q['tipo']}\n\n<questao>\n{q['texto']}\n</questao>")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provedor", choices=["anthropic", "openai", "claude_cli"], required=True)
    ap.add_argument("--modelo", required=True)
    ap.add_argument("--rotulo", default=None, help="nome da pasta em runs/ (padrão: modelo)")
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--limite", type=int, default=None)
    ap.add_argument("--ids", default=None)
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()

    temas = arv.carregar_temas()
    sistema, n_enr = montar_sistema(temas)
    qs = [json.loads(l) for l in (RAIZ / "data" / "questoes_limpas.jsonl").open(encoding="utf-8")]
    if a.ids:
        qs = [q for q in qs if q["id"] in a.ids.split(",")]
    if a.limite:
        qs = qs[:a.limite]
    pasta = RAIZ / "runs" / (a.rotulo or a.modelo)
    pasta.mkdir(parents=True, exist_ok=True)
    pendentes = [q for q in qs if not (pasta / f"{q['id']}.json").exists()]
    print(f"provedor={a.provedor} modelo={a.modelo} effort={a.effort} temas enriquecidos={n_enr} "
          f"sistema={len(sistema)} chars; {len(pendentes)} pendentes de {len(qs)}", flush=True)

    uso = {"in": 0, "out": 0, "cache_w": 0, "cache_r": 0, "custo_usd": 0.0}
    erros, t0 = [], time.time()

    def tarefa(q):
        dados, u = chamar_json(a.provedor, a.modelo, sistema, montar_pedido(q), ESQUEMA, a.effort)
        dados.update({"id": q["id"], "modelo": a.modelo, "provedor": a.provedor, "effort": a.effort, "uso": u})
        (pasta / f"{q['id']}.json").write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
        return q["id"], u

    def acumular(u):
        for k in ("in", "out", "cache_w", "cache_r"):
            uso[k] += u.get(k, 0) or 0
        uso["custo_usd"] += u.get("custo_usd") or 0.0

    if pendentes:  # primeira chamada sozinha: grava o cache antes das paralelas
        qid, u = tarefa(pendentes[0])
        acumular(u)
        print(f"[1/{len(pendentes)}] {qid} ok uso={u}", flush=True)
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(tarefa, q): q for q in pendentes[1:]}
        for i, f in enumerate(as_completed(futs), 2):
            q = futs[f]
            try:
                qid, u = f.result()
                acumular(u)
                if i % 10 == 0 or i == len(pendentes):
                    print(f"[{i}/{len(pendentes)}] {qid} ok", flush=True)
            except Exception as e:
                erros.append({"id": q["id"], "erro": re.sub(r"org-[A-Za-z0-9]+", "org-REDACTED", repr(e))[:400]})
                print(f"ERRO {q['id']}: {e!r}"[:300], flush=True)

    resumo_path = pasta / "_usage.json"
    antigo = (json.loads(resumo_path.read_text(encoding="utf-8")) if resumo_path.exists()
              else {"uso": {k: 0 for k in uso}, "segundos": 0})
    for k in uso:
        antigo["uso"][k] = antigo["uso"].get(k, 0) + uso[k]
    antigo.update({"segundos": antigo["segundos"] + round(time.time() - t0), "erros": erros,
                   "modelo": a.modelo, "provedor": a.provedor, "effort": a.effort})
    resumo_path.write_text(json.dumps(antigo, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"fim: uso acumulado={antigo['uso']} segundos={antigo['segundos']} erros={len(erros)}")

if __name__ == "__main__":
    main()
