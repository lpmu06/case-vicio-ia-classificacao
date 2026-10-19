"""Etapa 6b: escreve previsao.txt a partir de runs/previsao.json (números) e do texto explicativo.

Uso: python src/61_escrever_previsao.py
"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def pct(x):
    return f"{100 * x:.1f}%"


def main():
    r = json.loads((RAIZ / "runs" / "previsao.json").read_text(encoding="utf-8"))
    lo, hi = r["precisao_intervalo"]
    clo, chi = r["cobertura_intervalo"]
    e2, e3 = r["E2_outra_familia"], r["E3_auditoria"]
    txt = f"""precisao_prevista: {r['precisao_prevista']:.2f}
precisao_intervalo: {lo:.2f}-{hi:.2f}
cobertura_prevista: {r['cobertura_prevista']:.2f}
cobertura_intervalo: {clo:.2f}-{chi:.2f}

COMO CHEGAMOS NESTES NÚMEROS

Cobertura. Ela é escolha nossa: publicamos {r['publicadas']} das {r['total']} questões ({pct(r['cobertura_prevista'])}),
sendo {r['publicadas_nivel2']} no subtema e {r['publicadas'] - r['publicadas_nivel2']} no tema de nível 1. O intervalo só
cobre uma dúvida de denominador: se as questões que a equipe também considera "fora" ({r['fora']} na nossa decisão)
forem excluídas da conta, a cobertura sobe para {pct(chi)}.

Precisão. Não tivemos gabarito nem rotulagem humana. Usamos estimadores independentes, cada um com uma hipótese
declarada, e combinamos de forma conservadora.

1. Dawid-Skene (E1 = {pct(r['E1_independencia'])}). Modelo estatístico que estima a taxa de acerto de cada
   classificador só pelo padrão de concordâncias entre eles (Opus plano, Sonnet em 2 e 3 estágios, árbitro, a origem
   e as rodadas parciais), e dá a probabilidade de o ramo de cada questão estar certo. Supõe erros independentes;
   como todos os classificadores são LLMs e compartilham a mesma taxonomia enriquecida, é um limite SUPERIOR.

2. Outra família de modelo (E2 = {pct(e2['taxa']) if e2['taxa'] is not None else 'n/d'}, {e2['acertos']} de {e2['n']},
   intervalo de 95% {pct(e2['wilson95'][0]) if e2['wilson95'] else 'n/d'}-{pct(e2['wilson95'][1]) if e2['wilson95'] else 'n/d'}).
   O GPT-5.5, de outra empresa, classificou 63 questões antes de acabarem nossos créditos. Medimos, pela régua do
   case, quantas das nossas publicadas ele também colocaria no mesmo nó, pai ou filho. Erros de famílias diferentes
   são menos correlacionados, mas a amostra é pequena.

3. Auditoria (E3 = {pct(e3['taxa']) if e3['taxa'] is not None else 'n/d'}, {e3['pontos']:g} de {e3['n']:g},
   intervalo de 95% {pct(e3['wilson95'][0]) if e3['wilson95'] else 'n/d'}-{pct(e3['wilson95'][1]) if e3['wilson95'] else 'n/d'}).
   Uma amostra aleatória das publicadas foi lida questão a questão com olhar cético, procurando onde um professor
   arquivaria a questão; "duvidoso" contou como meio erro. A leitura foi feita por IA, não por especialista; os
   vereditos estão em data/auditoria_ia.csv e o caderno em docs/auditoria_caderno.md.

4. Margem de convenção ({pct(r['margem_convencao'])}). O professor pode seguir convenções que nenhum modelo conhece:
   onde guarda progressão de regime (Execução Penal ou Teoria da Pena), questões de juizado (Legislação Especial ou
   Procedimento Sumaríssimo), ou se usou os temas duplicados criados em Penal (ids 67xx) em vez dos da Legislação
   Especial, que foi a nossa escolha. Isso não é mensurável sem gabarito, então entra como desconto explícito.

Ponto: a menor das três estimativas menos a margem de convenção.
Intervalo: limite inferior = o menor limite inferior de 95% entre E2 e E3, menos a margem; limite superior = E1.

Por que acreditamos que a precisão fica acima de 95%: só publicamos quando o árbitro e os dois classificadores
principais (métodos e tamanhos de modelo diferentes) concordam no ramo, o árbitro tem confiança de pelo menos 0,80 e
não vê a questão como multi-tema; nos pares de ramos que os modelos confundem entre si exigimos unanimidade; e
publicamos no subtema só com concordância forte, usando o tema de nível 1 nos demais casos, o que pela régua é certo
sempre que o ramo está certo.

O que poderia derrubar a previsão: uma convenção sistemática da equipe diferente da nossa num ramo com muitas
publicadas, ou a equipe ter usado os temas duplicados de Penal. A sensibilidade a cada um está no relatório.
"""
    (RAIZ / "previsao.txt").write_text(txt, encoding="utf-8")
    print(txt)


if __name__ == "__main__":
    main()
