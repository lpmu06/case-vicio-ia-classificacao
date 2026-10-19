"""Etapa 5c: sensibilidade da regra de decisão aos limiares (cobertura x precisão estimada).

Roda src/47_decisao.py e src/60_previsao.py para uma grade de parâmetros, em arquivos temporários,
e tabula cobertura, publicações no subtema e os estimadores E1 (independência) e E2 (outra família).
Uso: python src/49_sensibilidade.py
Saída: docs/sensibilidade.md
"""
import itertools
import json
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
GRADE = {"t_arb": [0.7, 0.8, 0.9], "min_frac": [0.67, 0.75, 1.0], "modo": ["hibrido", "n1"]}


def main():
    tmp = Path(tempfile.mkdtemp())
    linhas = []
    for t_arb, min_frac, modo in itertools.product(GRADE["t_arb"], GRADE["min_frac"], GRADE["modo"]):
        dec, csvp, js = tmp / "d.jsonl", tmp / "p.csv", tmp / "prev.json"
        subprocess.run([sys.executable, str(RAIZ / "src" / "47_decisao.py"), "--t_arb", str(t_arb), "--min_frac", str(min_frac),
                        "--modo", modo, "--saida", str(csvp), "--saida_jsonl", str(dec)], check=True, capture_output=True)
        subprocess.run([sys.executable, str(RAIZ / "src" / "60_previsao.py"), "--decisoes", str(dec), "--saida_json", str(js)],
                       check=True, capture_output=True)
        r = json.loads(js.read_text(encoding="utf-8"))
        linhas.append({"t_arb": t_arb, "min_frac": min_frac, "modo": modo, "publicadas": r["publicadas"], "cobertura": r["cobertura_prevista"],
                       "nivel2": r["publicadas_nivel2"], "E1": r["E1_independencia"], "E2": r["E2_outra_familia"]["taxa"],
                       "E2_n": r["E2_outra_familia"]["n"]})
        print(linhas[-1], flush=True)
    md = ["# Sensibilidade da regra de decisão\n", "Gerado por `src/49_sensibilidade.py`. E1: precisão estimada supondo erros independentes "
          "(limite superior). E2: concordância do GPT-5.5 com o tema publicado nas questões que ele classificou.\n",
          "| Confiança mínima do árbitro | Fração mínima de votos no ramo | Modo | Publicadas | Cobertura | No subtema | E1 | E2 (n) |",
          "|---|---|---|---|---|---|---|---|"]
    for l in linhas:
        md.append(f"| {l['t_arb']} | {l['min_frac']} | {l['modo']} | {l['publicadas']} | {l['cobertura']:.1%} | {l['nivel2']} | "
                  f"{l['E1']:.1%} | {l['E2']:.1%} ({l['E2_n']}) |")
    (RAIZ / "docs" / "sensibilidade.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
