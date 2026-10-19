# Comparação de métodos e modelos

Gerado por `src/42_comparar_metodos.py`. Tokens de prompt reconstruídos a partir dos prompts reais e das saídas intermediárias gravadas, sem o contexto fixo do Claude Code; razão caracteres/token medida neste corpus (`runs/calibracao_tokens.json`). Custos a preço de lista da API; "com cache" supõe o system prompt lido do cache (as rodadas reais foram feitas pela assinatura, sem custo marginal).

| Rodada | Método | Modelo | Questões | Chamadas/q | Tokens prompt/q | Tokens saída/q | US$/q sem cache | US$/q com cache | US$ 50 mil q (cache) | Fora | Multi | Escolheu subtema | Conf. ramo média |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| claude-opus | plano | Opus 5.5 | 359 | 1.0 | 211,517 | 508 | 0.85623 | 0.05418 | 2709 | 2 | 62 | 210 | 0.8 |
| claude-sonnet-h | 2 estágios | Sonnet 5 | 358 | 1.99 | 20,801 | 1,589 | 0.05749 | 0.03146 | 1573 | 4 | 95 | 204 | 0.911 |
| claude-sonnet-3n | 3 estágios | Sonnet 5 | 151 | 2.99 | 13,568 | 2,009 | 0.04722 | 0.03788 | 1894 | 1 | 33 | 80 | 0.918 |
| gpt-5.5 | plano | GPT-5.5 (parcial) | 63 | 1.0 | 131,352 | 589 | None | None | None | 0 | 11 | 39 | 0.922 |

## Concordância par a par

| A | B | n | Mesmo ramo | n (ambos escolheram subtema) | Mesmo subtema quando ambos escolhem |
|---|---|---|---|---|---|
| claude-opus | claude-sonnet-h | 358 | 88.5% | 183 | 91.8% |
| claude-opus | claude-sonnet-3n | 151 | 83.4% | 73 | 93.2% |
| claude-opus | gpt-5.5 | 63 | 98.4% | 37 | 97.3% |
| claude-sonnet-h | claude-sonnet-3n | 151 | 86.1% | 77 | 92.2% |
| claude-sonnet-h | gpt-5.5 | 63 | 88.9% | 33 | 90.9% |
| claude-sonnet-3n | gpt-5.5 | 38 | 78.9% | 17 | 82.4% |

## Concordância com a classificação de origem (só onde a origem tem um tema correspondente)

| Rodada | n | Mesmo ramo da origem |
|---|---|---|
| claude-opus | 225 | 29.8% |
| claude-sonnet-h | 224 | 31.7% |
| claude-sonnet-3n | 100 | 38.0% |
| gpt-5.5 | 44 | 22.7% |
