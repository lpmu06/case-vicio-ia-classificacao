# Comparação de métodos e modelos

Gerado por `src/42_comparar_metodos.py`. Tokens de prompt reconstruídos a partir dos prompts reais e das saídas intermediárias gravadas, sem o contexto fixo do Claude Code; razão caracteres/token medida neste corpus (`runs/calibracao_tokens.json`). Custos a preço de lista da API; "com cache" supõe o system prompt lido do cache (as rodadas reais foram feitas pela assinatura, sem custo marginal).

| Rodada | Método | Modelo | Questões | Chamadas/q | Tokens prompt/q | Tokens saída/q | US$/q sem cache | US$/q com cache | US$ 50 mil q (cache) | Fora | Multi | Escolheu subtema | Conf. ramo média |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| claude-opus | plano | Opus 5.5 | 359 | 1.0 | 211,517 | 508 | 0.85623 | 0.05418 | 2709 | 2 | 62 | 210 | 0.8 |
| claude-sonnet-h | 2 estágios | Sonnet 5 | 359 | 1.99 | 20,790 | 1,589 | 0.05747 | 0.03145 | 1572 | 4 | 95 | 204 | 0.911 |
| claude-sonnet-3n | 3 estágios | Sonnet 5 | 218 | 2.97 | 13,671 | 2,003 | 0.04737 | 0.03806 | 1903 | 4 | 51 | 115 | 0.909 |
| claude-haiku-h | 2 estágios | Haiku 4.5 | 21 | 2.0 | 16,384 | 6,318 | 0.04798 | 0.03763 | 1881 | 0 | 2 | 15 | 0.97 |
| claude-haiku-3n | 3 estágios | Haiku 4.5 | 6 | 3.0 | 11,182 | 12,252 | 0.07244 | 0.06872 | 3436 | 0 | 0 | 3 | 0.962 |
| gpt-5.5 | plano | GPT-5.5 (parcial) | 63 | 1.0 | 131,352 | 589 | None | None | None | 0 | 11 | 39 | 0.922 |
| claude-sonnet-plano | plano | Sonnet 5 (amostra 80) | 80 | 1.0 | 211,517 | 717 | 0.4302 | 0.05028 | 2514 | 0 | 19 | 61 | 0.872 |
| claude-opus-h | 2 estágios | Opus 5.5 (amostra 80) | 73 | 2.0 | 22,612 | 1,186 | 0.11417 | 0.05918 | 2959 | 0 | 10 | 48 | 0.869 |

## Concordância par a par

| A | B | n | Mesmo ramo | n (ambos escolheram subtema) | Mesmo subtema quando ambos escolhem |
|---|---|---|---|---|---|
| claude-opus | claude-sonnet-h | 359 | 88.6% | 183 | 91.8% |
| claude-opus | claude-sonnet-3n | 218 | 83.0% | 103 | 92.2% |
| claude-opus | claude-haiku-h | 21 | 95.2% | 15 | 93.3% |
| claude-opus | claude-haiku-3n | 6 | 100.0% | 3 | 66.7% |
| claude-opus | gpt-5.5 | 63 | 98.4% | 37 | 97.3% |
| claude-opus | claude-sonnet-plano | 80 | 90.0% | 55 | 87.3% |
| claude-opus | claude-opus-h | 73 | 97.3% | 48 | 100.0% |
| claude-sonnet-h | claude-sonnet-3n | 218 | 87.2% | 108 | 92.6% |
| claude-sonnet-h | claude-haiku-h | 21 | 95.2% | 12 | 100.0% |
| claude-sonnet-h | claude-haiku-3n | 6 | 100.0% | 2 | 100.0% |
| claude-sonnet-h | gpt-5.5 | 63 | 88.9% | 33 | 90.9% |
| claude-sonnet-h | claude-sonnet-plano | 80 | 91.2% | 51 | 92.2% |
| claude-sonnet-h | claude-opus-h | 73 | 91.8% | 44 | 95.5% |
| claude-sonnet-3n | claude-haiku-h | 21 | 90.5% | 10 | 100.0% |
| claude-sonnet-3n | claude-haiku-3n | 6 | 100.0% | 2 | 100.0% |
| claude-sonnet-3n | gpt-5.5 | 46 | 80.4% | 22 | 86.4% |
| claude-sonnet-3n | claude-sonnet-plano | 38 | 84.2% | 23 | 87.0% |
| claude-sonnet-3n | claude-opus-h | 38 | 86.8% | 20 | 95.0% |
| claude-haiku-h | claude-haiku-3n | 6 | 100.0% | 3 | 100.0% |
| claude-haiku-h | gpt-5.5 | 13 | 100.0% | 6 | 100.0% |
| claude-haiku-h | claude-sonnet-plano | 10 | 100.0% | 8 | 100.0% |
| claude-haiku-h | claude-opus-h | 10 | 100.0% | 8 | 100.0% |
| claude-haiku-3n | gpt-5.5 | 6 | 100.0% | 2 | 100.0% |
| claude-haiku-3n | claude-sonnet-plano | 2 | 100.0% | 1 | 100.0% |
| claude-haiku-3n | claude-opus-h | 2 | 100.0% | 1 | 100.0% |
| gpt-5.5 | claude-sonnet-plano | 13 | 92.3% | 10 | 70.0% |
| gpt-5.5 | claude-opus-h | 12 | 91.7% | 7 | 100.0% |
| claude-sonnet-plano | claude-opus-h | 73 | 87.7% | 48 | 91.7% |

## Concordância com a classificação de origem (só onde a origem tem um tema correspondente)

| Rodada | n | Mesmo ramo da origem |
|---|---|---|
| claude-opus | 225 | 29.8% |
| claude-sonnet-h | 225 | 31.6% |
| claude-sonnet-3n | 142 | 35.2% |
| claude-haiku-h | 14 | 28.6% |
| claude-haiku-3n | 4 | 50.0% |
| gpt-5.5 | 44 | 22.7% |
| claude-sonnet-plano | 47 | 29.8% |
| claude-opus-h | 42 | 33.3% |

## Experimento 2×2 nas 80 questões sorteadas

Cada rodada comparada com a maioria das demais rodadas e do árbitro, excluindo a própria (leave-one-out). Não é acurácia; é o quanto a rodada acompanha o consenso dos outros.

| Rodada | Método | Modelo | n | Concorda com a maioria dos demais | Tokens prompt/q | Tokens saída/q | US$/q com cache |
|---|---|---|---|---|---|---|---|
| claude-opus-h | 2 estágios | Opus 5.5 (amostra 80) | 73 | 95.9% | 22,612 | 1,186 | 0.05918 |
| claude-opus | plano | Opus 5.5 | 80 | 93.8% | 211,517 | 508 | 0.05418 |
| claude-sonnet-h | 2 estágios | Sonnet 5 | 80 | 92.5% | 20,790 | 1,589 | 0.03145 |
| claude-sonnet-plano | plano | Sonnet 5 (amostra 80) | 80 | 88.7% | 211,517 | 717 | 0.05028 |
