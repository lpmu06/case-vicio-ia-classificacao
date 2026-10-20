"""Etapa 4e: árbitro independente (modelo forte, esforço alto) sobre os candidatos de todos os classificadores.

Para cada questão, junta os ramos e subtemas votados pelas rodadas (e o da origem), embaralha, mostra os metadados
completos desses ramos e pede ao árbitro que escolha de forma independente, sem saber qual é a maioria.
O árbitro pode escolher fora da lista (recebe o resumo da árvore inteira no system prompt).

Uso: python src/classificar/46_arbitragem.py --modelo opus --rotulo arbitro-opus [--effort high] [--ids ...]
Saída: runs/<rotulo>/<id>.json no mesmo esquema das classificações (+ campos do árbitro)
"""
import argparse
import importlib
import json
import re
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import caminhos  # noqa: F401,E402  (pastas de etapas no sys.path)
from llm import chamar_json
from comum import Arvore, RAIZ, carregar_rodada, carregar_questoes, carregar_origem

c30 = importlib.import_module("30_classificar")
c31 = importlib.import_module("31_classificar_hierarquico")

RODADAS = ["claude-opus", "claude-sonnet-h", "claude-sonnet-3n", "claude-haiku-h", "claude-haiku-3n",
           "claude-sonnet-plano", "claude-opus-h", "gpt-5.5"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provedor", default="claude_cli")
    ap.add_argument("--modelo", default="opus")
    ap.add_argument("--rotulo", default="arbitro-opus")
    ap.add_argument("--effort", default="high")
    ap.add_argument("--ids", default=None)
    ap.add_argument("--workers", type=int, default=3)
    a = ap.parse_args()

    A = Arvore()
    enr = json.loads((RAIZ / "data" / "temas_enriquecidos.json").read_text(encoding="utf-8"))
    resumo_arvore = c31.sistema_estagio1(A.t, enr).split("<arvore>")[1].split("</arvore>")[0]
    sistema = (RAIZ / "prompts" / "arbitro_sistema.md").read_text(encoding="utf-8").replace("{arvore}", resumo_arvore)
    rodadas = {r: carregar_rodada(r, A) for r in RODADAS}
    origem = carregar_origem()
    qs = carregar_questoes()
    if a.ids:
        qs = [q for q in qs if q["id"] in a.ids.split(",")]
    pasta = RAIZ / "runs" / a.rotulo
    pasta.mkdir(parents=True, exist_ok=True)
    pend = [q for q in qs if not (pasta / f"{q['id']}.json").exists()]
    print(f"árbitro {a.modelo} effort={a.effort}; sistema={len(sistema)} chars; {len(pend)} pendentes", flush=True)

    def candidatos(qid):
        ramos, subs = [], []
        for r, rod in rodadas.items():
            if qid in rod:
                v = rod[qid][0]
                if v["ramo"] and v["ramo"] not in ramos:
                    ramos.append(v["ramo"])
                if v["sub"] and v["sub"] not in subs:
                    subs.append(v["sub"])
        o = origem.get(qid, {}).get("tema_id")
        if o and A.ramo_de(o) and A.ramo_de(o) not in ramos:
            ramos.append(A.ramo_de(o))
        rnd = random.Random(qid)
        rnd.shuffle(ramos)
        return ramos, subs

    def tarefa(q):
        ramos, subs = candidatos(q["id"])
        blocos = "\n\n=====\n\n".join(c31.bloco_ramo(A.t, enr, r) for r in ramos)
        sub_txt = ", ".join(f"{s} ({A.titulo(s)})" for s in subs) or "nenhum"
        pedido = (f"Candidatos de tema de nível 1 sugeridos (ordem aleatória), com metadados completos:\n\n{blocos}\n\n"
                  f"Subtemas que algum classificador sugeriu: {sub_txt}\n\n" + c30.montar_pedido(q))
        dados, u = chamar_json(a.provedor, a.modelo, sistema, pedido, c30.ESQUEMA, a.effort, max_tokens=8000)
        dados.update({"id": q["id"], "modelo": a.modelo, "provedor": a.provedor, "effort": a.effort,
                      "candidatos_ramos": ramos, "candidatos_subtemas": subs, "uso": u})
        (pasta / f"{q['id']}.json").write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
        return q["id"], u

    uso = {"in": 0, "out": 0, "cache_w": 0, "cache_r": 0, "custo_usd": 0.0}
    erros, t0 = [], time.time()
    if pend:
        qid, u = tarefa(pend[0])
        for k in uso:
            uso[k] += u.get(k) or 0
        print(f"[1/{len(pend)}] {qid} ok uso={u}", flush=True)
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(tarefa, q): q for q in pend[1:]}
        for i, f in enumerate(as_completed(futs), 2):
            q = futs[f]
            try:
                _, u = f.result()
                for k in uso:
                    uso[k] += u.get(k) or 0
                if i % 10 == 0 or i == len(pend):
                    print(f"[{i}/{len(pend)}] ok", flush=True)
            except Exception as e:
                erros.append({"id": q["id"], "erro": re.sub(r"org-[A-Za-z0-9]+", "org-REDACTED", repr(e))[:400]})
                print(f"ERRO {q['id']}: {e!r}"[:300], flush=True)
    resumo_path = pasta / "_usage.json"
    antigo = json.loads(resumo_path.read_text(encoding="utf-8")) if resumo_path.exists() else {"uso": {k: 0 for k in uso}, "segundos": 0}
    for k in uso:
        antigo["uso"][k] = antigo["uso"].get(k, 0) + uso[k]
    antigo.update({"segundos": antigo["segundos"] + round(time.time() - t0), "erros": erros, "modelo": a.modelo, "effort": a.effort,
                   "metodo": "arbitro_independente"})
    resumo_path.write_text(json.dumps(antigo, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"fim: {antigo}")


if __name__ == "__main__":
    main()
