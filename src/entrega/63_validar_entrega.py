"""Valida publicacao.csv (e variantes) contra o formato do LEIA-ME e contra a árvore.

Uso: python src/entrega/63_validar_entrega.py [arquivo.csv ...]
"""
import csv
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import caminhos  # noqa: F401,E402  (pastas de etapas no sys.path)
from comum import Arvore, usavel


def validar(caminho):
    A = Arvore()
    ids = [json.loads(l)["id"] for l in (RAIZ / "anexos" / "questoes.jsonl").open(encoding="utf-8")]
    linhas = list(csv.DictReader(open(caminho, encoding="utf-8")))
    erros = []
    if [*linhas[0].keys()] != ["id", "decisao", "tema_central_id", "extras_ids", "confianca", "motivo"]:
        erros.append(f"colunas: {list(linhas[0].keys())}")
    if sorted(r["id"] for r in linhas) != sorted(ids):
        erros.append("os ids não são exatamente as 359 questões")
    for r in linhas:
        d, t = r["decisao"], r["tema_central_id"]
        if d not in ("publicar", "revisar", "fora"):
            erros.append(f"{r['id']}: decisão inválida {d}")
        if d in ("publicar", "revisar") and not t:
            erros.append(f"{r['id']}: {d} sem tema")
        if d == "fora" and t:
            erros.append(f"{r['id']}: fora com tema")
        if t and (t not in A.t or not usavel(A.t[t])):
            erros.append(f"{r['id']}: tema {t} inexistente, raiz, inativo ou bucket")
        for e in filter(None, r["extras_ids"].split(";")):
            if e not in A.t or A.t[e]["status"] != "active":
                erros.append(f"{r['id']}: extra {e} inválido")
        c = float(r["confianca"])
        if not 0 <= c <= 1:
            erros.append(f"{r['id']}: confiança {c} fora de [0,1]")
        if d in ("revisar", "fora") and not r["motivo"].strip():
            erros.append(f"{r['id']}: {d} sem motivo")
    from collections import Counter
    print(f"{caminho}: {len(linhas)} linhas {dict(Counter(r['decisao'] for r in linhas))} -> {'OK' if not erros else f'{len(erros)} ERROS'}")
    for e in erros[:20]:
        print("   ", e)
    return not erros


if __name__ == "__main__":
    arqs = sys.argv[1:] or [str(RAIZ / f) for f in ("publicacao.csv", "publicacao_subtema.csv", "publicacao_sem_duplicados.csv")]
    ok = all([validar(a) for a in arqs])
    sys.exit(0 if ok else 1)
