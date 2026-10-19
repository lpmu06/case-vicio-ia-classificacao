"""Etapa 1b: enriquece a taxonomia com um LLM (uma vez só).

Para cada tema de nível 1 ativo (com seus subtemas), pede ao modelo: descrição de 2–3 linhas,
palavras-chave, dispositivos legais cobertos e "não confundir com" (fronteiras com irmãos).
Temas inativos e buckets de curso não são enriquecidos (nunca recebem publicação).

Uso: python src/11_enriquecer_temas.py --provedor openai --modelo gpt-5.5 [--effort medium]
Saída: data/temas_enriquecidos.json ; uso e custo em runs/11_enriquecer_usage.json
"""
import argparse, importlib, json, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from llm import chamar_json
arv = importlib.import_module("10_arvore")

RAIZ = Path(__file__).resolve().parents[1]

SISTEMA = """Você é um professor de Direito Penal, Processo Penal, Legislação Penal Especial e Criminologia, com experiência em concursos públicos e exame da OAB no Brasil, ajudando a organizar a taxonomia de uma plataforma de questões.

A árvore completa de temas da plataforma é esta (id | título; indentação = hierarquia):

<arvore>
{arvore}
</arvore>

Sua tarefa: para cada tema pedido, escrever metadados que permitam a uma pessoa ou a um modelo decidir com segurança se uma questão de concurso pertence a ele e, principalmente, distingui-lo dos temas vizinhos.

Para cada tema:
- descricao: 2 a 3 frases sobre o que o tema cobre, na prática das provas;
- palavras_chave: 8 a 15 termos e expressões típicos de enunciados sobre este tema;
- dispositivos: artigos de lei, leis e súmulas centrais (ex.: "art. 155 CP", "Lei 11.343/2006", "Súmula 582 STJ");
- nao_confundir: 1 a 3 frases dizendo com quais temas vizinhos (cite os ids) costuma ser confundido e qual é o critério de desempate.

Responda no esquema JSON fornecido, com um item por id pedido, exatamente os ids pedidos."""

ESQUEMA = {
    "type": "object",
    "properties": {
        "temas": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "tema_id": {"type": "string"},
                    "descricao": {"type": "string"},
                    "palavras_chave": {"type": "array", "items": {"type": "string"}},
                    "dispositivos": {"type": "array", "items": {"type": "string"}},
                    "nao_confundir": {"type": "string"},
                },
                "required": ["tema_id", "descricao", "palavras_chave", "dispositivos", "nao_confundir"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["temas"],
    "additionalProperties": False,
}

def montar_pedido(temas, t1):
    ok = lambda t: t["status"] == "active" and not t["bucket"]
    filhos = [temas[f] for f in t1["filhos"] if ok(temas[f])]
    irmaos = [temas[s] for s in temas[t1["parent_id"]]["filhos"] if s != t1["tema_id"] and ok(temas[s])]
    ids = [t1["tema_id"]] + [f["tema_id"] for f in filhos]
    linhas = [f"Disciplina: {t1['disciplina']}", f"Tema (nível 1): {t1['tema_id']} | {t1['titulo']}"]
    if filhos:
        linhas.append("Subtemas (nível 2) deste tema:")
        linhas += [f"  {f['tema_id']} | {f['titulo']}" for f in filhos]
    linhas.append("Outros temas de nível 1 da mesma disciplina (para o 'não confundir'):")
    linhas += [f"  {s['tema_id']} | {s['titulo']}" for s in irmaos]
    linhas.append(f"\nEscreva os metadados para estes ids: {', '.join(ids)}")
    return "\n".join(linhas), ids

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provedor", choices=["anthropic", "openai", "claude_cli"], required=True)
    ap.add_argument("--modelo", required=True)
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()

    temas = arv.carregar_temas()
    sistema = SISTEMA.format(arvore=arv.arvore_texto(temas))
    alvos = [t for t in temas.values() if t["nivel"] == 1 and t["status"] == "active" and not t["bucket"]]
    saida_path = RAIZ / "data" / "temas_enriquecidos.json"
    saida = json.loads(saida_path.read_text(encoding="utf-8")) if saida_path.exists() else {}
    alvos = [t for t in alvos if t["tema_id"] not in saida]
    uso_total = {"in": 0, "out": 0, "cache_w": 0, "cache_r": 0, "custo_usd": 0.0}
    erros, t0 = [], time.time()
    print(f"{len(alvos)} temas de nível 1 a enriquecer com {a.modelo}", flush=True)

    def tarefa(t1):
        pedido, ids = montar_pedido(temas, t1)
        dados, u = chamar_json(a.provedor, a.modelo, sistema, pedido, ESQUEMA, a.effort, max_tokens=12000)
        return t1, ids, dados, u

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = [ex.submit(tarefa, t1) for t1 in alvos]
        for i, fut in enumerate(as_completed(futs), 1):
            try:
                t1, ids, dados, u = fut.result()
                for item in dados["temas"]:
                    if item["tema_id"] in temas:
                        saida[item["tema_id"]] = {k: v for k, v in item.items() if k != "tema_id"}
                faltam = [x for x in ids if x not in saida]
                if faltam:
                    erros.append({"tema": t1["tema_id"], "faltam": faltam})
                for k in ("in", "out", "cache_w", "cache_r"):
                    uso_total[k] += u.get(k, 0) or 0
                uso_total["custo_usd"] += u.get("custo_usd") or 0.0
                print(f"[{i}/{len(alvos)}] {t1['titulo'][:50]:50s} ok ({len(dados['temas'])} ids)", flush=True)
            except Exception as e:
                erros.append({"erro": repr(e)[:300]})
                print(f"[{i}/{len(alvos)}] ERRO {e!r}"[:200], flush=True)
            if i % 10 == 0:
                saida_path.write_text(json.dumps(saida, ensure_ascii=False, indent=1), encoding="utf-8")

    saida_path.write_text(json.dumps(saida, ensure_ascii=False, indent=1), encoding="utf-8")
    (RAIZ / "runs").mkdir(exist_ok=True)
    (RAIZ / "runs" / "11_enriquecer_usage.json").write_text(json.dumps({
        "provedor": a.provedor, "modelo": a.modelo, "effort": a.effort, "chamadas": len(alvos),
        "temas_enriquecidos": len(saida), "uso_tokens": uso_total,
        "segundos": round(time.time() - t0), "erros": erros}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n{len(saida)} temas enriquecidos; {time.time()-t0:.0f}s; erros: {len(erros)}; uso: {uso_total}")

if __name__ == "__main__":
    main()
