"""Etapa 1b: enriquece a taxonomia com um LLM (uma vez só).

Para cada tema de nível 1 (com seus subtemas), pede ao modelo: descrição de 2–3 linhas,
palavras-chave, dispositivos legais cobertos e "não confundir com" (fronteiras com irmãos).
Temas inativos e buckets de curso não são enriquecidos (nunca recebem publicação).

Saída: data/temas_enriquecidos.json ; custo e uso em runs/11_enriquecer_usage.json
"""
import json, re, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import carregar_chaves
carregar_chaves()
import anthropic
import importlib
arv = importlib.import_module("10_arvore")

RAIZ = Path(__file__).resolve().parents[1]
MODEL = "claude-opus-5"
PRECO = {"in": 5.0, "out": 25.0, "cache_w": 6.25, "cache_r": 0.5}  # US$/M tokens

SISTEMA = """Você é um professor de Direito Penal, Processo Penal, Legislação Penal Especial e Criminologia, com experiência em concursos públicos e exame da OAB no Brasil, ajudando a organizar a taxonomia de uma plataforma de questões.

A árvore completa de temas da plataforma é esta (id | título; indentação = hierarquia):

<arvore>
{arvore}
</arvore>

Sua tarefa: para cada tema pedido, escrever metadados que permitam a uma pessoa ou a um modelo decidir com segurança se uma questão de concurso pertence a ele e, principalmente, distingui-lo dos temas vizinhos.

Responda SOMENTE com um objeto JSON válido, sem comentários nem markdown, no formato:
{{
  "<tema_id>": {{
    "descricao": "2 a 3 frases sobre o que o tema cobre, na prática das provas",
    "palavras_chave": ["8 a 15 termos e expressões típicos de enunciados sobre este tema"],
    "dispositivos": ["artigos de lei / leis / súmulas centrais, ex.: 'art. 155 CP', 'Lei 11.343/2006', 'Súmula 582 STJ'"],
    "nao_confundir": "em 1 a 3 frases: com quais temas vizinhos (cite ids) costuma ser confundido e qual é o critério de desempate"
  }}
}}
Inclua exatamente os ids pedidos, nenhum a mais."""

def montar_pedido(temas, t1):
    filhos = [temas[f] for f in t1["filhos"] if temas[f]["status"] == "active" and not temas[f]["bucket"]]
    irmaos = [temas[s] for s in temas[t1["parent_id"]]["filhos"] if s != t1["tema_id"] and temas[s]["status"] == "active" and not temas[s]["bucket"]]
    ids = [t1["tema_id"]] + [f["tema_id"] for f in filhos]
    linhas = [f"Disciplina: {t1['disciplina']}", f"Tema (nível 1): {t1['tema_id']} | {t1['titulo']}"]
    if filhos:
        linhas.append("Subtemas (nível 2) deste tema:")
        linhas += [f"  {f['tema_id']} | {f['titulo']}" for f in filhos]
    linhas.append("Outros temas de nível 1 da mesma disciplina (para o 'não confundir'):")
    linhas += [f"  {s['tema_id']} | {s['titulo']}" for s in irmaos]
    linhas.append(f"\nEscreva os metadados para estes ids: {', '.join(ids)}")
    return "\n".join(linhas), ids

def chamar(client, sistema, pedido, ids):
    r = client.messages.create(
        model=MODEL, max_tokens=12000,
        system=[{"type": "text", "text": sistema, "cache_control": {"type": "ephemeral"}}],
        output_config={"effort": "medium"},
        messages=[{"role": "user", "content": pedido}],
    )
    texto = "".join(b.text for b in r.content if b.type == "text")
    m = re.search(r"\{.*\}", texto, flags=re.S)
    dados = json.loads(m.group(0))
    faltam = [i for i in ids if i not in dados]
    return dados, faltam, r.usage

def main():
    temas = arv.carregar_temas()
    sistema = SISTEMA.format(arvore=arv.arvore_texto(temas))
    alvos = [t for t in temas.values() if t["nivel"] == 1 and t["status"] == "active" and not t["bucket"]]
    client = anthropic.Anthropic()
    saida, uso_total, erros = {}, {"in": 0, "out": 0, "cache_w": 0, "cache_r": 0}, []
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {}
        for t1 in alvos:
            pedido, ids = montar_pedido(temas, t1)
            futs[ex.submit(chamar, client, sistema, pedido, ids)] = (t1, ids)
        for i, fut in enumerate(as_completed(futs), 1):
            t1, ids = futs[fut]
            try:
                dados, faltam, u = fut.result()
                for k, v in dados.items():
                    if k in temas: saida[k] = v
                if faltam: erros.append({"tema": t1["tema_id"], "faltam": faltam})
                uso_total["in"] += u.input_tokens; uso_total["out"] += u.output_tokens
                uso_total["cache_w"] += u.cache_creation_input_tokens or 0
                uso_total["cache_r"] += u.cache_read_input_tokens or 0
                print(f"[{i}/{len(alvos)}] {t1['titulo'][:50]:50s} ok ({len(dados)} ids)", flush=True)
            except Exception as e:
                erros.append({"tema": t1["tema_id"], "erro": repr(e)[:300]})
                print(f"[{i}/{len(alvos)}] {t1['titulo'][:50]:50s} ERRO {e!r}"[:200], flush=True)
    custo = sum(uso_total[k] / 1e6 * PRECO[k] for k in PRECO)
    (RAIZ / "data" / "temas_enriquecidos.json").write_text(json.dumps(saida, ensure_ascii=False, indent=1), encoding="utf-8")
    (RAIZ / "runs").mkdir(exist_ok=True)
    (RAIZ / "runs" / "11_enriquecer_usage.json").write_text(json.dumps({
        "modelo": MODEL, "chamadas": len(alvos), "temas_enriquecidos": len(saida), "uso_tokens": uso_total,
        "custo_usd_estimado": round(custo, 3), "segundos": round(time.time() - t0), "erros": erros}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n{len(saida)} temas enriquecidos; custo ≈ US$ {custo:.2f}; {time.time()-t0:.0f}s; erros: {len(erros)}")

if __name__ == "__main__":
    main()
