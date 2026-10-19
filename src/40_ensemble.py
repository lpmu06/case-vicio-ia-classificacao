"""Etapa 4: combina as classificações de vários modelos e aplica as regras publicar / revisar / fora.

Uso: python src/40_ensemble.py --rotulos gpt-5.5,claude-opus-5 [--t_sub 0.85 --t_ramo 0.85]
Saída: data/ensemble.jsonl (uma linha por questão, com todos os votos e a decisão) e publicacao.csv

Regras (ver docs/00_entendimento_e_plano.md §6):
- votos são normalizados: um id de nível 2 no campo de ramo vira (pai, ele); buckets/inativos são
  redirecionados para o equivalente da Legislação Especial pelo título, ou para o pai;
- fora: todos os modelos dizem fora;
- publicar no nível 2: todos concordam no mesmo subtema e a menor confiança de subtema >= t_sub;
- publicar no nível 1 (backoff): todos concordam no ramo e a menor confiança de ramo >= t_ramo;
- senão: revisar, com a sugestão do modelo de referência e o motivo da divergência.
"""
import argparse, csv, importlib, json, re, sys, unicodedata
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
arv = importlib.import_module("10_arvore")
RAIZ = Path(__file__).resolve().parents[1]


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]+", " ", s)).strip()


def usavel(t):
    return t["nivel"] > 0 and t["status"] == "active" and not t["bucket"]


def redirecionar(tid, temas, por_titulo):
    """Devolve um id usável: redireciona buckets/inativos para o equivalente da Leg. Especial ou para o pai."""
    if tid is None or tid not in temas:
        return None
    t = temas[tid]
    if usavel(t):
        return tid
    for c in por_titulo.get(norm(t["titulo"]), []):
        if usavel(c):
            return c["tema_id"]
    pai = t["parent_id"]
    return pai if pai and temas[pai]["nivel"] > 0 and usavel(temas[pai]) else None


def normalizar_voto(v, temas, por_titulo):
    """Transforma a saída bruta de um modelo em (ramo_n1, subtema_n2 ou None)."""
    if v.get("fora"):
        return {"fora": True, "ramo": None, "sub": None, "c_ramo": v.get("confianca_ramo", 0),
                "c_sub": 0, "multi": v.get("multi_tema", False), "segunda": v.get("segunda_opcao_id"),
                "extras": v.get("extras_ids", []), "just": v.get("justificativa", "")}
    # nó mais específico e usável entre os dois ids informados (o modelo às vezes troca os campos ou põe a disciplina)
    ids = [redirecionar(v.get("tema_n1_id") or v.get("ramo_n1_id"), temas, por_titulo),
           redirecionar(v.get("subtema_n2_id"), temas, por_titulo)]
    ids = [i for i in ids if i and temas[i]["nivel"] > 0]
    ramo = sub = None
    if ids:
        no = max(ids, key=lambda i: temas[i]["nivel"])
        if temas[no]["nivel"] == 2:
            sub, ramo = no, temas[no]["parent_id"]
        else:
            ramo = no
    return {"fora": False, "ramo": ramo, "sub": sub, "c_ramo": float(v.get("confianca_ramo", 0)),
            "c_sub": float(v.get("confianca_subtema", 0)) if sub else 0.0, "multi": bool(v.get("multi_tema", False)),
            "segunda": v.get("segunda_opcao_id"), "extras": v.get("extras_ids", []), "just": v.get("justificativa", "")}


def decidir(votos, temas, t_sub, t_ramo, ref):
    """votos: dict rotulo -> voto normalizado. ref: rótulo do modelo de referência para a sugestão."""
    vs = list(votos.values())
    if all(v["fora"] for v in vs):
        return {"decisao": "fora", "tema": None, "nivel": None, "confianca": 0.0,
                "motivo": "nenhum tema da árvore cobre a questão: " + vs[0]["just"][:160]}
    nao_fora = [v for v in vs if not v["fora"]]
    ramos = Counter(v["ramo"] for v in nao_fora if v["ramo"])
    subs = Counter(v["sub"] for v in nao_fora if v["sub"])
    n = len(vs)
    ramo_unanime = len(nao_fora) == n and len(ramos) == 1 and all(v["ramo"] for v in nao_fora)
    sub_unanime = ramo_unanime and len(subs) == 1 and all(v["sub"] for v in nao_fora)
    algum_multi = any(v["multi"] for v in vs)
    if sub_unanime:
        c = min(v["c_sub"] for v in vs)
        if c >= t_sub and not algum_multi:
            return {"decisao": "publicar", "tema": vs[0]["sub"], "nivel": 2, "confianca": round(c, 2),
                    "motivo": ""}
    if ramo_unanime:
        c = min(v["c_ramo"] for v in vs)
        if c >= t_ramo:
            return {"decisao": "publicar", "tema": vs[0]["ramo"], "nivel": 1, "confianca": round(c, 2),
                    "motivo": "" if not algum_multi else ""}
    # revisar: sugestão do modelo de referência (ou do primeiro não-fora)
    sug = votos.get(ref) if votos.get(ref) and not votos[ref]["fora"] else nao_fora[0]
    tema = sug["sub"] or sug["ramo"]
    if not ramo_unanime:
        desc = "; ".join(f"{r}: {temas[v['ramo']]['titulo'] if v['ramo'] else 'fora'}" for r, v in votos.items())
        motivo = f"modelos divergem no ramo ({desc})"
        conf = round(min(v["c_ramo"] for v in nao_fora) * 0.5, 2)
    elif algum_multi:
        motivo = "questão multi-tema (alternativas sobre institutos diferentes); ramo " + temas[sug["ramo"]]["titulo"]
        conf = round(min(v["c_ramo"] for v in vs) * 0.8, 2)
    else:
        desc = "; ".join(f"{r}: {temas[v['sub']]['titulo'] if v['sub'] else 'nível 1'}" for r, v in votos.items())
        motivo = f"ramo certo, subtema incerto ({desc}); confiança abaixo do limiar"
        conf = round(min(v["c_ramo"] for v in vs) * 0.9, 2)
    return {"decisao": "revisar", "tema": tema, "nivel": temas[tema]["nivel"] if tema else None,
            "confianca": conf, "motivo": motivo[:200]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rotulos", required=True, help="pastas em runs/, separadas por vírgula; a primeira é a referência")
    ap.add_argument("--t_sub", type=float, default=0.85)
    ap.add_argument("--t_ramo", type=float, default=0.85)
    ap.add_argument("--saida_csv", default=str(RAIZ / "publicacao.csv"))
    a = ap.parse_args()
    rotulos = a.rotulos.split(",")

    temas = arv.carregar_temas()
    por_titulo = {}
    for t in temas.values():
        por_titulo.setdefault(norm(t["titulo"]), []).append(t)
    qs = [json.loads(l) for l in (RAIZ / "data" / "questoes_limpas.jsonl").open(encoding="utf-8")]

    linhas, stats = [], Counter()
    with (RAIZ / "data" / "ensemble.jsonl").open("w", encoding="utf-8") as g:
        for q in qs:
            votos, brutos = {}, {}
            for r in rotulos:
                p = RAIZ / "runs" / r / f"{q['id']}.json"
                if p.exists():
                    brutos[r] = json.loads(p.read_text(encoding="utf-8"))
                    votos[r] = normalizar_voto(brutos[r], temas, por_titulo)
            if not votos:
                d = {"decisao": "revisar", "tema": None, "nivel": None, "confianca": 0.0, "motivo": "sem classificação"}
            else:
                d = decidir(votos, temas, a.t_sub, a.t_ramo, rotulos[0])
            extras = []
            for v in votos.values():
                for e in v["extras"]:
                    e2 = redirecionar(e, temas, por_titulo)
                    if e2 and e2 != d["tema"] and e2 not in extras and temas[e2]["parent_id"] != d["tema"] and e2 != temas.get(d["tema"] or "", {}).get("parent_id"):
                        extras.append(e2)
            reg = {"id": q["id"], **d, "extras": extras[:3], "votos": votos,
                   "n_modelos": len(votos), "unanime_ramo": len({v["ramo"] for v in votos.values()}) == 1}
            g.write(json.dumps(reg, ensure_ascii=False) + "\n")
            linhas.append(reg)
            stats[(d["decisao"], d["nivel"])] += 1

    with open(a.saida_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "decisao", "tema_central_id", "extras_ids", "confianca", "motivo"])
        for r in linhas:
            w.writerow([r["id"], r["decisao"], r["tema"] or "", ";".join(r["extras"]), f"{r['confianca']:.2f}", r["motivo"]])
    tot = len(linhas)
    pub = sum(v for (d, _), v in stats.items() if d == "publicar")
    print(f"modelos: {rotulos} | t_sub={a.t_sub} t_ramo={a.t_ramo}")
    for k, v in sorted(stats.items(), key=lambda x: -x[1]):
        print(f"  {k[0]:9s} nível {k[1]}: {v}")
    print(f"cobertura (publicadas): {pub}/{tot} = {pub/tot:.1%}  -> {a.saida_csv}")


if __name__ == "__main__":
    main()
