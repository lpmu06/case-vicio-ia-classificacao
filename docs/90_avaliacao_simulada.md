# Case Vício: tudo a melhorar

19/10/2026 · avaliação simulada da entrega em `D:\case-vicio-ia`, com verificações diretas nos arquivos (ver apêndice). Prazo prorrogado para meia-noite de 19/10.

## 1. Resumo

A entrega está completa, reproduzível e bem argumentada. O que mais pode derrubar a nota é a estimativa de precisão, apoiada só em modelos correlacionados e numa amostra reaproveitada, e a escolha do híbrido, que arrisca subtema irmão sem ganhar cobertura.

**O que está sólido**

- Formato: o validador aprova os três CSVs, 359 linhas cada.
- Reprodutibilidade: `rodar_analises.sh` regenera 21 arquivos byte a byte, PDF incluído, em 30 segundos e sem LLM.
- Raciocínio, diagnóstico e produção: documentados, quantificados, com becos sem saída e diário de decisões datado.
- Memo: concreto, uma página, com pedidos e tempos.
- Amostra de 10 publicadas sorteadas: 9 claramente certas, 1 plausível.

**O que pesa contra, em ordem**

1. Estimativa de precisão otimista em 1 a 2 pontos, por sete causas (seção 3).
2. Variante principal escolhida contra a régua do case (seção 4).
3. Afirmações incorretas em previsao.txt, README, relatório, memo e diário (seção 5).
4. Repositório com arquivo do empregador e dados de bancada (seção 7).

**Notas provisórias por critério do PDF**

| Critério | Hoje | Alcançável até meia-noite | O que muda a nota |
| --- | --- | --- | --- |
| Cobertura com precisão ≥ 95% | 7 | 8 | nível 1 como principal elimina o risco de irmão com a mesma cobertura |
| Previsão acerta o próprio resultado | 7 | 8 | auditoria cega nova, risco 67xx completo, texto sem afirmações falsas |
| Raciocínio, diagnóstico e produção | 9 | 9 | custo do árbitro na tabela; fila do professor dimensionada |
| Clareza com não técnico | 8 | 9 | glossário de meia frase; menos números em prosa |

**Lógica do plano.** Primeiro o que muda o publicacao.csv e a previsão. Depois os textos. Depois o repositório e a publicação. Nenhuma rodada longa de LLM que possa não terminar até a meia-noite.

## 2. Plano para hoje, até meia-noite

Treze itens, cerca de 7 horas de trabalho, na ordem em que mais mudam a nota. Os itens 1 a 5 alteram o resultado; 6 a 11 alteram os textos; 12 e 13 fecham a entrega.

| # | Item | Esforço | Onde | Efeito |
| --- | --- | --- | --- | --- |
| 1 | Tornar o nível 1 com limiar 0,90 a entrega principal; o híbrido vira variante `publicacao_subtema.csv` | 30 min | `47_decisao.py` (padrão `--modo`), `rodar_analises.sh`, README, relatório, previsao.txt | mesma cobertura de 217, zero risco de subtema irmão em 69 questões |
| 2 | Incluir os gêmeos "(Parte N)" no risco 67xx ou justificar por escrito por que só as 8 cópias contam | 30 min | `60_previsao.py` (conjunto `dup`), previsao.txt item 5, relatório b) | exposição sobe de 17,5% para 39%; ponto cai para perto de 0,94 se incluído |
| 3 | Auditoria nova e cega: 40 a 60 publicadas fora das 60 já vistas, caderno sem votos nem justificativa do árbitro, prompt adversarial | 2 a 3 h | `48_auditoria.py` (flag `--cego`, semente nova), `data/auditoria_ia_v2.csv` | E3 deixa de ser medido na amostra que escolheu os limiares |
| 4 | Regra do `fora`: exigir confiança ≥ 0,80 do árbitro e os dois votantes; senão `revisar` com motivo "dúvida entre fora e X" | 15 min | `47_decisao.py` | Q0168 (confiança 0,60) sai de `fora` |
| 5 | Unanimidade só com rodadas completas (Opus, Sonnet 2 e 3 estágios, árbitro); hoje as 80 da amostra 2×2 enfrentam teste mais duro | 20 min | `47_decisao.py` (variável `todas` na linha do `unanime`) | critério igual para todas as questões, como o diário promete |
| 6 | Reescrever o bloco de precisão: tirar "independentes entre si", tirar o árbitro do Dawid-Skene, dizer que os limiares foram escolhidos com a auditoria, acrescentar sensibilidade do peso da dúvida (1/3, 1/2, 1) | 45 min | `61_escrever_previsao.py`, `src/modelos/relatorio.md` | previsão honesta sobre as próprias hipóteses |
| 7 | Corrigir números e frases: README "quase todas" → 359; diário "47 questões" → 63; relatório "20 temas 67xx" vs desconto de 8; memo "sem saber o que os outros disseram" | 20 min | README, `docs/00_entendimento_e_plano.md`, modelo do relatório, `memo_professor.md` | zero afirmações falsas |
| 8 | Árbitro na tabela de custos e tokens do Haiku 3 estágios preenchidos; US$ 48 passa a ser reconstruível | 30 min | `42_comparar_metodos.py`, `62_preencher_relatorio.py` | sustenta o custo declarado |
| 9 | Dimensionar a fila do professor na seção c): 39% de revisão em 50 mil por semana são 19,5 mil questões, cerca de 325 h a 1 min cada; dizer como baixar a taxa | 30 min | modelo do relatório, seção c) | fecha a maior lacuna do desenho de produção |
| 10 | Glossário de meia frase para Dawid-Skene, Wilson, leave-one-out, cache; tirar números de prosa onde há tabela | 30 min | modelo do relatório | clareza |
| 11 | Motivos: cortar em fim de frase em vez de 240 caracteres; `fora` sem corte no meio da palavra | 10 min | `47_decisao.py` | 3 motivos truncados hoje |
| 12 | Repositório: tirar `estudo_movai.md` do git ou reescrever sem caminhos; apagar `erros` com o id da organização OpenAI em `runs/gpt-5.5/_usage.json`; apagar `runs/faltam.py`; título do PDF; registrar a prorrogação no diário | 25 min | `.gitignore`, `git rm --cached`, `64_gerar_pdf.py`, diário | nada do empregador nem de bancada no repositório público |
| 13 | Regenerar tudo com `rodar_analises.sh`, validar, conferir 5 páginas, commit, tornar público, e-mail | 30 min | raiz | entrega |

**Se o tempo apertar.** Faça 1, 2, 6, 7, 12 e 13. São 3 horas e removem as afirmações falsas e o risco de irmão. O item 3 é o de maior valor, mas só vale se terminar antes do commit final.

**Não fazer hoje.** Rodar outra família nas 359 questões, destilação, Jev, rotulagem humana, novo experimento 2×2. Entram na seção 8.

## 3. Estimativa de precisão

A estrutura é defensável: três estimadores com hipóteses declaradas, dois descontos e um intervalo largo. O ponto 0,96 é otimista em 1 a 2 pontos por sete motivos, listados do mais grave ao menos grave. O intervalo 0,85 a 0,99 pode ficar.

**1. A auditoria escolheu os limiares e depois mediu a precisão.** As 60 questões foram sorteadas das publicadas com limiar 0,80. O diário registra que "a faixa 0,80 a 0,90 concentrava 6 das 9 dúvidas" e por isso o limiar subiu para 0,90. E3 = 97,8% é então medido nas 46 sobreviventes. Com uma amostra independente, a taxa de dúvida entre as publicadas seria maior que 3 em 46. Correção: item 3 do plano, auditoria nova com semente nova e questões fora das 60. Se não der tempo, dizer isso no previsao.txt e tratar E3 como otimista.

**2. O auditor estava ancorado.** O caderno em `docs/auditoria_caderno.md` mostra, para cada uma das 60 questões, os votos de ramo e a justificativa do árbitro antes do veredito. Um "olhar cético" que lê primeiro o argumento do pipeline tende a confirmá-lo. Além disso, o auditor é o mesmo Claude que escreveu os prompts. Correção: caderno cego (questão, tema publicado, descrição e irmãos, nada mais) e prompt que peça o melhor argumento a favor de outro tema antes do veredito.

**3. Os três estimadores não são "independentes entre si".** Dawid-Skene usa oito rodadas Claude e uma GPT. A auditoria é Claude. O GPT-5.5 escreveu as descrições que todos leram, está entre os candidatos do árbitro e entra na regra de unanimidade: em 5 das 39 publicadas com voto do GPT, a concordância dele era condição para publicar. Nas outras 34 ele concorda em 34, o que continua sendo um bom sinal. Correção: trocar a frase por "três estimadores com fontes de erro diferentes" e reportar E2 como 34 de 34 fora dos ramos confundíveis, ou tirar o GPT da regra de unanimidade (item 5 do plano) e manter 39 de 39.

**4. O risco das cópias 67xx cobre 8 dos 20 temas.** O desconto usa só as cópias da Legislação Especial. Os gêmeos "(Parte N)" têm a mesma origem, a mesma falta de descrição e a mesma chance de terem sido usados pela equipe. Se a equipe rotulou em "Teoria da Pena (Parte 2)", publicar em "Teoria da Pena" é erro, porque são irmãos sob a raiz Penal.

| Tema usável | Gêmeos 67xx | Publicadas |
| --- | --- | --- |
| Lei de Execução Penal | 6734 | 9 |
| Lei Maria da Penha | 6724 | 8 |
| Tráfico de Drogas | 6728 | 7 |
| Crimes contra o meio ambiente | 6717 | 5 |
| Lavagem de Dinheiro | 6723 | 3 |
| Organizações Criminosas | 6725 | 3 |
| Abuso de Autoridade | 6716 | 2 |
| Estatuto do Idoso | 6722 | 1 |
| Teoria da Pena | 6726, 6727 | 13 |
| Dos Crimes Contra a Administração Pública | 6718, 6719 | 11 |
| Dos Crimes Contra o Patrimônio | 6720, 6721 | 11 |
| Provas em Espécies | 6735 | 8 |
| Competência | 6732, 6733 | 4 |
| Sentença Penal | 6737, 6738 | 0 |

As 8 primeiras linhas são as 38 publicadas já descontadas, 17,5%. As 5 seguintes somam 47, mais 21,7%. Com os mesmos 10% de chance, a perda esperada vai de 1,75 para 3,9 pontos e o ponto cai para cerca de 0,94. Correção: incluir os gêmeos no conjunto `dup` de `60_previsao.py` e na variante sem duplicados, ou argumentar com dados por que os "(Parte N)" são menos prováveis: a origem rotula questões como "Teoria da Pena (Parte 02)", o que sugere que esses nós vieram da estrutura de aula do site de origem, não da equipe. Esse argumento vale também para as 8 cópias e precisa estar escrito.

**5. Parâmetros chutados sem sensibilidade.** Margem de convenção de 2%, probabilidade de 10% para o cenário das cópias, dúvida valendo 1/3 de erro, fator (1 + taxa de subtema)/2 para publicações no nível 2, concentração 0,5 do Dawid-Skene. Testei a concentração em 0,0, 0,5 e 0,8 e sem a origem: E1 fica entre 0,9876 e 0,9881, então esse parâmetro não importa. Os outros não foram testados. Correção: uma tabela de três linhas no previsao.txt com dúvida valendo 1/3, 1/2 e 1, e p das cópias em 5%, 10% e 25%.

**6. E1 é um teto por construção.** As publicadas são justamente as questões em que os anotadores concordam, então a posterior do ramo é quase 1 para todas. E1 não distingue a precisão das publicadas; serve para ranquear as revisar. O texto já diz "limite superior", mas usa E1 como limite superior do intervalo, 0,99, e como um dos três valores da mediana. Correção: dizer que o teto é do modelo, não da realidade, e considerar a mediana só de E2 e E3 ajustados, ou manter E1 e explicar.

**7. Afirmações do previsao.txt que não batem com o código.** O item 1 diz que o Dawid-Skene inclui o árbitro; `45_confiabilidade.py` e `runs/confiabilidade.json` não o incluem. O item 3 chama as 46 de "amostra aleatória"; são sobreviventes de uma amostra anterior. Correção no `61_escrever_previsao.py`.

**O que não é problema.** A cobertura prevista é exata por construção e o intervalo de denominador está explicado. O limite inferior 0,85 é honesto. A lógica de descontar a margem de convenção só de E1 e E2 está certa.

## 4. Regra de decisão e variante principal

A regra é conservadora e está bem implementada: as 69 publicações no subtema respeitam a regra declarada, nenhum extra aponta para tema inativo ou 67xx, e nenhuma revisão ficou sem árbitro. Os problemas estão na escolha da variante, no `fora`, na unanimidade e na coluna de confiança.

**1. O híbrido arrisca sem ganhar.** Pela régua, publicar no nível 1 é correto sempre que o ramo está certo. O híbrido põe 69 questões no subtema, onde um irmão errado conta como erro, e não publica nenhuma questão a mais. A própria tabela de sensibilidade mostra isso.

| Limiar do árbitro | Modo | Publicadas | Cobertura | No subtema | E3 auditoria | Previsão |
| --- | --- | --- | --- | --- | --- | --- |
| 0,90 | híbrido (entregue) | 217 | 60,4% | 69 | 97,8% (46) | 0,961 |
| 0,90 | nível 1 | 217 | 60,4% | 0 | 97,8% (46) | 0,962 |
| 0,85 | nível 1 | 249 | 69,4% | 0 | 96,3% (54) | 0,962 |
| 0,80 | nível 1 | 257 | 71,6% | 0 | 95,2% (56) | 0,963 |

Recomendação: nível 1 com 0,90 como `publicacao.csv`. Mesma cobertura, mesmo E3, risco de irmão zero. O argumento de produto, "quem estuda Juiz das Garantias não quer Inquérito Policial", continua válido e vai para o relatório como variante `publicacao_subtema.csv`, com a frase: "para o aluno, o subtema vale mais; para a régua deste case, o nível 1 é a aposta segura". Subir para 0,85 dá 32 questões a mais, mas E3 cai e a estimativa já está otimista; só faça isso se a auditoria nova (item 3 do plano) sair limpa nessa faixa.

**2. `fora` com um voto.** A regra exige árbitro em `fora` e metade dos votantes em `fora`. Com dois votantes, um basta. Q0168 (crimes da Lei Geral do Esporte) saiu como `fora` com confiança 0,60. Um `fora` errado não conta na precisão, mas some a questão do recorte, e o enunciado trata isso como custo. Correção: `fora` só com confiança ≥ 0,80 do árbitro e os dois votantes; senão `revisar` com "dúvida entre fora e X". Q0142 (ITCD) fica em `fora` com 0,97.

**3. A unanimidade não é igual para todas as questões.** Nos ramos confundíveis, a regra exige que todas as rodadas disponíveis concordem, inclusive as parciais. As 80 questões da amostra 2×2 têm até quatro votantes a mais que as outras 279, logo um teste mais difícil. O diário promete "critério igual para todas as questões". Correção: na linha do `unanime` em `47_decisao.py`, usar só rodadas completas (Opus plano, Sonnet 2 e 3 estágios) e o árbitro. Conferir quantas questões mudam de decisão e registrar no diário.

**4. A fila de revisão tem 98 questões em que os três concordam no ramo.** Elas foram barradas por confiança abaixo de 0,90 (56), por multi-tema (31) ou por falta de unanimidade (11). Isso é bom para a precisão e ruim para a cobertura. O relatório deve dizer isso com números e ordenar a fila: primeiro as 56 de fronteira, que o professor resolve em segundos, depois as 31 multi-tema, que exigem uma política.

**5. A coluna de confiança não separa as decisões.** As publicadas ficam entre 0,93 e 0,97. Seis questões em `revisar` têm confiança igual ou maior que 0,93. O LEIA-ME define confiança como "a chance de o tema central estar certo", e a sua previsão diz que essa chance é menor nos temas com cópia 67xx. Correção barata: subtrair o risco por questão (10% nas expostas às cópias) e, nas `revisar`, usar a confiança do árbitro sem a média com o Dawid-Skene. A coluna passa a dizer algo e fica coerente com o previsao.txt.

**6. Motivos cortados.** Três motivos terminam no caractere 240, no meio da palavra; os dois `fora` também. Correção: cortar no fim da última frase completa antes de 240.

**7. O árbitro vê os candidatos.** Ele concorda com os dois votantes em 315 de 316 casos em que eles concordam, e só uma vez escolheu fora da lista. Isso é consistência, não independência. O relatório já admite "alguma ancoragem"; falta dizer o que ele acrescenta: a confiança calibrada (0,89 contra 0,65 quando os votantes divergem) e a justificativa para o professor. Pergunta provável na entrevista.

## 5. Afirmações e números a corrigir

Dezesseis pontos, conferidos contra `runs/`, `data/` e o código. Os seis primeiros são afirmações falsas ou não sustentadas; os demais são inconsistências e lacunas. Tudo o mais que conferi bate (apêndice).

| # | Onde | Diz | O que é verdade | Correção |
| --- | --- | --- | --- | --- |
| 1 | previsao.txt, item 1 | o Dawid-Skene usa "Opus plano, Sonnet em 2 e 3 estágios, árbitro, rodadas parciais e a origem" | o árbitro não está na lista `PADRAO` de `45_confiabilidade.py` nem em `runs/confiabilidade.json` | tirar "árbitro" em `61_escrever_previsao.py` |
| 2 | previsao.txt, abertura da seção Precisão | "três estimadores independentes entre si" | todos usam modelos Claude; o GPT escreveu a taxonomia e entra na regra de unanimidade | "três estimadores com fontes de erro diferentes" e uma frase sobre a correlação |
| 3 | previsao.txt, item 3 | "amostra aleatória de 46 publicadas" | 46 sobreviventes de 60 sorteadas antes dos limiares finais, que foram escolhidos olhando essa amostra | dizer isso e marcar E3 como possivelmente otimista |
| 4 | relatório b), "Cópias recentes" | "20 temas com ids 67xx … Tratamos todos como não utilizáveis" | o desconto de risco cobre só 8 (exposição 17,5%); os outros 12 expõem mais 47 publicadas | incluir ou justificar (seção 3, item 4) |
| 5 | memo, "O que fizemos" | "Um leitor mais cuidadoso revisou tudo sem saber o que os outros disseram" | o árbitro recebe os candidatos de todos; não sabe só qual é a maioria | "sem saber qual era a maioria" |
| 6 | README e relatório, anexo de custo | "custaria cerca de US$ 48 para as 359 questões" | Opus plano 0,054 e Sonnet 2 estágios 0,031 por questão somam US$ 30,5; o árbitro não está em `comparacao_metodos.md`, então os US$ 17,5 restantes não são reconstruíveis | incluir o árbitro em `42_comparar_metodos.py` |
| 7 | README, tabela de modelos | "Classificador 3 estágios … quase todas" | `runs/claude-sonnet-3n` tem as 359 | "359" |
| 8 | diário, decisão de 19/10 | "esgotar os créditos em 47 questões" | `runs/gpt-5.5` tem 63; o relatório diz 63 | "63" |
| 9 | relatório a), tabela do experimento | Haiku 3 estágios com "-" em tokens e custo | `comparacao_metodos.md` tem 10.754 tokens e US$ 0,051 | acrescentar `TOK_HAIKU_3N` e `USD_HAIKU_3N` em `62_preencher_relatorio.py` |
| 10 | relatório a), auditoria | "Nenhum erro claro" em 60 | verdadeiro, mas o auditor viu os votos e a justificativa do árbitro | acrescentar "com acesso aos votos" ou refazer cega |
| 11 | README, "Modelos, custo e tempo" | "o tempo total foi de algumas horas" | Opus 18 min, Sonnet 2 estágios 59 min, Sonnet 3 estágios 13,3 h, árbitro 4,8 h, em paralelo; projeto de 16/10 a 19/10 | dar os dois números: tempo de máquina e tempo de calendário |
| 12 | relatório c) | "US$ 0,03 por questão" | as parcelas 0,016 + 0,005 + 0,008 somam 0,029; ok, mas a latência e o volume da fila não aparecem | acrescentar a fila do professor (seção 6) |
| 13 | memo, "Estimamos que cerca de 96%" | só o ponto | o intervalo é 0,85 a 0,99 e o professor é quem vai sentir a diferença | "entre 85% e 99%, mais provavelmente perto de 96%" |
| 14 | memo, tabela de pedidos | "cerca de 1 minuto por questão" | 140 questões são 2,5 h; em produção a fila seria de milhares por semana | dar o total e dizer que a ordem da fila importa |
| 15 | diário, seção 10 | "Rodadas votantes … critério igual para todas as questões" | a unanimidade nos ramos confundíveis usa as rodadas parciais, então 80 questões têm teste mais duro | corrigir o código (plano, item 5) ou a frase |
| 16 | PDF | título do documento é "relatorio_tmp.html" | metadado do Chrome | `<title>` no HTML em `64_gerar_pdf.py` |

**Conferido e correto.** 217/140/2; 69 no subtema e 148 no nível 1; 99,7% de concordância do árbitro (315 de 316); confiança 0,89 contra 0,65; uma escolha fora dos candidatos; 38 publicadas em temas com cópia; 44 multi-tema, todas em revisar; 8 questões em temas genéricos; 48 divergências de disciplina; 225 títulos iguais com 30% no mesmo ramo; 337 descrições geradas; 11 enunciados vazios; bge-m3 com 64% e 93%; destilação 60% em 227; sensibilidade 71,6% para 60,4%; 5 das 9 dúvidas na faixa 0,80 a 0,90; variante sem duplicados com 179 e 0,98; 5 páginas no PDF com o memo em uma.

## 6. Relatório e memo, seção por seção

O relatório cumpre as quatro seções do enunciado em 5 páginas. A maior lacuna é a seção c): o desenho de produção não dimensiona a fila do professor, que com a taxa atual de revisão é inviável.

**a) Como pensamos.** Forte. Quatro acréscimos:

- Uma frase sobre o que foi julgamento humano e o que foi do assistente. O enunciado diz que avalia o julgamento. Cite as decisões tomadas contra a sugestão inicial: descartar a busca em sites concorrentes, usar modelos menores, publicar no nível 1, não rotular sem conhecimento jurídico.
- Glossário de meia frase na primeira ocorrência: Dawid-Skene é "um modelo que estima a taxa de acerto de cada anotador só pelas concordâncias"; Wilson é "intervalo de confiança para proporções com amostra pequena"; leave-one-out é "cada rodada comparada com a maioria das outras"; cache é "a parte fixa do prompt cobrada a um décimo".
- Completar a linha do Haiku 3 estágios na tabela do experimento.
- Se a auditoria cega for feita, registrar a ancoragem da primeira como beco sem saída.

**b) Diagnóstico.** Forte e quantificado. Três acréscimos:

- A tabela dos 13 temas com gêmeo 67xx e quantas publicadas cada um tem (seção 3). É o diagnóstico mais acionável para a equipe.
- Os 22 temas de nível 1 sem nenhuma questão e os 60 sem subtema: a árvore tem ramos que talvez não precisem existir, ou o recorte não os cobre.
- As contagens dos pares confundíveis: Juizado × Sumaríssimo 7, LEP × Teoria da Pena 5, os outros três com 3. E a taxa de publicação por disciplina: Criminologia 50%, Processo Penal 57%, Penal 64%, Legislação Especial 67%.

**c) Produção.** A cascata, os custos por etapa e a destilação estão bons. Falta o que um gestor pergunta primeiro:

- Fila do professor. Hoje 140 de 359 vão para revisão, 39%. Em 50 mil questões por semana seriam 19,5 mil, cerca de 325 horas a um minuto cada. Diga que só as importações novas passam pela cascata, estime esse volume ou deixe a pergunta aberta, e fixe a meta: taxa de revisão abaixo de 10% em três meses, via regras de fronteira escritas pelo professor, segunda família em todas as questões e destilação.
- Ordem da fila: as 56 "fronteira" primeiro, porque o professor resolve em segundos e cada resposta vira regra; as 31 multi-tema por último, porque exigem uma política.
- Reportes de alunos com regra concreta: dois reportes em 30 dias despublicam a questão e a põem no topo da fila; um tema com reportes acima de 2 por mil questões sai da publicação automática.
- Mudança na árvore: versionar as descrições enriquecidas; reclassificar só os ramos afetados; recalcular embeddings dos temas.
- Auditoria semanal de 100: dizer que o intervalo é de mais ou menos 4 pontos, e que detectar uma queda de 95% para 90% pede cerca de 200 questões ou duas semanas acumuladas.
- Custo: incluir o árbitro e o custo de re-enriquecer a taxonomia a cada mudança; dizer a latência da API em lote, até 24 h.

**d) Memo.** Bom, cabe em uma página e pede coisas concretas. Cinco ajustes:

- Trocar "cerca de 96%" por "entre 85% e 99%, mais provavelmente perto de 96%".
- Corrigir "sem saber o que os outros disseram".
- Dar o total: 140 questões são cerca de 2,5 horas, e a fila vem ordenada.
- Pedir também a decisão sobre os temas "(Parte N)", não só sobre as cópias da Legislação Especial.
- Manter uma página: cortar o item 8 (erros de grafia) para uma linha dentro do item 6.

**Clareza em geral.** Números em prosa viram tabela quando são mais de três. Frases abaixo de 25 palavras. "E1, E2, E3" sempre com o nome ao lado. O PDF está bem diagramado; a tabela do anexo de custo aparece correta na página 4; só o extrator de texto a embaralha.

## 7. Código, repositório e publicação

O código faz o que o README diz e reproduz tudo. O que precisa mudar é o que vai para o público: um arquivo do empregador, um id da OpenAI e um script de bancada.

**Tirar antes de tornar público**

- `estudo_movai.md`: caminhos locais e nomes de projeto do empregador, além de resultados internos. Opções: `git rm --cached` mais `.gitignore`, mantendo no relatório a frase sobre "estudo anterior com andamentos processuais, 38%"; ou reescrever como `docs/licoes_estudo_anterior.md` com as três lições e nenhum caminho ou nome.
- `runs/gpt-5.5/_usage.json`: 11 mensagens de erro com o id da organização OpenAI. Apagar a lista `erros` ou trocar o id por `org-...`.
- `runs/faltam.py`: script de bancada dentro de `runs/`. Apagar ou mover para `src/legado`.
- Conferido e limpo: `keys.txt` nunca entrou no histórico; `.mypy_cache` e `__pycache__` ignorados; nenhum `sk-` nos arquivos rastreados.

**Mudanças de código do plano, por arquivo**

| Arquivo | Mudança | Item do plano |
| --- | --- | --- |
| `47_decisao.py` | padrão `--modo n1`; `fora` só com confiança ≥ 0,80 e dois votantes; unanimidade com rodadas completas; motivo cortado no fim da frase; confiança com desconto 67xx e, em revisar, só a do árbitro | 1, 4, 5, 11 |
| `60_previsao.py` | conjunto `dup` com os gêmeos "(Parte N)"; parâmetros `--peso_duvida` e `--p_copias` em grade de três valores | 2, 6 |
| `48_auditoria.py` | flag `--cego` que omite votos e justificativa; `--semente` nova; excluir ids já auditados; saída `auditoria_ia_v2.csv` | 3 |
| `61_escrever_previsao.py` | texto sem "árbitro" no Dawid-Skene e sem "independentes"; parágrafo sobre os limiares e a auditoria; tabela de sensibilidade | 6 |
| `42_comparar_metodos.py` | rodada `arbitro-opus` na tabela, prompt = sistema do árbitro mais blocos dos candidatos | 8 |
| `62_preencher_relatorio.py` | marcadores `TOK_HAIKU_3N`, `USD_HAIKU_3N`, `FILA_SEMANA` | 8, 9 |
| `64_gerar_pdf.py` | `<title>Relatório - Case Classificação de tópicos</title>` | 12 |
| `rodar_analises.sh` | gerar `publicacao_subtema.csv` como variante e `publicacao.csv` em nível 1 | 1 |
| README | tabela de modelos com 359; tempo de máquina e de calendário; `pip install` com `markdown`; avisar que `11_enriquecer_temas.py` não precisa rodar porque a saída está em `data/`; Chrome e poppler como requisitos do PDF | 7, 11 |
| `docs/00_entendimento_e_plano.md` | "63" no lugar de "47"; prorrogação até meia-noite de 19/10; decisões de hoje com motivo | 7, 12 |

**Reprodutibilidade.** Boa: `rodar_analises.sh` regenera tudo sem LLM, e cada chamada a modelo está gravada em `runs/`. Falta um `requirements.txt` com versões, mesmo que aproximadas. O provedor `claude_cli` depende de assinatura; o README já oferece `--provedor anthropic`, basta dizer que o custo de uma reexecução completa pela API é o da tabela.

**Fechamento**

1. Rodar `bash rodar_analises.sh` e `python src/63_validar_entrega.py`.
2. Conferir o PDF: 5 páginas, memo inteiro na última, tabela do anexo sem células vazias.
3. Conferir que `anexos/` segue idêntico ao oficial.
4. Commit, tornar o repositório público, abrir o link numa janela anônima.
5. E-mail para carla@viciodeumaestudante.com.br com o link e cinco linhas: o que foi entregue, 217 publicadas de 359, precisão prevista com intervalo, as variantes e uma frase sobre a prorrogação combinada.

## 8. Pesquisa e desenvolvimento depois da entrega

Quinze frentes, em ordem de valor para a precisão e para a cobertura. As quatro primeiras resolvem a fraqueza central: hoje nenhuma evidência de precisão vem de fora da família Claude.

| # | Frente | Por que vale | Esforço |
| --- | --- | --- | --- |
| 1 | Rotulagem por professor de 100 questões, estratificadas por decisão, nível e disciplina | único estimador sem viés; dá precisão por estrato e as regras de fronteira de graça | 3 a 4 h de professor |
| 2 | Segunda família nas 359 questões, em 2 estágios, fora da regra de publicação | E2 com n perto de 217 e sem circularidade; depois vira votante | menos de US$ 5 pela API; 1 h |
| 3 | Auditoria cega por outra família e por uma pessoa, na mesma amostra | mede a ancoragem do auditor Claude e dá um E3 limpo | 2 h |
| 4 | Perguntar à equipe sobre os 20 temas 67xx e as três convenções (prisão, ação penal, erro de tipo e de proibição) | remove o maior risco da previsão com um e-mail | 10 min |
| 5 | Dawid-Skene por família, não por rodada: agrupar os anotadores Claude como um só | E1 deixa de ser um teto trivial | 2 h |
| 6 | Precisão e limiar por estrato: publicar mais onde a evidência é forte (Legislação Especial, 67% publicadas) e menos onde é fraca (Criminologia, 50%) | cobertura sobe sem furar os 95% no total | 3 h |
| 7 | Auto-consistência: 3 amostras do Sonnet 2 estágios por questão | sinal de confiança barato; confere a calibração da confiança auto-reportada | US$ 20; 2 h |
| 8 | Medir a ancoragem do árbitro: rodá-lo sem candidatos em 80 questões, e com um candidato falso plausível | diz se o árbitro é um terceiro voto ou um juiz | 1 h |
| 9 | Regras de fronteira como texto no prompt e exemplos rotulados pelo professor; reclassificar as 56 "fronteira" | é onde está a cobertura perdida | 2 h depois do item 1 |
| 10 | Pré-filtro de embeddings mais 2 estágios, de ponta a ponta | mede a perda real de acerto e o ganho de custo; hoje só o recall@20 de 93% está medido | 3 h |
| 11 | Destilação com rótulos revisados: regressão logística sobre bge-m3 | define quando o LLM sai dos ramos fáceis | 2 h depois do item 1 |
| 12 | Política para as 44 multi-tema, decidida com o professor: tema mais amplo de nível 1 ou marcação miscelânea | 12% das questões estão paradas por falta de política, não de modelo | 1 h |
| 13 | Qualidade das sugestões em `revisar`: fração aceita pelo professor sem mudança | mede o valor da fila, não só o das publicadas | depende do item 1 |
| 14 | Jev (TypeSafe) como votante com probabilidades calibradas | integração pronta em `33_classificar_jev.py` | 1 h com chave |
| 15 | Prompt plano com pré-filtro em vez dos 211 mil tokens | mesmo custo com cache, menos latência e menos risco de contexto | 2 h |

**Como medir se melhorou.** Sempre contra o mesmo conjunto rotulado do item 1, com precisão, cobertura e intervalo de Wilson, e sempre comparando com a entrega de 19/10 como baseline.

## 9. Entrevista

Catorze perguntas que um avaliador exigente faria, com o que preparar para cada uma. As cinco primeiras são quase certas.

| # | Pergunta | O que preparar |
| --- | --- | --- |
| 1 | Os limiares foram escolhidos olhando a auditoria, e a auditoria mede a precisão final. Como separa as duas coisas? | Reconhecer. Mostrar a auditoria cega nova e o efeito em E3. Se não fez, dizer qual seria o efeito esperado e por que o intervalo cobre. |
| 2 | Por que 10% para o cenário das cópias, e por que só as 8 da Legislação Especial? Qual a precisão se a equipe usou "Teoria da Pena (Parte 2)"? | Levar a tabela dos 13 temas. Argumentos: descrição vazia, sem histórico, origem com "(Parte 02)". Precisão no cenário: cerca de 80% só com as cópias, cerca de 60% com todos os gêmeos. |
| 3 | Por que a entrega principal é o híbrido se o nível 1 tem a mesma cobertura e a mesma previsão? | Se mudou para nível 1: explicar a régua. Se manteve: dizer o que o aluno ganha e quanto de precisão esperada custa. |
| 4 | Pela sua tabela, nível 1 com 0,85 publica 249 com previsão 96,2%. Por que deixou 32 na fila? | E3 cai de 97,8% para 96,3% e a estimativa já é otimista. A régua é eliminatória. Dizer com que evidência subiria para 0,85. |
| 5 | O árbitro vê os candidatos e concorda em 99,7%. O que ele acrescenta? | Confiança calibrada (0,89 contra 0,65 na divergência), justificativa para o professor, uma escolha fora dos candidatos. Admitir a ancoragem e propor o experimento sem candidatos. |
| 6 | O que foi julgamento seu e o que foi do assistente? Um exemplo em que contrariou a IA. | Lista de decisões do diário: busca em concorrentes, modelos menores, nível 1, não rotular sem conhecimento jurídico, limiares. |
| 7 | Em 98 das 140 revisões os três modelos concordam no ramo. Que regra barata libera parte delas? | As 56 "fronteira": uma regra escrita pelo professor por par confundível. Estimar quantas publicaria e a que precisão. |
| 8 | Como o pipeline trata um tema novo sem histórico, e os 22 temas de nível 1 que não receberam questão? | Enriquecimento cobre temas vazios; embeddings do tema entram no pré-filtro; monitorar temas que nunca recebem questão. |
| 9 | Quanto custou de verdade, e precisa de Opus com 211 mil tokens de prompt? | Mais de US$ 200 em tokens a preço de lista pela assinatura. Não precisa: Sonnet 2 estágios empata no experimento; a cascata de produção não usa o plano. |
| 10 | Por que Dawid-Skene com anotadores tão correlacionados? | É teto declarado; serve para ranquear; sensibilidade à concentração e à origem é nula; proposta de agrupar por família. |
| 11 | Se a precisão real vier abaixo de 95%, onde você acha que errou e o que faria? | Ordem: cópias 67xx, convenções de prisão e ação penal, subtema irmão. Resposta: variante sem duplicados e nível 1, depois regras do professor. |
| 12 | Como lidou com o prazo? | Prorrogação combinada até meia-noite de 19/10; o que foi feito depois de domingo e por quê. |
| 13 | Com um professor por duas horas, o que pediria? | O memo: qual dos temas duplicados, regras de fronteira, 100 rótulos estratificados. Nessa ordem. |
| 14 | Qual é a política para questões sem tema central? | Hoje 44 em revisar. Proposta: tema mais amplo de nível 1 quando há eixo comum; marcação miscelânea quando não há. Decisão do professor. |

**Como se preparar.** Reler o diário e a tabela de sensibilidade. Ter na cabeça cinco números: 217 de 359, 0,96 com 0,85 a 0,99, 38 expostas às cópias, 99,7% do árbitro, US$ 0,03 por questão em produção. Dizer "não sei, mediria assim" quando for o caso.

## 10. Apêndice: o que foi verificado e como

Tudo foi conferido em 19/10 numa cópia do repositório, sem alterar o original. Ferramentas: Python 3.10, poppler (pdftotext, pdftoppm), git.

**Formato.** `python src/63_validar_entrega.py`: os três CSVs com 359 linhas, colunas, ids, decisões, temas usáveis, extras ativos, confiança em [0, 1] e motivos obrigatórios. Sem erros.

**Reconstrução.** `bash rodar_analises.sh` na cópia, 30 segundos, sem LLM. Vinte e um arquivos byte a byte iguais aos do repositório: os três CSVs, previsao.txt, relatorio.md, comparacao_metodos.md, sensibilidade.md, diagnostico.md, embeddings.md, os três previsao*.json, comparacao_metodos.json, confiabilidade.json, diagnostico.json, pares_confundiveis.json, embeddings.json, os três decisoes*.jsonl e confiabilidade.jsonl. Texto do PDF idêntico, 5 páginas.

**Amostra de 10 publicadas**, semente 20261019.

| Questão | Tema publicado | Juízo |
| --- | --- | --- |
| Q0251 | Penal > Punibilidade | correto |
| Q0138 | Penal > Teoria da Pena | correto; origem "Teoria da Pena (Parte 02)", gêmeo 67xx |
| Q0310 | PP > Lei Processual no Tempo e no Espaço | correto |
| Q0049 | Crimes contra a Vida > Induzimento ao Suicídio | correto |
| Q0086 | Crimes contra a Adm. Pública > Corrupção Passiva | correto |
| Q0203 | Leg. Especial > Lavagem de Dinheiro | correto; exposta à cópia 67xx |
| Q0233 | Iter Criminis > Desistência Voluntária | correto |
| Q0128 | PP > Ação Penal | plausível; "ação de prevenção penal" pode ir para Medida de Segurança ou Ação Penal de Penal |
| Q0115 | Criminologia > Teorias Sociológicas | correto |
| Q0308 | PP > Inquérito Policial | correto |

**Medições feitas nos dados**

- Árbitro: concorda com Opus plano e Sonnet 2 estágios em 315 de 316 casos em que eles concordam; confiança média 0,89 nesses casos e 0,65 nos outros; escolheu fora dos candidatos uma vez.
- GPT-5.5: 63 questões; 39 publicadas com voto dele; 5 em ramos confundíveis, onde a unanimidade dele era exigida; 34 de 34 concordam fora deles; as 2 discordâncias estão em revisar.
- Dawid-Skene: anotadores são as 8 rodadas de classificação e a origem, sem o árbitro; E1 de 0,9876 a 0,9881 com concentração 0,0, 0,5 e 0,8 e sem a origem.
- Exposição 67xx: 38 publicadas nas 8 cópias da Legislação Especial, 17,5%; mais 47 nos gêmeos "(Parte N)" e Provas em Espécie, 21,7%.
- Publicadas no subtema: 69, nenhuma viola a regra declarada. Extras: nenhum em tema inativo ou 67xx. Revisar sem árbitro: 0.
- Revisar: 140; em 98 os três concordam no ramo; razões principais: fronteira 56, discordância 40, multi-tema 31, confundível 11, dúvida com fora 2. Multi-tema pelo árbitro: 44, todas em revisar.
- Confiança: publicadas de 0,93 a 0,97; 6 revisar com 0,93 ou mais; 3 motivos com 240 caracteres.
- Auditoria: 60 questões, 9 duvidosas; 46 seguem publicadas com 3 duvidosas; o caderno mostra votos e justificativa do árbitro em todas as 60.
- Custo registrado pelo `claude -p` a preço de lista: Opus plano 63,8; Sonnet 2 estágios 53,0; Sonnet 3 estágios 53,5; árbitro 32,2; total acima de US$ 200 nas quatro rodadas principais.
- Commits: de 18/10 23h34 a 19/10 15h36, 19 commits, autor lpmu06.
- Vazamentos em arquivos rastreados: `estudo_movai.md` com caminhos e nomes do empregador; `runs/gpt-5.5/_usage.json` com id de organização OpenAI; nenhuma chave.

**O que não foi possível verificar.** A precisão real contra o gabarito da equipe; a cobertura que a equipe vai contar; se o repositório público e o e-mail foram enviados.
