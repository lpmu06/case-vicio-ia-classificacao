"""Etapa 5: decisão final publicar / revisar / fora, com níveis de evidência e consciência de risco.

Sinais por questão (todos gravados em data/decisoes.jsonl):
- votos de ramo e subtema dos classificadores (plano, 2 e 3 estágios; Opus, Sonnet, Haiku; GPT parcial);
- voto do árbitro (Opus, esforço alto, escolha independente entre candidatos embaralhados);
- voto fraco da origem;
- pares de ramos "confundíveis": pares que aparecem juntos em divergências entre classificadores em várias questões.

Regras (parâmetros na linha de comando; valores padrão escolhidos e justificados em docs/relatorio.md):
- fora: o árbitro e a maioria dos classificadores dizem fora;
- publicar exige: árbitro, Opus plano e Sonnet 2 estágios no mesmo ramo; fração de todos os votos de modelo nesse
  ramo >= --min_frac; confiança do árbitro no ramo >= --t_arb; questão não marcada multi-tema pelo árbitro;
  e, se o ramo pertence a um par confundível, todos os votos de modelo no mesmo ramo (unanimidade);
- nível de publicação: subtema só se o árbitro e o Opus plano escolheram o mesmo subtema, nenhum voto aponta um
  subtema irmão diferente, ao menos --min_sub votos escolheram esse subtema e o árbitro tem confiança >= --t_sub;
  senão, publica no tema de nível 1 (correto pela régua sempre que o ramo está certo);
- o resto vai para revisar, com a sugestão do árbitro e o motivo.
--modo n1 publica tudo no nível 1 (variante conservadora).

Uso: python src/47_decisao.py [--modo hibrido|n1] [--saida publicacao.csv]
"""
import argparse
import csv
import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import Arvore, RAIZ, carregar_rodada, carregar_questoes, carregar_origem

CLASSIFICADORES = ["claude-opus", "claude-sonnet-h", "claude-sonnet-3n", "claude-haiku-h", "claude-haiku-3n",
                   "claude-sonnet-plano", "claude-opus-h", "gpt-5.5", "jev-h"]
FORTES = ["claude-opus", "claude-sonnet-h"]
ARBITRO = "arbitro-opus"


def pares_confundiveis(rods, qids, minimo):
    cont = Counter()
    for q in qids:
        ramos = {rod[q][0]["ramo"] for rod in rods.values() if q in rod and rod[q][0]["ramo"]}
        for a, b in combinations(sorted(ramos), 2):
            cont[(a, b)] += 1
    return {p: n for p, n in cont.items() if n >= minimo}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modo", choices=["hibrido", "n1"], default="hibrido")
    ap.add_argument("--min_frac", type=float, default=0.75)
    ap.add_argument("--t_arb", type=float, default=0.80)
    ap.add_argument("--t_sub", type=float, default=0.85)
    ap.add_argument("--min_sub", type=int, default=2, help="mínimo de votos (incluindo o árbitro) no mesmo subtema")
    ap.add_argument("--min_par", type=int, default=3, help="mínimo de questões para um par de ramos ser 'confundível'")
    ap.add_argument("--margem", type=float, default=0.02, help="margem de convenção descontada da confiança")
    ap.add_argument("--saida", default=str(RAIZ / "publicacao.csv"))
    ap.add_argument("--saida_jsonl", default=str(RAIZ / "data" / "decisoes.jsonl"))
    a = ap.parse_args()

    A = Arvore()
    qs = carregar_questoes()
    qids = [q["id"] for q in qs]
    rods = {r: carregar_rodada(r, A) for r in CLASSIFICADORES}
    # só rodadas completas entram na regra, para o critério ser o mesmo em todas as questões;
    # as parciais (amostra 2x2, GPT, Haiku) servem à comparação e às estimativas
    parciais = [r for r, v in rods.items() if v and len(v) < len(qids)]
    todas = {r: v for r, v in rods.items() if v}
    rods = {r: v for r, v in rods.items() if len(v) >= len(qids)}
    print(f"rodadas na decisão: {list(rods)}; parciais ignoradas: {parciais}")
    arb = carregar_rodada(ARBITRO, A)
    origem = carregar_origem()
    # pares confundíveis medidos com todas as rodadas (inclusive parciais) e o árbitro: é uma medida empírica de confusão
    conf_pairs = pares_confundiveis({**todas, ARBITRO: arb}, qids, a.min_par)
    ramos_risco = Counter()
    for (x, y), n in conf_pairs.items():
        ramos_risco[x] += n
        ramos_risco[y] += n

    regs, stats = [], Counter()
    for q in qids:
        votos = {r: rod[q][0] for r, rod in rods.items() if q in rod}
        va = arb.get(q, (None, None))[0]
        o = origem.get(q, {}).get("tema_id")
        ramo_origem = A.ramo_de(o) if o else None
        cont = Counter("FORA" if v["fora"] else v["ramo"] for v in votos.values())
        n_mod = sum(cont.values())
        reg = {"id": q, "n_modelos": n_mod, "votos_ramo": {r: ("FORA" if v["fora"] else v["ramo"]) for r, v in votos.items()},
               "votos_sub": {r: v["sub"] for r, v in votos.items() if v["sub"]},
               "arbitro": None if va is None else {"ramo": "FORA" if va["fora"] else va["ramo"], "sub": va["sub"],
                                                   "c_ramo": va["c_ramo"], "c_sub": va["c_sub"], "multi": va["multi"], "just": va["just"]},
               "origem_ramo": ramo_origem}
        decisao, tema, nivel, motivo, flags = "revisar", None, None, "", []
        if va is None:
            motivo = "sem árbitro"
            ramo_m = cont.most_common(1)[0][0] if cont else None
            tema = ramo_m if ramo_m and ramo_m != "FORA" else None
        else:
            ramo_a = "FORA" if va["fora"] else va["ramo"]
            frac_fora = cont.get("FORA", 0) / n_mod if n_mod else 0
            if ramo_a == "FORA" and frac_fora >= 0.5:
                decisao, motivo = "fora", "nenhum tema da árvore cobre a questão: " + va["just"][:150]
            elif ramo_a == "FORA" or (frac_fora > 0 and ramo_a != "FORA" and frac_fora >= 0.34):
                tema = None if ramo_a == "FORA" else ramo_a
                if tema is None:
                    tema = next((r for r, _ in cont.most_common() if r != "FORA"), None)
                motivo = "dúvida entre 'fora' e um tema da árvore"
            else:
                tema = va["sub"] or ramo_a
                fortes_ok = all(q in rods.get(f, {}) and rods[f][q][0]["ramo"] == ramo_a for f in FORTES)
                frac = cont.get(ramo_a, 0) / n_mod if n_mod else 0
                risco = ramos_risco.get(ramo_a, 0) > 0
                unanime = cont.get(ramo_a, 0) == n_mod
                if risco:
                    flags.append("ramo em par confundível")
                if va["multi"]:
                    flags.append("multi-tema")
                if ramo_origem and ramo_origem == ramo_a:
                    flags.append("origem concorda")
                pub = fortes_ok and frac >= a.min_frac and va["c_ramo"] >= a.t_arb and not va["multi"] and (unanime or not risco)
                if pub:
                    decisao = "publicar"
                    tema, nivel = ramo_a, 1
                    sub_a = va["sub"]
                    if a.modo == "hibrido" and sub_a:
                        subs = Counter(v["sub"] for v in list(votos.values()) + [va] if v["sub"] and v["ramo"] == ramo_a)
                        irmao = any(s != sub_a for s in subs)
                        opus_sub = rods.get("claude-opus", {}).get(q, (None,))[0]
                        if (opus_sub and opus_sub["sub"] == sub_a and not irmao and subs.get(sub_a, 0) >= a.min_sub
                                and va["c_sub"] >= a.t_sub):
                            tema, nivel = sub_a, 2
                else:
                    partes = []
                    if not fortes_ok:
                        desc = "; ".join(f"{r}: {A.titulo(v['ramo']) if v['ramo'] else 'fora'}" for r, v in votos.items() if r in FORTES)
                        partes.append(f"classificadores divergem do árbitro ({desc}; árbitro: {A.titulo(ramo_a)})")
                    elif frac < a.min_frac:
                        partes.append(f"só {cont.get(ramo_a, 0)} de {n_mod} votos no ramo {A.titulo(ramo_a)}")
                    if va["c_ramo"] < a.t_arb:
                        partes.append(f"árbitro com confiança {va['c_ramo']:.2f}")
                    if va["multi"]:
                        partes.append("questão multi-tema (alternativas sobre institutos diferentes)")
                    if risco and not unanime and fortes_ok and frac >= a.min_frac:
                        outros = [A.titulo(r) for r in cont if r not in (ramo_a, "FORA")]
                        partes.append(f"ramo sujeito a confusão com {', '.join(outros)}")
                    motivo = "; ".join(partes) or "evidência insuficiente"
        reg.update({"decisao": decisao, "tema": tema, "nivel": nivel if decisao == "publicar" else (A.t[tema]["nivel"] if tema in A.t else None),
                    "motivo": motivo[:240], "flags": flags})
        regs.append(reg)
        stats[(decisao, reg["nivel"] if decisao == "publicar" else None)] += 1

    # extras: outros temas citados pelo árbitro e pelo Opus plano, fora do ramo central
    for reg in regs:
        ex = []
        for fonte in ([arb.get(reg["id"], (None, None))[0]] + [rods.get("claude-opus", {}).get(reg["id"], (None,))[0]]):
            if not fonte:
                continue
            for e in fonte["extras"]:
                e2 = A.redirecionar(e)
                if e2 and reg["tema"] and A.ramo_de(e2) != A.ramo_de(reg["tema"]) and e2 not in ex:
                    ex.append(e2)
        reg["extras"] = ex[:3]

    # confiança = média entre a posterior de Dawid-Skene do ramo e a confiança do árbitro no nó escolhido,
    # menos a margem de convenção (o que nenhum modelo vê); para "fora", a confiança do árbitro em "fora"
    cpath = RAIZ / "data" / "confiabilidade.jsonl"
    ds = {json.loads(l)["id"]: json.loads(l) for l in cpath.open(encoding="utf-8")} if cpath.exists() else {}
    for reg in regs:
        ar = reg["arbitro"]
        if reg["decisao"] == "fora":
            reg["confianca"] = round(ar["c_ramo"] if ar else 0.5, 2)
            continue
        if not reg["tema"]:
            reg["confianca"] = 0.0
            continue
        ramo = A.ramo_de(reg["tema"])
        d = ds.get(reg["id"], {})
        p_ds = d.get("p_ramo_map", 0.5) if d.get("ramo_map") == ramo else (1 - d.get("p_ramo_map", 0.5)) / 2
        p_arb = 0.5
        if ar and ar["ramo"] == ramo:
            p_arb = ar["c_sub"] if (A.t[reg["tema"]]["nivel"] == 2 and ar["sub"] == reg["tema"]) else ar["c_ramo"]
        elif ar:
            p_arb = max(0.0, 1 - ar["c_ramo"]) / 2
        reg["confianca"] = round(max(0.0, min(1.0, (p_ds + p_arb) / 2 - a.margem)), 2)

    with open(a.saida_jsonl, "w", encoding="utf-8") as g:
        for r in regs:
            g.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(a.saida, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "decisao", "tema_central_id", "extras_ids", "confianca", "motivo"])
        for r in regs:
            w.writerow([r["id"], r["decisao"], r["tema"] or "" if r["decisao"] != "fora" else "", ";".join(r["extras"]) if r["decisao"] != "fora" else "",
                        f"{r.get('confianca', 0):.2f}", r["motivo"]])
    n = len(regs)
    pub = sum(v for (d, _), v in stats.items() if d == "publicar")
    print(f"modo={a.modo} min_frac={a.min_frac} t_arb={a.t_arb} t_sub={a.t_sub} min_sub={a.min_sub}; pares confundíveis={len(conf_pairs)}")
    for k, v in sorted(stats.items(), key=lambda x: -x[1]):
        print(f"  {k[0]:9s} nível {k[1]}: {v}")
    print(f"cobertura: {pub}/{n} = {pub / n:.1%}")
    top = sorted(conf_pairs.items(), key=lambda x: -x[1])[:12]
    print("pares confundíveis mais frequentes:", [(A.titulo(x)[:30], A.titulo(y)[:30], c) for (x, y), c in top])


if __name__ == "__main__":
    main()
