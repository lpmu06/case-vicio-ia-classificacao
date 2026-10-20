"""Etapa 3b: classificação hierárquica (top-down) em dois estágios, com prompts ~6x menores que a etapa 3.

Estágio 1: árvore compacta (temas de nível 1 com uma linha de descrição e os títulos dos subtemas) -> escolhe o
           tema de nível 1 e uma segunda opção.
Estágio 2: só os metadados completos do ramo escolhido (e do ramo da segunda opção) -> confirma o tema e escolhe
           o subtema (ou null), com confianças, extras e flag multi-tema.
A saída final tem o mesmo esquema da etapa 3, então o ensemble (40) funciona sem mudanças.

Uso: python src/classificar/31_classificar_hierarquico.py --provedor claude_cli --modelo sonnet --rotulo claude-sonnet-h
"""
import argparse, importlib, json, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import caminhos  # noqa: F401,E402  (pastas de etapas no sys.path)
from llm import chamar_json
arv = importlib.import_module("10_arvore")
c30 = importlib.import_module("30_classificar")

RAIZ = Path(__file__).resolve().parents[2]

ESQUEMA_1 = {
    "type": "object",
    "properties": {
        "fora": {"type": "boolean"},
        "tema_n1_id": {"type": ["string", "null"]},
        "segunda_opcao_n1_id": {"type": ["string", "null"]},
        "confianca_ramo": {"type": "number"},
        "multi_tema": {"type": "boolean"},
        "justificativa": {"type": "string"},
    },
    "required": ["fora", "tema_n1_id", "segunda_opcao_n1_id", "confianca_ramo", "multi_tema", "justificativa"],
    "additionalProperties": False,
}

SAIDA_2 = ("## Saída\nResponda apenas com JSON no esquema fornecido. `tema_n1_id` é o tema de nível 1 "
           "(nunca a disciplina); `subtema_n2_id` é um subtema filho dele ou null; as confianças são "
           "probabilidades honestas (0 a 1); `segunda_opcao_id` é um id de nível 1 ou 2; `extras_ids` são "
           "outros temas relevantes (pode ser vazio).")

REGRAS = (RAIZ / "prompts" / "classificar_sistema.md").read_text(encoding="utf-8").split("## Árvore de temas")[0]


def chamar_validado(provedor, modelo, sistema, pedido, esquema, effort, temas, campo="tema_n1_id", tentativas=2):
    """Chama o modelo e valida que `campo` é um tema de nível 1 (subtema é normalizado para o pai).
    Se vier uma disciplina ou um id inexistente, repete a chamada explicando o erro (validação com realimentação)."""
    vazio = {"in": 0, "out": 0, "cache_w": 0, "cache_r": 0, "custo_usd": 0.0}
    uso = dict(vazio)
    nota = ""
    r = None
    for _ in range(tentativas + 1):
        r, u = chamar_json(provedor, modelo, sistema, pedido + nota, esquema, effort)
        for k in uso:
            uso[k] += u.get(k) or 0
        tid = r.get(campo)
        if r.get("fora"):
            return r, uso
        if tid in temas and temas[tid]["nivel"] == 2:
            r[campo] = temas[tid]["parent_id"]
            return r, uso
        if tid in temas and temas[tid]["nivel"] == 1 and temas[tid]["status"] == "active" and not temas[tid]["bucket"]:
            return r, uso
        motivo = ("é uma DISCIPLINA (nível 0), que nunca pode ser escolhida" if tid in temas and temas[tid]["nivel"] == 0
                  else "é um tema inativo ou bucket de curso" if tid in temas else "não existe na árvore")
        nota = (f"\n\nATENÇÃO: na tentativa anterior você respondeu {campo} = {tid!r}, que {motivo}. "
                "Responda de novo escolhendo o id de um tema de nível 1 (marcado como tema na árvore) dentro da disciplina adequada.")
    return r, uso


def primeira_frase(s, n=220):
    s = (s or "").strip()
    p = s.find(". ")
    s = s[: p + 1] if 0 < p < n else s[:n]
    return s


def sistema_estagio1(temas, enr):
    linhas = []
    for r in [t for t in temas.values() if t["nivel"] == 0]:
        linhas.append(f"\n### {r['tema_id']} | DISCIPLINA | {r['titulo']}")
        for f in r["filhos"]:
            t = temas[f]
            if t["status"] != "active" or t["bucket"]:
                continue
            filhos = [temas[x]["titulo"] for x in t["filhos"] if temas[x]["status"] == "active" and not temas[x]["bucket"]]
            linhas.append(f"{t['tema_id']} | {t['titulo']} — {primeira_frase(enr.get(f, {}).get('descricao'))}")
            if filhos:
                linhas.append(f"    subtemas: {'; '.join(filhos)}")
    arvore = "\n".join(linhas)
    saida = ("## Saída\nResponda apenas com JSON no esquema fornecido. `tema_n1_id` é o id do tema de nível 1 "
             "(nunca a disciplina). `segunda_opcao_n1_id` é o tema de nível 1 que seria sua segunda escolha "
             "(ou null). `confianca_ramo` é a probabilidade honesta (0 a 1) de o tema escolhido coincidir com o "
             "de um professor especialista.")
    return REGRAS + "## Temas de nível 1 (id | título — resumo; subtemas listados abaixo)\n<arvore>" + arvore + "\n</arvore>\n\n" + saida


def bloco_ramo(temas, enr, tid):
    t = temas[tid]
    def meta(x):
        e = enr.get(x["tema_id"], {})
        return (f"[{x['tema_id']}] {x['caminho']}\n  descrição: {e.get('descricao', '')}\n"
                f"  palavras-chave: {', '.join(e.get('palavras_chave', []))}\n"
                f"  dispositivos: {', '.join(e.get('dispositivos', []))}\n  não confundir: {e.get('nao_confundir', '')}")
    partes = [f"## Tema de nível 1: {meta(t)}"]
    filhos = [temas[x] for x in t["filhos"] if temas[x]["status"] == "active" and not temas[x]["bucket"]]
    if filhos:
        partes.append("## Subtemas (nível 2) deste tema:\n" + "\n\n".join(meta(f) for f in filhos))
    else:
        partes.append("(este tema não tem subtemas: subtema_n2_id deve ser null)")
    return "\n\n".join(partes)


def pedido_estagio2(temas, enr, q, r1):
    ramos = [r1["tema_n1_id"]] + ([r1["segunda_opcao_n1_id"]] if r1.get("segunda_opcao_n1_id") else [])
    ramos = [x for x in ramos if x in temas and temas[x]["nivel"] == 1]
    blocos = "\n\n=====\n\n".join(bloco_ramo(temas, enr, x) for x in ramos)
    return (f"No estágio anterior, o tema de nível 1 escolhido foi {ramos[0]}"
            + (f" e a segunda opção foi {ramos[1]}" if len(ramos) > 1 else "") +
            f". Justificativa anterior: {r1['justificativa']}\n\n"
            "Agora, com os metadados completos abaixo, confirme (ou troque pela segunda opção) o tema de nível 1 e "
            "escolha o subtema de nível 2 somente se tiver certeza; caso contrário, subtema_n2_id = null.\n\n"
            f"{blocos}\n\n" + c30.montar_pedido(q))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provedor", choices=["anthropic", "openai", "claude_cli"], required=True)
    ap.add_argument("--modelo", required=True)
    ap.add_argument("--rotulo", default=None)
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--limite", type=int, default=None)
    ap.add_argument("--ids", default=None)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()

    temas = arv.carregar_temas()
    enr = json.loads((RAIZ / "data" / "temas_enriquecidos.json").read_text(encoding="utf-8"))
    sis1 = sistema_estagio1(temas, enr)
    sis2 = REGRAS + SAIDA_2
    qs = [json.loads(l) for l in (RAIZ / "data" / "questoes_limpas.jsonl").open(encoding="utf-8")]
    if a.ids:
        qs = [q for q in qs if q["id"] in a.ids.split(",")]
    if a.limite:
        qs = qs[:a.limite]
    pasta = RAIZ / "runs" / (a.rotulo or f"{a.modelo}-h")
    pasta.mkdir(parents=True, exist_ok=True)
    pendentes = [q for q in qs if not (pasta / f"{q['id']}.json").exists()]
    print(f"hierárquico provedor={a.provedor} modelo={a.modelo} estágio1={len(sis1)} chars; {len(pendentes)} pendentes de {len(qs)}", flush=True)

    uso = {"in": 0, "out": 0, "cache_w": 0, "cache_r": 0, "custo_usd": 0.0}
    erros, t0 = [], time.time()

    def tarefa(q):
        r1, u1 = chamar_validado(a.provedor, a.modelo, sis1, c30.montar_pedido(q), ESQUEMA_1, a.effort, temas)
        if r1["fora"] or not r1.get("tema_n1_id") or r1["tema_n1_id"] not in temas:
            final = {"fora": True, "tema_n1_id": None, "subtema_n2_id": None, "confianca_ramo": r1["confianca_ramo"],
                     "confianca_subtema": 0, "segunda_opcao_id": r1.get("segunda_opcao_n1_id"), "extras_ids": [],
                     "multi_tema": r1["multi_tema"], "justificativa": r1["justificativa"]}
            u2 = {"in": 0, "out": 0, "cache_w": 0, "cache_r": 0, "custo_usd": 0.0}
        else:
            if temas[r1["tema_n1_id"]]["nivel"] != 1:  # devolveu disciplina ou subtema: normaliza
                t = temas[r1["tema_n1_id"]]
                r1["tema_n1_id"] = t["parent_id"] if t["nivel"] == 2 else None
            if not r1["tema_n1_id"]:
                raise ValueError("estágio 1 devolveu disciplina como tema")
            final, u2 = chamar_json(a.provedor, a.modelo, sis2, pedido_estagio2(temas, enr, q, r1), c30.ESQUEMA, a.effort)
        u = {k: (u1.get(k) or 0) + (u2.get(k) or 0) for k in ("in", "out", "cache_w", "cache_r", "custo_usd")}
        final.update({"id": q["id"], "modelo": a.modelo, "provedor": a.provedor, "effort": a.effort,
                      "estagio1": r1, "uso": u})
        (pasta / f"{q['id']}.json").write_text(json.dumps(final, ensure_ascii=False, indent=1), encoding="utf-8")
        return q["id"], u

    def acumular(u):
        for k in uso:
            uso[k] += u.get(k) or 0

    if pendentes:
        qid, u = tarefa(pendentes[0]); acumular(u)
        print(f"[1/{len(pendentes)}] {qid} ok uso={u}", flush=True)
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(tarefa, q): q for q in pendentes[1:]}
        for i, f in enumerate(as_completed(futs), 2):
            q = futs[f]
            try:
                qid, u = f.result(); acumular(u)
                if i % 10 == 0 or i == len(pendentes):
                    print(f"[{i}/{len(pendentes)}] {qid} ok", flush=True)
            except Exception as e:
                erros.append({"id": q["id"], "erro": re.sub(r"org-[A-Za-z0-9]+", "org-REDACTED", repr(e))[:400]}); print(f"ERRO {q['id']}: {e!r}"[:300], flush=True)

    resumo_path = pasta / "_usage.json"
    antigo = json.loads(resumo_path.read_text(encoding="utf-8")) if resumo_path.exists() else {"uso": {k: 0 for k in uso}, "segundos": 0}
    for k in uso:
        antigo["uso"][k] = antigo["uso"].get(k, 0) + uso[k]
    antigo.update({"segundos": antigo["segundos"] + round(time.time() - t0), "erros": erros, "modelo": a.modelo,
                   "provedor": a.provedor, "effort": a.effort, "metodo": "hierarquico_2_estagios"})
    resumo_path.write_text(json.dumps(antigo, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"fim: uso acumulado={antigo['uso']} segundos={antigo['segundos']} erros={len(erros)}")


if __name__ == "__main__":
    main()
