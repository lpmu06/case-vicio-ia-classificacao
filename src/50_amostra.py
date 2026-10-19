"""Etapa 5a: monta a amostra para rotulagem humana (gabarito interno).

Seleciona questões estratificadas por decisão do ensemble (publicar n2 / publicar n1 / revisar / fora)
e gera docs/amostra_rotulagem.md com o texto da questão e os candidatos dos modelos, para o
rotulador marcar o tema correto. As respostas vão em data/rotulos_humanos.csv (id,tema_id,comentario).

Uso: python src/50_amostra.py --n 60 [--semente 42]
"""
import argparse, csv, importlib, json, random, sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
arv = importlib.import_module("10_arvore")
RAIZ = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=60)
    ap.add_argument("--semente", type=int, default=42)
    ap.add_argument("--ids", default=None, help="forçar ids específicos (vírgula)")
    a = ap.parse_args()
    random.seed(a.semente)

    temas = arv.carregar_temas()
    qs = {json.loads(l)["id"]: json.loads(l) for l in (RAIZ / "data" / "questoes_limpas.jsonl").open(encoding="utf-8")}
    ens = {json.loads(l)["id"]: json.loads(l) for l in (RAIZ / "data" / "ensemble.jsonl").open(encoding="utf-8")}

    if a.ids:
        escolhidos = a.ids.split(",")
    else:
        grupos = defaultdict(list)
        for e in ens.values():
            grupos[(e["decisao"], e["nivel"])].append(e["id"])
        # cota: metade para publicadas (onde a precisão importa), metade para revisar/fora (onde a cobertura importa)
        pub = [i for (d, _), ids in grupos.items() if d == "publicar" for i in ids]
        resto = [i for (d, _), ids in grupos.items() if d != "publicar" for i in ids]
        random.shuffle(pub); random.shuffle(resto)
        n_pub = min(len(pub), a.n // 2)
        escolhidos = sorted(pub[:n_pub] + resto[:a.n - n_pub])

    def nome(tid):
        return f"{tid} · {temas[tid]['caminho']}" if tid and tid in temas else "—"

    linhas = ["# Amostra para rotulagem humana\n",
              "Para cada questão, escreva em `data/rotulos_humanos.csv` o `tema_id` que um professor atribuiria "
              "(nível 2 se houver subtema claro; nível 1 se a questão for genérica do tema; `FORA` se nenhum tema serve). "
              "A decisão dos modelos está escondida de propósito logo abaixo dos candidatos; tente decidir antes de olhar.\n"]
    for qid in escolhidos:
        q, e = qs[qid], ens[qid]
        cands = []
        for r, v in e["votos"].items():
            for t in (v["sub"], v["ramo"], v.get("segunda")):
                if t and t in temas and t not in cands:
                    cands.append(t)
        linhas.append(f"\n---\n\n## {qid}  (origem: {q['disciplina_origem'] or '-'} / {q['assunto_origem'] or '-'})\n")
        linhas.append("```\n" + q["texto"] + "\n```\n")
        linhas.append("Candidatos (em ordem aleatória):\n")
        random.shuffle(cands)
        linhas += [f"- {nome(t)}" for t in cands]
        linhas.append(f"\n<details><summary>decisão do ensemble</summary>{e['decisao']} → {nome(e['tema'])} "
                      f"(conf {e['confianca']}) {e['motivo']}</details>\n")
    (RAIZ / "docs" / "amostra_rotulagem.md").write_text("\n".join(linhas), encoding="utf-8")

    rot = RAIZ / "data" / "rotulos_humanos.csv"
    if not rot.exists():
        with rot.open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["id", "tema_id", "comentario"])
            for qid in escolhidos:
                w.writerow([qid, "", ""])
    print(f"{len(escolhidos)} questões -> docs/amostra_rotulagem.md ; respostas em {rot}")


if __name__ == "__main__":
    main()
