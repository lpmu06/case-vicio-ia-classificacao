"""Etapa 5: avaliação das variantes do Jev (bloco G do plano de melhorias).

Sem gabarito, a régua é a concordância de ramo (tema de nível 1) com duas referências que não usam o Jev:
  - maioria dos não-Jev: voto de maioria das rodadas de Claude/GPT e do árbitro (excluindo a rodada avaliada);
  - trio unânime: questões em que Opus plano, Sonnet 2 estágios e o árbitro escolheram o mesmo ramo.
Mede também a calibração (concordância por faixa de probabilidade), o ruído entre requisições idênticas,
o viés de ordem das opções, o efeito do beam search e o custo real (tokens devolvidos pela API).

As cinco variantes rodaram nas 359 questões (decisão do Luis, 19/10/2026); como a melhor é escolhida e medida nos
mesmos dados, a diferença entre variantes vale como indicação, não como estimativa sem viés.

Uso: python src/analise/50_avaliar_jev.py
Saída: runs/jev_avaliacao.json e docs/jev.md
"""
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import caminhos  # noqa: F401,E402  (pastas de etapas no sys.path)
from comum import Arvore, RAIZ, carregar_rodada

PRECO_POR_MILHAO = 0.042
VARIANTES = [("jev-h", "base (jev-latest 1.13, critérios curtos, guloso)"), ("jev-h-preview", "jev-preview (1.14)"),
             ("jev-h-ricos", "critérios ricos"), ("jev-h-beam3", "beam search K=3"), ("jev-h-ordens5", "5 ordens embaralhadas")]
NAO_JEV = ["claude-opus", "claude-sonnet-h", "claude-sonnet-3n", "claude-haiku-h", "claude-haiku-3n",
           "claude-sonnet-plano", "claude-opus-h", "gpt-5.5", "arbitro-opus"]
TRIO = ["claude-opus", "claude-sonnet-h", "arbitro-opus"]
FAIXAS = [(0, .5), (.5, .7), (.7, .9), (.9, .99), (.99, 1.01)]


def ramo(v):
    return "FORA" if v["fora"] else v["ramo"]


def maioria(rods, q, excluir=()):
    """(ramo da maioria, fração de votos) entre as rodadas não-Jev que cobrem q; empate desfeito pelo árbitro."""
    votos = {r: ramo(rods[r][q][0]) for r in NAO_JEV if r not in excluir and q in rods[r]}
    if not votos:
        return None, 0.0
    cont = Counter(votos.values()).most_common()
    topo = [k for k, n in cont if n == cont[0][1]]
    escolhido = votos.get("arbitro-opus") if len(topo) > 1 and votos.get("arbitro-opus") in topo else topo[0]
    return escolhido, cont[0][1] / len(votos)


def calibracao(pares):
    """pares: (probabilidade declarada, acertou). Tabela por faixa e erro de calibração esperado (ECE)."""
    linhas, ece = [], 0.0
    for lo, hi in FAIXAS:
        sel = [(p, ok) for p, ok in pares if lo <= p < hi]
        if not sel:
            continue
        conf = sum(p for p, _ in sel) / len(sel)
        acc = sum(ok for _, ok in sel) / len(sel)
        ece += len(sel) / len(pares) * abs(acc - conf)
        linhas.append({"faixa": f"{lo:.2f}–{min(hi, 1):.2f}", "n": len(sel), "prob_media": round(conf, 3), "concordancia": round(acc, 3)})
    return linhas, round(ece, 3)


def main():
    A = Arvore()
    rods = {r: carregar_rodada(r, A) for r in NAO_JEV}
    jev = {r: carregar_rodada(r, A) for r, _ in VARIANTES}
    jev = {r: v for r, v in jev.items() if v}
    qids = sorted(next(iter(jev.values())))
    ref = {q: maioria(rods, q) for q in qids}
    trio = [q for q in qids if all(q in rods[r] for r in TRIO) and len({ramo(rods[r][q][0]) for r in TRIO}) == 1]
    amostra = (RAIZ / "data" / "amostra_2x2.txt").read_text().strip().split(",")

    res = {"n_questoes": len(qids), "n_trio_unanime": len(trio), "variantes": [], "calibracao": {}}
    for rot, nome in VARIANTES:
        if rot not in jev:
            continue
        R = jev[rot]
        brutos = [b for _, b in R.values()]
        tok = sum(b["uso"]["input_tokens"] for b in brutos)
        uso = json.loads((RAIZ / "runs" / rot / "_usage.json").read_text(encoding="utf-8"))
        conc = [ramo(R[q][0]) == ref[q][0] for q in qids if ref[q][0]]
        conc_trio = [ramo(R[q][0]) == ramo(rods["claude-opus"][q][0]) for q in trio]
        conc_80 = [ramo(R[q][0]) == ref[q][0] for q in amostra if q in R and ref[q][0]]
        sub_ambos = [q for q in qids if R[q][0]["sub"] and q in rods["claude-opus"] and rods["claude-opus"][q][0]["sub"]]
        linha = {"rodada": rot, "variante": nome, "modelo": sorted({b["modelo"] for b in brutos}), "questoes": len(R),
                 "concorda_maioria": round(sum(conc) / len(conc), 3), "n_maioria": len(conc),
                 "concorda_trio_unanime": round(sum(conc_trio) / len(conc_trio), 3),
                 "concorda_maioria_amostra80": round(sum(conc_80) / len(conc_80), 3),
                 "fora": sum(v["fora"] for v, _ in R.values()), "escolheu_subtema": sum(1 for v, _ in R.values() if v["sub"]),
                 "subtema_igual_opus_quando_ambos": (round(sum(R[q][0]["sub"] == rods["claude-opus"][q][0]["sub"] for q in sub_ambos)
                                                     / len(sub_ambos), 3) if sub_ambos else None),
                 "chamadas_por_questao": round(sum(b["uso"]["chamadas"] for b in brutos) / len(R), 2),
                 "tokens_por_questao": round(tok / len(R)), "usd_por_questao": round(tok / len(R) * PRECO_POR_MILHAO / 1e6, 6),
                 "usd_total": round(tok * PRECO_POR_MILHAO / 1e6, 4), "usd_50mil": round(tok / len(R) * 50000 * PRECO_POR_MILHAO / 1e6, 2),
                 "segundos": uso.get("segundos")}
        linhas, ece = calibracao([(R[q][0]["c_ramo"], ramo(R[q][0]) == ref[q][0]) for q in qids if ref[q][0]])
        res["calibracao"][rot] = {"faixas": linhas, "ece": ece}
        linha["ece"] = ece
        res["variantes"].append(linha)

    # mesma régua aplicada à confiança declarada pelos modelos de linguagem (excluindo o próprio da maioria)
    for r in ["claude-opus", "claude-sonnet-h", "arbitro-opus"]:
        pares = []
        for q in qids:
            if q in rods[r]:
                m, _ = maioria(rods, q, excluir=(r,))
                if m:
                    pares.append((rods[r][q][0]["c_ramo"], ramo(rods[r][q][0]) == m))
        linhas, ece = calibracao(pares)
        res["calibracao"][r] = {"faixas": linhas, "ece": ece, "concordancia": round(sum(ok for _, ok in pares) / len(pares), 3)}

    # ruído: o estágio 1 do beam e a primeira ordem das 5 são a mesma requisição da base
    ruido = {}
    if "jev-h-beam3" in jev:
        B = jev["jev-h-beam3"]
        base = jev["jev-h"]
        mesmo = [base[q][1]["tema_n1_id"] or "FORA" for q in qids]
        gul = [B[q][1]["ramo_guloso"] for q in qids]
        ruido["base_vs_reexecucao_mesmo_ramo"] = round(sum(a == b for a, b in zip(mesmo, gul)) / len(qids), 3)
        dif = [abs(base[q][1]["probabilidades_estagio1"].get(k, 0) - B[q][1]["probabilidades_estagio1"].get(k, 0))
               for q in qids for k in [next(iter(base[q][1]["probabilidades_estagio1"]))]]
        ruido["dif_media_prob_topo"] = round(sum(dif) / len(dif), 3)
        ruido["dif_max_prob_topo"] = round(max(dif), 3)
        mudou = [q for q in qids if (B[q][1]["tema_n1_id"] or "FORA") != B[q][1]["ramo_guloso"]]
        res["beam"] = {"mudou_ramo": len(mudou),
                       "mudou_para_maioria": sum(ramo(B[q][0]) == ref[q][0] for q in mudou),
                       "saiu_da_maioria": sum(B[q][1]["ramo_guloso"] == ref[q][0] for q in mudou)}
    if "jev-h-ordens5" in jev:
        O = jev["jev-h-ordens5"]
        esc = {q: O[q][1]["escolhas_por_ordem_estagio1"] for q in qids}
        res["ordem"] = {"questoes_com_escolha_instavel": sum(len(set(e)) > 1 for e in esc.values()),
                        "media_diferente_da_ordem_original": sum((O[q][1]["tema_n1_id"] or "FORA") != esc[q][0] for q in qids),
                        "ordem_original_concorda_maioria": round(sum(esc[q][0] == ref[q][0] for q in qids if ref[q][0]) / len(qids), 3)}
        if "jev-h" in jev:
            ruido["base_vs_primeira_ordem_mesmo_ramo"] = round(
                sum((jev["jev-h"][q][1]["tema_n1_id"] or "FORA") == esc[q][0] for q in qids) / len(qids), 3)
    res["ruido"] = ruido

    # comparação pareada com a base nas mesmas questões: só as discordantes informam (lógica do teste de McNemar)
    res["pareado_vs_base"] = {}
    for rot in jev:
        if rot == "jev-h":
            continue
        com = [q for q in qids if ref[q][0]]
        so_var = sum(ramo(jev[rot][q][0]) == ref[q][0] != ramo(jev["jev-h"][q][0]) for q in com)
        so_base = sum(ramo(jev["jev-h"][q][0]) == ref[q][0] != ramo(jev[rot][q][0]) for q in com)
        res["pareado_vs_base"][rot] = {"so_variante_concorda": so_var, "so_base_concorda": so_base}

    # cascata: o Jev decide sozinho quando a probabilidade do ramo passa do limiar; o resto segue para os modelos de linguagem
    melhor = max(res["variantes"], key=lambda l: l["concorda_maioria"])["rodada"]
    R = jev[melhor]
    res["cascata"] = {"rodada": melhor, "limiares": []}
    for t in (0.999, 0.99, 0.95, 0.90, 0.80):
        sel = [q for q in qids if R[q][0]["c_ramo"] >= t]
        ok = [ramo(R[q][0]) == ref[q][0] for q in sel if ref[q][0]]
        ok_trio = [ramo(R[q][0]) == ramo(rods["claude-opus"][q][0]) for q in sel if q in trio]
        res["cascata"]["limiares"].append({"limiar": t, "questoes": len(sel), "fracao": round(len(sel) / len(qids), 3),
                                           "concorda_maioria": round(sum(ok) / len(ok), 3) if ok else None,
                                           "n_trio": len(ok_trio), "concorda_trio": round(sum(ok_trio) / len(ok_trio), 3) if ok_trio else None})
    (RAIZ / "runs" / "jev_avaliacao.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")

    md = ["# Jev (TypeSafe) como classificador adicional\n",
          "Gerado por `src/analise/50_avaliar_jev.py` a partir de `runs/jev-h*/`. Sem gabarito: \"concorda\" é concordância de ramo "
          "(tema de nível 1) com a maioria das rodadas de Claude/GPT e do árbitro, que não usam o Jev. O \"trio unânime\" são as "
          f"{len(trio)} questões em que Opus plano, Sonnet 2 estágios e o árbitro escolheram o mesmo ramo, o subconjunto com rótulo "
          "mais confiável. As cinco variantes rodaram nas 359 questões e mudam um fator por vez em relação à base; como a melhor é "
          "escolhida e medida nos mesmos dados, diferenças de um ou dois pontos são indicação, não prova.\n",
          "## Variantes\n",
          "| Variante | Modelo | Concorda com a maioria (359) | Trio unânime | Amostra 80 | ECE | Escolheu subtema | "
          "Subtema = Opus (quando ambos) | Chamadas/q | Tokens/q | US$ total (359) | US$ 50 mil q | Segundos |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for l in res["variantes"]:
        md.append(f"| {l['variante']} | {', '.join(l['modelo'])} | {l['concorda_maioria']:.1%} | {l['concorda_trio_unanime']:.1%} | "
                  f"{l['concorda_maioria_amostra80']:.1%} | {l['ece']:.3f} | {l['escolheu_subtema']} | "
                  f"{'' if l['subtema_igual_opus_quando_ambos'] is None else format(l['subtema_igual_opus_quando_ambos'], '.1%')} | "
                  f"{l['chamadas_por_questao']} | {l['tokens_por_questao']:,} | {l['usd_total']:.3f} | {l['usd_50mil']:.0f} | {l['segundos']} |")
    md += ["\nPreço de lista da TypeSafe em 19/10/2026: US$ 0,042 por milhão de tokens de entrada, saída grátis. Tokens são os "
           "devolvidos pela API, não estimados.\n",
           "## Calibração\n",
           "Concordância com a maioria por faixa da probabilidade que o classificador deu ao ramo escolhido. No Jev é a "
           "probabilidade do modelo; no Opus, no Sonnet e no árbitro é a confiança que o modelo declara no JSON (para eles a "
           "maioria exclui a própria rodada). ECE = média ponderada de |concordância − probabilidade| nas faixas.\n",
           "| Classificador | Faixa | n | Probabilidade média | Concordância |", "|---|---|---|---|---|"]
    for r, c in res["calibracao"].items():
        for f in c["faixas"]:
            md.append(f"| {r} | {f['faixa']} | {f['n']} | {f['prob_media']:.2f} | {f['concordancia']:.1%} |")
    md.append("\n| Classificador | ECE |\n|---|---|\n" + "\n".join(f"| {r} | {c['ece']:.3f} |" for r, c in res["calibracao"].items()))
    if ruido:
        md += ["\n## Ruído entre requisições idênticas\n",
               "O Jev não é determinístico: a mesma requisição devolve probabilidades um pouco diferentes. O estágio 1 do beam e a "
               "primeira das 5 ordens são requisições idênticas às da base, o que dá réplicas sem custo extra.\n"]
        for k, v in ruido.items():
            md.append(f"- `{k}`: {v:.1%}" if "mesmo_ramo" in k else f"- `{k}`: {v:.3f}")
    if "beam" in res:
        b = res["beam"]
        md += ["\n## Beam search\n", f"O beam trocou o ramo do guloso em {b['mudou_ramo']} questões: em {b['mudou_para_maioria']} passou a "
               f"concordar com a maioria e em {b['saiu_da_maioria']} deixou de concordar."]
    if "ordem" in res:
        o = res["ordem"]
        md += ["\n## Viés de ordem das opções\n", f"Com as 89 opções em 5 ordens diferentes, a escolha do estágio 1 mudou com a ordem em "
               f"{o['questoes_com_escolha_instavel']} das {len(qids)} questões; a média das 5 escolheu um ramo diferente da ordem original "
               f"em {o['media_diferente_da_ordem_original']}."]
    md += ["\n## Comparação pareada com a base\n",
           "Nas mesmas questões, quantas só a variante acerta (concorda com a maioria) e quantas só a base acerta. As que ambas "
           "acertam ou ambas erram não distinguem as duas. Para comparação: duas execuções idênticas da base discordam de ramo em "
           f"{1 - ruido.get('base_vs_reexecucao_mesmo_ramo', 1):.1%} das questões.\n",
           "| Variante | Só a variante concorda | Só a base concorda |", "|---|---|---|"]
    for rot, p in res["pareado_vs_base"].items():
        md.append(f"| {rot} | {p['so_variante_concorda']} | {p['so_base_concorda']} |")
    c = res["cascata"]
    md += [f"\n## Cascata: o Jev decide sozinho acima de um limiar ({c['rodada']})\n",
           "Questões em que a probabilidade do ramo escolhido pelo Jev passa do limiar e a concordância delas com a maioria e com o "
           "trio unânime. O resto seguiria para os modelos de linguagem.\n",
           "| Limiar | Questões | Fração | Concorda com a maioria | n no trio unânime | Concorda com o trio |", "|---|---|---|---|---|---|"]
    for l in c["limiares"]:
        md.append(f"| {l['limiar']} | {l['questoes']} | {l['fracao']:.1%} | {l['concorda_maioria']:.1%} | {l['n_trio']} | "
                  f"{'' if l['concorda_trio'] is None else format(l['concorda_trio'], '.1%')} |")
    desemp = RAIZ / "runs" / "jev_desempate.json"
    if desemp.exists() and "auditoria" in (d := json.loads(desemp.read_text(encoding="utf-8"))):
        p, c = d["auditoria"]["promovidas"], d["auditoria"]["controles"]
        md += ["\n## Camada final de desempate (src/analise/51_jev_desempate.py)\n",
               f"Nas {d['revisar']} questões que a regra mandou para revisão, o Jev escolheu só entre os ramos candidatos (2 a 4 em "
               f"{d['com_2_ou_mais_candidatos']} delas), com descrições inteiras e duas ordens. Regra fixada antes da auditoria: promover "
               f"quando a escolha é o ramo do árbitro com probabilidade ≥ {d['limiar']:.2f}. Escolha igual à do árbitro em "
               f"{d['escolha_igual_arbitro']}; {len(d['promovidas'])} promovidas; custo US$ {d['custo_usd']:.3f}.\n",
               "Validação por auditoria cega com controles: as promovidas misturadas com publicadas que nenhuma auditoria viu, em dois "
               "cadernos embaralhados, dois auditores (agentes Claude Opus com contexto limpo) que não sabiam quais eram quais.\n",
               "| Grupo | n | ok | duvidoso | erro | ok (IC 95%) |", "|---|---|---|---|---|---|",
               f"| Promovidas pelo Jev | {p['n']} | {p['ok']} | {p['duvidoso']} | {p['erro']} | {p['taxa_ok']:.1%} "
               f"({p['ic95_ok'][0]:.0%}–{p['ic95_ok'][1]:.0%}) |",
               f"| Controles (publicadas) | {c['n']} | {c['ok']} | {c['duvidoso']} | {c['erro']} | {c['taxa_ok']:.1%} "
               f"({c['ic95_ok'][0]:.0%}–{c['ic95_ok'][1]:.0%}) |",
               "\nAs dúvidas das promovidas são de convenção (assunto com dois endereços na árvore) ou de questões que misturam "
               "temas: o que a regra mandou para revisão é ambiguidade real, que o acordo entre Jev e árbitro não resolve. A "
               "calibração medida nas 359 não vale no subconjunto difícil. Desempate descartado."]
    (RAIZ / "docs" / "jev.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
