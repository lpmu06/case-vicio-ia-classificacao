# Comparação de métodos e modelos

Gerado por `src/42_comparar_metodos.py`. Tokens de prompt reconstruídos a partir dos prompts reais e das saídas intermediárias gravadas, sem o contexto fixo do Claude Code; razão caracteres/token medida neste corpus (`runs/calibracao_tokens.json`). Custos a preço de lista da API; "com cache" supõe o system prompt lido do cache (as rodadas reais foram feitas pela assinatura, sem custo marginal).

| Rodada | Método | Modelo | Questões | Chamadas/q | Tokens prompt/q | Tokens saída/q | US$/q sem cache | US$/q com cache | US$ 50 mil q (cache) | Fora | Multi | Escolheu subtema | Conf. ramo média |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| claude-opus | plano | Opus 5.5 | 359 | 1.0 | 211,517 | 508 | 0.85623 | 0.05418 | 2709 | 2 | 62 | 210 | 0.8 |
| claude-sonnet-h | 2 estágios | Sonnet 5 | 359 | 1.99 | 20,790 | 1,589 | 0.05747 | 0.03145 | 1572 | 4 | 95 | 204 | 0.911 |
| claude-sonnet-3n | 3 estágios | Sonnet 5 | 359 | 2.98 | 13,935 | 2,083 | 0.0487 | 0.03936 | 1968 | 4 | 106 | 189 | 0.899 |
| claude-haiku-h | 2 estágios | Haiku 4.5 | 91 | 2.0 | 16,525 | 6,941 | 0.05123 | 0.04088 | 2044 | 0 | 13 | 62 | 0.946 |
| claude-haiku-3n | 3 estágios | Haiku 4.5 | 44 | 3.0 | 10,754 | 8,863 | 0.05507 | 0.05135 | 2567 | 0 | 4 | 26 | 0.955 |
| gpt-5.5 | plano | GPT-5.5 (parcial) | 63 | 1.0 | 131,352 | 589 | None | None | None | 0 | 11 | 39 | 0.922 |
| claude-sonnet-plano | plano | Sonnet 5 (amostra 80) | 80 | 1.0 | 211,517 | 717 | 0.4302 | 0.05028 | 2514 | 0 | 19 | 61 | 0.872 |
| claude-opus-h | 2 estágios | Opus 5.5 (amostra 80) | 80 | 2.0 | 22,460 | 1,176 | 0.11335 | 0.05837 | 2919 | 0 | 10 | 50 | 0.871 |
| jev-h-ricos | Jev | Jev 1.13, critérios ricos | 359 | 1.76 | 31,564 | 0 | 0.00133 | 0.00133 | 66 | 2 | 0 | 218 | 0.852 |
| arbitro-opus | árbitro | Opus 5.5, esforço alto | 359 | 1.0 | 19,246 | 720 | 0.09138 | 0.04075 | 2037 | 2 | 44 | 192 | 0.861 |

## Concordância par a par

| A | B | n | Mesmo ramo | n (ambos escolheram subtema) | Mesmo subtema quando ambos escolhem |
|---|---|---|---|---|---|
| claude-opus | claude-sonnet-h | 359 | 88.6% | 183 | 91.8% |
| claude-opus | claude-sonnet-3n | 359 | 84.7% | 170 | 91.2% |
| claude-opus | claude-haiku-h | 91 | 90.1% | 58 | 87.9% |
| claude-opus | claude-haiku-3n | 44 | 86.4% | 26 | 88.5% |
| claude-opus | gpt-5.5 | 63 | 98.4% | 37 | 97.3% |
| claude-opus | claude-sonnet-plano | 80 | 90.0% | 55 | 87.3% |
| claude-opus | claude-opus-h | 80 | 96.3% | 50 | 100.0% |
| claude-opus | jev-h-ricos | 359 | 85.2% | 188 | 84.6% |
| claude-opus | arbitro-opus | 359 | 97.8% | 191 | 99.0% |
| claude-sonnet-h | claude-sonnet-3n | 359 | 85.8% | 175 | 92.0% |
| claude-sonnet-h | claude-haiku-h | 91 | 90.1% | 54 | 92.6% |
| claude-sonnet-h | claude-haiku-3n | 44 | 88.6% | 23 | 91.3% |
| claude-sonnet-h | gpt-5.5 | 63 | 88.9% | 33 | 90.9% |
| claude-sonnet-h | claude-sonnet-plano | 80 | 91.2% | 51 | 92.2% |
| claude-sonnet-h | claude-opus-h | 80 | 91.2% | 46 | 95.7% |
| claude-sonnet-h | jev-h-ricos | 359 | 79.4% | 177 | 80.8% |
| claude-sonnet-h | arbitro-opus | 359 | 90.3% | 174 | 93.1% |
| claude-sonnet-3n | claude-haiku-h | 91 | 85.7% | 50 | 90.0% |
| claude-sonnet-3n | claude-haiku-3n | 44 | 93.2% | 22 | 90.9% |
| claude-sonnet-3n | gpt-5.5 | 63 | 79.4% | 28 | 85.7% |
| claude-sonnet-3n | claude-sonnet-plano | 80 | 86.3% | 48 | 93.8% |
| claude-sonnet-3n | claude-opus-h | 80 | 90.0% | 43 | 97.7% |
| claude-sonnet-3n | jev-h-ricos | 359 | 79.7% | 167 | 81.4% |
| claude-sonnet-3n | arbitro-opus | 359 | 85.0% | 163 | 90.8% |
| claude-haiku-h | claude-haiku-3n | 44 | 88.6% | 25 | 96.0% |
| claude-haiku-h | gpt-5.5 | 22 | 95.5% | 12 | 91.7% |
| claude-haiku-h | claude-sonnet-plano | 80 | 92.5% | 53 | 88.7% |
| claude-haiku-h | claude-opus-h | 80 | 87.5% | 47 | 91.5% |
| claude-haiku-h | jev-h-ricos | 91 | 86.8% | 59 | 88.1% |
| claude-haiku-h | arbitro-opus | 91 | 90.1% | 54 | 90.7% |
| claude-haiku-3n | gpt-5.5 | 14 | 92.9% | 7 | 100.0% |
| claude-haiku-3n | claude-sonnet-plano | 40 | 82.5% | 24 | 83.3% |
| claude-haiku-3n | claude-opus-h | 40 | 87.5% | 23 | 91.3% |
| claude-haiku-3n | jev-h-ricos | 44 | 88.6% | 25 | 88.0% |
| claude-haiku-3n | arbitro-opus | 44 | 88.6% | 25 | 88.0% |
| gpt-5.5 | claude-sonnet-plano | 13 | 92.3% | 10 | 70.0% |
| gpt-5.5 | claude-opus-h | 13 | 84.6% | 7 | 100.0% |
| gpt-5.5 | jev-h-ricos | 63 | 82.5% | 33 | 69.7% |
| gpt-5.5 | arbitro-opus | 63 | 96.8% | 33 | 97.0% |
| claude-sonnet-plano | claude-opus-h | 80 | 87.5% | 50 | 92.0% |
| claude-sonnet-plano | jev-h-ricos | 80 | 87.5% | 53 | 88.7% |
| claude-sonnet-plano | arbitro-opus | 80 | 88.7% | 51 | 90.2% |
| claude-opus-h | jev-h-ricos | 80 | 90.0% | 48 | 91.7% |
| claude-opus-h | arbitro-opus | 80 | 95.0% | 48 | 97.9% |
| jev-h-ricos | arbitro-opus | 359 | 85.2% | 177 | 85.9% |

## Concordância com a classificação de origem (só onde a origem tem um tema correspondente)

| Rodada | n | Mesmo ramo da origem |
|---|---|---|
| claude-opus | 225 | 29.8% |
| claude-sonnet-h | 225 | 31.6% |
| claude-sonnet-3n | 225 | 33.8% |
| claude-haiku-h | 55 | 32.7% |
| claude-haiku-3n | 30 | 30.0% |
| gpt-5.5 | 44 | 22.7% |
| claude-sonnet-plano | 47 | 29.8% |
| claude-opus-h | 47 | 29.8% |
| jev-h-ricos | 225 | 27.1% |
| arbitro-opus | 225 | 29.3% |

## Experimento 2×2 nas 80 questões sorteadas

Cada rodada comparada com a maioria das demais rodadas e do árbitro, excluindo a própria (leave-one-out). Não é acurácia; é o quanto a rodada acompanha o consenso dos outros.

| Rodada | Método | Modelo | n | Concorda com a maioria dos demais | Tokens prompt/q | Tokens saída/q | US$/q com cache |
|---|---|---|---|---|---|---|---|
| arbitro-opus | árbitro | Opus 5.5, esforço alto | 80 | 96.3% | 19,246 | 720 | 0.04075 |
| claude-opus | plano | Opus 5.5 | 80 | 93.8% | 211,517 | 508 | 0.05418 |
| claude-sonnet-h | 2 estágios | Sonnet 5 | 80 | 93.8% | 20,790 | 1,589 | 0.03145 |
| claude-opus-h | 2 estágios | Opus 5.5 (amostra 80) | 80 | 93.8% | 22,460 | 1,176 | 0.05837 |
| claude-haiku-h | 2 estágios | Haiku 4.5 | 80 | 90.0% | 16,525 | 6,941 | 0.04088 |
| claude-sonnet-plano | plano | Sonnet 5 (amostra 80) | 80 | 90.0% | 211,517 | 717 | 0.05028 |
| claude-sonnet-3n | 3 estágios | Sonnet 5 | 80 | 88.7% | 13,935 | 2,083 | 0.03936 |
| jev-h-ricos | Jev | Jev 1.13, critérios ricos | 80 | 88.7% | 31,564 | 0 | 0.00133 |
| claude-haiku-3n | 3 estágios | Haiku 4.5 | 40 | 87.5% | 10,754 | 8,863 | 0.05135 |
