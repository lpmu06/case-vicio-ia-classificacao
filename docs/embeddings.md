# Experimento com embeddings (sem LLM)

Referência: 285 questões em que o Opus plano, o Sonnet 2 estágios e o árbitro concordam no ramo. Não é gabarito; é o consenso dos LLMs. "Top-1 ramo": o tema mais parecido está no ramo da referência. "Recall@k": o ramo da referência aparece entre os k temas mais parecidos. "Maior lixeira": o tema que mais atraiu questões como primeira opção. "Destilação": regressão logística treinada sobre os embeddings das questões com os rótulos do consenso, validação cruzada de 5 partes, só classes com ao menos 5 questões.

| Modelo | Grupo | Texto do tema | Top-1 ramo | Recall@5 | Recall@10 | Recall@20 | Maior lixeira | Temas distintos no top-1 | Destilação (acerto CV) | Tempo (s) |
|---|---|---|---|---|---|---|---|---|---|---|
| legal-bertimbau-base | jurídico PT | só caminho | 6% | 15% | 21% | 33% | Crimes contra o meio ambiente (38%) | 12 |  |  |
| legal-bertimbau-base | jurídico PT | enriquecido | 20% | 45% | 56% | 67% | Fraude Processual (8%) | 94 | 29% (n=200) | 245.0 |
| legal-bertimbau-sts-large | jurídico PT | só caminho | 24% | 49% | 56% | 67% | Impronúncia, Desclassificação, Absolvição Sumária e Pronúncia (8%) | 111 |  |  |
| legal-bertimbau-sts-large | jurídico PT | enriquecido | 33% | 57% | 68% | 79% | Mandado de Segurança (6%) | 134 | 50% (n=200) | 16734.4 |

Modelos: `rufimelo/Legal-BERTimbau-base` (BERT cru (MLM), sem treino de similaridade; o elo fraco do MoVAI); `rufimelo/Legal-BERTimbau-sts-large-ma-v3` (Legal-BERTimbau ajustado para similaridade (STS)).
