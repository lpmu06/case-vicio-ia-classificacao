# Comparação de métodos e modelos

Gerado por `src/42_comparar_metodos.py`. Tokens de prompt reconstruídos a partir dos prompts reais e das saídas intermediárias gravadas, sem o contexto fixo do Claude Code; razão caracteres/token medida neste corpus (`runs/calibracao_tokens.json`). Custos a preço de lista da API; "com cache" supõe o system prompt lido do cache (as rodadas reais foram feitas pela assinatura, sem custo marginal).

| Rodada | Método | Modelo | Questões | Chamadas/q | Tokens prompt/q | Tokens saída/q | US$/q sem cache | US$/q com cache | US$ 50 mil q (cache) | Fora | Multi | Escolheu subtema | Conf. ramo média |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| claude-opus | plano | Opus 5.5 | 359 | 1.0 | 211,517 | 508 | 0.85623 | 0.05418 | 2709 | 2 | 62 | 210 | 0.8 |
| claude-sonnet-h | 2 estágios | Sonnet 5 | 359 | 1.99 | 20,790 | 1,589 | 0.05747 | 0.03145 | 1572 | 4 | 95 | 204 | 0.911 |
| claude-sonnet-3n | 3 estágios | Sonnet 5 | 323 | 2.98 | 13,874 | 2,063 | 0.04838 | 0.03905 | 1952 | 4 | 89 | 173 | 0.899 |
| claude-haiku-h | 2 estágios | Haiku 4.5 | 70 | 2.0 | 16,795 | 6,878 | 0.05119 | 0.04084 | 2042 | 0 | 11 | 48 | 0.944 |
| claude-haiku-3n | 3 estágios | Haiku 4.5 | 29 | 3.0 | 10,504 | 8,809 | 0.05455 | 0.05083 | 2541 | 0 | 3 | 17 | 0.967 |
| gpt-5.5 | plano | GPT-5.5 (parcial) | 63 | 1.0 | 131,352 | 589 | None | None | None | 0 | 11 | 39 | 0.922 |
| claude-sonnet-plano | plano | Sonnet 5 (amostra 80) | 80 | 1.0 | 211,517 | 717 | 0.4302 | 0.05028 | 2514 | 0 | 19 | 61 | 0.872 |
| claude-opus-h | 2 estágios | Opus 5.5 (amostra 80) | 80 | 2.0 | 22,460 | 1,176 | 0.11335 | 0.05837 | 2919 | 0 | 10 | 50 | 0.871 |

## Concordância par a par

| A | B | n | Mesmo ramo | n (ambos escolheram subtema) | Mesmo subtema quando ambos escolhem |
|---|---|---|---|---|---|
| claude-opus | claude-sonnet-h | 359 | 88.6% | 183 | 91.8% |
| claude-opus | claude-sonnet-3n | 323 | 84.5% | 156 | 91.0% |
| claude-opus | claude-haiku-h | 70 | 90.0% | 45 | 91.1% |
| claude-opus | claude-haiku-3n | 29 | 96.6% | 17 | 88.2% |
| claude-opus | gpt-5.5 | 63 | 98.4% | 37 | 97.3% |
| claude-opus | claude-sonnet-plano | 80 | 90.0% | 55 | 87.3% |
| claude-opus | claude-opus-h | 80 | 96.3% | 50 | 100.0% |
| claude-sonnet-h | claude-sonnet-3n | 323 | 85.4% | 162 | 92.0% |
| claude-sonnet-h | claude-haiku-h | 70 | 90.0% | 41 | 95.1% |
| claude-sonnet-h | claude-haiku-3n | 29 | 96.6% | 15 | 93.3% |
| claude-sonnet-h | gpt-5.5 | 63 | 88.9% | 33 | 90.9% |
| claude-sonnet-h | claude-sonnet-plano | 80 | 91.2% | 51 | 92.2% |
| claude-sonnet-h | claude-opus-h | 80 | 91.2% | 46 | 95.7% |
| claude-sonnet-3n | claude-haiku-h | 70 | 85.7% | 38 | 92.1% |
| claude-sonnet-3n | claude-haiku-3n | 29 | 93.1% | 14 | 92.9% |
| claude-sonnet-3n | gpt-5.5 | 59 | 79.7% | 26 | 84.6% |
| claude-sonnet-3n | claude-sonnet-plano | 72 | 86.1% | 45 | 93.3% |
| claude-sonnet-3n | claude-opus-h | 72 | 88.9% | 40 | 97.5% |
| claude-haiku-h | claude-haiku-3n | 29 | 96.6% | 16 | 93.8% |
| claude-haiku-h | gpt-5.5 | 20 | 95.0% | 10 | 100.0% |
| claude-haiku-h | claude-sonnet-plano | 59 | 93.2% | 40 | 90.0% |
| claude-haiku-h | claude-opus-h | 59 | 88.1% | 36 | 94.4% |
| claude-haiku-3n | gpt-5.5 | 12 | 100.0% | 6 | 100.0% |
| claude-haiku-3n | claude-sonnet-plano | 25 | 96.0% | 15 | 86.7% |
| claude-haiku-3n | claude-opus-h | 25 | 96.0% | 15 | 93.3% |
| gpt-5.5 | claude-sonnet-plano | 13 | 92.3% | 10 | 70.0% |
| gpt-5.5 | claude-opus-h | 13 | 84.6% | 7 | 100.0% |
| claude-sonnet-plano | claude-opus-h | 80 | 87.5% | 50 | 92.0% |

## Concordância com a classificação de origem (só onde a origem tem um tema correspondente)

| Rodada | n | Mesmo ramo da origem |
|---|---|---|
| claude-opus | 225 | 29.8% |
| claude-sonnet-h | 225 | 31.6% |
| claude-sonnet-3n | 201 | 35.3% |
| claude-haiku-h | 43 | 32.6% |
| claude-haiku-3n | 19 | 31.6% |
| gpt-5.5 | 44 | 22.7% |
| claude-sonnet-plano | 47 | 29.8% |
| claude-opus-h | 47 | 29.8% |

## Experimento 2×2 nas 80 questões sorteadas

Cada rodada comparada com a maioria das demais rodadas e do árbitro, excluindo a própria (leave-one-out). Não é acurácia; é o quanto a rodada acompanha o consenso dos outros.

| Rodada | Método | Modelo | n | Concorda com a maioria dos demais | Tokens prompt/q | Tokens saída/q | US$/q com cache |
|---|---|---|---|---|---|---|---|
| claude-opus | plano | Opus 5.5 | 80 | 93.8% | 211,517 | 508 | 0.05418 |
| claude-sonnet-h | 2 estágios | Sonnet 5 | 80 | 92.5% | 20,790 | 1,589 | 0.03145 |
| claude-opus-h | 2 estágios | Opus 5.5 (amostra 80) | 80 | 92.5% | 22,460 | 1,176 | 0.05837 |
| claude-sonnet-plano | plano | Sonnet 5 (amostra 80) | 80 | 90.0% | 211,517 | 717 | 0.05028 |
| claude-haiku-h | 2 estágios | Haiku 4.5 | 59 | 89.8% | 16,795 | 6,878 | 0.04084 |
| claude-sonnet-3n | 3 estágios | Sonnet 5 | 72 | 87.5% | 13,874 | 2,063 | 0.03905 |
