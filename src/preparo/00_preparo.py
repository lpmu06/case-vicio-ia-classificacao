"""Etapa 0: limpa o HTML das questões e gera data/questoes_limpas.jsonl.

Texto classificável = enunciado + alternativas (o `comando` é vazio ou gerado e é ignorado).
A limpeza remove comentários HTML, blocos <xml>/<style> (lixo do Word, ex.: Q0099),
tags, entidades e espaços repetidos.
"""
import html, json, re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ENTRADA = RAIZ / "anexos" / "questoes.jsonl"
SAIDA = RAIZ / "data" / "questoes_limpas.jsonl"

def limpar(s: str) -> str:
    s = re.sub(r"\\n|\n", " ", s)                                   # "\n" literal vindo do banco
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)               # comentários (inclui condicionais do Word)
    s = re.sub(r"<(xml|style|script)\b.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<\s*br\s*/?>|</p>|</div>|</li>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s).replace("\xa0", " ")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\s*\n\s*", "\n", s)
    return s.strip()

def main():
    SAIDA.parent.mkdir(exist_ok=True)
    n = 0
    with ENTRADA.open(encoding="utf-8") as f, SAIDA.open("w", encoding="utf-8") as g:
        for linha in f:
            q = json.loads(linha)
            enun = limpar(q["enunciado_html"])
            alts = {k: limpar(v) for k, v in q["alternativas"].items()}
            tipo = "certo_errado" if set(alts) == {"C", "E"} else "multipla_escolha"
            texto = enun + "\n\n" + "\n".join(f"({k}) {v}" for k, v in alts.items())
            g.write(json.dumps({
                "id": q["id"], "texto": texto, "enunciado": enun, "alternativas": alts,
                "tipo": tipo, "disciplina_origem": q["disciplina_origem"],
                "assunto_origem": q["assunto_origem"], "n_chars": len(texto),
            }, ensure_ascii=False) + "\n")
            n += 1
    print(f"{n} questões -> {SAIDA}")

if __name__ == "__main__":
    main()
