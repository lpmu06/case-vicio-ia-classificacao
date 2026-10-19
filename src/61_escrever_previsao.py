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
    e2, e3 = r["E2_outra_familia"], r["E3_auditoria"]
    m = r["margem_convencao"]
    c67 = r["copias_67xx"]
    txt = f"""precisao_prevista: {r['precisao_prevista']:.2f}
precisao_intervalo: {lo:.2f}-{hi:.2f}
cobertura_prevista: {r['cobertura_prevista']:.2f}
cobertura_intervalo: {clo:.2f}-{chi:.2f}

COMO CHEGAMOS NESTES NÚMEROS

Cobertura
Ela é escolha nossa: publicamos {r['publicadas']} das {r['total']} questões ({pct(r['cobertura_prevista'])}), sendo
{r['publicadas_nivel2']} no subtema e {r['publicadas'] - r['publicadas_nivel2']} no tema de nível 1. O intervalo só cobre uma dúvida
de denominador: se as questões que a equipe também considera "fora" ({r['fora']} na nossa decisão) saírem da conta,
a cobertura sobe para {pct(chi)}.

Precisão
Não tivemos gabarito nem rotulagem humana. Usamos três estimadores independentes entre si, cada um com uma
hipótese declarada, e dois descontos para o que nenhum deles enxerga.

1. Dawid-Skene: {pct(r['E1_independencia'])}.
   Modelo estatístico que estima a taxa de acerto de cada classificador só pelo padrão de concordâncias entre eles
   (Opus plano, Sonnet em 2 e 3 estágios, árbitro, rodadas parciais e a classificação de origem) e dá a
   probabilidade de o ramo de cada questão estar certo. Supõe erros independentes. Como todos são LLMs que leram a
   mesma taxonomia, é um limite superior.

2. Outra família de modelo: {pct(e2['taxa'])} ({e2['acertos']} de {e2['n']}; intervalo de 95% de {pct(e2['wilson95'][0] if e2['wilson95'] else None)} a {pct(e2['wilson95'][1] if e2['wilson95'] else None)}).
   O GPT-5.5, de outra empresa, classificou 63 questões antes de acabarem nossos créditos. Medimos quantas das
   nossas publicadas ele colocaria no mesmo tema, pai ou filho, pela régua do case. Erros de famílias diferentes
   são menos correlacionados, mas a amostra é pequena e ele também não conhece as convenções da equipe.

3. Auditoria: {pct(e3['taxa'])} (amostra aleatória de {e3['n']:g} publicadas).
   Cada questão foi lida com olhar cético, perguntando onde um professor a arquivaria. Nenhum erro claro; as
   dúvidas genuínas (um tema alternativo plausível por convenção) contam como 1/3 de erro na estimativa central e
   como 1/2 na conservadora ({pct(e3['taxa_conservadora'])}; intervalo de 95% de {pct(e3['wilson95_conservador'][0] if e3['wilson95_conservador'] else None)} a {pct(e3['wilson95_conservador'][1] if e3['wilson95_conservador'] else None)}).
   A leitura foi feita por IA, não por especialista. Vereditos em data/auditoria_ia.csv, caderno em
   docs/auditoria_caderno.md.

4. Margem de convenção ({pct(m)}, descontada de 1 e 2).
   O professor pode seguir convenções que nenhum modelo conhece. A auditoria mostrou onde: assuntos com dois
   endereços na árvore (prisão em "Prisões em Espécie" ou em "Teoria Geral das Prisões"; ação penal e decadência
   em Penal ou em Processo Penal) e fronteiras de teoria do crime (erro de tipo ou de proibição).

5. Cópias dos temas da Legislação Especial ({pct(c67['perda_esperada'])} de perda esperada, descontada de todos).
   A árvore tem cópias recentes, em Penal e em Processo Penal, de 8 temas da Legislação Especial (Lei Maria da
   Penha, Tráfico de Drogas, Lei de Execução Penal...). Publicamos sempre no tema da Legislação Especial, que tem
   histórico de questões; as cópias não têm descrição nem histórico. Se a equipe tiver rotulado nas cópias,
   {pct(c67['exposicao'])} das publicadas estariam erradas e a precisão cairia para cerca de {pct(c67['precisao_se_cenario_ocorrer'])}.
   Atribuímos {pct(c67['p_cenario'])} de chance a esse cenário. A variante publicacao_sem_duplicados.csv manda essas
   questões para revisão e elimina o risco, ao custo de cerca de 10 pontos de cobertura.

Ponto: a mediana dos três estimadores ajustados ({', '.join(pct(x) for x in r['estimadores_ajustados'])}).
Intervalo: limite inferior = o menor limite inferior de 95% entre 2 e 3, menos o item 5; limite superior = 1,
a estimativa sob independência. O intervalo é largo porque a auditoria e a outra família têm poucas dezenas de
questões; preferimos um intervalo honesto a um estreito.

Por que esperamos ficar acima de 95%
Só publicamos quando o árbitro e os dois classificadores principais, de métodos e tamanhos diferentes, concordam
no ramo, o árbitro tem confiança de pelo menos 0,90 e não vê a questão como multi-tema. Nos pares de ramos que os
modelos confundem entre si exigimos unanimidade. Publicamos no subtema só com concordância forte e confiança de pelo
menos 0,90; nos demais casos, no tema de nível 1, que pela régua está certo sempre que o ramo está certo.

O que poderia derrubar a previsão
O uso das cópias da Legislação Especial pela equipe (item 5) ou uma convenção sistemática diferente da nossa num
ramo com muitas publicadas. A entrega está toda no tema de nível 1, o que elimina o risco de subtema irmão; a
variante publicacao_subtema.csv mostra o que a versão híbrida faria. A sensibilidade aos limiares está em
docs/sensibilidade.md.
"""
    (RAIZ / "previsao.txt").write_text(txt, encoding="utf-8")
    print(txt)


if __name__ == "__main__":
    main()
