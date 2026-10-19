"""Etapa 1a: carrega temas.csv e gera data/temas.json (árvore) e data/arvore.txt (texto para prompts).

Regras registradas aqui (ver docs/00_entendimento_e_plano.md):
- temas inativos ficam marcados e nunca recebem publicação;
- temas 67xx com nomes de aula "(Parte N)" e cópias vazias ficam marcados como `bucket` (não publicar).
"""
import csv, json, re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

def carregar_temas():
    rows = list(csv.DictReader((RAIZ / "anexos" / "temas.csv").open(encoding="utf-8")))
    temas = {}
    for r in rows:
        m = re.search(r"(\d+)\s+quest", r["descricao"])
        temas[r["tema_id"]] = {
            "tema_id": r["tema_id"], "parent_id": r["parent_id"] or None, "disciplina": r["disciplina"],
            "nivel": int(r["nivel"]), "titulo": r["titulo"].strip(), "caminho": r["caminho"],
            "descricao_original": r["descricao"], "status": r["status"],
            "n_source": int(m.group(1)) if m else None,
            "bucket": bool(re.search(r"\(Parte \d+\)|Parte 0\d", r["titulo"])) or (int(r["tema_id"]) >= 6700),
            "filhos": [],
        }
    for t in temas.values():
        if t["parent_id"]:
            temas[t["parent_id"]]["filhos"].append(t["tema_id"])
    return temas

def arvore_texto(temas, incluir_marcas=True):
    linhas = []
    def walk(tid, prof):
        t = temas[tid]
        marca = ""
        if incluir_marcas:
            if t["status"] != "active": marca = "  [INATIVO - não usar]"
            elif t["bucket"]: marca = "  [bucket de curso - não usar]"
        rotulo = {0: "DISCIPLINA (nível 0)", 1: "tema (nível 1)", 2: "subtema (nível 2)"}[t["nivel"]]
        linhas.append(f"{'    ' * prof}{t['tema_id']} | {rotulo} | {t['titulo']}{marca}")
        for f in t["filhos"]:
            walk(f, prof + 1)
    for r in [t for t in temas.values() if t["nivel"] == 0]:
        walk(r["tema_id"], 0)
    return "\n".join(linhas)

if __name__ == "__main__":
    temas = carregar_temas()
    (RAIZ / "data" / "temas.json").write_text(json.dumps(temas, ensure_ascii=False, indent=1), encoding="utf-8")
    txt = arvore_texto(temas)
    (RAIZ / "data" / "arvore.txt").write_text(txt, encoding="utf-8")
    print(len(temas), "temas;", sum(t["bucket"] for t in temas.values()), "buckets;", len(txt), "chars na árvore")
