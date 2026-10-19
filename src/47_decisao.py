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
from comum import Arvore, RAIZ, carregar_rodada, carregar_questoes, carregar_origem, norm

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
    ap.add_argument("--t_arb", type=float, default=0.90)
    ap.add_argument("--t_sub", type=float, default=0.90)
    ap.add_argument("--min_sub", type=int, default=2, help="mínimo de votos (incluindo o árbitro) no mesmo subtema")
    ap.add_argument("--min_par", type=int, default=3, help="mínimo de questões para um par de ramos ser 'confundível'")
    ap.add_argument("--margem", type=float, default=0.02, help="margem de convenção descontada da confiança")
    ap.add_argument("--evitar_duplicados", action="store_true",
                    help="manda para revisar as questões de temas da Legislação Especial que têm cópia em Penal/Processo Penal (ids 67xx)")
    ap.add_argument("--votantes", default="claude-opus,claude-sonnet-h",
                    help="rodadas completas que votam na decisão, além do árbitro (as melhores no experimento 2x2)")
    ap.add_argument("--saida", default=str(RAIZ / "publicacao.csv"))
    ap.add_argument("--saida_jsonl", default=str(RAIZ / "data" / "decisoes.jsonl"))
    a = ap.parse_args()

    A = Arvore()
    qs = carregar_questoes()
    qids = [q["id"] for q in qs]
    rods = {r: carregar_rodada(r, A) for r in CLASSIFICADORES}
    # só rodadas completas entram na regra, para o critério ser o mesmo em todas as questões;
    # as parciais (amostra 2x2, GPT, Haiku) servem à comparação e às estimativas
    todas = {r: v for r, v in rods.items() if v}
    votantes = a.votantes.split(",")
    rods = {r: v for r, v in rods.items() if r in votantes and len(v) >= len(qids)}
    assert set(rods) == set(votantes), f"rodadas votantes incompletas: {set(votantes) - set(rods)}"
    print(f"rodadas na decisão: {list(rods)} + árbitro; demais (só pares confundíveis e estimativas): {[r for r in todas if r not in rods]}")
    arb = carregar_rodada(ARBITRO, A)
    origem = carregar_origem()
    # pares confundíveis medidos com todas as rodadas (inclusive parciais) e o árbitro: é uma medida empírica de confusão
    conf_pairs = pares_confundiveis({**todas, ARBITRO: arb}, qids, a.min_par)
    ramos_risco = Counter()
    for (x, y), n in conf_pairs.items():
        ramos_risco[x] += n
        ramos_risco[y] += n

    # temas usáveis que têm uma cópia "bucket" (ids 67xx) em outra disciplina, com o mesmo título
    duplicados_le = {}
    for t in A.t.values():
        if t["bucket"] and t["status"] == "active":
            for c in A.por_titulo.get(norm(t["titulo"]), []):
                if c["tema_id"] != t["tema_id"] and not c["bucket"] and c["nivel"] == 1:
                    duplicados_le[c["tema_id"]] = t["disciplina"]
    if "4696" in A.t and "6722" in A.t:  # "Estaturo de Idoso" (erro de grafia) x "Estatuto do Idoso - Crimes"
        duplicados_le["4696"] = A.t["6722"]["disciplina"]
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
                motivo = (f"dúvida entre 'fora' (nenhum tema serve) e {A.rotulo(tema)}" if tema
                          else "dúvida entre 'fora' e um tema da árvore")
            else:
                tema = va["sub"] or ramo_a
                fortes_ok = all(q in rods.get(f, {}) and rods[f][q][0]["ramo"] == ramo_a for f in FORTES)
                frac = cont.get(ramo_a, 0) / n_mod if n_mod else 0
                risco = ramos_risco.get(ramo_a, 0) > 0
                # nos ramos confundíveis, exige que TODAS as rodadas disponíveis (inclusive as não votantes) concordem
                unanime = all(rod[q][0]["ramo"] == ramo_a for rod in todas.values() if q in rod and not rod[q][0]["fora"])
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
                    # motivo escrito para o professor: "dúvida entre X e Y", com a razão principal
                    alternativas = []
                    seg = A.redirecionar(arb[q][1].get("segunda_opcao_id")) if q in arb else None
                    candidatos = [seg] + [v["sub"] or v["ramo"] for v in votos.values() if not v["fora"]]
                    for c in candidatos:
                        if c and A.ramo_de(c) != A.ramo_de(tema) and c not in alternativas:
                            alternativas.append(c)
                    if not alternativas:
                        for c in [seg] + [v["sub"] for v in votos.values()]:
                            if c and c != tema and c not in alternativas and A.ramo_de(c) == A.ramo_de(tema):
                                alternativas.append(c)
                    base = (f"dúvida entre {A.rotulo(tema)} e {' / '.join(A.rotulo(x) for x in alternativas[:2])}" if alternativas
                            else f"tema provável {A.rotulo(tema)}, mas sem segurança suficiente")
                    razoes = []
                    if not fortes_ok:
                        razoes.append("os classificadores não concordam no tema")
                    if va["multi"]:
                        razoes.append("cada alternativa cobra um instituto diferente")
                    if risco and not unanime and fortes_ok:
                        razoes.append("ramos que os modelos costumam confundir")
                    if va["c_ramo"] < a.t_arb and not razoes:
                        razoes.append("fronteira entre temas")
                    motivo = f"{base} ({'; '.join(razoes)}; confiança do revisor automático {va['c_ramo']:.2f})" if razoes else base
        if a.evitar_duplicados and decisao == "publicar" and A.ramo_de(tema) in duplicados_le:
            decisao, nivel = "revisar", None
            motivo = (f"tema provável {A.rotulo(tema)}, mas ele existe em duplicata (Legislação Especial e cópia recente em "
                      f"{duplicados_le[A.ramo_de(tema)]}); confirmar qual dos dois a equipe usa")
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
