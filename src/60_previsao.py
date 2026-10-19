"""Etapa 6: previsão de precisão e cobertura sem gabarito -> previsao.txt e runs/previsao.json.

Estimadores da precisão do conjunto publicado (todos registrados; a previsão final combina de forma conservadora):
  E1 independência  posterior de Dawid-Skene do ramo (data/confiabilidade.jsonl); para publicações no subtema,
                    multiplica pela taxa de concordância de subtema entre classificadores. Supõe erros independentes:
                    é um limite superior.
  E2 outra família  concordância do GPT-5.5 (única família diferente; 63 questões) com o tema publicado, pela régua.
  E3 auditoria      auditoria cética, questão a questão, de uma amostra aleatória das publicadas
                    (data/auditoria_ia.csv: id, veredito ok/duvidoso/erro). Duvidoso conta como meio erro.
  Margem de convenção: o professor pode seguir convenções que nenhum modelo conhece (por exemplo, onde guarda
                    progressão de regime ou o princípio da insignificância). Não é estimável sem gabarito; entra
                    como desconto explícito (--margem_convencao).

Uso: python src/60_previsao.py [--margem_convencao 0.02]
"""
import argparse
import csv
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import Arvore, RAIZ, carregar_rodada


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--decisoes", default=str(RAIZ / "data" / "decisoes.jsonl"))
    ap.add_argument("--margem_convencao", type=float, default=0.02)
    ap.add_argument("--saida_json", default=str(RAIZ / "runs" / "previsao.json"))
    a = ap.parse_args()

    A = Arvore()
    dec = [json.loads(l) for l in open(a.decisoes, encoding="utf-8")]
    n = len(dec)
    pub = [d for d in dec if d["decisao"] == "publicar"]
    fora = [d for d in dec if d["decisao"] == "fora"]
    npub = len(pub)
    conf = {json.loads(l)["id"]: json.loads(l) for l in (RAIZ / "data" / "confiabilidade.jsonl").open(encoding="utf-8")}

    # taxa de concordância de subtema quando dois classificadores escolhem subtema no mesmo ramo
    comp = json.loads((RAIZ / "runs" / "comparacao_metodos.json").read_text(encoding="utf-8"))
    taxas_sub = [p["subtema_igual_quando_ambos_escolhem"] for p in comp["concordancia"]
                 if p["subtema_igual_quando_ambos_escolhem"] is not None and p["n_ambos_subtema"] >= 30]
    taxa_sub = sum(taxas_sub) / len(taxas_sub) if taxas_sub else 0.9

    # E1
    e1_vals = []
    for d in pub:
        c = conf.get(d["id"], {})
        pr = c.get("p_ramo_map", 0.0) if c.get("ramo_map") == A.ramo_de(d["tema"]) else 1 - c.get("p_ramo_map", 0.0)
        if d["nivel"] == 2:
            pr *= (1 + taxa_sub) / 2  # o subtema publicado é o do árbitro e do Opus; meio caminho entre a taxa par a par e 1
        e1_vals.append(pr)
    e1 = sum(e1_vals) / npub if npub else None

    # E2
    gpt = carregar_rodada("gpt-5.5", A)
    k2 = n2 = 0
    for d in pub:
        if d["id"] in gpt:
            v = gpt[d["id"]][0]
            n2 += 1
            alvo = v["sub"] or v["ramo"]
            k2 += 1 if (alvo and (A.acerto(d["tema"], alvo) or A.ramo_de(alvo) == A.ramo_de(d["tema"]) and A.t[d["tema"]]["nivel"] == 1)) else 0
    e2 = (k2 / n2) if n2 else None
    e2_ic = wilson(k2, n2) if n2 else None

    # E3: a auditoria já embute o risco de convenção (cada "duvidoso" é uma convenção plausível diferente da nossa).
    # Estimativa central: duvidoso = 1/3 de erro (avaliação do auditor); conservadora (limite inferior): 1/2.
    # Dúvida só de subtema irmão não conta quando a questão foi publicada no tema de nível 1.
    aud_path = RAIZ / "data" / "auditoria_ia.csv"
    e3 = e3_cons = e3_ic = None
    k3 = k3c = n3 = 0.0
    if aud_path.exists():
        pub_por_id = {d["id"]: d for d in pub}
        for r in csv.DictReader(aud_path.open(encoding="utf-8")):
            d = pub_por_id.get(r["id"])
            if not d or not r["veredito"].strip():
                continue
            v = r["veredito"].strip()
            if v == "duvidoso" and r.get("tipo_duvida") == "subtema" and d["nivel"] == 1:
                v = "ok"
            n3 += 1
            k3 += {"ok": 1.0, "duvidoso": 2 / 3, "erro": 0.0}[v]
            k3c += {"ok": 1.0, "duvidoso": 0.5, "erro": 0.0}[v]
        if n3:
            e3, e3_cons = k3 / n3, k3c / n3
            e3_ic = wilson(k3c, n3)

    # combinação conservadora: E1 e E2 não enxergam convenções do professor, então descontam a margem; E3 já a embute.
    # ponto = menor estimativa; intervalo: inferior = menor limite inferior de Wilson (E2 com margem, E3 conservador),
    # superior = E1 (independência).
    pontos = [x - a.margem_convencao for x in (e1, e2) if x is not None] + ([e3] if e3 is not None else [])
    ponto = min(pontos)
    inferiores = ([e2_ic[0] - a.margem_convencao] if e2_ic else []) + ([e3_ic[0]] if e3_ic else [])
    lo = min(inferiores) if inferiores else ponto - 0.05
    hi = min(e1 if e1 else 1.0, 1.0)
    lo = max(min(lo, ponto - 0.01), 0.0)
    hi = max(hi, ponto + 0.005)
    cob = npub / n
    cob_hi = npub / (n - len(fora)) if n - len(fora) else cob

    res = {"publicadas": npub, "total": n, "fora": len(fora), "revisar": n - npub - len(fora),
           "publicadas_nivel2": sum(1 for d in pub if d["nivel"] == 2),
           "E1_independencia": round(e1, 4) if e1 is not None else None,
           "E2_outra_familia": {"acertos": k2, "n": n2, "taxa": round(e2, 4) if e2 is not None else None,
                                "wilson95": [round(x, 4) for x in e2_ic] if e2_ic else None},
           "E3_auditoria": {"pontos_central": round(k3, 2), "pontos_conservador": k3c, "n": n3,
                            "taxa": round(e3, 4) if e3 is not None else None,
                            "taxa_conservadora": round(e3_cons, 4) if e3_cons is not None else None,
                            "wilson95_conservador": [round(x, 4) for x in e3_ic] if e3_ic else None},
           "margem_convencao": a.margem_convencao, "taxa_subtema": round(taxa_sub, 4),
           "precisao_prevista": round(ponto, 3), "precisao_intervalo": [round(lo, 3), round(hi, 3)],
           "cobertura_prevista": round(cob, 3), "cobertura_intervalo": [round(cob, 3), round(cob_hi, 3)]}
    Path(a.saida_json).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
