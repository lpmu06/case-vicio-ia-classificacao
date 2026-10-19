"""Etapa 4f: experimento com embeddings (modelos jurídicos brasileiros/portugueses e multilíngues), sem LLM.

Pergunta 1 (lição do MoVAI): similaridade entre questão e tema decide bem o tema? Ou cria "lixeiras"?
Pergunta 2 (produção): os embeddings servem como pré-filtro (o ramo certo está entre os k mais parecidos)?
Pergunta 3 (produção): um classificador leve treinado sobre embeddings, com rótulos do consenso dos LLMs
            ("destilação"), reproduz o consenso?

Duas versões do texto dos temas: só o caminho na árvore (como no MoVAI) e o caminho + metadados enriquecidos.
Referência: questões em que o Opus plano, o Sonnet 2 estágios e o árbitro concordam no ramo (não é gabarito;
é o consenso dos LLMs).

Uso: python src/43_embeddings.py calcular [--modelos ...]   # grava data/embeddings/*.npy
     python src/43_embeddings.py avaliar                    # docs/embeddings.md e runs/embeddings.json
"""
import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import Arvore, RAIZ, carregar_rodada, carregar_questoes

PASTA = RAIZ / "data" / "embeddings"
# (apelido, origem, id, grupo, observação)
MODELOS = [
    ("legal-bertimbau-base", "st", "rufimelo/Legal-BERTimbau-base", "jurídico PT", "BERT cru (MLM), sem treino de similaridade; o elo fraco do MoVAI"),
    ("legal-bertimbau-sts-large", "st", "rufimelo/Legal-BERTimbau-sts-large-ma-v3", "jurídico PT", "Legal-BERTimbau ajustado para similaridade (STS)"),
    ("jurisbert-sts", "st", "alfaneo/jurisbert-base-portuguese-sts", "jurídico BR", "JurisBERT: pré-treino em decisões do STJ, ajustado para STS"),
    ("stjiris-legal-sts-large", "st", "stjiris/bert-large-portuguese-cased-legal-mlm-sts-v1.0", "jurídico PT", "BERTimbau large com MLM em acórdãos do STJ português + STS"),
    ("bertimbau-base", "st", "neuralmind/bert-base-portuguese-cased", "português geral", "BERTimbau cru (MLM)"),
    ("serafim-335m-ir", "st", "PORTULAN/serafim-335m-portuguese-pt-sentence-encoder-ir", "português geral", "codificador de sentenças para busca"),
    ("mpnet-multilingual", "st", "sentence-transformers/paraphrase-multilingual-mpnet-base-v2", "multilíngue", "paráfrase multilíngue (2019)"),
    ("e5-base", "st", "intfloat/multilingual-e5-base", "multilíngue", "E5 base, com prefixos query/passage"),
    ("qwen3-emb-0.6b", "st", "Qwen/Qwen3-Embedding-0.6B", "multilíngue", "Qwen3 Embedding 0.6B (2025)"),
    ("bge-m3", "ollama", "bge-m3", "multilíngue", "BGE-M3 via Ollama (GPU local)"),
    ("mxbai-large", "ollama", "mxbai-embed-large", "inglês", "mxbai-embed-large via Ollama, treinado sobretudo em inglês"),
]


def textos(A, enr):
    qs = carregar_questoes()
    q_txt = [q["texto"][:3000] for q in qs]
    temas = [t for t in A.t.values() if t["nivel"] > 0 and t["status"] == "active" and not t["bucket"]]
    t_tit = [t["caminho"] for t in temas]
    t_enr = []
    for t in temas:
        e = enr.get(t["tema_id"], {})
        t_enr.append(f"{t['caminho']}. {e.get('descricao', '')} Palavras-chave: {', '.join(e.get('palavras_chave', []))}. "
                     f"Dispositivos: {', '.join(e.get('dispositivos', []))}.")
    return [q["id"] for q in qs], q_txt, [t["tema_id"] for t in temas], t_tit, t_enr


def codificar_st(mid, lista, tipo):
    from sentence_transformers import SentenceTransformer
    m = codificar_st.cache.get(mid)
    if m is None:
        m = SentenceTransformer(mid, device="cpu", trust_remote_code=True)
        m.max_seq_length = min(512, m.max_seq_length or 512)
        codificar_st.cache = {mid: m}
    if "e5" in mid:
        lista = [("query: " if tipo == "q" else "passage: ") + x for x in lista]
        return m.encode(lista, batch_size=16, normalize_embeddings=True, show_progress_bar=False)
    if "Qwen3-Embedding" in mid and tipo == "q":
        return m.encode(lista, batch_size=8, normalize_embeddings=True, prompt_name="query", show_progress_bar=False)
    return m.encode(lista, batch_size=16, normalize_embeddings=True, show_progress_bar=False)


codificar_st.cache = {}


def codificar_ollama(mid, lista, tipo):
    import httpx
    out = []
    for i in range(0, len(lista), 16):
        r = httpx.post("http://localhost:11434/api/embed", json={"model": mid, "input": [x[:6000] for x in lista[i:i + 16]]}, timeout=600)
        r.raise_for_status()
        out.extend(r.json()["embeddings"])
    v = np.array(out, dtype=np.float32)
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def calcular(a):
    A = Arvore()
    enr = json.loads((RAIZ / "data" / "temas_enriquecidos.json").read_text(encoding="utf-8"))
    qids, q_txt, tids, t_tit, t_enr = textos(A, enr)
    PASTA.mkdir(parents=True, exist_ok=True)
    (PASTA / "ids.json").write_text(json.dumps({"questoes": qids, "temas": tids}), encoding="utf-8")
    tempos = json.loads((PASTA / "tempos.json").read_text(encoding="utf-8")) if (PASTA / "tempos.json").exists() else {}
    escolhidos = a.modelos.split(",") if a.modelos else [m[0] for m in MODELOS]
    for apelido, origem, mid, grupo, obs in MODELOS:
        if apelido not in escolhidos:
            continue
        alvo = PASTA / f"{apelido}__temas_enriq.npy"
        if alvo.exists():
            print(f"{apelido}: já calculado")
            continue
        t0 = time.time()
        try:
            fn = codificar_st if origem == "st" else codificar_ollama
            q = fn(mid, q_txt, "q")
            tt = fn(mid, t_tit, "t")
            te = fn(mid, t_enr, "t")
        except Exception as e:  # noqa: BLE001
            print(f"{apelido}: ERRO {e!r}"[:300])
            continue
        np.save(PASTA / f"{apelido}__questoes.npy", np.asarray(q, dtype=np.float32))
        np.save(PASTA / f"{apelido}__temas_titulo.npy", np.asarray(tt, dtype=np.float32))
        np.save(alvo, np.asarray(te, dtype=np.float32))
        tempos[apelido] = round(time.time() - t0, 1)
        (PASTA / "tempos.json").write_text(json.dumps(tempos, indent=1), encoding="utf-8")
        print(f"{apelido}: ok em {tempos[apelido]}s, dim={np.asarray(q).shape[1]}", flush=True)


def referencia(A, qids):
    rods = {r: carregar_rodada(r, A) for r in ["claude-opus", "claude-sonnet-h", "arbitro-opus"]}
    ref = {}
    for q in qids:
        vs = [rods[r][q][0] for r in rods if q in rods[r]]
        if len(vs) == len(rods) and all(v["ramo"] and not v["fora"] for v in vs) and len({v["ramo"] for v in vs}) == 1:
            ref[q] = vs[0]["ramo"]
    return ref


def avaliar(a):
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import StratifiedKFold, cross_val_predict
    A = Arvore()
    ids = json.loads((PASTA / "ids.json").read_text(encoding="utf-8"))
    qids, tids = ids["questoes"], ids["temas"]
    ramo_do_tema = np.array([A.ramo_de(t) for t in tids])
    ref = referencia(A, qids)
    idx = [i for i, q in enumerate(qids) if q in ref]
    y = np.array([ref[qids[i]] for i in idx])
    tempos = json.loads((PASTA / "tempos.json").read_text(encoding="utf-8")) if (PASTA / "tempos.json").exists() else {}
    linhas = []
    for apelido, origem, mid, grupo, obs in MODELOS:
        if not (PASTA / f"{apelido}__temas_enriq.npy").exists():
            continue
        Q = np.load(PASTA / f"{apelido}__questoes.npy")
        res = {"modelo": apelido, "hf_id": mid, "grupo": grupo, "obs": obs, "segundos": tempos.get(apelido), "n_ref": len(idx)}
        for var in ("titulo", "enriq"):
            Tm = np.load(PASTA / f"{apelido}__temas_{var}.npy")
            S = Q[idx] @ Tm.T
            ordem = np.argsort(-S, axis=1)
            top1 = ramo_do_tema[ordem[:, 0]]
            acc = float(np.mean(top1 == y))
            rec = {}
            for k in (5, 10, 20):
                rec[k] = float(np.mean([y[i] in set(ramo_do_tema[ordem[i, :k]]) for i in range(len(idx))]))
            cont = Counter(tids[j] for j in ordem[:, 0])
            no_top, n_top = cont.most_common(1)[0]
            res[var] = {"top1_ramo": round(acc, 3), "recall_ramo@5": round(rec[5], 3), "recall_ramo@10": round(rec[10], 3),
                        "recall_ramo@20": round(rec[20], 3), "maior_lixeira": f"{A.titulo(no_top)} ({n_top / len(idx):.0%})",
                        "maior_lixeira_frac": round(n_top / len(idx), 3), "temas_distintos_top1": len(cont)}
        # destilação: regressão logística sobre os embeddings das questões, rótulos = consenso; CV estratificada
        cont_y = Counter(y)
        ok = [i for i, lab in enumerate(y) if cont_y[lab] >= 5]
        if len(ok) > 50:
            Xd, yd = Q[idx][ok], y[ok]
            pred = cross_val_predict(LogisticRegression(max_iter=2000, C=4.0), Xd, yd,
                                     cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=0))
            res["destilacao"] = {"acerto_cv": round(float(np.mean(pred == yd)), 3), "n": len(ok), "classes": len(set(yd))}
        linhas.append(res)
    (RAIZ / "runs" / "embeddings.json").write_text(json.dumps(linhas, ensure_ascii=False, indent=1), encoding="utf-8")

    md = ["# Experimento com embeddings (sem LLM)\n",
          f"Referência: {len(idx)} questões em que o Opus plano, o Sonnet 2 estágios e o árbitro concordam no ramo. "
          "Não é gabarito; é o consenso dos LLMs. \"Top-1 ramo\": o tema mais parecido está no ramo da referência. "
          "\"Recall@k\": o ramo da referência aparece entre os k temas mais parecidos. \"Maior lixeira\": o tema que mais "
          "atraiu questões como primeira opção. \"Destilação\": regressão logística treinada sobre os embeddings das questões "
          "com os rótulos do consenso, validação cruzada de 5 partes, só classes com ao menos 5 questões.\n",
          "| Modelo | Grupo | Texto do tema | Top-1 ramo | Recall@5 | Recall@10 | Recall@20 | Maior lixeira | Temas distintos no top-1 | Destilação (acerto CV) | Tempo (s) |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in linhas:
        for var, nome in (("titulo", "só caminho"), ("enriq", "enriquecido")):
            v = r[var]
            dest = f"{r['destilacao']['acerto_cv']:.0%} (n={r['destilacao']['n']})" if var == "enriq" and "destilacao" in r else ""
            md.append(f"| {r['modelo']} | {r['grupo']} | {nome} | {v['top1_ramo']:.0%} | {v['recall_ramo@5']:.0%} | {v['recall_ramo@10']:.0%} | "
                      f"{v['recall_ramo@20']:.0%} | {v['maior_lixeira']} | {v['temas_distintos_top1']} | {dest} | {r['segundos'] if var == 'enriq' else ''} |")
    md.append("\nModelos: " + "; ".join(f"`{r['hf_id']}` ({r['obs']})" for r in linhas) + ".")
    (RAIZ / "docs" / "embeddings.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("acao", choices=["calcular", "avaliar"])
    ap.add_argument("--modelos", default=None)
    a = ap.parse_args()
    calcular(a) if a.acao == "calcular" else avaliar(a)
