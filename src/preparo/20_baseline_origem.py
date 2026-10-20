"""Etapa 2 (baseline A0): "copiar a origem".

Mapeia assunto_origem -> tema pelo título (normalizado), restrito à disciplina de origem.
Não é uma solução; serve para medir quão longe a origem fica dos modelos e como voto fraco no ensemble.
Saída: data/baseline_origem.jsonl
"""
import importlib, json, re, sys, unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import caminhos  # noqa: F401,E402  (pastas de etapas no sys.path)
arv = importlib.import_module("10_arvore")
RAIZ = Path(__file__).resolve().parents[2]

DISC = {"Direito Penal": "Penal", "Penal": "Penal", "Processo Penal": "Processo Penal",
        "Direito Processual Penal": "Processo Penal", "Criminologia": "Criminologia",
        "Direito Penal - Legislação Especial": "Direito Penal - Legislação Especial"}

def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    s = re.sub(r"\(.*?\)|parte \d+", " ", s)
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def main():
    temas = arv.carregar_temas()
    usaveis = [t for t in temas.values() if t["nivel"] > 0 and t["status"] == "active" and not t["bucket"]]
    por_titulo = {}
    for t in usaveis:
        por_titulo.setdefault(norm(t["titulo"]), []).append(t)
    qs = [json.loads(l) for l in (RAIZ / "data" / "questoes_limpas.jsonl").open(encoding="utf-8")]
    saida, n_ok = [], 0
    for q in qs:
        disc = DISC.get(q["disciplina_origem"])
        cands = por_titulo.get(norm(q["assunto_origem"]), [])
        if disc:
            mesmo = [t for t in cands if t["disciplina"] == disc]
            cands = mesmo or cands
        tema = cands[0]["tema_id"] if len(cands) == 1 else None
        n_ok += tema is not None
        saida.append({"id": q["id"], "tema_id": tema, "ambiguo": len(cands) > 1,
                      "candidatos": [c["tema_id"] for c in cands]})
    with (RAIZ / "data" / "baseline_origem.jsonl").open("w", encoding="utf-8") as g:
        for s in saida:
            g.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"{n_ok}/{len(qs)} questões com tema único pela origem; "
          f"{sum(s['ambiguo'] for s in saida)} ambíguas; {len(qs)-n_ok-sum(s['ambiguo'] for s in saida)} sem match")

if __name__ == "__main__":
    main()
