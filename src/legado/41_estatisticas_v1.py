"""Etapa 4b: estatísticas do ensemble para o relatório (concordância, decisões por disciplina, custo e tempo).

Uso: python src/41_estatisticas.py --rotulos gpt-5.5,claude-opus
"""
import argparse, importlib, json, sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
arv = importlib.import_module("10_arvore")
RAIZ = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rotulos", required=True)
    a = ap.parse_args()
    rotulos = a.rotulos.split(",")
    temas = arv.carregar_temas()
    qs = {json.loads(l)["id"]: json.loads(l) for l in (RAIZ / "data" / "questoes_limpas.jsonl").open(encoding="utf-8")}
    ens = [json.loads(l) for l in (RAIZ / "data" / "ensemble.jsonl").open(encoding="utf-8")]
    base = {json.loads(l)["id"]: json.loads(l) for l in (RAIZ / "data" / "baseline_origem.jsonl").open(encoding="utf-8")}

    n = len(ens)
    dec = Counter((e["decisao"], e["nivel"]) for e in ens)
    print("== decisões ==")
    for k, v in sorted(dec.items(), key=lambda x: -x[1]):
        print(f"  {k[0]} nível {k[1]}: {v} ({v/n:.1%})")

    print("\n== concordância entre modelos ==")
    ramo_ok = sum(1 for e in ens if e["n_modelos"] >= 2 and e["unanime_ramo"])
    sub_ok = sum(1 for e in ens if e["n_modelos"] >= 2 and len({v["sub"] for v in e["votos"].values()}) == 1 and all(v["sub"] for v in e["votos"].values()))
    fora_any = sum(1 for e in ens if any(v["fora"] for v in e["votos"].values()))
    multi_any = sum(1 for e in ens if any(v["multi"] for v in e["votos"].values()))
    print(f"  mesmo ramo (nível 1): {ramo_ok}/{n} = {ramo_ok/n:.1%}")
    print(f"  mesmo subtema (ambos escolheram e coincidem): {sub_ok}/{n} = {sub_ok/n:.1%}")
    print(f"  algum modelo disse fora: {fora_any}; algum marcou multi-tema: {multi_any}")

    print("\n== por disciplina de origem ==")
    por = defaultdict(Counter)
    for e in ens:
        d = qs[e["id"]]["disciplina_origem"] or "(vazia)"
        por[d][e["decisao"]] += 1
        por[d]["unanime"] += e["unanime_ramo"]
    for d, c in sorted(por.items(), key=lambda x: -sum(v for k, v in x[1].items() if k != "unanime")):
        tot = sum(v for k, v in c.items() if k != "unanime")
        print(f"  {d:40s} n={tot:3d} publicar={c['publicar']:3d} revisar={c['revisar']:3d} fora={c['fora']:2d} ramo unânime={c['unanime']/tot:.0%}")

    print("\n== baseline 'copiar a origem' vs decisão do ensemble ==")
    comp = Counter()
    for e in ens:
        b = base[e["id"]]["tema_id"]
        if not b or not e["tema"]:
            comp["sem comparação"] += 1
        elif b == e["tema"] or temas[b]["parent_id"] == e["tema"] or temas[e["tema"]]["parent_id"] == b:
            comp["origem no mesmo ramo"] += 1
        else:
            comp["origem em outro ramo"] += 1
    for k, v in comp.items():
        print(f"  {k}: {v}")

    print("\n== disciplina escolhida (raiz) por questão ==")
    raiz = Counter()
    for e in ens:
        if e["tema"]:
            t = temas[e["tema"]]
            raiz[t["disciplina"]] += 1
    print("  ", dict(raiz))

    print("\n== uso e custo por modelo ==")
    for r in rotulos:
        p = RAIZ / "runs" / r / "_usage.json"
        if p.exists():
            u = json.loads(p.read_text(encoding="utf-8"))
            print(f"  {r}: {u['uso']} segundos={u['segundos']} erros={len(u.get('erros', []))}")
    p = RAIZ / "runs" / "11_enriquecer_usage.json"
    if p.exists():
        u = json.loads(p.read_text(encoding="utf-8"))
        print(f"  enriquecimento ({u['modelo']}): {u['uso_tokens']} segundos={u['segundos']} chamadas={u['chamadas']}")


if __name__ == "__main__":
    main()
