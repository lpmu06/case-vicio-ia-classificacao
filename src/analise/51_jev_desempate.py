"""Etapa 5c: o Jev como camada final de desempate nas questões que a regra mandou para revisão.

Ideia (19/10/2026, noite): no fim do pipeline sobram poucos temas candidatos por questão, então o Jev escolhe
entre 2 a 4 opções em vez de 89. Com poucas opções cabem as descrições inteiras (sem o corte do "não confundir")
e o viés de ordem é neutralizado perguntando em duas ordens (original e invertida) e tirando a média.

Candidatos: os ramos votados por todas as rodadas não-Jev (completas e parciais), o ramo do árbitro e a segunda opção
do árbitro (quando é de nível 1); 'fora' entra se alguém votou 'fora'. Questões com um só candidato ficam de fora
(estão em revisão por outro motivo, e o Jev não tem o que escolher).

Regra de promoção, fixada antes de qualquer auditoria: a questão passa de 'revisar' para 'publicar' no ramo escolhido
quando a escolha do Jev é o ramo do árbitro, não é 'fora', e a probabilidade média é >= 0,90.

Validação (--caderno): auditoria cega com controles. As promovidas entram misturadas, em ordem aleatória, com questões
publicadas que nenhuma auditoria anterior viu, no mesmo formato do caderno cego v2 (src/analise/48_auditoria.py --cego). O
auditor não sabe quais são quais; a chave fica em runs/jev_desempate.json.

Uso: python src/analise/51_jev_desempate.py                  (chama o Jev; ~US$ 0,03)
     python src/analise/51_jev_desempate.py --caderno --controles 40
     python src/analise/51_jev_desempate.py --avaliar        (depois que o auditor preencher o CSV)
Saída: runs/jev-desempate/Q*.json, runs/jev_desempate.json, docs/auditoria_jev_caderno_{1,2}.md, data/auditoria_ia_v3_{1,2}.csv
"""
import argparse
import csv
import importlib
import json
import math
import random
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import caminhos  # noqa: F401,E402  (pastas de etapas no sys.path)
from config import carregar_chaves
from comum import Arvore, RAIZ, carregar_rodada, carregar_questoes, usavel

j33 = importlib.import_module("33_classificar_jev")
aud = importlib.import_module("48_auditoria")

NAO_JEV = ["claude-opus", "claude-sonnet-h", "claude-sonnet-3n", "claude-haiku-h", "claude-haiku-3n",
           "claude-sonnet-plano", "claude-opus-h", "gpt-5.5", "arbitro-opus"]
LIMIAR = 0.90
INSTR = ("Esta é uma questão de concurso público jurídico brasileiro. Qual destes temas de estudo da plataforma ela testa? "
         "Escolha o tema cujo instituto jurídico é necessário para responder, não o cenário da história. "
         "Use 'fora' apenas se nenhum tema servir.")
PASTA = RAIZ / "runs" / "jev-desempate"
RESUMO = RAIZ / "runs" / "jev_desempate.json"
CADERNO = RAIZ / "docs" / "auditoria_jev_caderno_{}.md"
CSV_AUD = RAIZ / "data" / "auditoria_ia_v3_{}.csv"
PARTES = 2  # dois auditores, cada um com metade do caderno embaralhado


def ramo(v):
    return "FORA" if v["fora"] else v["ramo"]


def candidatos(A, rods, q):
    c = {ramo(rods[r][q][0]) for r in NAO_JEV if q in rods[r]}
    seg = A.redirecionar(rods["arbitro-opus"][q][1].get("segunda_opcao_id")) if q in rods["arbitro-opus"] else None
    if seg and A.t[seg]["nivel"] == 1:
        c.add(seg)
    c.discard(None)
    return sorted(c, key=lambda x: (x == "FORA", x))


def criterio(A, enr, tid):
    if tid == "FORA":
        return {"what": j33.FORA_TXT}
    t, e = A.t[tid], enr.get(tid, {})
    d = {"what": e.get("descricao", ""), "not_for": j33.nao_confundir(A, e), "key_terms": e.get("palavras_chave", [])}
    filhos = j33.ativos(A, t["filhos"])
    if filhos:
        d["subtopics"] = [f["titulo"] for f in filhos]
    return d


def perguntar_duas_ordens(chave, estado, crit, uso):
    nomes = list(crit)
    soma = dict.fromkeys(nomes, 0.0)
    for ordem in (nomes, nomes[::-1]):
        r, u, m = j33.chamar(chave, "jev-latest", estado, INSTR, {n: crit[n] for n in ordem})
        for n in nomes:
            soma[n] += r["probabilities"].get(n, 0.0) / 2
        uso["chamadas"] += 1
        uso["input_tokens"] += u.get("input_tokens", 0)
        uso["modelo"] = m
    return soma


def rodar(A, rods, pub, qs):
    chaves = carregar_chaves()
    chave = chaves.get("typesafe") or chaves.get("jev")
    enr = json.loads((RAIZ / "data" / "temas_enriquecidos.json").read_text(encoding="utf-8"))
    PASTA.mkdir(parents=True, exist_ok=True)
    rev = [q for q in pub if pub[q]["decisao"] == "revisar"]

    def tarefa(q):
        arq = PASTA / f"{q}.json"
        if arq.exists():
            return
        cands = candidatos(A, rods, q)
        out = {"id": q, "candidatos": cands, "ramo_arbitro": ramo(rods["arbitro-opus"][q][0])}
        if len(cands) >= 2:
            # nomes legíveis (caminho do tema); 'fora' com esse nome, como nas instruções
            nome = {c: ("fora" if c == "FORA" else A.t[c]["caminho"]) for c in cands}
            uso = {"chamadas": 0, "input_tokens": 0, "output_tokens": 0, "modelo": None}
            p = perguntar_duas_ordens(chave, qs[q]["texto"][:6000], {nome[c]: criterio(A, enr, c) for c in cands}, uso)
            probs = {c: p[nome[c]] for c in cands}
            esc = max(probs, key=probs.get)
            out.update({"probabilidades": probs, "escolha": esc, "p_escolha": probs[esc], "uso": uso,
                        "promovida": esc == out["ramo_arbitro"] and esc != "FORA" and probs[esc] >= LIMIAR})
        else:
            out.update({"escolha": None, "promovida": False, "motivo": "um só candidato"})
        arq.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    with ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(tarefa, rev))
    feitos = [json.loads((PASTA / f"{q}.json").read_text(encoding="utf-8")) for q in rev]
    tok = sum(d.get("uso", {}).get("input_tokens", 0) for d in feitos)
    perg = [d for d in feitos if d["escolha"]]
    res = {"revisar": len(rev), "com_2_ou_mais_candidatos": len(perg),
           "escolha_igual_arbitro": sum(d["escolha"] == d["ramo_arbitro"] for d in perg),
           "promovidas": sorted(d["id"] for d in feitos if d["promovida"]),
           "discorda_do_arbitro_com_p_alta": sorted(d["id"] for d in perg if d["escolha"] != d["ramo_arbitro"] and d["p_escolha"] >= LIMIAR),
           "limiar": LIMIAR, "tokens_entrada": tok, "custo_usd": round(tok * j33.PRECO_POR_MILHAO / 1e6, 4)}
    for t in (0.8, 0.9, 0.95, 0.99):
        res[f"promovidas_com_limiar_{t}"] = sum(d["escolha"] == d["ramo_arbitro"] and d["escolha"] != "FORA" and d["p_escolha"] >= t for d in perg)
    RESUMO.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in res.items()}, ensure_ascii=False, indent=1))


def caderno(A, pub, qs, n_controles, semente):
    res = json.loads(RESUMO.read_text(encoding="utf-8"))
    enr = json.loads((RAIZ / "data" / "temas_enriquecidos.json").read_text(encoding="utf-8"))
    ja = set()
    for arq in ("auditoria_ia.csv", "auditoria_ia_v2.csv"):
        ja |= {r["id"] for r in csv.DictReader(open(RAIZ / "data" / arq, encoding="utf-8"))}
    elegiveis = sorted(q for q in pub if pub[q]["decisao"] == "publicar" and q not in ja)
    rnd = random.Random(semente)
    controles = sorted(rnd.sample(elegiveis, min(n_controles, len(elegiveis))))
    tema = {q: json.loads((PASTA / f"{q}.json").read_text(encoding="utf-8"))["escolha"] for q in res["promovidas"]}
    tema.update({q: pub[q]["tema_central_id"] for q in controles})
    ordem = sorted(tema)
    rnd.shuffle(ordem)
    blocos = {}
    for q in ordem:
        md = blocos[q] = []
        t = A.t[tema[q]]
        e = enr.get(t["tema_id"], {})
        if t["nivel"] == 2:
            viz = ("irmãos (subtemas do mesmo tema)", [A.titulo(x) for x in A.t[t["parent_id"]]["filhos"] if x != t["tema_id"] and usavel(A.t[x])])
        else:
            viz = ("subtemas deste tema", [A.titulo(x) for x in t["filhos"] if usavel(A.t[x])])
        md.append(f"\n---\n\n## {q} → publicado em {t['tema_id']} · {t['caminho']} (nível {t['nivel']})\n")
        md.append("```\n" + qs[q]["texto"] + "\n```\n")
        md.append(f"- descrição do tema: {e.get('descricao', '')}")
        md.append(f"- não confundir: {e.get('nao_confundir', '')}")
        md.append(f"- {viz[0]}: {'; '.join(viz[1]) or 'nenhum'}")
        md.append("- outros temas de nível 1 com título parecido: " + "; ".join(f"{p['tema_id']} {p['caminho']}" for p in aud.parecidos(A, t["tema_id"])))
    for k in range(PARTES):
        parte = ordem[k::PARTES]
        md = ["# Caderno de auditoria cega (questões publicadas, sem os votos do pipeline)\n",
              "Para cada questão: o texto, o tema em que foi publicada, a descrição desse tema e os temas vizinhos. "
              "A árvore completa está em `data/arvore.txt`. Instruções para o auditor em `prompts/auditoria_cega.md`.\n"]
        for q in parte:
            md += blocos[q]
        Path(str(CADERNO).format(k + 1)).write_text("\n".join(md) + "\n", encoding="utf-8")
        with open(str(CSV_AUD).format(k + 1), "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["id", "tema_publicado", "veredito", "tipo_duvida", "tema_sugerido", "comentario"])
            for q in parte:
                w.writerow([q, tema[q], "", "", "", ""])
    res["controles"] = controles
    res["semente_caderno"] = semente
    RESUMO.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"caderno: {len(ordem)} questões ({len(res['promovidas'])} promovidas + {len(controles)} controles, de {len(elegiveis)} elegíveis)")


def wilson(k, n, z=1.96):
    if not n:
        return (None, None)
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (round(c - m, 3), round(c + m, 3))


def avaliar():
    res = json.loads(RESUMO.read_text(encoding="utf-8"))
    linhas = {r["id"]: r for k in range(PARTES) for r in csv.DictReader(open(str(CSV_AUD).format(k + 1), encoding="utf-8"))}
    assert all(r["veredito"] for r in linhas.values()), "auditoria incompleta"
    out = {}
    for grupo, ids in (("promovidas", res["promovidas"]), ("controles", res["controles"])):
        v = [linhas[q]["veredito"] for q in ids]
        n, ok, duv, err = len(v), v.count("ok"), v.count("duvidoso"), v.count("erro")
        out[grupo] = {"n": n, "ok": ok, "duvidoso": duv, "erro": err, "taxa_ok": round(ok / n, 3), "ic95_ok": wilson(ok, n),
                      "taxa_erro": round(err / n, 3), "ic95_erro": wilson(err, n)}
    res["auditoria"] = out
    RESUMO.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1))
    for q in res["promovidas"]:
        r = linhas[q]
        if r["veredito"] != "ok":
            print("promovida", q, r["veredito"], r["tipo_duvida"], r["tema_sugerido"], r["comentario"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--caderno", action="store_true")
    ap.add_argument("--controles", type=int, default=40)
    ap.add_argument("--semente", type=int, default=1910)
    ap.add_argument("--avaliar", action="store_true")
    a = ap.parse_args()
    if a.avaliar:
        return avaliar()
    A = Arvore()
    qs = {q["id"]: q for q in carregar_questoes()}
    pub = {r["id"]: r for r in csv.DictReader(open(RAIZ / "publicacao.csv", encoding="utf-8"))}
    if a.caderno:
        return caderno(A, pub, qs, a.controles, a.semente)
    rods = {r: carregar_rodada(r, A) for r in NAO_JEV}
    rodar(A, rods, pub, qs)


if __name__ == "__main__":
    main()
