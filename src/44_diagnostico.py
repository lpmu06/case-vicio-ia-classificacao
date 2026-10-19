"""Etapa 4g: diagnóstico quantitativo para a seção (b) do relatório.

Mede onde os classificadores divergem (proxy de dificuldade), por tipo de questão, tamanho, disciplina do consenso,
multi-tema e origem; quanto a origem erra a disciplina; como as questões se distribuem pela árvore (temas vazios,
concentração, temas genéricos que viram "lixeira").

Uso: python src/44_diagnostico.py
Saída: docs/diagnostico.md e runs/diagnostico.json
"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import Arvore, RAIZ, carregar_rodada, carregar_questoes

RODADAS = ["claude-opus", "claude-sonnet-h", "claude-sonnet-3n", "claude-haiku-h", "claude-haiku-3n", "arbitro-opus"]
DISC_ORIGEM = {"Direito Penal": "Penal", "Penal": "Penal", "Processo Penal": "Processo Penal", "Direito Processual Penal": "Processo Penal",
               "Criminologia": "Criminologia", "Direito Penal - Legislação Especial": "Direito Penal - Legislação Especial"}
GENERICOS = ["5580", "5582", "5581", "5170", "5171", "5584", "5585", "5499", "5467", "5088", "5200", "5212"]


def main():
    A = Arvore()
    qs = {q["id"]: q for q in carregar_questoes()}
    rods = {r: carregar_rodada(r, A) for r in RODADAS}
    rods = {r: v for r, v in rods.items() if v}
    dec = {json.loads(l)["id"]: json.loads(l) for l in (RAIZ / "data" / "decisoes.jsonl").open(encoding="utf-8")}

    linhas = []
    for qid, q in qs.items():
        votos = ["FORA" if rod[qid][0]["fora"] else rod[qid][0]["ramo"] for rod in rods.values() if qid in rod]
        c = Counter(votos)
        maj, nmaj = c.most_common(1)[0] if c else (None, 0)
        multi = any(rod[qid][0]["multi"] for rod in rods.values() if qid in rod)
        linhas.append({"id": qid, "tipo": q["tipo"], "chars": q["n_chars"], "maj": maj, "unanime": nmaj == len(votos) and len(votos) > 0,
                       "frac": nmaj / len(votos) if votos else 0, "multi": multi, "disc_origem": q["disciplina_origem"],
                       "decisao": dec[qid]["decisao"]})

    res = {"grupos": {}}

    def taxa(grupo, chave=None):
        u = sum(x['unanime'] for x in grupo) / len(grupo)
        pb = sum(x['decisao'] == 'publicar' for x in grupo) / len(grupo)
        if chave:
            res["grupos"][chave] = {"unanimes": round(u, 3), "publicadas": round(pb, 3), "n": len(grupo)}
        return f"{u:.0%} unânimes; {pb:.0%} publicadas (n={len(grupo)})"

    md = ["# Diagnóstico quantitativo\n", "Gerado por `src/44_diagnostico.py`. \"Unânime\": todas as rodadas de classificação e o árbitro "
          f"escolheram o mesmo ramo ({len(rods)} rodadas). É uma medida de dificuldade sem gabarito.\n"]

    md.append("## Por tipo de questão")
    for t in ("multipla_escolha", "certo_errado"):
        g = [x for x in linhas if x["tipo"] == t]
        md.append(f"- {t.replace('_', ' ')}: {taxa(g, t)}")
    md.append("\n## Por tamanho do texto (terços)")
    ordem = sorted(linhas, key=lambda x: x["chars"])
    for i, nome in enumerate(("curtas", "médias", "longas")):
        g = ordem[i * len(ordem) // 3:(i + 1) * len(ordem) // 3]
        md.append(f"- {nome} ({g[0]['chars']}–{g[-1]['chars']} caracteres): {taxa(g)}")
    md.append("\n## Multi-tema (algum classificador marcou alternativas sobre institutos diferentes)")
    md.append(f"- marcadas: {taxa([x for x in linhas if x['multi']], 'multi')}")
    md.append(f"- não marcadas: {taxa([x for x in linhas if not x['multi']], 'nao_multi')}")

    md.append("\n## Por disciplina do ramo majoritário")
    por = defaultdict(list)
    for x in linhas:
        d = A.t[x["maj"]]["disciplina"] if x["maj"] in A.t else "fora"
        por[d].append(x)
    for d, g in sorted(por.items(), key=lambda kv: -len(kv[1])):
        md.append(f"- {d}: {taxa(g)}")

    md.append("\n## A disciplina de origem bate com a disciplina do ramo majoritário?")
    ok = errado = sem = 0
    trocas = Counter()
    for x in linhas:
        d_o = DISC_ORIGEM.get(x["disc_origem"])
        d_m = A.t[x["maj"]]["disciplina"] if x["maj"] in A.t else None
        if not d_o or not d_m:
            sem += 1
        elif d_o == d_m:
            ok += 1
        else:
            errado += 1
            trocas[(d_o, d_m)] += 1
    md.append(f"- igual: {ok}; diferente: {errado}; origem fora do recorte ou vazia: {sem}")
    md.append("- trocas mais comuns (origem → consenso): " + "; ".join(f"{a} → {b}: {n}" for (a, b), n in trocas.most_common(6)))
    res["disciplina_origem"] = {"igual": ok, "diferente": errado, "sem": sem}

    md.append("\n## Distribuição das questões pela árvore (tema central decidido, publicadas e revisar)")
    cont = Counter()
    for x in dec.values():
        if x["tema"]:
            cont[A.ramo_de(x["tema"])] += 1
    usaveis_n1 = [t for t in A.t.values() if t["nivel"] == 1 and t["status"] == "active" and not t["bucket"]]
    vazios = [t["titulo"] for t in usaveis_n1 if cont.get(t["tema_id"], 0) == 0]
    md.append(f"- temas de nível 1 usados: {len(cont)} de {len(usaveis_n1)}; sem nenhuma questão: {len(vazios)}")
    md.append("- mais frequentes: " + "; ".join(f"{A.titulo(t)}: {n}" for t, n in cont.most_common(10)))
    gen = Counter()
    for x in dec.values():
        if x["tema"] in GENERICOS or A.ramo_de(x["tema"]) in ("5580", "5170"):
            gen[A.titulo(x["tema"])] += 1
    md.append("- questões cujo tema central é um dos temas genéricos que a Vício chama de lixeira: "
              + (", ".join(f"{t}: {n}" for t, n in gen.most_common()) or "nenhuma"))
    res["temas_vazios_n1"] = vazios
    (RAIZ / "runs" / "diagnostico.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    (RAIZ / "docs" / "diagnostico.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
