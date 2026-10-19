"""Etapa 4c: compara os métodos/modelos (plano, 2 estágios, 3 estágios; Opus, Sonnet, Haiku; GPT parcial).

Para cada rodada: questões classificadas, tokens de prompt do próprio método por questão (reconstruídos a partir
dos prompts e das saídas intermediárias gravadas, sem o contexto fixo do Claude Code), tokens de saída, custo
estimado a preço de lista com e sem cache do system prompt, distribuição de saídas, e concordância de ramo e de
nó entre rodadas e com a origem.

Uso: python src/42_comparar_metodos.py
Saída: runs/comparacao_metodos.json e docs/comparacao_metodos.md
"""
import importlib
import json
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import Arvore, RAIZ, carregar_rodada, carregar_questoes, carregar_origem, MODELO_REAL, PRECO, CHARS_POR_TOKEN

c30 = importlib.import_module("30_classificar")
c31 = importlib.import_module("31_classificar_hierarquico")
c32 = importlib.import_module("32_classificar_3niveis")

RODADAS = [("claude-opus", "plano", "Opus 5.5"), ("claude-sonnet-h", "2 estágios", "Sonnet 5"),
           ("claude-sonnet-3n", "3 estágios", "Sonnet 5"), ("claude-haiku-h", "2 estágios", "Haiku 4.5"),
           ("claude-haiku-3n", "3 estágios", "Haiku 4.5"), ("gpt-5.5", "plano", "GPT-5.5 (parcial)"),
           ("claude-sonnet-plano", "plano", "Sonnet 5 (amostra 80)"), ("claude-opus-h", "2 estágios", "Opus 5.5 (amostra 80)"),
           ("jev-h", "2 estágios", "Jev")]


def prompts_por_questao(A, enr, metodo, q, bruto, cache):
    """Lista de (sistema, pedido) efetivamente enviados para a questão."""
    if metodo == "plano":
        return [(cache["flat"], c30.montar_pedido(q))]
    if metodo == "2 estágios":
        r1 = bruto.get("estagio1") or {}
        out = [(cache["s1"], c30.montar_pedido(q))]
        if r1.get("tema_n1_id") and not r1.get("fora"):
            out.append((cache["s2"], c31.pedido_estagio2(A.t, enr, q, r1)))
        return out
    ra, rb = bruto.get("estagioA") or {}, bruto.get("estagioB")
    out = [(cache["sA"], c30.montar_pedido(q))]
    if ra.get("grupo_id") and not ra.get("fora"):
        out.append((cache["sB"], c32.pedido_estagio_b(A.t, enr, cache["grupos"], q, ra)))
        if rb and rb.get("tema_n1_id") and not rb.get("fora") and rb["tema_n1_id"] in A.t:
            out.append((cache["sC"], c31.pedido_estagio2(A.t, enr, q, rb)))
    return out


def main():
    A = Arvore()
    enr = json.loads((RAIZ / "data" / "temas_enriquecidos.json").read_text(encoding="utf-8"))
    qs = {q["id"]: q for q in carregar_questoes()}
    origem = carregar_origem()
    grupos = c32.carregar_grupos(A.t)
    flat, _ = c30.montar_sistema(A.t)
    regras = c31.REGRAS
    cache = {"flat": flat, "s1": c31.sistema_estagio1(A.t, enr), "grupos": grupos,
             "s2": regras + c31.SAIDA_2, "sA": c32.sistema_estagio_a(A.t, grupos),
             "sB": regras + c32.SAIDA_B, "sC": regras + c31.SAIDA_2}

    rod = {}
    tabela = []
    for rot, metodo, nome in RODADAS:
        r = carregar_rodada(rot, A)
        if not r:
            continue
        rod[rot] = r
        modelo = MODELO_REAL[rot]
        cpt = CHARS_POR_TOKEN.get(modelo, 2.5)
        sis_tok = pedido_tok = 0
        chamadas = 0
        out_tok = 0
        for qid, (v, b) in r.items():
            for s, p in prompts_por_questao(A, enr, metodo, qs[qid], b, cache):
                sis_tok += len(s) / cpt
                pedido_tok += len(p) / cpt
                chamadas += 1
            out_tok += (b.get("uso") or {}).get("out", 0)
        n = len(r)
        pin, pout, pcache = PRECO.get(modelo, (None, None, None))
        sem_cache = (sis_tok + pedido_tok) / n * pin / 1e6 + out_tok / n * pout / 1e6 if pin else None
        com_cache = (sis_tok / n * pcache + pedido_tok / n * pin) / 1e6 + out_tok / n * pout / 1e6 if pin else None
        votos = [v for v, _ in r.values()]
        linha = {
            "rodada": rot, "metodo": metodo, "modelo": nome, "questoes": n, "chamadas_por_questao": round(chamadas / n, 2),
            "tokens_prompt_por_questao": round((sis_tok + pedido_tok) / n), "tokens_saida_por_questao": round(out_tok / n),
            "custo_usd_por_questao_sem_cache": round(sem_cache, 5) if sem_cache else None,
            "custo_usd_por_questao_com_cache": round(com_cache, 5) if com_cache else None,
            "custo_usd_50mil_com_cache": round(com_cache * 50000) if com_cache else None,
            "fora": sum(v["fora"] for v in votos), "multi_tema": sum(v["multi"] for v in votos),
            "escolheu_subtema": sum(1 for v in votos if v["sub"]),
            "conf_ramo_media": round(sum(v["c_ramo"] for v in votos) / n, 3),
        }
        tabela.append(linha)

    # concordância par a par (ramo e nó mais específico)
    def chave_ramo(v):
        return "FORA" if v["fora"] else v["ramo"]

    pares = []
    for a, b in combinations(rod, 2):
        comuns = set(rod[a]) & set(rod[b])
        if not comuns:
            continue
        ramo = sum(chave_ramo(rod[a][q][0]) == chave_ramo(rod[b][q][0]) for q in comuns) / len(comuns)
        ambos_sub = [q for q in comuns if rod[a][q][0]["sub"] and rod[b][q][0]["sub"]]
        sub = sum(rod[a][q][0]["sub"] == rod[b][q][0]["sub"] for q in ambos_sub) / len(ambos_sub) if ambos_sub else None
        pares.append({"a": a, "b": b, "n": len(comuns), "ramo": round(ramo, 3), "n_ambos_subtema": len(ambos_sub),
                      "subtema_igual_quando_ambos_escolhem": round(sub, 3) if sub is not None else None})
    com_origem = []
    for a in rod:
        cmp = [q for q in rod[a] if origem.get(q, {}).get("tema_id")]
        ok = sum(A.ramo_de(origem[q]["tema_id"]) == chave_ramo(rod[a][q][0]) for q in cmp)
        com_origem.append({"rodada": a, "n": len(cmp), "ramo_igual_origem": round(ok / len(cmp), 3) if cmp else None})

    # experimento 2x2 (e Haiku) nas 80 questões sorteadas: concordância de cada rodada com a maioria das DEMAIS
    # rodadas e do árbitro (leave-one-out), para não usar como referência um modelo igual ao avaliado
    amostra_p = RAIZ / "data" / "amostra_2x2.txt"
    loo = []
    if amostra_p.exists():
        from collections import Counter as _C
        amostra = amostra_p.read_text().strip().split(",")
        arb = carregar_rodada("arbitro-opus", A)
        refs = {**rod, "arbitro-opus": arb} if arb else dict(rod)
        for r in rod:
            cobertas = [q for q in amostra if q in rod[r]]
            if len(cobertas) < 30:
                continue
            ok = n_ok = 0
            for q in cobertas:
                outros = _C(chave_ramo(refs[o][q][0]) for o in refs if o != r and q in refs[o])
                if not outros:
                    continue
                maj, nmaj = outros.most_common(1)[0]
                n_ok += 1
                ok += chave_ramo(rod[r][q][0]) == maj
            met = next(l for l in tabela if l["rodada"] == r)
            loo.append({"rodada": r, "metodo": met["metodo"], "modelo": met["modelo"], "n": n_ok,
                        "concorda_maioria_demais": round(ok / n_ok, 3) if n_ok else None,
                        "tokens_prompt_por_questao": met["tokens_prompt_por_questao"], "tokens_saida_por_questao": met["tokens_saida_por_questao"],
                        "custo_usd_por_questao_com_cache": met["custo_usd_por_questao_com_cache"]})
    res = {"metodos": tabela, "concordancia": pares, "com_origem": com_origem, "amostra_2x2": loo}
    (RAIZ / "runs" / "comparacao_metodos.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")

    md = ["# Comparação de métodos e modelos\n",
          "Gerado por `src/42_comparar_metodos.py`. Tokens de prompt reconstruídos a partir dos prompts reais e das saídas "
          "intermediárias gravadas, sem o contexto fixo do Claude Code; razão caracteres/token medida neste corpus "
          "(`runs/calibracao_tokens.json`). Custos a preço de lista da API; \"com cache\" supõe o system prompt lido do cache "
          "(as rodadas reais foram feitas pela assinatura, sem custo marginal).\n",
          "| Rodada | Método | Modelo | Questões | Chamadas/q | Tokens prompt/q | Tokens saída/q | US$/q sem cache | US$/q com cache | US$ 50 mil q (cache) | Fora | Multi | Escolheu subtema | Conf. ramo média |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for l in tabela:
        md.append(f"| {l['rodada']} | {l['metodo']} | {l['modelo']} | {l['questoes']} | {l['chamadas_por_questao']} | "
                  f"{l['tokens_prompt_por_questao']:,} | {l['tokens_saida_por_questao']:,} | {l['custo_usd_por_questao_sem_cache']} | "
                  f"{l['custo_usd_por_questao_com_cache']} | {l['custo_usd_50mil_com_cache']} | {l['fora']} | {l['multi_tema']} | "
                  f"{l['escolheu_subtema']} | {l['conf_ramo_media']} |")
    md += ["\n## Concordância par a par\n", "| A | B | n | Mesmo ramo | n (ambos escolheram subtema) | Mesmo subtema quando ambos escolhem |", "|---|---|---|---|---|---|"]
    for p in pares:
        md.append(f"| {p['a']} | {p['b']} | {p['n']} | {p['ramo']:.1%} | {p['n_ambos_subtema']} | "
                  f"{'' if p['subtema_igual_quando_ambos_escolhem'] is None else format(p['subtema_igual_quando_ambos_escolhem'], '.1%')} |")
    md += ["\n## Concordância com a classificação de origem (só onde a origem tem um tema correspondente)\n", "| Rodada | n | Mesmo ramo da origem |", "|---|---|---|"]
    for c in com_origem:
        md.append(f"| {c['rodada']} | {c['n']} | {c['ramo_igual_origem']:.1%} |" if c["ramo_igual_origem"] is not None else f"| {c['rodada']} | 0 | |")
    if loo:
        md += ["\n## Experimento 2×2 nas 80 questões sorteadas\n",
               "Cada rodada comparada com a maioria das demais rodadas e do árbitro, excluindo a própria (leave-one-out). "
               "Não é acurácia; é o quanto a rodada acompanha o consenso dos outros.\n",
               "| Rodada | Método | Modelo | n | Concorda com a maioria dos demais | Tokens prompt/q | Tokens saída/q | US$/q com cache |", "|---|---|---|---|---|---|---|---|"]
        for l in sorted(loo, key=lambda x: -(x["concorda_maioria_demais"] or 0)):
            md.append(f"| {l['rodada']} | {l['metodo']} | {l['modelo']} | {l['n']} | {l['concorda_maioria_demais']:.1%} | "
                      f"{l['tokens_prompt_por_questao']:,} | {l['tokens_saida_por_questao']:,} | {l['custo_usd_por_questao_com_cache']} |")
    (RAIZ / "docs" / "comparacao_metodos.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
