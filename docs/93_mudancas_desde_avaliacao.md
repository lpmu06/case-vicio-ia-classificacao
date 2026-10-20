# O que mudou desde a avaliação simulada

19/10/2026, 23h. Resposta a `docs/90_avaliacao_simulada.md`, para uma nova rodada de revisão. A execução seguiu o plano `docs/91_plano_melhorias.md`, com as decisões do Luis registradas no diário (`docs/00_entendimento_e_plano.md`, seção 10). Cada bloco tem um commit próprio. Tudo continua reproduzível sem LLM com `bash rodar_analises.sh`, e o validador aprova os três CSVs.

## Números: antes e depois

| | Na avaliação | Agora |
|---|---|---|
| Entrega principal | híbrido (69 no subtema) | nível 1 (0 no subtema); híbrido vira `publicacao_subtema.csv` |
| Publicadas / revisar / fora | 217 / 140 / 2 | 218 / 140 / 1 |
| Precisão prevista | 0,96 (0,85–0,99) | 0,95 (0,86–1,00) |
| Ponto da previsão | mediana de E1, E2 e E3 | média de E2 e E3 ajustados; E1 só como teto do intervalo |
| E3 | 97,8% em 46 sobreviventes da auditoria que escolheu os limiares | 99,3% em 50 publicadas de uma auditoria cega nova (49 ok, 1 duvidoso, 0 erro); a antiga fica como "ancorada" |
| E2 (GPT-5.5) | 39 de 39, com o GPT na regra de unanimidade | 39 de 39, com o GPT fora da regra (só rodadas completas votam) |
| Exposição aos gêmeos 67xx | 38 publicadas (17,5%), só as cópias | 46 cópias de título idêntico (21,1%, p = 10%) + 45 nomes de aula "(Parte N)" (20,6%, p = 5%); perda esperada de 3,1 pontos |
| Sensibilidade | nenhuma | grade 3×3 (p das cópias × peso da dúvida): de 0,90 a 0,97 |
| Variante sem duplicados | 179 publicadas, 0,98 | 127 publicadas, 0,98 (agora cobre os dois grupos de gêmeos) |
| Custo do pipeline nas 359 | "US$ 48", sem o árbitro na tabela | US$ 45 (US$ 23 em lote), reconstruído com o árbitro em `comparacao_metodos.md` |

## Os 13 itens do plano da seção 2

| # | Item | O que foi feito | Commit |
|---|---|---|---|
| 1 | Nível 1 como principal | `47_decisao.py --modo n1` por padrão; o híbrido aparece na seção a) do relatório como a tentativa que a régua descarta | 4007f9a, 2b33d14 |
| 2 | Gêmeos "(Parte N)" no risco | Mapa de gêmeos construído da árvore (`comum.gemeos_67xx`), em dois grupos: cópias a 10% e nomes de aula a 5% (decisão do Luis), com sensibilidade | 4007f9a |
| 3 | Auditoria cega nova | 50 publicadas, semente 2026, nenhuma das 60 anteriores. Caderno sem votos, confiança nem justificativa. Auditor: subagente Opus com contexto limpo, que primeiro argumenta a favor de outro tema (`prompts/auditoria_cega.md`). Resultado: 49 ok, 1 duvidoso (Q0278, Lei 9.099 com dois endereços), 0 erro | 273442b |
| 4 | `fora` com evidência forte | Exige árbitro ≥ 0,80 e os dois votantes; Q0168 passou a revisar | 4007f9a |
| 5 | Unanimidade igual para todas | Só rodadas completas e o árbitro; Q0013 passou a publicar | 4007f9a |
| 6 | Bloco de precisão | Sem "independentes entre si" e sem o árbitro no Dawid-Skene; limiares escolhidos com a auditoria v1 e E3 medido na v2; E1 descrito como teto; grade de sensibilidade | 2e36834 |
| 7 | Números e frases | Os 16 pontos da seção 5 corrigidos (README com 359 e tempos, diário com 63, memo "sem saber qual era a maioria" e com a faixa de precisão, linha do Haiku 3 estágios, etc.) | 2e36834 |
| 8 | Árbitro no custo | Rodada "árbitro" na comparação de métodos (19.246 tokens, US$ 0,041 por questão) e marcador `CUSTO_PIPELINE` | fd9b21d |
| 9 | Fila do professor | Seção c): fila semanal dimensionada, meta abaixo de 10% em três meses, causas da fila de hoje e ordem de atendimento | 2e36834 |
| 10 | Glossário e clareza | Meia frase para Dawid-Skene, Wilson, leave-one-out e cache; parágrafo "o que foi julgamento, não medida" | 2e36834 |
| 11 | Motivos cortados | Corte no fim da última frase completa, fechando o parêntese aberto | 4007f9a, 2b33d14 |
| 12 | Repositório | `estudo_movai.md` fora do índice e do histórico (git filter-repo); id da OpenAI redigido no histórico; `runs/faltam.py` apagado; título do PDF | 691b1e4 |
| 13 | Fechamento | Entregáveis regenerados e validados; PDF com 5 páginas e o memo na última; `anexos/` conferido contra os hashes oficiais; rascunho do e-mail em `docs/92_email_entrega.md` | fd199e7 |

Também atendidos, fora da lista de 13:
- **Coluna de confiança (seção 4, item 5):** desconto por gêmeo nas publicadas; nas revisar, só a confiança do árbitro.
- **`requirements.txt` (seção 7):** criado.

## Feito depois do fechamento: o Jev (bloco G)

A avaliação punha o Jev em "não fazer hoje". Ele foi testado depois do fechamento, quando a chave chegou, e **não altera nenhum entregável**: `publicacao*.csv`, `previsao.txt` e o memo estão idênticos aos do commit fd199e7. Commit 90ca881. Detalhes em `docs/jev.md`.

- **Cinco variantes nas 359 questões, um fator por vez:** base, versão nova do modelo, descrições enriquecidas em vez das curtas, beam search na árvore e média de 5 ordens embaralhadas das opções. Só as descrições enriquecidas ajudam: 85,8% de concordância de ramo com a maioria dos não-Jev, contra 79,7% da base. Na comparação pareada, 33 questões contra 11; duas execuções idênticas divergem em 3,3%. Custo total: US$ 1,82.
- **Calibração:** erro de calibração de 0,014, contra 0,144 da confiança que o Opus declara. Com probabilidade ≥ 0,99, o Jev cobre 39% das questões, e todas concordam com a maioria.
- **Desempate nas 140 questões em revisão:** o Jev escolheu só entre os 2 a 4 temas candidatos, e 39 questões foram promovidas por uma regra fixada antes de qualquer auditoria. Na auditoria cega com controles, as promovidas vieram misturadas a 40 publicadas que nenhuma auditoria tinha visto. Dois auditores, sem saber quais eram quais: 26 de 39 promovidas ok, contra 39 de 40 controles (0 erro). O desempate foi descartado. As dúvidas são de convenção e de questões mistas: a fila de revisão é ambiguidade real.
- **Fora da regra:** o Jev não entra no Dawid-Skene, nos pares confundíveis nem na média de subtema da previsão. Com ele, 7 publicadas iriam para revisão, por causa de pares confundíveis criados pelos votos dele, onde os votantes e o árbitro concordavam.
- **Relatório:**
  - linha na tabela "o que testamos";
  - frase em "becos sem saída";
  - na cascata da seção c), o Jev substitui o modelo pequeno como segunda opinião de outra família (US$ 0,0013 em vez de US$ 0,005 por questão; o total vai de US$ 0,03 para US$ 0,025);
  - uma frase repetida sobre os créditos da OpenAI saiu do anexo, para caber em 5 páginas.
- **Efeito colateral útil:** os 40 controles funcionam como uma terceira auditoria cega das publicadas (0 erro, 1 dúvida). Não entram no E3, porque o número da previsão foi fixado antes.

## O que não foi feito

- **Seção 6 b):** os 22 temas de nível 1 sem questão e os 60 sem subtema; a taxa de publicação por disciplina; a tabela dos 13 temas com gêmeo dentro do relatório (os números por tema estão em `runs/previsao.json`).
- **Seção 6 c):** a frase sobre as cerca de 200 questões necessárias para detectar uma queda de 95% para 90%; o custo de re-enriquecer a taxonomia a cada mudança na árvore.
- **Seção 8:** nada além da frente 14 (Jev). Sem rotulagem por professor, sem segunda família de LLM nas 359 (os créditos da OpenAI acabaram), sem auditoria por outra família, sem o experimento do árbitro sem candidatos.

## O que pedimos nesta revisão

1. **A previsão de 0,95 (0,86–1,00) agora é honesta sobre as próprias hipóteses?** O limite superior continua sendo o teto do Dawid-Skene.
2. **Os acréscimos do Jev no relatório ajudam ou tiram o foco?** A seção a) e a cascata da seção c) mudaram, sempre dentro das 5 páginas.
3. **Algum item de "o que não foi feito" vale antes da entrega?** O prazo combinado é meia-noite de 19/10.
