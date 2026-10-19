"""Etapa 6b: escreve previsao.txt a partir de runs/previsao.json (números) e do texto explicativo.

Uso: python src/61_escrever_previsao.py
"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def pct(x):
    return f"{100 * x:.1f}%" if x is not None else "n/d"


def main():
    r = json.loads((RAIZ / "runs" / "previsao.json").read_text(encoding="utf-8"))
    lo, hi = r["precisao_intervalo"]
    clo, chi = r["cobertura_intervalo"]
    e2, e3, anc = r["E2_outra_familia"], r["E3_auditoria"], r.get("E3_ancorada")
    m = r["margem_convencao"]
    c67 = r["copias_67xx"]
    cega = e3.get("cega")
    ic = lambda d, k: (f"intervalo de 95% de {pct(d[k][0])} a {pct(d[k][1])}" if d and d.get(k) else "sem intervalo")

    grade = {}
    for g in r["sensibilidade"]:
        grade.setdefault(g["p_copias"], {})[g["peso_duvida"]] = g["precisao"]
    pesos = sorted(next(iter(grade.values())))
    linhas_grade = ["   p(cópias) / p(nomes de aula)   " + "   ".join(f"dúvida={p:.2f}" for p in pesos)]
    for p_c in sorted(grade):
        linhas_grade.append(f"   {pct(p_c):>6} / {pct(p_c / 2):<6}" + " " * 11 + "   ".join(f"{pct(grade[p_c][p]):>11}" for p in pesos))
    tabela = "\n".join(linhas_grade)

    if cega:
        bloco_e3 = f"""3. Auditoria cega: {pct(e3['taxa'])} (amostra aleatória de {e3['n']:g} publicadas; {e3['erros']} erro(s) e {e3['duvidosos']} dúvida(s)).
   Um agente de IA com contexto limpo, sem acesso aos votos, às confianças ou às justificativas do pipeline, leu
   cada questão com a instrução de primeiro argumentar a favor de OUTRO tema e só depois dar o veredito. A amostra
   não repete nenhuma das 60 questões da primeira auditoria. Uma dúvida genuína conta como {r['peso_duvida']:.2f} de erro na
   estimativa central e como 1/2 na conservadora ({pct(e3['taxa_conservadora'])}; {ic(e3, 'wilson95_conservador')}).
   Vereditos em data/auditoria_ia_v2.csv, caderno em docs/auditoria_cega_caderno.md, instruções em
   prompts/auditoria_cega.md.
   A primeira auditoria (data/auditoria_ia.csv, 60 questões, com acesso aos votos) serviu para escolher os
   limiares de publicação e por isso não entra na estimativa; nas publicadas atuais ela daria {pct(anc['taxa']) if anc else 'n/d'}
   ({anc['n']:g} questões, {anc['duvidosos']} dúvidas, {anc['erros']} erros)."""
    else:
        bloco_e3 = f"""3. Auditoria: {pct(e3['taxa'])} (amostra aleatória de {e3['n']:g} publicadas).
   Cada questão foi lida com olhar cético, perguntando onde um professor a arquivaria. O auditor tinha acesso aos
   votos, e essa mesma amostra serviu para escolher os limiares de publicação: por isso o número é otimista.
   Uma dúvida genuína conta como {r['peso_duvida']:.2f} de erro na estimativa central e como 1/2 na conservadora
   ({pct(e3['taxa_conservadora'])}; {ic(e3, 'wilson95_conservador')}). Vereditos em data/auditoria_ia.csv."""

    txt = f"""precisao_prevista: {r['precisao_prevista']:.2f}
precisao_intervalo: {lo:.2f}-{hi:.2f}
cobertura_prevista: {r['cobertura_prevista']:.2f}
cobertura_intervalo: {clo:.2f}-{chi:.2f}

COMO CHEGAMOS NESTES NÚMEROS

Cobertura
Ela é escolha nossa: publicamos {r['publicadas']} das {r['total']} questões ({pct(r['cobertura_prevista'])}), todas no tema de
nível 1 ({r['publicadas_nivel2']} no subtema). O intervalo só cobre uma dúvida de denominador: se as questões que a equipe
também considera "fora" ({r['fora']} na nossa decisão) saírem da conta, a cobertura sobe para {pct(chi)}.

Precisão
Não tivemos gabarito nem rotulagem humana. Usamos três estimadores com fontes de erro diferentes, cada um com uma
hipótese declarada, e dois descontos para o que nenhum deles enxerga. Eles não são independentes: os
classificadores são todos da mesma família (Claude), e a taxonomia enriquecida que todos leram foi escrita pelo
GPT-5.5, que é também o modelo da outra família. Por isso combinamos de forma conservadora.

1. Dawid-Skene: {pct(r['E1_independencia'])}.
   Modelo estatístico que estima a taxa de acerto de cada classificador só pelo padrão de concordâncias entre eles
   (Opus plano, Sonnet em 2 e 3 estágios, as rodadas parciais de Sonnet, Opus, Haiku e GPT, e a classificação de
   origem; o árbitro fica de fora, porque escolhe entre os candidatos desses mesmos classificadores) e dá a
   probabilidade de o ramo de cada questão estar certo. Supõe erros independentes, e as publicadas são justamente as
   questões em que todos concordam: é um teto do modelo. Entra só como limite superior do intervalo, não no ponto.

2. Outra família de modelo: {pct(e2['taxa'])} ({e2['acertos']} de {e2['n']}; {ic(e2, 'wilson95')}).
   O GPT-5.5, de outra empresa, classificou 63 questões antes de acabarem nossos créditos. Medimos quantas das
   nossas publicadas ele colocaria no mesmo tema, pai ou filho, pela régua do case. Erros de famílias diferentes
   são menos correlacionados, mas a amostra é pequena e ele também não conhece as convenções da equipe.

{bloco_e3}

4. Margem de convenção ({pct(m)}, descontada de 1 e 2; a auditoria já a embute, porque conta as dúvidas).
   O professor pode seguir convenções que nenhum modelo conhece. As auditorias mostraram onde: assuntos com dois
   endereços na árvore (prisão em "Prisões em Espécie" ou em "Teoria Geral das Prisões"; ação penal e decadência
   em Penal ou em Processo Penal) e fronteiras de teoria do crime (erro de tipo ou de proibição).

5. Gêmeos 67xx ({pct(c67['perda_esperada'])} de perda esperada, descontada de todos).
   A árvore tem 20 temas recentes, ids 67xx, sem descrição nem histórico, que nunca usamos. {c67['n_copias']} publicadas
   estão em temas que têm uma cópia 67xx de título idêntico em outra disciplina (Lei Maria da Penha, Tráfico de
   Drogas, Lei de Execução Penal...), e {c67['n_partes']} em temas que têm um gêmeo com nome de aula, "X (Parte N)"
   (Teoria da Pena, Crimes contra o Patrimônio, Competência...). Se a equipe rotular nesses gêmeos, as nossas
   publicadas nesses temas contam como erro pela régua. Atribuímos {pct(c67['p_copias'])} de chance ao uso das cópias (quem
   rotula à mão vê dois títulos iguais) e {pct(c67['p_partes'])} ao dos nomes de aula (um nome de aula diz pouco a quem
   arquiva). Se só as cópias forem usadas, a precisão cai para cerca de {pct(c67['precisao_se_copias'])}; se os dois grupos,
   para {pct(c67['precisao_se_todos'])}. A variante publicacao_sem_duplicados.csv manda essas questões para revisão e
   elimina o risco, ao custo de cerca de 25 pontos de cobertura.

Ponto: a média dos dois estimadores que não supõem independência, ajustados ({', '.join(pct(x) for x in r['estimadores_ajustados'])}).
Intervalo: limite inferior = o menor limite inferior de 95% entre 2 e 3, menos o item 5; limite superior = o teto
de independência (1), limitado pelo limite superior da auditoria. O intervalo é largo porque a auditoria e a outra
família têm poucas dezenas de questões; preferimos um intervalo honesto a um estreito.

Sensibilidade do ponto às duas hipóteses que não podemos medir (chance de a equipe usar os gêmeos 67xx e peso de
uma dúvida da auditoria como erro):
{tabela}

Por que esperamos ficar acima de 95%
Só publicamos quando o árbitro e os dois classificadores principais, de métodos e tamanhos diferentes, concordam
no ramo, o árbitro tem confiança de pelo menos 0,90 e não vê a questão como multi-tema. Nos pares de ramos que os
modelos confundem entre si exigimos que todas as rodadas completas concordem. Publicamos sempre no tema de nível 1,
que pela régua está certo sempre que o ramo está certo. Os limiares (0,90) foram escolhidos com a primeira
auditoria e com a análise de sensibilidade (docs/sensibilidade.md).

O que poderia derrubar a previsão
O uso dos gêmeos 67xx pela equipe (item 5) ou uma convenção sistemática diferente da nossa num ramo com muitas
publicadas. A entrega está toda no tema de nível 1, o que elimina o risco de subtema irmão; a variante
publicacao_subtema.csv mostra o que a versão híbrida faria.
"""
    (RAIZ / "previsao.txt").write_text(txt, encoding="utf-8")
    print(txt)


if __name__ == "__main__":
    main()
