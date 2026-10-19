"""Etapa 4d: estimativa cega de confiabilidade (sem gabarito), no nível do ramo (tema de nível 1).

Modelo de Dawid-Skene "one-coin": cada anotador j acerta o ramo verdadeiro com probabilidade p_j e, quando erra,
escolhe outro ramo. Para não supor erros uniformes entre 92 opções (o que tornaria "dois anotadores errando
igual" quase impossível e o modelo otimista demais), o erro é distribuído com peso maior nos ramos que algum
anotador também escolheu para aquela questão (os "confundíveis"), controlado por `--concentracao`.
EM alterna entre a posterior do ramo verdadeiro por questão e as taxas p_j.

Anotadores: as rodadas dos classificadores (cobertura total ou parcial) e a classificação de origem, que é fraca,
mas erra de forma independente dos modelos. Faltas são ignoradas naturalmente.

Uso: python src/45_confiabilidade.py [--rodadas claude-opus,claude-sonnet-h,...] [--concentracao 0.5]
Saída: data/confiabilidade.jsonl (posterior por questão) e runs/confiabilidade.json (p_j e resumo).
"""
import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import Arvore, RAIZ, carregar_rodada, carregar_questoes, carregar_origem

PADRAO = "claude-opus,claude-sonnet-h,claude-sonnet-3n,claude-haiku-h,claude-haiku-3n,claude-sonnet-plano,claude-opus-h,gpt-5.5,jev-h"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rodadas", default=PADRAO)
    ap.add_argument("--sem_origem", action="store_true")
    ap.add_argument("--concentracao", type=float, default=0.5,
                    help="fração da massa de erro que vai para os ramos 'confundíveis' da questão (0 = erros uniformes)")
    ap.add_argument("--iter", type=int, default=50)
    a = ap.parse_args()

    A = Arvore()
    qs = [q["id"] for q in carregar_questoes()]
    ramos = sorted({t["tema_id"] for t in A.t.values() if t["nivel"] == 1 and t["status"] == "active" and not t["bucket"]})
    rotulos = ramos + ["FORA"]
    K = len(rotulos)

    anot = {}  # anotador -> {qid: rotulo}
    for r in [x for x in a.rodadas.split(",") if x]:
        rod = carregar_rodada(r, A)
        if rod:
            anot[r] = {q: ("FORA" if v["fora"] else v["ramo"]) for q, (v, _) in rod.items() if v["fora"] or v["ramo"]}
    if not a.sem_origem:
        org = carregar_origem()
        anot["origem"] = {q: A.ramo_de(o["tema_id"]) for q, o in org.items() if o.get("tema_id") and A.ramo_de(o["tema_id"])}
    nomes = list(anot)

    # inicialização: voto majoritário ponderado igualmente
    p = {j: 0.8 for j in nomes}
    if "origem" in p:
        p["origem"] = 0.4
    post = {}
    for _ in range(a.iter):
        # E: posterior por questão
        for q in qs:
            votos = {j: anot[j][q] for j in nomes if q in anot[j]}
            if not votos:
                post[q] = {}
                continue
            confund = set(votos.values())
            nconf = len(confund)
            logs = {}
            for k in confund | ({"FORA"} if "FORA" not in confund else set()):
                s = 0.0
                for j, l in votos.items():
                    if l == k:
                        s += math.log(max(p[j], 1e-6))
                    else:
                        # massa de erro: parte concentrada nos confundíveis (exceto k), parte uniforme no resto
                        m_conf = max(nconf - (1 if k in confund else 0), 1)
                        q_err = a.concentracao / m_conf if l in confund else 0.0
                        q_err += (1 - a.concentracao) / (K - 1)
                        s += math.log(max((1 - p[j]) * q_err, 1e-12))
                logs[k] = s
            # rótulos não votados têm verossimilhança desprezível relativa; ignoramos (aproximação)
            mx = max(logs.values())
            z = sum(math.exp(v - mx) for v in logs.values())
            post[q] = {k: math.exp(v - mx) / z for k, v in logs.items()}
        # M: p_j = acerto esperado
        for j in nomes:
            num = den = 0.0
            for q, l in anot[j].items():
                if post.get(q):
                    num += post[q].get(l, 0.0)
                    den += 1
            p[j] = min(max(num / den if den else 0.5, 0.05), 0.995)

    saida = []
    for q in qs:
        if not post.get(q):
            saida.append({"id": q, "ramo_map": None, "p_ramo_map": 0.0, "n_votos": 0, "votos": {}})
            continue
        k = max(post[q], key=post[q].get)
        votos = {j: anot[j][q] for j in nomes if q in anot[j]}
        cont = Counter(v for j, v in votos.items() if j != "origem")
        saida.append({"id": q, "ramo_map": k, "p_ramo_map": round(post[q][k], 4), "n_votos": len(votos),
                      "n_modelos_concordam": cont.get(k, 0), "n_modelos": sum(cont.values()), "votos": votos})
    with (RAIZ / "data" / "confiabilidade.jsonl").open("w", encoding="utf-8") as g:
        for s in saida:
            g.write(json.dumps(s, ensure_ascii=False) + "\n")

    faixas = Counter()
    for s in saida:
        pr = s["p_ramo_map"]
        faixas["≥0.99" if pr >= 0.99 else "0.95–0.99" if pr >= 0.95 else "0.80–0.95" if pr >= 0.8 else "<0.80"] += 1
    resumo = {"concentracao": a.concentracao, "anotadores": {j: {"p_acerto_ramo": round(p[j], 4), "n": len(anot[j])} for j in nomes},
              "faixas_posterior": dict(faixas),
              "acerto_esperado_ramo_map_todas": round(sum(s["p_ramo_map"] for s in saida) / len(saida), 4)}
    (RAIZ / "runs" / "confiabilidade.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(resumo, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
