# Experimento com embeddings (sem LLM)

Referência: 315 questões em que o Opus plano, o Sonnet 2 estágios e o árbitro concordam no ramo. Não é gabarito; é o consenso dos LLMs. "Top-1 ramo": o tema mais parecido está no ramo da referência. "Recall@k": o ramo da referência aparece entre os k temas mais parecidos. "Maior lixeira": o tema que mais atraiu questões como primeira opção. "Destilação": regressão logística treinada sobre os embeddings das questões com os rótulos do consenso, validação cruzada de 5 partes, só classes com ao menos 5 questões.

| Modelo | Grupo | Texto do tema | Top-1 ramo | Recall@5 | Recall@10 | Recall@20 | Maior lixeira | Temas distintos no top-1 | Destilação (acerto CV) |
|---|---|---|---|---|---|---|---|---|---|
| legal-bertimbau-base | jurídico PT | só caminho | 5% | 15% | 21% | 32% | Crimes contra o meio ambiente (39%) | 12 |  |
| legal-bertimbau-base | jurídico PT | enriquecido | 21% | 44% | 56% | 67% | Fraude Processual (8%) | 98 | 29% (n=227) |
| legal-bertimbau-sts-large | jurídico PT | só caminho | 22% | 49% | 57% | 68% | Impronúncia, Desclassificação, Absolvição Sumária e Pronúncia (8%) | 115 |  |
| legal-bertimbau-sts-large | jurídico PT | enriquecido | 34% | 57% | 69% | 80% | Mandado de Segurança (6%) | 140 | 49% (n=227) |
| jurisbert-sts | jurídico BR | só caminho | 18% | 38% | 50% | 63% | Autoria Mediata, Colateral e Coautoria (5%) | 126 |  |
| jurisbert-sts | jurídico BR | enriquecido | 33% | 55% | 67% | 79% | Escolas Crimonológicas (2%) | 171 | 47% (n=227) |
| bertimbau-base | português geral | só caminho | 13% | 27% | 36% | 47% | Noções gerais dos crimes praticados contra a administração pública (24%) | 30 |  |
| bertimbau-base | português geral | enriquecido | 30% | 52% | 64% | 75% | Ação Penal Privada (4%) | 106 | 36% (n=227) |
| mpnet-multilingual | multilíngue | só caminho | 32% | 51% | 62% | 71% | Lei Maria da Penha (6%) | 124 |  |
| mpnet-multilingual | multilíngue | enriquecido | 40% | 63% | 75% | 84% | Condescendência Criminosa (3%) | 149 | 56% (n=227) |
| e5-base | multilíngue | só caminho | 34% | 55% | 67% | 75% | Fases do Iter Criminis (8%) | 123 |  |
| e5-base | multilíngue | enriquecido | 57% | 79% | 86% | 90% | Ameaça e Perseguição (4%) | 152 | 23% (n=227) |
| bge-m3 | multilíngue | só caminho | 46% | 70% | 76% | 81% | Falso Testemunha ou Falsa Perícia e Corrupção Ativa de Testemunha ou Perito (4%) | 138 |  |
| bge-m3 | multilíngue | enriquecido | 64% | 85% | 89% | 93% | Inquérito Policial (2%) | 165 | 60% (n=227) |
| mxbai-large | inglês | só caminho | 36% | 56% | 65% | 75% | Ação Penal Pública Incondicionada (3%) | 128 |  |
| mxbai-large | inglês | enriquecido | 49% | 72% | 80% | 87% | Omissão de Socorro (3%) | 156 | 48% (n=227) |

Modelos: `rufimelo/Legal-BERTimbau-base` (BERT cru (MLM), sem treino de similaridade; a hipótese mais fraca); `rufimelo/Legal-BERTimbau-sts-large-ma-v3` (Legal-BERTimbau ajustado para similaridade (STS)); `alfaneo/jurisbert-base-portuguese-sts` (JurisBERT: pré-treino em decisões do STJ, ajustado para STS); `neuralmind/bert-base-portuguese-cased` (BERTimbau cru (MLM)); `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` (paráfrase multilíngue (2019)); `intfloat/multilingual-e5-base` (E5 base, com prefixos query/passage); `bge-m3` (BGE-M3 via Ollama (GPU local)); `mxbai-embed-large` (mxbai-embed-large via Ollama, treinado sobretudo em inglês).
