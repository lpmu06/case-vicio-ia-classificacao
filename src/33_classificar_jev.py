"""Etapa 3d: classificação hierárquica com o Jev (TypeSafe "System One"), um modelo de decisão estruturada
que devolve uma distribuição de probabilidade sobre as opções (até 255 por pergunta).

Estágio 1: escolhe o tema de nível 1 entre os temas ativos de nível 1 (+ opção "fora").
Estágio 2: escolhe entre "o próprio tema (genérico)" e os subtemas do tema escolhido.
A saída segue o esquema das outras rodadas; as confianças são as probabilidades do Jev.

Variantes (um fator por vez em relação à base; decisão do Luis em 19/10/2026, 22h):
  base               jev-latest; critérios curtos (caminho + descrição cortada em 300 caracteres, chaves t<id>);
                     guloso (só o tema mais provável vai ao estágio 2); opções na ordem da árvore
  --modelo jev-preview   versão seguinte do modelo (1.14)
  --criterios ricos      cada opção vira um objeto {what, not_for, key_terms, subtopics}, com a descrição inteira, o
                         "não confundir" (ids trocados por nomes) e os subtemas; nomes de opção legíveis (caminho do tema)
  --beam 3               estágio 2 para os 3 temas mais prováveis; decide pela média geométrica das probabilidades
                         das duas decisões (cookbook "Hierarchical classification" da TypeSafe)
  --ordens 5             cada pergunta 5 vezes com as opções embaralhadas; média das probabilidades (mede o viés de ordem)

Requer TYPESAFE_API_KEY (ou a linha `jev = ...` / `typesafe = ...` em keys.txt). API: POST https://api.typesafe.ai/v1/systemone
Uso: python src/33_classificar_jev.py [--limite 5] [--modelo jev-preview] [--criterios ricos] [--beam 3] [--ordens 5]
Saída: runs/<rótulo>/, rótulo padrão jev-h (base) ou jev-h-<variante>.
Preço de lista (docs.typesafe.ai/models, 19/10/2026): US$ 0,042 por milhão de tokens de entrada; saída grátis.
"""
import argparse
import json
import os
import random
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import carregar_chaves
from comum import Arvore, RAIZ, carregar_questoes

URL = "https://api.typesafe.ai/v1/systemone"
PRECO_POR_MILHAO = 0.042
INSTR_1 = ("Esta é uma questão de concurso público jurídico brasileiro. Qual tema de estudo da plataforma ela testa? "
           "Escolha o tema cujo instituto jurídico é necessário para responder, não o cenário da história. "
           "Use 'fora' apenas se nenhum tema servir.")
INSTR_2 = ("Dentro do tema escolhido, a questão testa especificamente um destes subtemas? Escolha 'generico' se a questão "
           "cobre o tema de forma geral ou se houver dúvida entre subtemas.")
FORA_TXT = "Nenhum tema de Direito Penal, Processo Penal, Legislação Penal Especial ou Criminologia serve (ex.: Direito Tributário)."
# nomes das opções especiais nos critérios ricos (as instruções citam 'fora' e 'generico')
FORA_RICO, GENERICO_RICO = "fora", "generico"


def ativos(A, ids):
    return [A.t[i] for i in ids if A.t[i]["status"] == "active" and not A.t[i]["bucket"]]


def nao_confundir(A, e, limite=None):
    """Texto do "não confundir" com os ids trocados pelo título do tema; com limite, corta na última frase que cabe."""
    s = re.sub(r"\b(\d{3,5})\b", lambda m: A.rotulo(m.group(1)) if m.group(1) in A.t else m.group(0), e.get("nao_confundir") or "")
    if limite and len(s) > limite:
        corte = s[:limite]
        fim = corte.rfind(". ")
        s = corte[:fim + 1] if fim > 0 else corte
    return s


def opcoes_n1(A, enr, estilo):
    """(critérios, {nome da opção: tema_id ou 'FORA'})"""
    n1 = [t for t in A.t.values() if t["nivel"] == 1 and t["status"] == "active" and not t["bucket"]]
    crit, mapa = {}, {}
    for t in n1:
        e = enr.get(t["tema_id"], {})
        if estilo == "curtos":
            nome, desc = f"t{t['tema_id']}", f"{t['caminho']}: {e.get('descricao', '')[:300]}"
        else:
            # a versão completa (~44 mil tokens) passa do limite de 32 mil por pergunta: "não confundir" até ~350
            # caracteres e 8 palavras-chave
            nome = t["caminho"]
            desc = {"what": e.get("descricao", ""), "not_for": nao_confundir(A, e, 350), "key_terms": e.get("palavras_chave", [])[:8]}
            filhos = ativos(A, t["filhos"])
            if filhos:
                desc["subtopics"] = [f["titulo"] for f in filhos]
        crit[nome], mapa[nome] = desc, t["tema_id"]
    crit["fora"] = FORA_TXT if estilo == "curtos" else {"what": FORA_TXT}
    mapa["fora"] = "FORA"
    return crit, mapa


def opcoes_n2(A, enr, tid, estilo):
    """(critérios, {nome da opção: subtema_id ou None para o genérico}); vazio se o tema não tem subtemas."""
    filhos = ativos(A, A.t[tid]["filhos"])
    if not filhos:
        return {}, {}
    gen = f"A questão cobre {A.t[tid]['titulo']} de forma geral, ou há dúvida entre subtemas."
    crit = {"generico": gen if estilo == "curtos" else {"what": gen}}
    mapa = {"generico": None}
    for f in filhos:
        e = enr.get(f["tema_id"], {})
        if estilo == "curtos":
            nome, desc = f"t{f['tema_id']}", f"{f['titulo']}: {e.get('descricao', '')[:300]}"
        else:
            nome = f["titulo"]
            desc = {"what": e.get("descricao", ""), "not_for": nao_confundir(A, e), "key_terms": e.get("palavras_chave", [])}
        crit[nome], mapa[nome] = desc, f["tema_id"]
    return crit, mapa


def chamar(chave, modelo, estado, instr, criterios):
    corpo = {"state": estado, "model": modelo,
             "questions": {"q": {"type": "choice", "instructions": instr, "criteria": criterios}}}
    for tentativa in range(6):
        r = httpx.post(URL, json=corpo, headers={"Authorization": f"Bearer {chave}"}, timeout=120)
        if r.status_code in (429, 500, 502, 503, 529):
            time.sleep(2 ** tentativa)
            continue
        if r.status_code != 200:
            raise RuntimeError(f"Jev {r.status_code}: {r.text[:300]}")
        j = r.json()
        return j["answers"]["q"], j.get("usage", {}), j.get("model")
    raise RuntimeError("Jev: limite de requisições")


def perguntar(chave, modelo, estado, instr, crit, ordens, semente, uso):
    """Probabilidades médias sobre `ordens` repetições (a primeira na ordem original, as demais embaralhadas)
    e a escolha de cada repetição. Acumula tokens em `uso`."""
    nomes = list(crit)
    soma = dict.fromkeys(nomes, 0.0)
    escolhas = []
    for k in range(ordens):
        ordem = nomes if k == 0 else random.Random(f"{semente}-{k}").sample(nomes, len(nomes))
        r, u, m = chamar(chave, modelo, estado, instr, {n: crit[n] for n in ordem})
        for n in nomes:
            soma[n] += r["probabilities"].get(n, 0.0)
        escolhas.append(r["choice"])
        uso["chamadas"] += 1
        uso["input_tokens"] += u.get("input_tokens", 0)
        uso["output_tokens"] += u.get("output_tokens", 0)
        uso["modelo"] = m
    return {n: v / ordens for n, v in soma.items()}, escolhas


def confianca(p):
    """Fórmula da TypeSafe para Choice: quanto a maior probabilidade passa da divisão uniforme."""
    n = len(p)
    return (max(p.values()) - 1 / n) / (1 - 1 / n) if n > 1 else 1.0


def rotulo_padrao(a):
    partes = [s for s, ativo in (("preview", a.modelo == "jev-preview"), ("ricos", a.criterios == "ricos"),
                                 (f"beam{a.beam}", a.beam > 1), (f"ordens{a.ordens}", a.ordens > 1)) if ativo]
    return "-".join(["jev-h"] + partes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rotulo", default=None)
    ap.add_argument("--limite", type=int, default=None)
    ap.add_argument("--ids", default=None)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--modelo", default="jev-latest")
    ap.add_argument("--criterios", choices=["curtos", "ricos"], default="curtos")
    ap.add_argument("--beam", type=int, default=1)
    ap.add_argument("--ordens", type=int, default=1)
    a = ap.parse_args()
    chaves = carregar_chaves()
    chave = os.environ.get("TYPESAFE_API_KEY") or chaves.get("typesafe") or chaves.get("jev")
    if not chave:
        sys.exit("Falta a chave do Jev: crie em https://console.typesafe.ai/ e adicione 'jev = ...' em keys.txt")
    rotulo = a.rotulo or rotulo_padrao(a)
    variante = {"modelo": a.modelo, "criterios": a.criterios, "beam": a.beam, "ordens": a.ordens}

    A = Arvore()
    enr = json.loads((RAIZ / "data" / "temas_enriquecidos.json").read_text(encoding="utf-8"))
    crit1, mapa1 = opcoes_n1(A, enr, a.criterios)
    qs = carregar_questoes()
    if a.ids:
        qs = [q for q in qs if q["id"] in a.ids.split(",")]
    if a.limite:
        qs = qs[:a.limite]
    pasta = RAIZ / "runs" / rotulo
    pasta.mkdir(parents=True, exist_ok=True)
    pend = [q for q in qs if not (pasta / f"{q['id']}.json").exists()]
    print(f"Jev {rotulo} {variante}: {len(crit1)} opções no estágio 1; {len(pend)} pendentes", flush=True)

    def tarefa(q):
        estado = q["texto"][:6000]
        uso = {"chamadas": 0, "input_tokens": 0, "output_tokens": 0, "modelo": None}
        p1, esc1 = perguntar(chave, a.modelo, estado, INSTR_1, crit1, a.ordens, f"{q['id']}-1", uso)
        cands = sorted(p1.items(), key=lambda kv: -kv[1])
        # folhas: (pontuação, tema n1 ou FORA, subtema ou None, prob. do ramo, prob. do subtema, probs do estágio 2)
        folhas = []
        for nome, p in cands[:a.beam]:
            tid = mapa1[nome]
            crit2, mapa2 = opcoes_n2(A, enr, tid, a.criterios) if tid != "FORA" else ({}, {})
            if not crit2:
                folhas.append((p, tid, None, p, None, None))
                continue
            p2, _ = perguntar(chave, a.modelo, estado, INSTR_2, crit2, a.ordens, f"{q['id']}-2-{tid}", uso)
            p2_ids = {(mapa2[n] or "generico"): v for n, v in p2.items()}
            for n, v in p2.items():
                folhas.append(((p * v) ** 0.5, tid, mapa2[n], p, v, p2_ids))
        melhor = max(folhas, key=lambda f: f[0])
        _, tid, sub, p_ramo, p_sub, p2_ids = melhor
        segunda = next((mapa1[n] for n, _ in cands if mapa1[n] not in (tid, "FORA")), None)
        top3 = [(A.rotulo(mapa1[n]) if mapa1[n] != "FORA" else "fora", round(v, 3)) for n, v in cands[:3]]
        out = {"fora": tid == "FORA", "tema_n1_id": None if tid == "FORA" else tid, "subtema_n2_id": sub,
               "confianca_ramo": p_ramo, "confianca_subtema": p_sub if sub else 0.0, "segunda_opcao_id": segunda,
               "extras_ids": [], "multi_tema": False,
               "justificativa": f"Jev: top-3 do estágio 1 {top3}; confiança {confianca(p1):.2f}",
               "confianca_estagio1": confianca(p1),
               "probabilidades_estagio1": {mapa1[n]: v for n, v in cands[:10]}}
        if p2_ids:
            out["probabilidades_estagio2"] = p2_ids
        if a.ordens > 1:
            out["escolhas_por_ordem_estagio1"] = [mapa1[n] for n in esc1]
        if a.beam > 1:
            out["folhas_beam"] = [{"tema": f[1], "subtema": f[2], "pontuacao": round(f[0], 4)}
                                  for f in sorted(folhas, key=lambda f: -f[0])[:5]]
            out["ramo_guloso"] = mapa1[cands[0][0]]
        out.update({"id": q["id"], "modelo": uso["modelo"] or a.modelo, "provedor": "typesafe", "variante": variante, "uso": uso})
        (pasta / f"{q['id']}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        return q["id"]

    t0 = time.time()
    erros = []
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(tarefa, q): q for q in pend}
        for i, f in enumerate(as_completed(futs), 1):
            try:
                f.result()
                if i % 50 == 0:
                    print(f"[{i}/{len(pend)}]", flush=True)
            except Exception as e:  # noqa: BLE001
                erros.append({"id": futs[f]["id"], "erro": repr(e)[:300]})
                print(f"ERRO {futs[f]['id']}: {e!r}"[:300], flush=True)
    feitos = [json.loads(p.read_text(encoding="utf-8")) for p in pasta.glob("Q*.json")]
    tok = sum(d["uso"]["input_tokens"] for d in feitos)
    (pasta / "_usage.json").write_text(json.dumps(
        {"segundos": round(time.time() - t0), "erros": erros, "variante": variante,
         "modelo_resolvido": sorted({d["modelo"] for d in feitos}), "questoes": len(feitos),
         "chamadas": sum(d["uso"]["chamadas"] for d in feitos), "tokens_entrada": tok,
         "custo_usd": round(tok * PRECO_POR_MILHAO / 1e6, 4)}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"fim: {len(pend) - len(erros)} ok, {len(erros)} erros, {time.time() - t0:.0f}s; "
          f"{tok:,} tokens de entrada, US$ {tok * PRECO_POR_MILHAO / 1e6:.4f}")


if __name__ == "__main__":
    main()
