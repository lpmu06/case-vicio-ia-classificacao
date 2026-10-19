"""Etapa 3d: classificação hierárquica com o Jev (TypeSafe "System One"), um modelo de decisão estruturada
que devolve uma distribuição de probabilidade calibrada sobre as opções (até 255 por pergunta).

Estágio 1: escolhe o tema de nível 1 entre os temas ativos de nível 1 (+ opção "fora"), cada um com uma descrição curta.
Estágio 2: escolhe entre "o próprio tema (genérico)" e os subtemas do tema escolhido, com as descrições enriquecidas.
A saída segue o esquema das outras rodadas; as confianças são as probabilidades do Jev.

Requer TYPESAFE_API_KEY (ou a linha `typesafe = ...` em keys.txt). API: POST https://api.typesafe.ai/v1/systemone
Uso: python src/33_classificar_jev.py [--limite 5]
"""
import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import carregar_chaves
from comum import Arvore, RAIZ, carregar_questoes

URL = "https://api.typesafe.ai/v1/systemone"
INSTR_1 = ("Esta é uma questão de concurso público jurídico brasileiro. Qual tema de estudo da plataforma ela testa? "
           "Escolha o tema cujo instituto jurídico é necessário para responder, não o cenário da história. "
           "Use 'fora' apenas se nenhum tema servir.")
INSTR_2 = ("Dentro do tema escolhido, a questão testa especificamente um destes subtemas? Escolha 'generico' se a questão "
           "cobre o tema de forma geral ou se houver dúvida entre subtemas.")


def chamar(chave, estado, nome, instr, criterios):
    corpo = {"state": estado, "model": "jev-latest",
             "questions": {nome: {"type": "choice", "instructions": instr, "criteria": criterios}}}
    for tentativa in range(5):
        r = httpx.post(URL, json=corpo, headers={"Authorization": f"Bearer {chave}"}, timeout=120)
        if r.status_code in (429, 529):
            time.sleep(2 ** tentativa)
            continue
        r.raise_for_status()
        j = r.json()
        return j["answers"][nome], j.get("usage", {})
    raise RuntimeError("Jev: limite de requisições")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rotulo", default="jev-h")
    ap.add_argument("--limite", type=int, default=None)
    ap.add_argument("--ids", default=None)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    chaves = carregar_chaves()
    chave = os.environ.get("TYPESAFE_API_KEY") or chaves.get("typesafe")
    if not chave:
        sys.exit("Falta a chave do Jev: crie em https://console.typesafe.ai/ e adicione 'typesafe = ...' em keys.txt")

    A = Arvore()
    enr = json.loads((RAIZ / "data" / "temas_enriquecidos.json").read_text(encoding="utf-8"))
    n1 = [t for t in A.t.values() if t["nivel"] == 1 and t["status"] == "active" and not t["bucket"]]
    crit1 = {f"t{t['tema_id']}": f"{t['caminho']}: {enr.get(t['tema_id'], {}).get('descricao', '')[:300]}" for t in n1}
    crit1["fora"] = "Nenhum tema de Direito Penal, Processo Penal, Legislação Penal Especial ou Criminologia serve (ex.: Direito Tributário)."
    qs = carregar_questoes()
    if a.ids:
        qs = [q for q in qs if q["id"] in a.ids.split(",")]
    if a.limite:
        qs = qs[:a.limite]
    pasta = RAIZ / "runs" / a.rotulo
    pasta.mkdir(parents=True, exist_ok=True)
    pend = [q for q in qs if not (pasta / f"{q['id']}.json").exists()]
    print(f"Jev: {len(crit1)} opções no estágio 1; {len(pend)} pendentes", flush=True)

    def tarefa(q):
        estado = q["texto"][:6000]
        r1, u1 = chamar(chave, estado, "tema", INSTR_1, crit1)
        probs1 = sorted(r1["probabilities"].items(), key=lambda kv: -kv[1])
        escolha = r1["choice"]
        out = {"fora": escolha == "fora", "tema_n1_id": None, "subtema_n2_id": None, "confianca_ramo": probs1[0][1],
               "confianca_subtema": 0.0, "segunda_opcao_id": probs1[1][0].lstrip("t") if len(probs1) > 1 and probs1[1][0] != "fora" else None,
               "extras_ids": [], "multi_tema": False, "justificativa": f"Jev: top-3 {probs1[:3]}; confiança {r1.get('confidence')}",
               "probabilidades_estagio1": dict(probs1[:10])}
        u2 = {}
        if escolha != "fora":
            tid = escolha.lstrip("t")
            out["tema_n1_id"] = tid
            filhos = [A.t[f] for f in A.t[tid]["filhos"] if A.t[f]["status"] == "active" and not A.t[f]["bucket"]]
            if filhos:
                crit2 = {"generico": f"A questão cobre {A.t[tid]['titulo']} de forma geral, ou há dúvida entre subtemas."}
                crit2.update({f"t{f['tema_id']}": f"{f['titulo']}: {enr.get(f['tema_id'], {}).get('descricao', '')[:300]}" for f in filhos})
                r2, u2 = chamar(chave, estado, "subtema", INSTR_2, crit2)
                if r2["choice"] != "generico":
                    out["subtema_n2_id"] = r2["choice"].lstrip("t")
                    out["confianca_subtema"] = r2["probabilities"][r2["choice"]]
                out["probabilidades_estagio2"] = r2["probabilities"]
        out.update({"id": q["id"], "modelo": "jev-latest", "provedor": "typesafe", "uso": {"estagio1": u1, "estagio2": u2}})
        (pasta / f"{q['id']}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        return q["id"]

    t0 = time.time()
    erros = []
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(tarefa, q): q for q in pend}
        for i, f in enumerate(as_completed(futs), 1):
            try:
                f.result()
                if i % 20 == 0:
                    print(f"[{i}/{len(pend)}]", flush=True)
            except Exception as e:  # noqa: BLE001
                erros.append({"id": futs[f]["id"], "erro": repr(e)[:300]})
                print(f"ERRO {futs[f]['id']}: {e!r}"[:300], flush=True)
    (pasta / "_usage.json").write_text(json.dumps({"segundos": round(time.time() - t0), "erros": erros, "modelo": "jev-latest"},
                                                  ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"fim: {len(pend) - len(erros)} ok, {len(erros)} erros, {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
