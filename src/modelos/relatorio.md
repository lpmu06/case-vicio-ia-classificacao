# Relatório — Case "Classificação de tópicos"

Luis Paulo · lpmu06@gmail.com · 19/10/2026 · código, dados e saídas brutas de todos os modelos neste repositório

| Resultado | Valor |
|---|---|
| Publicadas | **«PUB» de 359 («COB»)**: «PUB2» no subtema e «PUB1» no tema de nível 1 |
| Para revisão do professor | «REV», cada uma com a sugestão do revisor automático e o motivo da dúvida |
| Fora da árvore | «FORA» (imposto estadual; crimes da Lei Geral do Esporte) |
| Precisão prevista nas publicadas | **«PREC»**, intervalo de «PREC_LO» a «PREC_HI» |
| Variante sem os temas duplicados | «VAR_PUB» publicadas («VAR_COB»), precisão prevista «VAR_PREC» (`publicacao_sem_duplicados.csv`) |

## a) Como pensamos

**O problema não é classificar; é saber quando não confiar.** Um LLM acerta a maior parte das questões, mas a régua exige 95% de acerto nas publicadas, sem gabarito. Isso é *predição seletiva*: o valor está em separar as questões quase certas das que precisam de um professor e em estimar a própria taxa de erro sem rótulos.

**Três leituras da régua guiaram o desenho.**
- Só as publicadas contam. Revisar e fora custam cobertura, não precisão.
- Acerto inclui pai e filho do tema do especialista, mas não o irmão. Quando o ramo é certo e o subtema é duvidoso, publicar no tema de nível 1 é correto e honesto com o aluno, que vê a questão ao estudar o tema. Publicamos no subtema só com evidência forte, porque é isso que serve a quem estuda "Juiz das Garantias" e não "Inquérito Policial". A variante `publicacao_nivel1.csv` põe tudo no nível 1, com a mesma cobertura e sem risco de irmão.
- A própria previsão é avaliada, então ela precisa ser conservadora e explicada.

**O que testamos, do simples ao caro.**

| Abordagem | O que aconteceu | Ficou? |
|---|---|---|
| Copiar a origem (`assunto_origem` → tema pelo título) | 225 questões têm um tema de título igual, mas só 30% caem no mesmo ramo que o consenso dos modelos. "Concurso de Crimes" rotula 43 questões, quase todas sobre outra coisa | Só como voto fraco e diagnóstico |
| Similaridade de embeddings, 8 modelos (jurídicos brasileiros, portugueses e multilíngues) | Comparar a questão com o nome do tema cria lixeiras: com o Legal-BERTimbau cru, 39% das questões caem num único tema, o mesmo efeito do nosso estudo anterior com andamentos processuais (38%). O melhor modelo, bge-m3, multilíngue e não jurídico, acerta o ramo em 64% e traz o ramo certo entre os 20 primeiros em 93% | Como pré-filtro em produção, não como decisor ([anexo](embeddings.md)) |
| Enriquecer a taxonomia | 337 de 377 descrições eram texto gerado. Um LLM escreveu descrição, palavras-chave, artigos de lei e "não confundir com" para os 351 temas usáveis. Isso melhora todos os embeddings em 10 a 20 pontos | Sim, é a base de tudo |
| LLM com a árvore inteira no prompt ("plano") | Funciona, mas o prompt tem 211 mil tokens por questão | Sim, como classificador principal |
| LLM em camadas: 2 estágios (tema, depois subtema) e 3 estágios (grupo, tema, subtema) | Ver o experimento abaixo. 2 estágios fica no mesmo patamar do plano com um prompt 10 vezes menor; 3 estágios perde alguns pontos | 2 estágios sim; 3 estágios não |
| Modelos menores (Sonnet, Haiku) | Em 2 estágios, o Sonnet empata com o Opus; o Haiku fica alguns pontos atrás | Sonnet em 2 estágios é um dos dois votantes |
| Árbitro (Opus, esforço alto) | Escolhe entre os candidatos de todos, embaralhados, sem saber a maioria. Concorda com o consenso em 99,7% dos casos em que os dois classificadores principais concordam, e baixa a confiança de 0,89 para 0,65 quando eles divergem; só uma vez escolheu fora dos candidatos, o que indica alguma ancoragem | Sim, como filtro e como sugestão para o professor |
| Buscar a questão em bancos de outros sites | As questões estão na web, mas usar a classificação de um concorrente não nos pareceu correto | Descartado |

**Experimento de camadas.** Em 80 questões sorteadas, cruzamos modelo e método. A tabela mostra o quanto cada um acompanha a maioria dos demais classificadores, sem contar a si mesmo; não é acurácia, é consistência.

| Método | Modelo | Acompanha a maioria | Tokens de prompt por questão | US$ por questão, com cache |
|---|---|---|---|---|
| Plano | Opus 5.5 | «LOO_OPUS» | 211.517 | 0,054 |
| Plano | Sonnet 5 | «LOO_SONNET_P» | 211.517 | 0,050 |
| 2 estágios | Opus 5.5 | «LOO_OPUS_H» | 22.460 | 0,058 |
| 2 estágios | Sonnet 5 | «LOO_SONNET_H» | 20.790 | 0,031 |
| 2 estágios | Haiku 4.5 | «LOO_HAIKU_H» | «TOK_HAIKU_H» | «USD_HAIKU_H» |
| 3 estágios | Sonnet 5 | «LOO_S3N» | «TOK_S3N» | «USD_S3N» |
| 3 estágios | Haiku 4.5 | «LOO_HAIKU_3N» | - | - |

A segunda camada compensa: o prompt cai dez vezes e a consistência praticamente não cai. A terceira não compensa: cada etapa a mais é uma chance a mais de errar sem volta, e grupos de temas criados à mão não têm fronteiras naturais. Com cache, o prompt plano gigante custa quase o mesmo que o de 2 estágios, porque a parte fixa é lida do cache a um décimo do preço; sem cache, custaria 15 vezes mais. O Haiku sai caro aqui só porque, pelo Claude Code, gera milhares de tokens de raciocínio; pela API, sem raciocínio estendido, custaria uma fração disso. Tabelas completas no [anexo](comparacao_metodos.md).

**Becos sem saída.** Começamos pelo modelo mais caro com o prompt maior e esgotamos os créditos da OpenAI em 63 questões; a lição é medir custo em cinco questões antes de escalar. A rotulagem humana de uma amostra, que seria o caminho mais sólido para a previsão, não foi possível, então a estimativa é cega. A primeira regra de unanimidade nos ramos confundíveis não tinha efeito com só dois votantes; corrigimos para exigir a concordância de todas as rodadas.

**Como estimamos a precisão sem gabarito.** Nenhum estimador sozinho é confiável, então usamos três, com hipóteses declaradas, e dois descontos para o que nenhum deles vê.

| Estimador | Hipótese | Nas publicadas |
|---|---|---|
| Dawid-Skene sobre todos os classificadores e a origem | Erros independentes; é um limite superior | «E1» |
| Concordância com o GPT-5.5, a única família diferente | Famílias diferentes erram de forma pouco correlacionada; amostra pequena | «E2» |
| Auditoria cética, por IA, de 60 publicadas sorteadas | Um leitor cuidadoso acha os erros visíveis; dúvida conta 1/3 de erro | «E3» («E3_N» seguem publicadas após os limiares finais) |
| Desconto de convenção | O professor pode arquivar diferente de qualquer modelo | −2 pontos nos dois primeiros |
| Desconto das cópias da Legislação Especial | 10% de chance de a equipe ter usado as cópias recentes em Penal; «EXPO» das publicadas expostas | −«M67» pontos em todos |

A previsão é a mediana dos três estimadores ajustados: **«PREC»**. O intervalo vai do pior limite inferior de 95% («PREC_LO») ao estimador sob independência («PREC_HI»). Se a equipe tiver rotulado nas cópias, a precisão real cairia para cerca de «PREC_67». Os limiares finais vieram da [análise de sensibilidade](sensibilidade.md): exigir confiança 0,90 do árbitro em vez de 0,80 corta 11 pontos de cobertura, mas 5 das 9 dúvidas da auditoria estavam nessa faixa, e o limiar de 0,90 no subtema neutraliza uma sexta, de subtema irmão; subir para 0,95 corta mais 16 pontos sem ganho visível.

## b) Diagnóstico: o que atrapalha máquina e humano

**Nos dados das questões.**
- O texto útil exige as alternativas: 11 enunciados são só "Assinale a alternativa correta".
- A origem é ruidosa: 18 assuntos vazios, 9 disciplinas fora do recorte, nomes de aula como "Ação Penal (Parte 01)" e rótulos trocados. A disciplina de origem diverge da do consenso em 48 questões, quase sempre leis especiais rotuladas como Penal ou Processo Penal.
- HTML cru, `\n` literal e, numa questão, 100 mil caracteres de lixo do Word.

**Na árvore.**
- **Assuntos com dois endereços.** Prisão aparece em "Teoria Geral das Prisões" e em "Prisões em Espécie"; sentença, em "Sentença Penal" e em "Procedimento Ordinário > Sentença"; ação penal, em Penal e em Processo Penal, cada uma com subtemas de ação pública e privada; juizados, em Legislação Especial e em "Procedimento Sumaríssimo". Foi a principal fonte de dúvida na auditoria.
- **Cópias recentes.** 20 temas com ids 67xx: oito copiam temas da Legislação Especial dentro de Penal ou Processo Penal; os outros são nomes de aula, "(Parte 1)" e "(Parte 2)". Nenhum tem descrição nem histórico. Tratamos todos como não utilizáveis.
- **Lixeiras.** Temas genéricos acumulavam centenas de questões, como Sistemas e Princípios Processuais Penais (538) e Introdução ao Estudo do Direito Penal (424). Na nossa classificação, só 8 das 359 questões têm um desses temas genéricos como tema central.
- **Descrições.** 337 de 377 eram texto gerado; há erros de grafia ("Crimonológicas", "Estaturo de Idoso", "Comeptência").

**Onde está a dificuldade.** Medimos pela unanimidade entre classificadores, uma medida de dificuldade que não depende de gabarito ([anexo](diagnostico.md)).

| Tipo de questão | Unânimes | Publicadas |
|---|---|---|
| Múltipla escolha («N_ME») | «D_ME_U» | «D_ME_P» |
| Certo ou errado («N_CE») | «D_CE_U» | «D_CE_P» |
| Alternativas sobre institutos diferentes, segundo algum classificador («N_MT») | «D_MT_U» | «D_MT_P» |
| As demais | «D_NMT_U» | «D_NMT_P» |

Questões multi-tema e de certo ou errado são as mais difíceis: as primeiras não têm tema central, e as segundas trazem uma afirmação curta com pouco contexto. Os pares de ramos que os modelos mais confundem foram: «PARES». São fronteiras em que até professores divergem, e nelas exigimos unanimidade para publicar.

## c) Produção: 50 mil questões por semana

**Reclassificar só o que mudou.** Rodar as 50 mil toda semana desperdiça dinheiro. O fluxo classifica as importações novas, reclassifica os ramos cuja descrição ou estrutura mudou e audita uma amostra do resto.

**Cascata, do barato ao caro.**
1. **Importação**: limpeza de HTML, deduplicação por hash e extração dos dispositivos citados por regex. A origem entra como metadado, nunca como rótulo.
2. **Pré-filtro por embeddings** (bge-m3 local, custo desprezível): os 20 temas mais parecidos contêm o ramo certo em 93% dos casos e encurtam o prompt.
3. **Classificador principal em 2 estágios** com modelo de porte médio, pela API em lote (metade do preço) e com cache: cerca de US$ 0,016 por questão.
4. **Segunda opinião de outra família** em todas, com modelo pequeno, para ter concordância entre famílias: cerca de US$ 0,005.
5. **Árbitro forte só onde há dúvida**: divergência, confiança baixa ou ramo confundível, cerca de um terço das questões, a US$ 0,025 por chamada em lote: cerca de US$ 0,008.
6. **Publicação** pelas regras deste case; o resto vai para a fila do professor com a sugestão e o motivo.

O total fica em torno de **US$ 0,03 por questão**, ou US$ 1.500 por semana se todas as 50 mil passassem pela cascata; classificando só as novas, é uma fração disso. Os números vêm dos tokens medidos neste case ([anexo](comparacao_metodos.md)).

**Destilação.** Os rótulos confirmados pelo professor treinam um classificador leve sobre embeddings. Com só os 227 rótulos de consenso deste case, ele já reproduz o consenso em 60% dos casos. Com alguns milhares de rótulos revisados, deve assumir os ramos fáceis e virar mais um voto nos demais.

**Qualidade contínua.**
- Auditoria semanal de 100 publicadas sorteadas, feita por professor, com intervalo de confiança: é o único estimador sem viés.
- Painel com taxa de revisão, concordância entre modelos e distribuição por tema. Um salto num tema sinaliza mudança no banco ou na árvore.
- Reportes de alunos entram como rótulo negativo prioritário. Um tema com reportes acima do normal sai da publicação automática até ser revisado.
- A fila do professor é ordenada por impacto, com os temas mais estudados e as menores confianças primeiro. Cada decisão dele realimenta as descrições dos temas e o classificador destilado.

## d) Memo para o professor

Em [`memo_professor.md`](memo_professor.md), uma página.

## Anexo: modelos, tempo e custo desta execução

| Etapa | Modelo | Questões | Tempo de parede |
|---|---|---|---|
| Enriquecimento da taxonomia | GPT-5.5 | 89 chamadas | 8 min |
| Classificador plano | Opus 5.5 | 359 | 18 min |
| Classificador 2 estágios | Sonnet 5 | 359 | 59 min |
| Classificador 3 estágios | Sonnet 5 | «S3N_N» | várias horas, em paralelo com as demais |
| Árbitro | Opus 5.5, esforço alto | 359 | 4,8 h, em paralelo com as demais |
| Experimento 2×2 e Haiku | Sonnet 5, Opus 5.5, Haiku 4.5 | 80 | várias horas |
| GPT-5.5 plano | GPT-5.5 | 63, até acabar o crédito | 8 min |

Os modelos Claude foram chamados pelo Claude Code em modo headless, numa assinatura, sem custo marginal; a lentidão veio de dividir a cota da assinatura entre rodadas paralelas. A preço de lista da API, com cache e sem o contexto do Claude Code, o pipeline final (Opus plano, Sonnet 2 estágios e árbitro) custaria cerca de US$ 48 para as 359 questões, ou US$ 24 pela API em lote. Os créditos da OpenAI foram de teste e se esgotaram.

**O que faríamos com mais tempo.** Rotular 100 questões com um professor para calibrar de verdade; rodar uma segunda família de modelos em todas as questões; testar o Jev, um modelo de decisão estruturada com probabilidades calibradas, cuja integração está pronta em `src/33_classificar_jev.py` e só depende de uma chave; e perguntar à equipe qual dos temas duplicados ela usa.
