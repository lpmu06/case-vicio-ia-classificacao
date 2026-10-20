# Jev (TypeSafe) como classificador adicional

Gerado por `src/50_avaliar_jev.py` a partir de `runs/jev-h*/`. Sem gabarito: "concorda" é concordância de ramo (tema de nível 1) com a maioria das rodadas de Claude/GPT e do árbitro, que não usam o Jev. O "trio unânime" são as 317 questões em que Opus plano, Sonnet 2 estágios e o árbitro escolheram o mesmo ramo, o subconjunto com rótulo mais confiável. As cinco variantes rodaram nas 359 questões e mudam um fator por vez em relação à base; como a melhor é escolhida e medida nos mesmos dados, diferenças de um ou dois pontos são indicação, não prova.

## Variantes

| Variante | Modelo | Concorda com a maioria (359) | Trio unânime | Amostra 80 | ECE | Escolheu subtema | Subtema = Opus (quando ambos) | Chamadas/q | Tokens/q | US$ total (359) | US$ 50 mil q | Segundos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base (jev-latest 1.13, critérios curtos, guloso) | jev-1.13.0 | 79.7% | 83.6% | 76.2% | 0.043 | 206 | 75.7% | 1.76 | 10,888 | 0.164 | 23 | 23 |
| jev-preview (1.14) | jev-1.14.0 | 79.1% | 82.0% | 76.2% | 0.062 | 204 | 74.3% | 1.75 | 10,885 | 0.164 | 23 | 27 |
| critérios ricos | jev-1.13.0 | 85.8% | 87.7% | 88.7% | 0.014 | 218 | 84.6% | 1.76 | 31,564 | 0.476 | 66 | 30 |
| beam search K=3 | jev-1.13.0 | 78.6% | 83.0% | 73.8% | 0.051 | 209 | 75.7% | 2.74 | 12,032 | 0.181 | 25 | 34 |
| 5 ordens embaralhadas | jev-1.13.0 | 78.3% | 81.4% | 75.0% | 0.036 | 207 | 73.2% | 8.72 | 54,345 | 0.819 | 114 | 118 |

Preço de lista da TypeSafe em 19/10/2026: US$ 0,042 por milhão de tokens de entrada, saída grátis. Tokens são os devolvidos pela API, não estimados.

## Calibração

Concordância com a maioria por faixa da probabilidade que o classificador deu ao ramo escolhido. No Jev é a probabilidade do modelo; no Opus, no Sonnet e no árbitro é a confiança que o modelo declara no JSON (para eles a maioria exclui a própria rodada). ECE = média ponderada de |concordância − probabilidade| nas faixas.

| Classificador | Faixa | n | Probabilidade média | Concordância |
|---|---|---|---|---|
| jev-h | 0.00–0.50 | 42 | 0.40 | 38.1% |
| jev-h | 0.50–0.70 | 57 | 0.60 | 64.9% |
| jev-h | 0.70–0.90 | 55 | 0.79 | 76.4% |
| jev-h | 0.90–0.99 | 71 | 0.95 | 88.7% |
| jev-h | 0.99–1.00 | 134 | 1.00 | 95.5% |
| jev-h-preview | 0.00–0.50 | 41 | 0.39 | 48.8% |
| jev-h-preview | 0.50–0.70 | 64 | 0.58 | 65.6% |
| jev-h-preview | 0.70–0.90 | 69 | 0.80 | 71.0% |
| jev-h-preview | 0.90–0.99 | 85 | 0.95 | 91.8% |
| jev-h-preview | 0.99–1.00 | 100 | 1.00 | 95.0% |
| jev-h-ricos | 0.00–0.50 | 22 | 0.39 | 50.0% |
| jev-h-ricos | 0.50–0.70 | 58 | 0.59 | 60.3% |
| jev-h-ricos | 0.70–0.90 | 66 | 0.81 | 81.8% |
| jev-h-ricos | 0.90–0.99 | 73 | 0.95 | 93.2% |
| jev-h-ricos | 0.99–1.00 | 140 | 1.00 | 100.0% |
| jev-h-beam3 | 0.00–0.50 | 43 | 0.39 | 34.9% |
| jev-h-beam3 | 0.50–0.70 | 59 | 0.60 | 64.4% |
| jev-h-beam3 | 0.70–0.90 | 50 | 0.80 | 72.0% |
| jev-h-beam3 | 0.90–0.99 | 74 | 0.95 | 89.2% |
| jev-h-beam3 | 0.99–1.00 | 133 | 1.00 | 95.5% |
| jev-h-ordens5 | 0.00–0.50 | 46 | 0.40 | 39.1% |
| jev-h-ordens5 | 0.50–0.70 | 55 | 0.60 | 54.5% |
| jev-h-ordens5 | 0.70–0.90 | 60 | 0.80 | 76.7% |
| jev-h-ordens5 | 0.90–0.99 | 75 | 0.95 | 93.3% |
| jev-h-ordens5 | 0.99–1.00 | 123 | 1.00 | 95.1% |
| claude-opus | 0.00–0.50 | 20 | 0.40 | 70.0% |
| claude-opus | 0.50–0.70 | 67 | 0.56 | 82.1% |
| claude-opus | 0.70–0.90 | 110 | 0.82 | 98.2% |
| claude-opus | 0.90–0.99 | 162 | 0.94 | 100.0% |
| claude-sonnet-h | 0.00–0.50 | 6 | 0.44 | 83.3% |
| claude-sonnet-h | 0.50–0.70 | 16 | 0.58 | 68.8% |
| claude-sonnet-h | 0.70–0.90 | 48 | 0.79 | 79.2% |
| claude-sonnet-h | 0.90–0.99 | 282 | 0.96 | 92.6% |
| claude-sonnet-h | 0.99–1.00 | 7 | 0.99 | 100.0% |
| arbitro-opus | 0.00–0.50 | 8 | 0.43 | 62.5% |
| arbitro-opus | 0.50–0.70 | 46 | 0.58 | 71.7% |
| arbitro-opus | 0.70–0.90 | 79 | 0.81 | 97.5% |
| arbitro-opus | 0.90–0.99 | 226 | 0.95 | 100.0% |

| Classificador | ECE |
|---|---|
| jev-h | 0.043 |
| jev-h-preview | 0.062 |
| jev-h-ricos | 0.014 |
| jev-h-beam3 | 0.051 |
| jev-h-ordens5 | 0.036 |
| claude-opus | 0.144 |
| claude-sonnet-h | 0.038 |
| arbitro-opus | 0.089 |

## Ruído entre requisições idênticas

O Jev não é determinístico: a mesma requisição devolve probabilidades um pouco diferentes. O estágio 1 do beam e a primeira das 5 ordens são requisições idênticas às da base, o que dá réplicas sem custo extra.

- `base_vs_reexecucao_mesmo_ramo`: 96.7%
- `dif_media_prob_topo`: 0.017
- `dif_max_prob_topo`: 0.130
- `base_vs_primeira_ordem_mesmo_ramo`: 98.1%

## Beam search

O beam trocou o ramo do guloso em 9 questões: em 3 passou a concordar com a maioria e em 4 deixou de concordar.

## Viés de ordem das opções

Com as 89 opções em 5 ordens diferentes, a escolha do estágio 1 mudou com a ordem em 57 das 359 questões; a média das 5 escolheu um ramo diferente da ordem original em 26.

## Comparação pareada com a base

Nas mesmas questões, quantas só a variante acerta (concorda com a maioria) e quantas só a base acerta. As que ambas acertam ou ambas erram não distinguem as duas. Para comparação: duas execuções idênticas da base discordam de ramo em 3.3% das questões.

| Variante | Só a variante concorda | Só a base concorda |
|---|---|---|
| jev-h-preview | 11 | 13 |
| jev-h-ricos | 33 | 11 |
| jev-h-beam3 | 3 | 7 |
| jev-h-ordens5 | 8 | 13 |

## Cascata: o Jev decide sozinho acima de um limiar (jev-h-ricos)

Questões em que a probabilidade do ramo escolhido pelo Jev passa do limiar e a concordância delas com a maioria e com o trio unânime. O resto seguiria para os modelos de linguagem.

| Limiar | Questões | Fração | Concorda com a maioria | n no trio unânime | Concorda com o trio |
|---|---|---|---|---|---|
| 0.999 | 119 | 33.1% | 100.0% | 118 | 100.0% |
| 0.99 | 140 | 39.0% | 100.0% | 137 | 100.0% |
| 0.95 | 187 | 52.1% | 98.9% | 182 | 98.9% |
| 0.9 | 213 | 59.3% | 97.7% | 204 | 98.0% |
| 0.8 | 257 | 71.6% | 94.6% | 240 | 95.4% |

## Camada final de desempate (src/51_jev_desempate.py)

Nas 140 questões que a regra mandou para revisão, o Jev escolheu só entre os ramos candidatos (2 a 4 em 119 delas), com descrições inteiras e duas ordens. Regra fixada antes da auditoria: promover quando a escolha é o ramo do árbitro com probabilidade ≥ 0.90. Escolha igual à do árbitro em 80; 39 promovidas; custo US$ 0.016.

Validação por auditoria cega com controles: as promovidas misturadas com publicadas que nenhuma auditoria viu, em dois cadernos embaralhados, dois auditores (subagentes Opus com contexto limpo) que não sabiam quais eram quais.

| Grupo | n | ok | duvidoso | erro | ok (IC 95%) |
|---|---|---|---|---|---|
| Promovidas pelo Jev | 39 | 26 | 12 | 1 | 66.7% (51%–79%) |
| Controles (publicadas) | 40 | 39 | 1 | 0 | 97.5% (87%–100%) |

As dúvidas das promovidas são de convenção (assunto com dois endereços na árvore) ou de questões que misturam temas: o que a regra mandou para revisão é ambiguidade real, que o acordo entre Jev e árbitro não resolve. A calibração medida nas 359 não vale no subconjunto difícil. Desempate descartado.
