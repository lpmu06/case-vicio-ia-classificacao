"""Etapa 3c: classificação hierárquica em três estágios (grupo -> tema -> subtema).

Estágio A: lista de grupos artificiais de temas (data/grupos_n1.json) com os títulos dos temas de cada grupo
           -> escolhe o grupo e um segundo grupo.
Estágio B: temas dos dois grupos, com resumo e títulos dos subtemas -> escolhe o tema de nível 1 e segunda opção.
Estágio C: igual ao estágio 2 do classificador de dois níveis (metadados completos do ramo) -> subtema ou null.
Saída no mesmo esquema das etapas 3 e 3b.

Uso: python src/classificar/32_classificar_3niveis.py --provedor claude_cli --modelo sonnet --rotulo claude-sonnet-3n
"""
import argparse, importlib, json, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import caminhos  # noqa: F401,E402  (pastas de etapas no sys.path)
from llm import chamar_json
arv = importlib.import_module("10_arvore")
c30 = importlib.import_module("30_classificar")
c31 = importlib.import_module("31_classificar_hierarquico")

RAIZ = Path(__file__).resolve().parents[2]

ESQUEMA_A = {
    "type": "object",
    "properties": {
        "fora": {"type": "boolean"},
        "grupo_id": {"type": ["string", "null"]},
        "segundo_grupo_id": {"type": ["string", "null"]},
        "confianca": {"type": "number"},
        "multi_tema": {"type": "boolean"},
        "justificativa": {"type": "string"},
    },
    "required": ["fora", "grupo_id", "segundo_grupo_id", "confianca", "multi_tema", "justificativa"],
    "additionalProperties": False,
}


SAIDA_B = ("## Saída\nResponda apenas com JSON no esquema fornecido. `tema_n1_id` é o id do tema de nível 1 "
           "escolhido (nunca a disciplina); `segunda_opcao_n1_id` outro tema de nível 1 ou null; "
           "`confianca_ramo` é a probabilidade honesta (0 a 1) de coincidir com o professor.")


def carregar_grupos(temas):
    g = json.loads((RAIZ / "data" / "grupos_n1.json").read_text(encoding="utf-8"))["grupos"]
    usaveis = {t["tema_id"] for t in temas.values() if t["nivel"] == 1 and t["status"] == "active" and not t["bucket"]}
    cobertos = [x for grp in g for x in grp["temas"]]
    assert sorted(cobertos) == sorted(usaveis), f"grupos não cobrem exatamente os temas usáveis: faltam {usaveis - set(cobertos)}, sobram {set(cobertos) - usaveis}"
    return g


def sistema_estagio_a(temas, grupos):
    linhas = []
    atual = None
    for grp in grupos:
        if grp["disciplina"] != atual:
            atual = grp["disciplina"]
            linhas.append(f"\n### DISCIPLINA: {atual}")
        linhas.append(f"{grp['id']} | {grp['titulo']}")
        linhas.append("    temas: " + "; ".join(temas[x]["titulo"] for x in grp["temas"]))
    saida = ("## Saída\nResponda apenas com JSON no esquema fornecido. `grupo_id` é o id do grupo (ex.: P2, PP4, LE1, C3) "
             "cujos temas melhor cobrem o que a questão testa; `segundo_grupo_id` é o segundo grupo mais provável ou null; "
             "`confianca` é a probabilidade honesta (0 a 1) de o grupo escolhido conter o tema que um professor atribuiria.")
    return c31.REGRAS + "## Grupos de temas (id | título; temas do grupo listados abaixo)\n<grupos>" + "\n".join(linhas) + "\n</grupos>\n\n" + saida


def pedido_estagio_b(temas, enr, grupos, q, ra):
    ids = [ra["grupo_id"]] + ([ra["segundo_grupo_id"]] if ra.get("segundo_grupo_id") else [])
    por_id = {g["id"]: g for g in grupos}
    blocos = []
    for gid in ids:
        if gid not in por_id:
            continue
        g = por_id[gid]
        linhas = [f"## Grupo {gid} | {g['disciplina']} | {g['titulo']}"]
        for x in g["temas"]:
            t = temas[x]
            filhos = [temas[f]["titulo"] for f in t["filhos"] if temas[f]["status"] == "active" and not temas[f]["bucket"]]
            linhas.append(f"{x} | {t['titulo']} — {c31.primeira_frase(enr.get(x, {}).get('descricao'), 300)}")
            if filhos:
                linhas.append(f"    subtemas: {'; '.join(filhos)}")
        blocos.append("\n".join(linhas))
    return (f"No estágio anterior, o grupo escolhido foi {ids[0]}" + (f" e o segundo foi {ids[1]}" if len(ids) > 1 else "") +
            f". Justificativa anterior: {ra['justificativa']}\n\nEscolha agora o tema de nível 1 entre os listados abaixo "
            "(pode ser do segundo grupo) e indique uma segunda opção.\n\n" + "\n\n=====\n\n".join(blocos) + "\n\n" + c30.montar_pedido(q))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provedor", choices=["anthropic", "openai", "claude_cli"], required=True)
    ap.add_argument("--modelo", required=True)
    ap.add_argument("--rotulo", default=None)
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--limite", type=int, default=None)
    ap.add_argument("--ids", default=None)
    ap.add_argument("--workers", type=int, default=3)
    a = ap.parse_args()

    temas = arv.carregar_temas()
    enr = json.loads((RAIZ / "data" / "temas_enriquecidos.json").read_text(encoding="utf-8"))
    grupos = carregar_grupos(temas)
    sis_a = sistema_estagio_a(temas, grupos)
    sis_b = c31.REGRAS + SAIDA_B
    sis_c = c31.REGRAS + c31.SAIDA_2
    qs = [json.loads(l) for l in (RAIZ / "data" / "questoes_limpas.jsonl").open(encoding="utf-8")]
    if a.ids:
        qs = [q for q in qs if q["id"] in a.ids.split(",")]
    if a.limite:
        qs = qs[:a.limite]
    pasta = RAIZ / "runs" / (a.rotulo or f"{a.modelo}-3n")
    pasta.mkdir(parents=True, exist_ok=True)
    pendentes = [q for q in qs if not (pasta / f"{q['id']}.json").exists()]
    print(f"3 níveis provedor={a.provedor} modelo={a.modelo} estágioA={len(sis_a)} chars; {len(pendentes)} pendentes de {len(qs)}", flush=True)

    uso = {"in": 0, "out": 0, "cache_w": 0, "cache_r": 0, "custo_usd": 0.0}
    erros, t0 = [], time.time()
    vazio = {"in": 0, "out": 0, "cache_w": 0, "cache_r": 0, "custo_usd": 0.0}

    def tarefa(q):
        ra, ua = chamar_json(a.provedor, a.modelo, sis_a, c30.montar_pedido(q), ESQUEMA_A, a.effort)
        ids_grupos = {g["id"] for g in grupos}
        if not ra["fora"] and ra.get("grupo_id") not in ids_grupos:  # validação com realimentação
            nota = (f"\n\nATENÇÃO: na tentativa anterior você respondeu grupo_id = {ra.get('grupo_id')!r}, que não é um dos ids "
                    f"de grupo ({', '.join(sorted(ids_grupos))}). Responda de novo com um desses ids.")
            ra, ua2 = chamar_json(a.provedor, a.modelo, sis_a, c30.montar_pedido(q) + nota, ESQUEMA_A, a.effort)
            ua = {k: (ua.get(k) or 0) + (ua2.get(k) or 0) for k in vazio}
            if not ra["fora"] and ra.get("grupo_id") not in ids_grupos:
                raise ValueError(f"estágio A devolveu grupo inválido: {ra.get('grupo_id')!r}")
        rb, ub, final, uc = None, vazio, None, vazio
        if ra["fora"] or not ra.get("grupo_id"):
            final = {"fora": True, "tema_n1_id": None, "subtema_n2_id": None, "confianca_ramo": ra["confianca"],
                     "confianca_subtema": 0, "segunda_opcao_id": None, "extras_ids": [], "multi_tema": ra["multi_tema"],
                     "justificativa": ra["justificativa"]}
        else:
            rb, ub = c31.chamar_validado(a.provedor, a.modelo, sis_b, pedido_estagio_b(temas, enr, grupos, q, ra), c31.ESQUEMA_1,
                                         a.effort, temas)
            if rb["fora"] or not rb.get("tema_n1_id") or rb["tema_n1_id"] not in temas:
                final = {"fora": True, "tema_n1_id": None, "subtema_n2_id": None, "confianca_ramo": rb["confianca_ramo"],
                         "confianca_subtema": 0, "segunda_opcao_id": rb.get("segunda_opcao_n1_id"), "extras_ids": [],
                         "multi_tema": rb["multi_tema"], "justificativa": rb["justificativa"]}
            else:
                t = temas[rb["tema_n1_id"]]
                if t["nivel"] == 2:
                    rb["tema_n1_id"] = t["parent_id"]
                elif t["nivel"] == 0:
                    raise ValueError("estágio B devolveu disciplina")
                final, uc = chamar_json(a.provedor, a.modelo, sis_c, c31.pedido_estagio2(temas, enr, q, rb), c30.ESQUEMA, a.effort)
        u = {k: (ua.get(k) or 0) + (ub.get(k) or 0) + (uc.get(k) or 0) for k in vazio}
        final.update({"id": q["id"], "modelo": a.modelo, "provedor": a.provedor, "effort": a.effort,
                      "estagioA": ra, "estagioB": rb, "uso": u})
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
                   "provedor": a.provedor, "effort": a.effort, "metodo": "hierarquico_3_estagios"})
    resumo_path.write_text(json.dumps(antigo, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"fim: uso acumulado={antigo['uso']} segundos={antigo['segundos']} erros={len(erros)}")


if __name__ == "__main__":
    main()
