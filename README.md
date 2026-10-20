# Case Vício / Método VDE — classificação de tópicos

Entrega do processo seletivo da área de IA. Classifica 359 questões de concurso (Penal, Processo Penal, Legislação Penal Especial e Criminologia) em uma árvore de 377 temas, decidindo entre **publicar**, **revisar** e **fora**, com a meta de pelo menos 95% de precisão nas publicadas e sem nenhum gabarito.

| Entregável | Onde |
|---|---|
| Decisão por questão | [`publicacao.csv`](publicacao.csv): 218 publicadas (todas no tema de nível 1), 140 para revisão, 1 fora |
| Variantes | [`publicacao_subtema.csv`](publicacao_subtema.csv) (versão híbrida: desce ao subtema quando a evidência é forte; a tentativa que não compensou pela régua) e [`publicacao_sem_duplicados.csv`](publicacao_sem_duplicados.csv) (os temas que têm um gêmeo 67xx na árvore vão para revisão) |
| Previsão de precisão e cobertura | [`previsao.txt`](previsao.txt): precisão 0,95 (0,86 a 1,00), cobertura 0,61 |
| Relatório: raciocínio, diagnóstico, produção e memo (5 páginas) | [`docs/relatorio.pdf`](docs/relatorio.pdf) e [`docs/relatorio.md`](docs/relatorio.md) |
| Memo para o professor (1 página) | [`docs/memo_professor.md`](docs/memo_professor.md) |
| Anexos do relatório | [`docs/comparacao_metodos.md`](docs/comparacao_metodos.md), [`docs/embeddings.md`](docs/embeddings.md), [`docs/diagnostico.md`](docs/diagnostico.md), [`docs/sensibilidade.md`](docs/sensibilidade.md), [`docs/auditoria_cega_caderno.md`](docs/auditoria_cega_caderno.md) (auditoria cega) e [`docs/auditoria_caderno.md`](docs/auditoria_caderno.md) (primeira auditoria, usada para os limiares) |
| Diário de bordo: entendimento, plano e todas as decisões, com data e motivo | [`docs/00_entendimento_e_plano.md`](docs/00_entendimento_e_plano.md) |
| Avaliação simulada (como um avaliador leria a entrega) e plano de melhorias executado na noite de 19/10 | [`docs/90_avaliacao_simulada.md`](docs/90_avaliacao_simulada.md), [`docs/91_plano_melhorias.md`](docs/91_plano_melhorias.md) |
| Enunciado original | [`case-ia-classificacao-de-topicos.pdf`](case-ia-classificacao-de-topicos.pdf), [`docs/enunciado_README_original.md`](docs/enunciado_README_original.md) |

## Como rodar

Requisitos: Python 3.10+ e `pip install -r requirements.txt` (anthropic, openai, httpx, numpy, scikit-learn, sentence-transformers, markdown; versões usadas em `requirements.txt`). O PDF exige o Chrome instalado (impressão headless) e o `pdfinfo` do poppler para a conferência de páginas. Os modelos Claude foram chamados pelo Claude Code em modo headless (`claude -p`, provedor `claude_cli`), logado numa assinatura; os mesmos scripts aceitam `--provedor anthropic` (chave em `ANTHROPIC_API_KEY`) ou `--provedor openai` (`OPENAI_API_KEY`). As chaves também podem ficar em `keys.txt`, que não é versionado. O experimento de embeddings usa o Ollama local para `bge-m3` e `mxbai-embed-large`.

Para reproduzir os entregáveis não é preciso chamar nenhum modelo: as saídas brutas de todas as chamadas estão em `runs/`, e `bash rodar_analises.sh` refaz tudo a partir delas. O passo `11_enriquecer_temas.py` também não precisa rodar: seu resultado está em `data/temas_enriquecidos.json`.

```bash
# 0. Dados e taxonomia
python src/00_preparo.py                 # limpa o HTML -> data/questoes_limpas.jsonl
python src/10_arvore.py                  # árvore -> data/temas.json, data/arvore.txt
python src/11_enriquecer_temas.py --provedor openai --modelo gpt-5.5   # metadados dos 351 temas usáveis (uma vez)
python src/20_baseline_origem.py         # "copiar a origem" -> data/baseline_origem.jsonl

# 1. Classificadores (cada um grava runs/<rótulo>/<id>.json e retoma de onde parou)
python src/30_classificar.py --provedor claude_cli --modelo opus --rotulo claude-opus                        # plano
python src/31_classificar_hierarquico.py --provedor claude_cli --modelo sonnet --rotulo claude-sonnet-h       # 2 estágios
python src/32_classificar_3niveis.py --provedor claude_cli --modelo sonnet --rotulo claude-sonnet-3n          # 3 estágios
python src/31_classificar_hierarquico.py --provedor claude_cli --modelo haiku --effort low --rotulo claude-haiku-h
python src/32_classificar_3niveis.py --provedor claude_cli --modelo haiku --effort low --rotulo claude-haiku-3n
# experimento 2x2 em 80 questões sorteadas (data/amostra_2x2.txt)
python src/30_classificar.py --provedor claude_cli --modelo sonnet --rotulo claude-sonnet-plano --ids $(cat data/amostra_2x2.txt)
python src/31_classificar_hierarquico.py --provedor claude_cli --modelo opus --rotulo claude-opus-h --ids $(cat data/amostra_2x2.txt)
# Jev (TypeSafe), só como estudo, fora da regra de publicação; exige a chave (jev = ... em keys.txt). US$ 1,82 nas 5 variantes
python src/33_classificar_jev.py                      # base -> runs/jev-h
python src/33_classificar_jev.py --criterios ricos    # a melhor; também --modelo jev-preview, --beam 3, --ordens 5
python src/51_jev_desempate.py                        # desempate nas questões em revisão (+ --caderno, --avaliar)

# 2. Árbitro, análises e decisão
python src/46_arbitragem.py --modelo opus --effort high --rotulo arbitro-opus
python src/42_comparar_metodos.py        # tokens, custo, concordância -> docs/comparacao_metodos.md
python src/45_confiabilidade.py          # Dawid-Skene -> data/confiabilidade.jsonl
python src/47_decisao.py                 # regras -> publicacao.csv e data/decisoes.jsonl
python src/43_embeddings.py calcular && python src/43_embeddings.py avaliar   # -> docs/embeddings.md
python src/44_diagnostico.py             # -> docs/diagnostico.md
python src/50_avaliar_jev.py             # variantes, calibração, cascata e desempate do Jev -> docs/jev.md
python src/48_auditoria.py --n 50        # caderno da primeira auditoria -> docs/auditoria_caderno.md, data/auditoria_ia.csv
python src/48_auditoria.py --cego --n 50 --semente 2026 --excluir data/auditoria_ia.csv   # caderno cego -> docs/auditoria_cega_caderno.md
#   (os vereditos em data/auditoria_ia_v2.csv foram dados por um agente com contexto limpo, prompts/auditoria_cega.md)
python src/60_previsao.py                # estimadores de precisão -> runs/previsao.json
python src/61_escrever_previsao.py       # -> previsao.txt
python src/49_sensibilidade.py           # limiares x cobertura x precisão -> docs/sensibilidade.md
python src/47_decisao.py --modo hibrido --saida publicacao_subtema.csv --saida_jsonl data/decisoes_subtema.jsonl
python src/47_decisao.py --evitar_duplicados --saida publicacao_sem_duplicados.csv --saida_jsonl data/decisoes_sem_duplicados.jsonl
python src/62_preencher_relatorio.py     # docs/relatorio.md a partir de src/modelos/relatorio.md e das saídas
python src/64_gerar_pdf.py               # docs/relatorio.pdf (relatório + memo)
python src/63_validar_entrega.py         # confere o formato dos CSVs de entrega
```

Os passos de análise, sem nenhuma chamada a LLM, estão juntos em `rodar_analises.sh`.

**O que gera o `publicacao.csv`:** o passo `47_decisao.py`, lendo as saídas brutas em `runs/`. Todas as chamadas a modelos ficam gravadas em `runs/<rodada>/<id>.json`, com a resposta, a justificativa e o uso de tokens.

## Como a classificação é feita, em resumo

1. **Limpeza**: enunciado mais alternativas, sem HTML. Uma questão trazia 100 mil caracteres de lixo do Word.
2. **Taxonomia enriquecida**: um LLM escreve, uma única vez, descrição, palavras-chave, dispositivos legais e "não confundir com" para cada tema usável. Temas inativos e os 20 temas-"bucket" (ids 67xx, nomes de aula como "(Parte 1)") nunca recebem publicação.
3. **Vários classificadores independentes**: plano (árvore inteira em uma chamada), 2 estágios (tema, depois subtema) e 3 estágios (grupo, tema, subtema), com modelos de tamanhos diferentes.
4. **Árbitro**: um modelo forte escolhe entre os candidatos de todos, embaralhados, sem saber qual é a maioria.
5. **Decisão**: publica só quando o árbitro e os dois classificadores principais concordam no ramo, com confiança e maioria suficientes; exige unanimidade das rodadas completas nos ramos que os modelos costumam confundir entre si; publica sempre no tema de nível 1, o que é correto pela régua sempre que o ramo está certo (a variante `publicacao_subtema.csv` desce ao subtema quando a evidência é forte). O resto vai para revisar, com a sugestão do árbitro e o motivo; `fora` só quando o árbitro e os dois classificadores dizem fora com confiança alta.
6. **Previsão sem gabarito**: quatro estimadores, com as hipóteses declaradas, combinados de forma conservadora. Detalhes no relatório.

## Decisões tomadas à mão

Todas registradas com data e motivo na seção 10 do [diário de bordo](docs/00_entendimento_e_plano.md). As principais: os temas 67xx e os inativos nunca são usados; nos títulos duplicados, o nó da Legislação Especial é o alvo; os 23 grupos do classificador de 3 estágios foram definidos à mão (`data/grupos_n1.json`); a busca da questão em bancos de outros sites foi descartada por ser conteúdo de concorrente; a estimativa de precisão é cega, porque não houve rotulagem humana.

## Modelos, custo e tempo

| Etapa | Modelo | Questões |
|---|---|---|
| Enriquecimento da taxonomia | GPT-5.5 (API OpenAI) | 89 chamadas, 351 temas |
| Classificador plano | Claude Opus 5.5 | 359 |
| Classificador 2 estágios | Claude Sonnet 5 | 359 |
| Classificador 3 estágios | Claude Sonnet 5 | 359 |
| Árbitro | Claude Opus 5.5, esforço alto | 359 |
| Experimento 2×2 e modelo pequeno | Sonnet 5, Opus 5.5, Haiku 4.5 | 80 sorteadas |
| Outra família | GPT-5.5 | 63, até acabar o crédito |
| Embeddings | 8 modelos locais (Legal-BERTimbau, JurisBERT, BERTimbau, mpnet, E5, bge-m3, mxbai) | 359 |

O trabalho foi feito entre 16/10 e 19/10/2026. Os modelos Claude rodaram pelo Claude Code numa assinatura, sem custo marginal; o tempo de máquina das rodadas foi de algumas horas cada (o árbitro, 4,8 h), por dividir a cota entre rodadas paralelas. A preço de lista da API, com cache, o pipeline final (Opus plano, Sonnet 2 estágios e árbitro) custaria cerca de US$ 45 para as 359 questões, ou US$ 23 pela API em lote (soma das três linhas da tabela de métodos, reconstruída pelo `42_comparar_metodos.py`); em produção, a cascata proposta no relatório fica perto de US$ 0,03 por questão. Detalhes por método em [`docs/comparacao_metodos.md`](docs/comparacao_metodos.md).
