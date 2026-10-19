"""Etapa 7b: gera docs/relatorio.pdf (relatório + memo) a partir do Markdown, via HTML e Chrome headless.

Uso: python src/64_gerar_pdf.py
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

import markdown

RAIZ = Path(__file__).resolve().parents[1]
CSS = """
@page { size: A4; margin: 14mm 15mm 14mm 15mm; }
body { font-family: "Segoe UI", Arial, sans-serif; font-size: 9.6pt; line-height: 1.38; color: #1b1b1b; }
h1 { font-size: 15pt; margin: 0 0 4px 0; } h2 { font-size: 12pt; margin: 12px 0 4px 0; border-bottom: 1px solid #ccc; }
p { margin: 4px 0; } ul, ol { margin: 3px 0 3px 18px; padding: 0; } li { margin: 1px 0; }
table { border-collapse: collapse; width: 100%; margin: 5px 0; font-size: 8.6pt; }
th, td { border: 1px solid #cfcfcf; padding: 2px 5px; vertical-align: top; text-align: left; }
th { background: #f1f3f5; } code { font-size: 8.4pt; background: #f4f4f4; padding: 0 2px; }
.quebra { page-break-before: always; } em { color: #444; }
"""


def html(md_texto):
    # o python-markdown só reconhece uma lista se houver linha em branco antes dela (o GitHub não exige)
    linhas, saida = md_texto.split(chr(10)), []
    for l in linhas:
        eh_lista = re.match(r"^\s*(-|\d+\.)\s", l)
        anterior = saida[-1] if saida else ""
        if eh_lista and anterior.strip() and not re.match(r"^\s*(-|\d+\.)\s", anterior):
            saida.append("")
        saida.append(l)
    return markdown.markdown(chr(10).join(saida), extensions=["tables"])


def main():
    rel = (RAIZ / "docs" / "relatorio.md").read_text(encoding="utf-8")
    memo = (RAIZ / "docs" / "memo_professor.md").read_text(encoding="utf-8")
    rel = rel.replace("Em [`memo_professor.md`](memo_professor.md), uma página.", "Na última página deste documento.")
    corpo = html(rel) + '<div class="quebra"></div>' + html(memo)
    pagina = f"<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><title>Relatório — Case Classificação de tópicos</title><style>{CSS}</style></head><body>{corpo}</body></html>"
    tmp = RAIZ / "runs" / "relatorio_tmp.html"
    tmp.write_text(pagina, encoding="utf-8")
    chrome = (shutil.which("chrome") or r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    saida = RAIZ / "docs" / "relatorio.pdf"
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={saida}", tmp.resolve().as_uri()],
                   check=True, capture_output=True, timeout=120)
    tmp.unlink(missing_ok=True)
    print(f"{saida} gerado")


if __name__ == "__main__":
    sys.exit(main())
