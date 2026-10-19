"""Etapa 5b: caderno de auditoria de uma amostra aleatória das questões publicadas.

A auditoria é feita por IA (o assistente que construiu o pipeline, lendo questão a questão com olhar cético),
não por um especialista: serve para achar erros sistemáticos e dar um terceiro estimador de precisão (E3 em
src/60_previsao.py), declarado como tal no relatório.

Uso: python src/48_auditoria.py --n 50 --semente 7
Saída: docs/auditoria_caderno.md e data/auditoria_ia.csv (id, tema_publicado, veredito, tema_sugerido, comentario)
"""
import argparse
import csv
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import Arvore, RAIZ, carregar_questoes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=50)
    ap.add_argument("--semente", type=int, default=7)
    a = ap.parse_args()
    A = Arvore()
    enr = json.loads((RAIZ / "data" / "temas_enriquecidos.json").read_text(encoding="utf-8"))
    qs = {q["id"]: q for q in carregar_questoes()}
    dec = [json.loads(l) for l in (RAIZ / "data" / "decisoes.jsonl").open(encoding="utf-8")]
    pub = [d for d in dec if d["decisao"] == "publicar"]
    random.seed(a.semente)
    amostra = sorted(random.sample(pub, min(a.n, len(pub))), key=lambda d: d["id"])
    md = ["# Caderno de auditoria (amostra aleatória das publicadas)\n"]
    for d in amostra:
        t = A.t[d["tema"]]
        irmaos = [A.titulo(x) for x in A.t[t["parent_id"]]["filhos"] if x != t["tema_id"]] if t["nivel"] == 2 else [A.titulo(x) for x in t["filhos"]]
        md.append(f"\n---\n\n## {d['id']} → publicado em {t['tema_id']} · {t['caminho']} (nível {t['nivel']})\n")
        md.append("```\n" + qs[d["id"]]["texto"][:2500] + "\n```\n")
        md.append(f"- descrição do tema: {enr.get(t['tema_id'], {}).get('descricao', '')}")
        md.append(f"- não confundir: {enr.get(t['tema_id'], {}).get('nao_confundir', '')}")
        md.append(f"- {'irmãos' if t['nivel'] == 2 else 'subtemas'}: {'; '.join(irmaos)}")
        md.append(f"- votos de ramo: {', '.join(f'{r}={A.titulo(v)[:25]}' for r, v in d['votos_ramo'].items())}")
        md.append(f"- árbitro: {d['arbitro']['just'][:300] if d['arbitro'] else ''}")
    (RAIZ / "docs" / "auditoria_caderno.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    p = RAIZ / "data" / "auditoria_ia.csv"
    antigos = {r["id"]: r for r in csv.DictReader(p.open(encoding="utf-8"))} if p.exists() else {}
    with p.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "tema_publicado", "veredito", "tema_sugerido", "comentario"])
        for d in amostra:
            o = antigos.get(d["id"], {})
            w.writerow([d["id"], d["tema"], o.get("veredito", ""), o.get("tema_sugerido", ""), o.get("comentario", "")])
    print(f"{len(amostra)} questões -> docs/auditoria_caderno.md ; vereditos em {p}")


if __name__ == "__main__":
    main()
