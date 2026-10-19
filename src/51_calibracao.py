"""Etapa 5b: calibração com o gabarito interno e previsão de precisão/cobertura.

Lê data/rotulos_humanos.csv (id, tema_id ou FORA) e data/ensemble.jsonl. Um acerto segue a régua do case:
o tema publicado é o rotulado, ou pai, ou filho dele. Calcula:
- precisão observada nas publicadas rotuladas (com intervalo de Wilson e bootstrap);
- precisão por faixa de confiança e por nível (1 ou 2);
- taxa de "fora"/"revisar" que o rotulador considerou publicável (cobertura perdida).
Grava runs/calibracao.json e imprime um rascunho para previsao.txt.

Uso: python src/51_calibracao.py
"""
import csv, importlib, json, math, random, sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
arv = importlib.import_module("10_arvore")
RAIZ = Path(__file__).resolve().parents[1]


def mesmo_ramo(pub, rot, temas):
    """Acerto pela régua: igual, pai ou filho."""
    if not pub or not rot or rot == "FORA":
        return False
    if pub == rot:
        return True
    return temas[pub]["parent_id"] == rot or temas[rot]["parent_id"] == pub


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0, c - h), min(1, c + h))


def main():
    temas = arv.carregar_temas()
    ens = {json.loads(l)["id"]: json.loads(l) for l in (RAIZ / "data" / "ensemble.jsonl").open(encoding="utf-8")}
    rot = {}
    for r in csv.DictReader((RAIZ / "data" / "rotulos_humanos.csv").open(encoding="utf-8")):
        if r["tema_id"].strip():
            rot[r["id"]] = r["tema_id"].strip().upper() if r["tema_id"].strip().upper() == "FORA" else r["tema_id"].strip()
    if not rot:
        print("nenhum rótulo preenchido em data/rotulos_humanos.csv"); return

    pub = [(i, ens[i]) for i in rot if ens[i]["decisao"] == "publicar"]
    acertos = [mesmo_ramo(e["tema"], rot[i], temas) for i, e in pub]
    k, n = sum(acertos), len(acertos)
    lo, hi = wilson(k, n)
    # bootstrap
    random.seed(0)
    bs = []
    for _ in range(2000):
        s = [random.choice(acertos) for _ in acertos] if acertos else [0]
        bs.append(sum(s) / len(s))
    bs.sort()
    b_lo, b_hi = bs[int(0.025 * len(bs))], bs[int(0.975 * len(bs))]

    por_nivel = defaultdict(lambda: [0, 0]); por_faixa = defaultdict(lambda: [0, 0])
    erros = []
    for (i, e), ok in zip(pub, acertos):
        por_nivel[e["nivel"]][1] += 1; por_nivel[e["nivel"]][0] += ok
        faixa = "≥0.95" if e["confianca"] >= 0.95 else "0.90–0.95" if e["confianca"] >= 0.90 else "<0.90"
        por_faixa[faixa][1] += 1; por_faixa[faixa][0] += ok
        if not ok:
            erros.append({"id": i, "publicado": e["tema"], "rotulo": rot[i], "confianca": e["confianca"]})

    nao_pub = [(i, ens[i]) for i in rot if ens[i]["decisao"] != "publicar"]
    publicaveis = sum(1 for i, e in nao_pub if rot[i] != "FORA")
    sugestao_ok = sum(1 for i, e in nao_pub if e["decisao"] == "revisar" and mesmo_ramo(e["tema"], rot[i], temas))

    total = len(ens)
    cobertura = sum(1 for e in ens.values() if e["decisao"] == "publicar") / total
    res = {"rotulados": len(rot), "publicadas_rotuladas": n, "acertos": k,
           "precisao_amostra": round(k / n, 4) if n else None, "wilson95": [round(lo, 4), round(hi, 4)],
           "bootstrap95": [round(b_lo, 4), round(b_hi, 4)],
           "por_nivel": {str(kk): {"acertos": v[0], "n": v[1]} for kk, v in por_nivel.items()},
           "por_faixa_confianca": {kk: {"acertos": v[0], "n": v[1]} for kk, v in por_faixa.items()},
           "nao_publicadas_rotuladas": len(nao_pub), "nao_publicadas_mas_publicaveis": publicaveis,
           "revisar_com_sugestao_certa": sugestao_ok, "cobertura_total": round(cobertura, 4), "erros": erros}
    (RAIZ / "runs" / "calibracao.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in res.items() if k != "erros"}, ensure_ascii=False, indent=1))
    print("erros:", erros)


if __name__ == "__main__":
    main()
