"""Etapa 7: gera docs/relatorio.md e docs/memo_professor.md a partir dos modelos em src/modelos/, preenchendo os
marcadores «CHAVE» com os números das saídas (runs/*.json, data/decisoes.jsonl). Assim os textos nunca ficam com
números velhos.

Uso: python src/62_preencher_relatorio.py
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import Arvore, RAIZ, gemeos_67xx

PIPELINE = ["claude-opus", "claude-sonnet-h", "arbitro-opus"]  # o que gera publicacao.csv


def p1(x):
    return f"{100 * x:.1f}".replace(".", ",") + "%"


def p0(x):
    return f"{100 * x:.0f}%"


def dec2(x):
    return f"{x:.2f}".replace(".", ",")


def milhar(x):
    return f"{int(round(x)):,}".replace(",", ".")


def usd(x):
    return f"{x:.3f}".replace(".", ",")


def main():
    A = Arvore()
    prev = json.loads((RAIZ / "runs" / "previsao.json").read_text(encoding="utf-8"))
    prev_sd = json.loads((RAIZ / "runs" / "previsao_sem_duplicados.json").read_text(encoding="utf-8"))
    prev_sub = json.loads((RAIZ / "runs" / "previsao_subtema.json").read_text(encoding="utf-8"))
    comp = json.loads((RAIZ / "runs" / "comparacao_metodos.json").read_text(encoding="utf-8"))
    diag = json.loads((RAIZ / "runs" / "diagnostico.json").read_text(encoding="utf-8"))
    dec = [json.loads(l) for l in (RAIZ / "data" / "decisoes.jsonl").open(encoding="utf-8")]
    c = Counter(d["decisao"] for d in dec)
    loo = {l["rodada"]: l for l in comp.get("amostra_2x2", [])}
    met = {l["rodada"]: l for l in comp["metodos"]}

    def loo_txt(r):
        return f"{p1(loo[r]['concorda_maioria_demais'])} (n={loo[r]['n']})" if r in loo else "não concluído"

    def tok(r):
        return milhar(met[r]["tokens_prompt_por_questao"]) if r in met else "-"

    def custo(r):
        return usd(met[r]["custo_usd_por_questao_com_cache"]) if r in met and met[r]["custo_usd_por_questao_com_cache"] else "-"

    # fila do professor: motivos das revisões, em categorias exclusivas
    rev = [d for d in dec if d["decisao"] == "revisar"]
    n_multi = sum("instituto diferente" in d["motivo"] for d in rev)
    n_disc = sum("instituto diferente" not in d["motivo"] and "não concordam" in d["motivo"] for d in rev)
    n_front = sum("instituto diferente" not in d["motivo"] and "não concordam" not in d["motivo"]
                  and ("fronteira" in d["motivo"] or "costumam confundir" in d["motivo"]) for d in rev)
    taxa_rev = len(rev) / len(dec)
    fila_semana = round(taxa_rev * 50000, -2)
    minutos = len(rev)
    fila_case = f"{minutos // 60} h {minutos % 60:02d}" if minutos % 60 else f"{minutos // 60} h"

    # gêmeos 67xx: quantos buckets em cada grupo
    gem = gemeos_67xx(A)
    buckets = [t for t in A.t.values() if t["bucket"]]
    b_copia = {g for v in gem.values() if v["grupo"] == "copia" for g in v["gemeos"]}
    b_parte = {g for v in gem.values() if v["grupo"] == "parte" for g in v["gemeos"]}

    # E3: cega (v2) ou ancorada (v1)
    e3, anc = prev["E3_auditoria"], prev.get("E3_ancorada")
    if e3.get("cega"):
        e3_desc = (f"Auditoria cega, por um agente de IA com contexto limpo, de {e3['n']:g} publicadas sorteadas fora das 60 da "
                   f"primeira auditoria ([caderno](auditoria_cega_caderno.md), [instruções](../prompts/auditoria_cega.md))")
        e3_hip = (f"Quem primeiro argumenta a favor de outro tema acha os erros visíveis; dúvida conta 1/3 de erro. "
                  f"Resultado: {e3['erros']} erro(s), {e3['duvidosos']} dúvida(s)")
    else:
        e3_desc = f"Auditoria cética, por IA, de 60 publicadas sorteadas, com acesso aos votos ({e3['n']:g} seguem publicadas)"
        e3_hip = "Um leitor cuidadoso acha os erros visíveis; dúvida conta 1/3 de erro. Otimista: a mesma amostra escolheu os limiares"
    e3_anc = f"{p1(anc['taxa'])} nas {anc['n']:g} que seguem publicadas, {anc['duvidosos']} dúvidas e {anc['erros']} erros" if anc else "sem dados"

    sens = [g["precisao"] for g in prev["sensibilidade"]]
    custo_pipe = (sum(met[r]["custo_usd_por_questao_com_cache"] for r in PIPELINE) * len(dec)
                  if all(r in met and met[r]["custo_usd_por_questao_com_cache"] for r in PIPELINE) else None)

    g = diag["grupos"]
    c67 = prev["copias_67xx"]

    # Jev (bloco G): variantes, cascata e desempate auditado (src/50_avaliar_jev.py e src/51_jev_desempate.py)
    jev = json.loads((RAIZ / "runs" / "jev_avaliacao.json").read_text(encoding="utf-8"))
    jdes = json.loads((RAIZ / "runs" / "jev_desempate.json").read_text(encoding="utf-8"))
    jv = {l["rodada"]: l for l in jev["variantes"]}
    casc = next(l for l in jev["cascata"]["limiares"] if l["limiar"] == 0.99)
    jaud = jdes["auditoria"]
    jev_usd = sum(l["usd_total"] for l in jev["variantes"]) + jdes["custo_usd"]
    jev_min = sum(l["segundos"] for l in jev["variantes"]) / 60
    v = {
        "PUB": str(prev["publicadas"]), "COB": p1(prev["cobertura_prevista"]), "PUB2": str(prev["publicadas_nivel2"]),
        "PUB1": str(prev["publicadas"] - prev["publicadas_nivel2"]), "REV": str(c["revisar"]), "FORA": str(c["fora"]),
        "PREC": dec2(prev["precisao_prevista"]), "PREC_LO": dec2(prev["precisao_intervalo"][0]), "PREC_HI": dec2(prev["precisao_intervalo"][1]),
        "PREC_P": p0(prev["precisao_prevista"]), "PREC_LO_P": p0(prev["precisao_intervalo"][0]), "PREC_HI_P": p0(prev["precisao_intervalo"][1]),
        "VAR_PUB": str(prev_sd["publicadas"]), "VAR_COB": p1(prev_sd["cobertura_prevista"]), "VAR_PREC": dec2(prev_sd["precisao_prevista"]),
        "PUB2_SUB": str(prev_sub["publicadas_nivel2"]), "PREC_SUB": dec2(prev_sub["precisao_prevista"]),
        "E1": p1(prev["E1_independencia"]), "E2": f"{prev['E2_outra_familia']['acertos']} de {prev['E2_outra_familia']['n']}",
        "E3": p1(e3["taxa"]), "E3_N": f"{e3['n']:g}", "E3_DESC": e3_desc, "E3_HIP": e3_hip, "E3_ANC": e3_anc,
        "M67": dec2(100 * c67["perda_esperada"]).replace(",00", ""),
        "EXPO": p0(c67["exposicao_copias"]), "EXPO_N": str(c67["n_copias"]),
        "N_COPIAS": str(c67["n_copias"]), "N_PARTES": str(c67["n_partes"]),
        "PREC_67": p0(c67["precisao_se_copias"]), "PREC_67T": p0(c67["precisao_se_todos"]),
        "SENS_MIN": dec2(min(sens)), "SENS_MAX": dec2(max(sens)),
        "N67": str(len(buckets)), "N67_COPIAS": str(len(b_copia)), "N67_PARTES": str(len(b_parte)),
        "N67_PARTES_M1": str(len(b_parte) - 2), "N67_RESTO": str(len(buckets) - len(b_copia) - len(b_parte)),
        "LOO_OPUS": loo_txt("claude-opus"), "LOO_SONNET_P": loo_txt("claude-sonnet-plano"), "LOO_OPUS_H": loo_txt("claude-opus-h"),
        "LOO_SONNET_H": loo_txt("claude-sonnet-h"), "LOO_HAIKU_H": loo_txt("claude-haiku-h"), "LOO_S3N": loo_txt("claude-sonnet-3n"),
        "LOO_HAIKU_3N": loo_txt("claude-haiku-3n"), "LOO_ARB": loo_txt("arbitro-opus"), "LOO_JEV": loo_txt("jev-h-ricos"),
        "TOK_HAIKU_H": tok("claude-haiku-h"), "TOK_S3N": tok("claude-sonnet-3n"), "TOK_HAIKU_3N": tok("claude-haiku-3n"),
        "TOK_ARB": tok("arbitro-opus"), "TOK_JEV": tok("jev-h-ricos"),
        "USD_HAIKU_H": custo("claude-haiku-h"), "USD_S3N": custo("claude-sonnet-3n"), "USD_HAIKU_3N": custo("claude-haiku-3n"),
        "USD_ARB": custo("arbitro-opus"), "USD_JEV": f"{met['jev-h-ricos']['custo_usd_por_questao_com_cache']:.4f}".replace(".", ","),
        "JEV_BASE": p1(jv["jev-h"]["concorda_maioria"]), "JEV_RICOS": p1(jv["jev-h-ricos"]["concorda_maioria"]),
        "JEV_USD_Q": f"{jv['jev-h-ricos']['usd_por_questao']:.4f}".replace(".", ","),
        "JEV_ECE": f"{jev['calibracao']['jev-h-ricos']['ece']:.3f}".replace(".", ","),
        "OPUS_ECE": f"{jev['calibracao']['claude-opus']['ece']:.3f}".replace(".", ","),
        "JEV_CASC_FRAC": p0(casc["fracao"]), "JEV_CASC_N": str(casc["questoes"]),
        "JEV_DES_OK": str(jaud["promovidas"]["ok"]), "JEV_DES_PROM": str(jaud["promovidas"]["n"]),
        "JEV_CTRL_OK": str(jaud["controles"]["ok"]), "JEV_CTRL_N": str(jaud["controles"]["n"]),
        "JEV_CTRL_ERR": str(jaud["controles"]["erro"]),
        "JEV_USD_TOTAL": f"{jev_usd:.2f}".replace(".", ","), "JEV_MIN": f"{jev_min:.0f}",
        "S3N_N": str(met["claude-sonnet-3n"]["questoes"]) if "claude-sonnet-3n" in met else "-",
        "CUSTO_PIPELINE": f"US$ {custo_pipe:.0f}" if custo_pipe else "(custo do árbitro não medido)",
        "CUSTO_PIPELINE_LOTE": f"US$ {custo_pipe / 2:.0f}" if custo_pipe else "-",
        "REV_TAXA": p0(taxa_rev), "FILA_SEMANA": milhar(fila_semana), "FILA_HORAS": milhar(fila_semana / 60),
        "REV_DISCORDAM": str(n_disc), "REV_FRONTEIRA": str(n_front), "REV_MULTI": str(n_multi), "FILA_CASE_H": fila_case,
        "D_ME_U": p0(g["multipla_escolha"]["unanimes"]), "D_ME_P": p0(g["multipla_escolha"]["publicadas"]),
        "D_CE_U": p0(g["certo_errado"]["unanimes"]), "D_CE_P": p0(g["certo_errado"]["publicadas"]),
        "D_MT_U": p0(g["multi"]["unanimes"]), "D_MT_P": p0(g["multi"]["publicadas"]),
        "D_NMT_U": p0(g["nao_multi"]["unanimes"]), "D_NMT_P": p0(g["nao_multi"]["publicadas"]),
        "N_MT": str(g["multi"]["n"]), "N_CE": str(g["certo_errado"]["n"]), "N_ME": str(g["multipla_escolha"]["n"]),
        "PARES": ", ".join(f"{p['titulo_a']} × {p['titulo_b']}" for p in
                           json.loads((RAIZ / "runs" / "pares_confundiveis.json").read_text(encoding="utf-8"))),
    }
    for nome in ("relatorio", "memo_professor"):
        modelo = (RAIZ / "src" / "modelos" / f"{nome}.md").read_text(encoding="utf-8")
        faltando = sorted(set(re.findall(r"«([A-Z0-9_]+)»", modelo)) - set(v))
        if faltando:
            sys.exit(f"{nome}: marcadores sem valor: {faltando}")
        out = re.sub(r"«([A-Z0-9_]+)»", lambda m: v[m.group(1)], modelo)
        (RAIZ / "docs" / f"{nome}.md").write_text(out, encoding="utf-8")
        print(f"docs/{nome}.md gerado;", len(out.split()), "palavras")
    for k in sorted(v):
        print(f"  {k} = {v[k]}")


if __name__ == "__main__":
    main()
