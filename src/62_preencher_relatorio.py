"""Etapa 7: gera docs/relatorio.md a partir do modelo src/modelos/relatorio.md, preenchendo os marcadores «CHAVE»
com os números das saídas (runs/*.json, data/decisoes.jsonl). Assim o relatório nunca fica com números velhos.

Uso: python src/62_preencher_relatorio.py
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import Arvore, RAIZ


def p1(x):
    return f"{100 * x:.1f}".replace(".", ",") + "%"


def p0(x):
    return f"{100 * x:.0f}%"


def dec2(x):
    return f"{x:.2f}".replace(".", ",")


def main():
    A = Arvore()
    prev = json.loads((RAIZ / "runs" / "previsao.json").read_text(encoding="utf-8"))
    prev_sd = json.loads((RAIZ / "runs" / "previsao_sem_duplicados.json").read_text(encoding="utf-8"))
    comp = json.loads((RAIZ / "runs" / "comparacao_metodos.json").read_text(encoding="utf-8"))
    diag = json.loads((RAIZ / "runs" / "diagnostico.json").read_text(encoding="utf-8"))
    dec = [json.loads(l) for l in (RAIZ / "data" / "decisoes.jsonl").open(encoding="utf-8")]
    c = Counter(d["decisao"] for d in dec)
    loo = {l["rodada"]: l for l in comp.get("amostra_2x2", [])}
    met = {l["rodada"]: l for l in comp["metodos"]}

    def loo_txt(r):
        return f"{p1(loo[r]['concorda_maioria_demais'])} (n={loo[r]['n']})" if r in loo else "não concluído"

    g = diag["grupos"]
    v = {
        "PUB": str(prev["publicadas"]), "COB": p1(prev["cobertura_prevista"]), "PUB2": str(prev["publicadas_nivel2"]),
        "PUB1": str(prev["publicadas"] - prev["publicadas_nivel2"]), "REV": str(c["revisar"]), "FORA": str(c["fora"]),
        "PREC": dec2(prev["precisao_prevista"]), "PREC_LO": dec2(prev["precisao_intervalo"][0]), "PREC_HI": dec2(prev["precisao_intervalo"][1]),
        "VAR_PUB": str(prev_sd["publicadas"]), "VAR_COB": p1(prev_sd["cobertura_prevista"]), "VAR_PREC": dec2(prev_sd["precisao_prevista"]),
        "E1": p1(prev["E1_independencia"]), "E2": f"{prev['E2_outra_familia']['acertos']} de {prev['E2_outra_familia']['n']}",
        "E3": p1(prev["E3_auditoria"]["taxa"]), "E3_N": f"{prev['E3_auditoria']['n']:g}",
        "M67": dec2(100 * prev["copias_67xx"]["perda_esperada"]).replace(",00", ""), "EXPO": p0(prev["copias_67xx"]["exposicao"]),
        "EXPO_N": str(round(prev["copias_67xx"]["exposicao"] * prev["publicadas"])),
        "PREC_67": p0(prev["copias_67xx"]["precisao_se_cenario_ocorrer"]),
        "LOO_OPUS": loo_txt("claude-opus"), "LOO_SONNET_P": loo_txt("claude-sonnet-plano"), "LOO_OPUS_H": loo_txt("claude-opus-h"),
        "LOO_SONNET_H": loo_txt("claude-sonnet-h"), "LOO_HAIKU_H": loo_txt("claude-haiku-h"), "LOO_S3N": loo_txt("claude-sonnet-3n"),
        "LOO_HAIKU_3N": loo_txt("claude-haiku-3n"),
        "TOK_HAIKU_H": f"{met['claude-haiku-h']['tokens_prompt_por_questao']:,}".replace(",", ".") if "claude-haiku-h" in met else "-",
        "TOK_S3N": f"{met['claude-sonnet-3n']['tokens_prompt_por_questao']:,}".replace(",", ".") if "claude-sonnet-3n" in met else "-",
        "USD_HAIKU_H": f"{met['claude-haiku-h']['custo_usd_por_questao_com_cache']:.3f}".replace(".", ",") if "claude-haiku-h" in met else "-",
        "USD_S3N": f"{met['claude-sonnet-3n']['custo_usd_por_questao_com_cache']:.3f}".replace(".", ",") if "claude-sonnet-3n" in met else "-",
        "S3N_N": str(met["claude-sonnet-3n"]["questoes"]) if "claude-sonnet-3n" in met else "-",
        "D_ME_U": p0(g["multipla_escolha"]["unanimes"]), "D_ME_P": p0(g["multipla_escolha"]["publicadas"]),
        "D_CE_U": p0(g["certo_errado"]["unanimes"]), "D_CE_P": p0(g["certo_errado"]["publicadas"]),
        "D_MT_U": p0(g["multi"]["unanimes"]), "D_MT_P": p0(g["multi"]["publicadas"]),
        "D_NMT_U": p0(g["nao_multi"]["unanimes"]), "D_NMT_P": p0(g["nao_multi"]["publicadas"]),
        "N_MT": str(g["multi"]["n"]), "N_CE": str(g["certo_errado"]["n"]), "N_ME": str(g["multipla_escolha"]["n"]),
        "PARES": ", ".join(f"{p['titulo_a']} × {p['titulo_b']}" for p in
                           json.loads((RAIZ / "runs" / "pares_confundiveis.json").read_text(encoding="utf-8"))),
    }
    modelo = (RAIZ / "src" / "modelos" / "relatorio.md").read_text(encoding="utf-8")
    faltando = sorted(set(re.findall(r"«([A-Z0-9_]+)»", modelo)) - set(v))
    if faltando:
        sys.exit(f"marcadores sem valor: {faltando}")
    out = re.sub(r"«([A-Z0-9_]+)»", lambda m: v[m.group(1)], modelo)
    (RAIZ / "docs" / "relatorio.md").write_text(out, encoding="utf-8")
    print("docs/relatorio.md gerado;", len(out.split()), "palavras")
    for k in sorted(v):
        print(f"  {k} = {v[k]}")


if __name__ == "__main__":
    main()
