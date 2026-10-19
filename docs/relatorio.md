# Relatório — Case "Classificação de tópicos"

Luis Paulo · lpmu06@gmail.com · outubro de 2026 · código e dados em github.com/lpmu06/case-vicio-ia-classificacao

| Resultado | Valor |
|---|---|
| Publicadas | «PUB» de 359 («COB»), sendo «PUB2» no subtema e «PUB1» no tema de nível 1 |
| Para revisão do professor | «REV», cada uma com a sugestão do árbitro e o motivo da dúvida |
| Fora da árvore | «FORA» |
| Precisão prevista nas publicadas | «PREC» (intervalo «PREC_IC») |
| Custo para reproduzir via API | «CUSTO_TOTAL»; em produção, «CUSTO_Q» por questão |

## a) Como pensamos

**O problema não é classificar, é saber quando não confiar.** Um LLM acerta a maior parte das questões, mas a régua é precisão de 95% nas publicadas, sem gabarito. Isso é um problema de *predição seletiva*: o valor está em separar as questões quase certas das que precisam de um professor, e em estimar a própria taxa de erro sem rótulos.

**Três leituras da régua guiaram o desenho.** Primeiro, só as publicadas contam; revisar e fora custam cobertura, não precisão. Segundo, acerto inclui pai e filho do tema do especialista, mas não o irmão. Então, quando o ramo é certo e o subtema é duvidoso, publicar no tema de nível 1 é correto e honesto com o aluno, que vê a questão ao estudar o tema. Pela régua, publicar sempre no nível 1 nunca perde; publicamos no subtema só quando a evidência é forte, porque é isso que torna a questão útil para quem estuda "Juiz das Garantias" e não "Inquérito Policial". O arquivo `publicacao_nivel1.csv` mostra a variante que maximiza a régua. Terceiro, a própria previsão é avaliada, então ela precisa ser conservadora e explicada.

**O que testamos, do simples ao caro.**

| Abordagem | O que aconteceu | Ficou? |
|---|---|---|
| Copiar a origem (`assunto_origem` → tema pelo título) | Só «ORIG_MATCH» questões têm um tema correspondente, e nelas a origem concorda com o consenso dos modelos em apenas «ORIG_AG» dos ramos. Ex.: "Concurso de Crimes" rotula 43 questões, quase todas sobre outra coisa | Só como voto fraco e diagnóstico |
| Similaridade de embeddings, 11 modelos | Ver tabela abaixo. Comparar a questão com o nome do tema cria lixeiras, como no nosso estudo anterior com andamentos processuais, em que 38% dos itens caíram numa única categoria. Com a taxonomia enriquecida, o melhor modelo acerta o ramo em «EMB_TOP1» e traz o ramo certo entre os 10 primeiros em «EMB_R10» | Como pré-filtro em produção, não como decisor |
| Enriquecer a taxonomia | 337 de 377 descrições eram texto gerado ("N questões no source"). Um LLM escreveu descrição, palavras-chave, artigos de lei e "não confundir com" para os 351 temas usáveis | Sim; é o que separa "Fato Típico" de "Tipicidade" |
| LLM com a árvore inteira no prompt (plano) | Funciona bem, mas o prompt tem 211 mil tokens por questão | Sim, como classificador principal |
| LLM em 2 e 3 estágios (tema → subtema; grupo → tema → subtema) | Prompt 10 a 15 vezes menor. A concordância com o plano caiu, e o experimento 2×2 mostrou que «CONCL_2X2» | Sim, como votos independentes e desenho de produção |
| Modelos menores (Sonnet, Haiku) | «CONCL_MODELOS» | Como votos |
| Árbitro (Opus, esforço alto) | Escolhe entre os candidatos de todos, embaralhados, sem saber a maioria. Concorda com o consenso em 99,5% dos casos em que os dois classificadores principais concordam, e baixa a confiança de 0,89 para 0,63 quando eles divergem | Sim, como filtro e como sugestão para o professor |
| Buscar a questão em bancos de outros sites | As questões existem na web, mas usar a classificação de um concorrente não pareceu correto, e o site bloqueia acesso automatizado | Descartado |

**Becos sem saída que valem registro.** Começamos pelo modelo mais caro com o prompt maior e esgotamos os créditos da OpenAI em 63 questões: a lição é medir custo em cinco questões antes de escalar. A rotulagem humana de uma amostra, que seria o caminho mais sólido para a previsão, não foi possível, então a estimativa é cega. No esforço médio, o Haiku gastava cerca de 10 mil tokens de raciocínio por questão, o que anula a vantagem de ser barato.

**Como estimamos a precisão sem gabarito.** Nenhum estimador sozinho é confiável, então usamos quatro e declaramos as hipóteses:

| Estimador | Hipótese | Resultado nas publicadas |
|---|---|---|
| Dawid-Skene sobre todos os classificadores e a origem | Erros independentes; é um limite superior | «E1» |
| Concordância com o GPT-5.5, a única família diferente | Erros de famílias diferentes são pouco correlacionados; só 63 questões | «E2» |
| Auditoria cética por IA de uma amostra aleatória de «AUD_N» publicadas | Um leitor cuidadoso acha os erros visíveis; é IA, não especialista | «E3» |
| Margem de convenção | O professor pode seguir convenções que nenhum modelo conhece | desconto de «MARGEM» |

A previsão é o menor dos estimadores menos a margem: «PREC», com intervalo «PREC_IC». A cobertura é escolha nossa e quase determinística: «COB».

## b) Diagnóstico: o que atrapalha máquina e humano

**Nos dados das questões.** O texto útil exige as alternativas: 11 enunciados são só "Assinale a alternativa correta". A origem é ruidosa: 18 assuntos vazios, 9 disciplinas fora do recorte, nomes de aula ("Ação Penal (Parte 01)") e rótulos trocados; a disciplina de origem diverge da do consenso em «DISC_DIV» questões. Há HTML cru e, numa questão, 100 mil caracteres de lixo do Word.

**Na árvore.** 20 temas criados por importação têm nomes de aula, "(Parte 1)", "(Parte 2)", e não dizem o que se estuda. Oito títulos se repetem em disciplinas diferentes, como Lei Maria da Penha em Penal e em Legislação Especial, e errar o ramo é erro mesmo com o assunto certo. Temas genéricos acumulam centenas de questões de origem, como Sistemas e Princípios Processuais Penais (538) e Introdução ao Estudo do Direito Penal (424). Faltam descrições em 337 temas.

**Onde está a dificuldade.** Medimos pela concordância entre classificadores:
- «DIAG_TIPO»
- «DIAG_MULTI»
- «DIAG_DISC»
- Pares de ramos que os modelos confundem entre si: «PARES». São fronteiras em que até professores divergem, como progressão de regime (Lei de Execução Penal ou Teoria da Pena) e princípio da insignificância (Princípios do Direito Penal ou Tipicidade). Nesses ramos exigimos unanimidade para publicar.

## c) Produção: 50 mil questões por semana

**Custo medido por questão** (preço de lista da API, system prompt em cache):

«TABELA_CUSTO»

**Desenho proposto.**
1. **Importação**: limpeza de HTML, deduplicação por hash e extração de dispositivos citados por regex. A origem entra como metadado, nunca como rótulo.
2. **Taxonomia como produto**: cada tema com descrição, palavras-chave, dispositivos e "não confundir com", mantidos pelo professor. Temas-bucket e duplicados bloqueados para publicação automática. Mudar a árvore reclassifica só os ramos afetados.
3. **Classificação em cascata**: embeddings selecionam os candidatos; um modelo barato classifica em 2 estágios; um modelo forte de outra família vota em paralelo só onde o barato tem confiança baixa ou o ramo é confundível. Concordância publica; divergência vai para a fila com as duas sugestões. Com «PCT_FORTE» das questões indo ao modelo forte, o custo fica em torno de «CUSTO_Q» por questão, ou «CUSTO_SEMANA» por semana.
4. **Destilação**: os rótulos confirmados pelo professor treinam um classificador leve sobre embeddings. No nosso experimento, com rótulos de consenso, ele já reproduz o consenso em «DESTIL» dos casos. Onde atingir a precisão alvo, substitui o LLM barato; nos demais, vira mais um voto.
5. **Qualidade contínua**: auditoria semanal de 100 publicadas por professor, com intervalo de confiança; monitoramento da taxa de revisão, da concordância entre modelos e da distribuição por tema; reportes de alunos entram como rótulo negativo prioritário, e um tema com reportes acima do normal sai da publicação automática até ser revisado.
6. **Fila do professor**: ordenada por impacto, com os temas mais estudados e as menores confianças primeiro. Cada decisão realimenta as descrições dos temas e o classificador destilado.

## d) Memo para o professor

Em [`memo_professor.md`](memo_professor.md), uma página.

## Anexo: modelos, tempo e custo desta execução

«ANEXO»
