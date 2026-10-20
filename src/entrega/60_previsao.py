"""Etapa 6: previsão de precisão e cobertura sem gabarito -> runs/previsao.json (o texto sai de 61_escrever_previsao.py).

Estimadores da precisão do conjunto publicado (todos gravados; a previsão final combina de forma conservadora):
  E1 independência  posterior de Dawid-Skene do ramo (data/confiabilidade.jsonl; anotadores: as rodadas de classificação e a
                    origem, sem o árbitro). Para publicações no subtema, multiplica pela taxa de concordância de subtema.
                    Supõe erros independentes e as publicadas são justamente onde os anotadores concordam: é um teto do
                    modelo, usado só como limite superior do intervalo.
  E2 outra família  concordância do GPT-5.5 (única família diferente; 63 questões) com o tema publicado, pela régua.
  E3 auditoria      auditoria cega (data/auditoria_ia_v2.csv: amostra nova, caderno sem votos, agente com contexto limpo).
                    "duvidoso" vale --peso_duvida de erro no ponto (1/3) e 1/2 no limite inferior. A auditoria anterior
                    (data/auditoria_ia.csv), que viu os votos e serviu para escolher os limiares, é reportada à parte.
  Descontos: margem de convenção (em E1 e E2; E3 já a embute) e risco dos gêmeos 67xx, em todos os estimadores:
             p_copias × exposição às cópias de título idêntico + p_partes × exposição aos nomes de aula "(Parte N)".
  Ponto = média de E2 e E3 ajustados (E1 fica fora do ponto). Intervalo: inferior = menor limite inferior de Wilson entre
  E2 (com margem) e E3 conservador, menos o risco 67xx; superior = E1.
  Sensibilidade: grade p_copias ∈ {5, 10, 25}% (p_partes = metade) × peso da dúvida ∈ {1/3, 1/2, 1}.

Uso: python src/entrega/60_previsao.py [--margem_convencao 0.02 --p_copias 0.10 --p_partes 0.05 --peso_duvida 0.3333]
"""
import argparse
import csv
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import caminhos  # noqa: F401,E402  (pastas de etapas no sys.path)
from comum import Arvore, RAIZ, carregar_rodada, gemeos_67xx


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


def ler_auditoria(path, pub_por_id, peso):
    """Precisão observada numa auditoria, restrita às questões publicadas atuais. Devolve None se não houver dados."""
    if not path.exists():
        return None
    k = kc = n = 0.0
    duvidas = erros = 0
    for r in csv.DictReader(path.open(encoding="utf-8")):
        d = pub_por_id.get(r["id"])
        if not d or not r["veredito"].strip():
            continue
        v = r["veredito"].strip()
        if v == "duvidoso" and r.get("tipo_duvida") == "subtema" and d["nivel"] == 1:
            v = "ok"
        n += 1
        k += {"ok": 1.0, "duvidoso": 1 - peso, "erro": 0.0}[v]
        kc += {"ok": 1.0, "duvidoso": 0.5, "erro": 0.0}[v]
        duvidas += v == "duvidoso"
        erros += v == "erro"
    if not n:
        return None
    return {"arquivo": path.name, "n": n, "duvidosos": duvidas, "erros": erros, "pontos_central": round(k, 2),
            "pontos_conservador": kc, "taxa": round(k / n, 4), "taxa_conservadora": round(kc / n, 4),
            "wilson95_conservador": [round(x, 4) for x in wilson(kc, n)]}


def combinar(e1, e2, e2_ic, e3, margem, m67):
    """Ponto e intervalo a partir dos estimadores. e3 é o dict de ler_auditoria (ou None)."""
    ajustados = ([e2 - margem - m67] if e2 is not None else []) + ([e3["taxa"] - m67] if e3 else [])
    if not ajustados:
        ajustados = [e1 - margem - m67]
    ponto = sum(ajustados) / len(ajustados)
    inferiores = ([e2_ic[0] - margem] if e2_ic else []) + ([e3["wilson95_conservador"][0]] if e3 else [])
    lo = (min(inferiores) if inferiores else ponto - 0.05) - m67
    # superior: o teto do Dawid-Skene, limitado pelo limite superior de Wilson da auditoria (E1 é ~1 por construção)
    hi = min(e1 if e1 is not None else 1.0, e3["wilson95_conservador"][1] if e3 else 1.0, 1.0)
    lo = max(min(lo, ponto - 0.01), 0.0)
    hi = max(hi, ponto + 0.005)
    return ponto, lo, hi, ajustados


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--decisoes", default=str(RAIZ / "data" / "decisoes.jsonl"))
    ap.add_argument("--margem_convencao", type=float, default=0.02)
    ap.add_argument("--p_copias", type=float, default=0.10, help="probabilidade de a equipe ter usado as cópias 67xx de título idêntico")
    ap.add_argument("--p_partes", type=float, default=0.05, help="probabilidade de a equipe ter usado os gêmeos 'nome de aula (Parte N)'")
    ap.add_argument("--peso_duvida", type=float, default=1 / 3, help="fração de erro atribuída a um veredito 'duvidoso' no ponto")
    ap.add_argument("--saida_json", default=str(RAIZ / "runs" / "previsao.json"))
    a = ap.parse_args()

    A = Arvore()
    dec = [json.loads(l) for l in open(a.decisoes, encoding="utf-8")]
    n = len(dec)
    pub = [d for d in dec if d["decisao"] == "publicar"]
    fora = [d for d in dec if d["decisao"] == "fora"]
    npub = len(pub)
    pub_por_id = {d["id"]: d for d in pub}
    conf = {json.loads(l)["id"]: json.loads(l) for l in (RAIZ / "data" / "confiabilidade.jsonl").open(encoding="utf-8")}

    # taxa de concordância de subtema quando dois classificadores escolhem subtema no mesmo ramo
    # (sem os pares com o Jev, que entra só como estudo)
    comp = json.loads((RAIZ / "runs" / "comparacao_metodos.json").read_text(encoding="utf-8"))
    taxas_sub = [p["subtema_igual_quando_ambos_escolhem"] for p in comp["concordancia"]
                 if p["subtema_igual_quando_ambos_escolhem"] is not None and p["n_ambos_subtema"] >= 30
                 and not (p["a"].startswith("jev") or p["b"].startswith("jev"))]
    taxa_sub = sum(taxas_sub) / len(taxas_sub) if taxas_sub else 0.9

    # E1
    e1_vals = []
    for d in pub:
        c = conf.get(d["id"], {})
        pr = c.get("p_ramo_map", 0.0) if c.get("ramo_map") == A.ramo_de(d["tema"]) else 1 - c.get("p_ramo_map", 0.0)
        if d["nivel"] == 2:
            pr *= (1 + taxa_sub) / 2
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

    # E3: auditoria cega (v2) como estimador; a ancorada (v1) só reportada
    v2 = ler_auditoria(RAIZ / "data" / "auditoria_ia_v2.csv", pub_por_id, a.peso_duvida)
    v1 = ler_auditoria(RAIZ / "data" / "auditoria_ia.csv", pub_por_id, a.peso_duvida)
    e3 = v2 or v1
    e3_cega = v2 is not None

    # risco dos gêmeos 67xx
    gem = gemeos_67xx(A)
    por_tema = {}
    for d in pub:
        r = A.ramo_de(d["tema"])
        if r in gem:
            por_tema.setdefault(r, {"tema": r, "titulo": A.titulo(r), "grupo": gem[r]["grupo"], "gemeos": gem[r]["gemeos"], "publicadas": 0})
            por_tema[r]["publicadas"] += 1
    exp_c = sum(x["publicadas"] for x in por_tema.values() if x["grupo"] == "copia") / npub if npub else 0.0
    exp_p = sum(x["publicadas"] for x in por_tema.values() if x["grupo"] == "parte") / npub if npub else 0.0
    m67 = a.p_copias * exp_c + a.p_partes * exp_p

    ponto, lo, hi, ajustados = combinar(e1, e2, e2_ic, e3, a.margem_convencao, m67)

    # sensibilidade: p das cópias (p_partes = metade) × peso da dúvida
    grade = []
    for p_c in (0.05, 0.10, 0.25):
        for peso in (1 / 3, 1 / 2, 1.0):
            e3_g = (ler_auditoria(RAIZ / "data" / "auditoria_ia_v2.csv", pub_por_id, peso)
                    or ler_auditoria(RAIZ / "data" / "auditoria_ia.csv", pub_por_id, peso))
            m = p_c * exp_c + (p_c / 2) * exp_p
            pt, _, _, _ = combinar(e1, e2, e2_ic, e3_g, a.margem_convencao, m)
            grade.append({"p_copias": p_c, "p_partes": round(p_c / 2, 3), "peso_duvida": round(peso, 3), "precisao": round(pt, 3)})

    cob = npub / n
    cob_hi = npub / (n - len(fora)) if n - len(fora) else cob
    sem_desconto = ponto + m67
    res = {"publicadas": npub, "total": n, "fora": len(fora), "revisar": n - npub - len(fora),
           "publicadas_nivel2": sum(1 for d in pub if d["nivel"] == 2),
           "E1_independencia": round(e1, 4) if e1 is not None else None,
           "E2_outra_familia": {"acertos": k2, "n": n2, "taxa": round(e2, 4) if e2 is not None else None,
                                "wilson95": [round(x, 4) for x in e2_ic] if e2_ic else None},
           "E3_auditoria": {**(e3 or {}), "cega": e3_cega},
           "E3_ancorada": v1,
           "peso_duvida": round(a.peso_duvida, 4), "margem_convencao": a.margem_convencao, "taxa_subtema": round(taxa_sub, 4),
           "copias_67xx": {"p_copias": a.p_copias, "p_partes": a.p_partes,
                           "exposicao_copias": round(exp_c, 4), "exposicao_partes": round(exp_p, 4),
                           "n_copias": sum(x["publicadas"] for x in por_tema.values() if x["grupo"] == "copia"),
                           "n_partes": sum(x["publicadas"] for x in por_tema.values() if x["grupo"] == "parte"),
                           "perda_esperada": round(m67, 4),
                           "precisao_se_copias": round(sem_desconto - exp_c, 3),
                           "precisao_se_todos": round(sem_desconto - exp_c - exp_p, 3),
                           "por_tema": sorted(por_tema.values(), key=lambda x: -x["publicadas"]),
                           # compatibilidade com leitores antigos
                           "p_cenario": a.p_copias, "exposicao": round(exp_c, 4), "precisao_se_cenario_ocorrer": round(sem_desconto - exp_c, 3)},
           "estimadores_ajustados": [round(x, 4) for x in ajustados],
           "sensibilidade": grade,
           "precisao_prevista": round(ponto, 3), "precisao_intervalo": [round(lo, 3), round(hi, 3)],
           "cobertura_prevista": round(cob, 3), "cobertura_intervalo": [round(cob, 3), round(cob_hi, 3)]}
    Path(a.saida_json).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in res.items() if k not in ("sensibilidade",)}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
