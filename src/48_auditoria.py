"""Etapa 5b: caderno de auditoria de uma amostra aleatória das questões publicadas.

A auditoria é feita por IA, não por um especialista: serve para achar erros sistemáticos e dar um terceiro estimador
de precisão (E3 em src/60_previsao.py), declarado como tal no relatório. Dois modos:

- padrão (v1, manhã de 19/10): caderno com os votos de ramo e a justificativa do árbitro. Serviu para escolher os
  limiares; o auditor estava ancorado. Saída: docs/auditoria_caderno.md e data/auditoria_ia.csv.
- --cego (v2, noite de 19/10): amostra nova (--excluir tira as questões da v1), caderno sem votos, sem confiança e
  sem justificativa do pipeline; para cada questão, só o texto, o tema publicado com descrição e "não confundir",
  os subtemas (ou irmãos) e os três temas de nível 1 de título mais parecido, sem dizer de onde vêm. O auditor é um
  agente Claude Opus separado, com contexto limpo (prompts/auditoria_cega.md). Saída: docs/auditoria_cega_caderno.md e
  data/auditoria_ia_v2.csv.

Uso: python src/48_auditoria.py --n 50 --semente 7
     python src/48_auditoria.py --cego --n 50 --semente 2026 --excluir data/auditoria_ia.csv
Colunas do CSV: id, tema_publicado, veredito (ok | duvidoso | erro), tipo_duvida (ramo | subtema), tema_sugerido, comentario
"""
import argparse
import csv
import difflib
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import Arvore, RAIZ, carregar_questoes, norm, usavel


def parecidos(A, tid, k=3):
    """Temas de nível 1 usáveis, de outros ramos, com título mais parecido ao do tema publicado."""
    alvo = norm(A.titulo(tid))
    ramo = A.ramo_de(tid)
    cands = [t for t in A.t.values() if usavel(t) and t["nivel"] == 1 and t["tema_id"] != ramo]
    cands.sort(key=lambda t: -difflib.SequenceMatcher(None, alvo, norm(t["titulo"])).ratio())
    return cands[:k]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=50)
    ap.add_argument("--semente", type=int, default=7)
    ap.add_argument("--cego", action="store_true", help="caderno sem votos nem justificativa do pipeline (auditoria v2)")
    ap.add_argument("--excluir", default=None, help="CSV de auditoria anterior cujas questões não entram na amostra")
    ap.add_argument("--saida", default=None, help="CSV de vereditos (padrão: data/auditoria_ia.csv ou _v2 no modo cego)")
    ap.add_argument("--caderno", default=None, help="caderno em Markdown (padrão: docs/auditoria_caderno.md ou _cega_ no modo cego)")
    a = ap.parse_args()
    saida = Path(a.saida) if a.saida else RAIZ / "data" / ("auditoria_ia_v2.csv" if a.cego else "auditoria_ia.csv")
    caderno = Path(a.caderno) if a.caderno else RAIZ / "docs" / ("auditoria_cega_caderno.md" if a.cego else "auditoria_caderno.md")

    A = Arvore()
    enr = json.loads((RAIZ / "data" / "temas_enriquecidos.json").read_text(encoding="utf-8"))
    qs = {q["id"]: q for q in carregar_questoes()}
    dec = [json.loads(l) for l in (RAIZ / "data" / "decisoes.jsonl").open(encoding="utf-8")]
    pub = [d for d in dec if d["decisao"] == "publicar"]
    excluidos = set()
    if a.excluir:
        excluidos = {r["id"] for r in csv.DictReader(open(a.excluir, encoding="utf-8"))}
    elegiveis = [d for d in pub if d["id"] not in excluidos]
    random.seed(a.semente)
    amostra = sorted(random.sample(elegiveis, min(a.n, len(elegiveis))), key=lambda d: d["id"])

    if a.cego:
        md = ["# Caderno de auditoria cega (amostra aleatória das publicadas, sem os votos do pipeline)\n",
              "Para cada questão: o texto, o tema em que foi publicada, a descrição desse tema e os temas vizinhos. "
              "A árvore completa está em `data/arvore.txt`. Instruções para o auditor em `prompts/auditoria_cega.md`.\n"]
    else:
        md = ["# Caderno de auditoria (amostra aleatória das publicadas)\n"]
    for d in amostra:
        t = A.t[d["tema"]]
        e = enr.get(t["tema_id"], {})
        if t["nivel"] == 2:
            vizinhos = ("irmãos (subtemas do mesmo tema)", [A.titulo(x) for x in A.t[t["parent_id"]]["filhos"]
                                                           if x != t["tema_id"] and usavel(A.t[x])])
        else:
            vizinhos = ("subtemas deste tema", [A.titulo(x) for x in t["filhos"] if usavel(A.t[x])])
        md.append(f"\n---\n\n## {d['id']} → publicado em {t['tema_id']} · {t['caminho']} (nível {t['nivel']})\n")
        texto = qs[d["id"]]["texto"] if a.cego else qs[d["id"]]["texto"][:2500]
        md.append("```\n" + texto + "\n```\n")
        md.append(f"- descrição do tema: {e.get('descricao', '')}")
        md.append(f"- não confundir: {e.get('nao_confundir', '')}")
        md.append(f"- {vizinhos[0]}: {'; '.join(vizinhos[1]) or 'nenhum'}")
        if a.cego:
            md.append("- outros temas de nível 1 com título parecido: " + "; ".join(
                f"{p['tema_id']} {p['caminho']}" for p in parecidos(A, t["tema_id"])))
        else:
            md.append(f"- votos de ramo: {', '.join(f'{r}={A.titulo(v)[:25]}' for r, v in d['votos_ramo'].items())}")
            md.append(f"- árbitro: {d['arbitro']['just'][:300] if d['arbitro'] else ''}")
    caderno.write_text("\n".join(md) + "\n", encoding="utf-8")

    antigos = {r["id"]: r for r in csv.DictReader(saida.open(encoding="utf-8"))} if saida.exists() else {}
    with saida.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "tema_publicado", "veredito", "tipo_duvida", "tema_sugerido", "comentario"])
        for d in amostra:
            o = antigos.get(d["id"], {})
            w.writerow([d["id"], d["tema"], o.get("veredito", ""), o.get("tipo_duvida", ""), o.get("tema_sugerido", ""),
                        o.get("comentario", "")])
    print(f"{len(amostra)} questões (de {len(elegiveis)} elegíveis, {len(excluidos)} excluídas) -> {caderno.name} ; "
          f"vereditos em {saida}")


if __name__ == "__main__":
    main()
