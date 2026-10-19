# Amostra para rotulagem humana

Para cada questão, escreva em `data/rotulos_humanos.csv` o `tema_id` que um professor atribuiria (nível 2 se houver subtema claro; nível 1 se a questão for genérica do tema; `FORA` se nenhum tema serve). A decisão dos modelos está escondida de propósito logo abaixo dos candidatos; tente decidir antes de olhar.


---

## Q0005  (origem: Direito Penal / Fixação do regime inicial da pena privativa de liberdade)

```
Carlos foi denunciado pelo crime de furto qualificado,
praticado em 15/5/2022. Após a tramitação regular do processo,
o juiz fixou a pena base no mínimo legal, tendo em seguida
agravado em 1/6 a pena em face da reincidência, sob o
fundamento de que o réu possuía uma condenação anterior
transitada em julgado, e impôs o regime fechado para início de
cumprimento de pena. Na condenação anterior, Carlos havia
recebido o livramento condicional em 27/4/2015, cumprindo-o
sem revogações até 27/4/2019, e a decisão que declarou extinta a
pena foi proferida em 29/6/2020.
Considerando-se a situação hipotética apresentada, bem como a
pena e o regime fixados pelo juiz, é correto afirmar que, em
relação ao crime de furto qualificado praticado em 15/5/2022,
Carlos é

(A) reincidente, e o regime inicial cabível é o fechado, visto que o\nperíodo depurador referente à condenação anterior começou a\ncorrer em 27/4/2019.
(B) reincidente, e o regime inicial cabível é o fechado, visto que o\nperíodo depurador referente à condenação anterior começou a\ncorrer em 29/6/2020.
(C) primário, e o regime inicial cabível é o semiaberto, visto que\no período depurador se iniciou em 27/4/2015 e a pena é\nsuperior a quatro anos.
(D) primário, e o regime cabível é o aberto, visto que o período\ndepurador foi cumprido sem revogação e a pena é inferior a\nquatro anos.
(E) reincidente, e o regime cabível é o semiaberto, visto que,\ndada a pena aplicada, incide no caso a súmula n.º 269 do STJ.
```

Candidatos (em ordem aleatória):

- 5201 · Penal > Teoria da Pena > Penas Privativas de Liberdade
- 5199 · Penal > Teoria da Pena
- 5203 · Penal > Teoria da Pena > Segunda Fase da Dosimetria: Agravantes e Atenuantes

<details><summary>decisão do ensemble</summary>publicar → 5199 · Penal > Teoria da Pena (conf 0.93) </details>


---

## Q0008  (origem: Direito Penal / Teoria da Pena (Parte 02))

```
A progressão de regime do cumprimento da pena de condenado por crime contra a administração pública condiciona-se à reparação do dano que ele causou, ou à devolução do produto do ilícito praticado, com os acréscimos legais.

(C) Certo
(E) Errado
```

Candidatos (em ordem aleatória):

- 5201 · Penal > Teoria da Pena > Penas Privativas de Liberdade
- 4703 · Direito Penal - Legislação Especial > Lei de Execução Penal
- 5199 · Penal > Teoria da Pena

<details><summary>decisão do ensemble</summary>revisar → 5201 · Penal > Teoria da Pena > Penas Privativas de Liberdade (conf 0.72) ramo certo, subtema incerto (claude-opus: Penas Privativas de Liberdade); confiança abaixo do limiar</details>


---

## Q0010  (origem: Direito Penal / Concurso de Crimes)

```
Com relação aos crimes contra o meio ambiente, assinale a opção correta, conforme entendimento do STJ e do STF.

(A) Considere que Gil, a fim de comemorar, durante a madrugada, em zona urbana, a vitória de determinado time de futebol, tenha ajustado o aparelho de som do veículo em volume muito acima do limite permitido na legislação local, perturbando o sono e o sossego da vizinhança, e que esta tenha acionado o órgão municipal responsável. Considere, ainda, que o referido aparelho de som tenha sido apreendido, e Gil, conduzido à delegacia de polícia. Nessa situação, a conduta de Gil é atípica, visto que a poluição sonora não está expressamente prevista na lei de crimes ambientais.
(B) O crime ambiental que consiste em impedir o nascimento de nova vegetação ou dificultar a regeneração natural de florestas e demais formas de vegetação é crime permanente, visto que a consumação do delito se protrai no tempo, violando o bem jurídico tutelado de forma contínua e duradoura, renovando-se, a cada momento a consumação, consoante entendimento do STF.
(C) Em se tratando dos crimes contra o meio ambiente, admite-se responsabilização penal unicamente da pessoa jurídica, salvo se a imputação for pela prática de delitos culposos.
(D) Os tribunais superiores, no que concerne aos crimes ambientais, rejeitam a incidência do sistema da dupla imputação ou sistema da imputação paralela dada a ocorrência de bis in idem na responsabilização, pelo mesmo crime, de mais de uma pessoa.
(E) O crime de deixar de cumprir obrigação de relevante interesse ambiental, previsto no rol dos crimes contra a administração pública ambiental, é crime omissivo próprio, punido apenas na forma dolosa, e se caracteriza quando o agente público deixa de praticar o ato, contrariando o dever legal de fazê-lo para evitar o resultado lesivo ao meio ambiente, consoante entendimento do STJ.
```

Candidatos (em ordem aleatória):

- 5066 · Penal > Concurso de Crimes
- 4688 · Direito Penal - Legislação Especial > Crimes contra o meio ambiente

<details><summary>decisão do ensemble</summary>publicar → 4688 · Direito Penal - Legislação Especial > Crimes contra o meio ambiente (conf 0.95) </details>


---

## Q0014  (origem: Disciplina Unificada / Medidas Socioeducativas)

```
Caso a decisão do magistrado em relação à internação de Pedro seja questionada em juízo, ela não pode ser sanada pela via do habeas corpus , pois tal instrumento processual não se aplica às situações que envolvam decisões tomadas por vara da infância e da juventude em detrimento da liberdade de criança ou adolescente.

(C) Certo
(E) Errado
```

Candidatos (em ordem aleatória):

- 4709 · Direito Penal - Legislação Especial > Violência contra Criança e Adolescente
- 5476 · Processo Penal > Ações Autônomas de Impugnação
- 5477 · Processo Penal > Ações Autônomas de Impugnação > Habeas Corpus

<details><summary>decisão do ensemble</summary>revisar → 5477 · Processo Penal > Ações Autônomas de Impugnação > Habeas Corpus (conf 0.54) ramo certo, subtema incerto (claude-opus: Habeas Corpus); confiança abaixo do limiar</details>


---

## Q0017  (origem: Processo Penal / Ação Penal (Parte 01))

```
No processo e julgamento dos crimes de responsabilidade dos funcionários públicos,

(A) nos crimes afiançáveis e inafiançáveis, após a denúncia, o juiz ordenará a notificação do acusado para responder por escrito, dentro do prazo de 15 (quinze) dias.
(B) nos crimes inafiançáveis, após a denúncia, o juiz ordenará a notificação do acusado para responder por escrito, dentro do prazo de 15 (quinze) dias.
(C) nos crimes afiançáveis e inafiançáveis, o eventual recebimento da denúncia é feito depois da notificação do acusado e, caso existente, de sua resposta.
(D) nos crimes afiançáveis, o eventual recebimento da denúncia é feito depois da notificação do acusado e, caso existente, de sua resposta.
(E) a falta de notificação do acusado para, se quiser, responder à acusação causa nulidade absoluta, conforme súmulas do Superior Tribunal de Justiça e do Supremo Tribunal Federal.
```

Candidatos (em ordem aleatória):

- 5533 · Processo Penal > Procedimento Ordinário > Defesa Preliminar
- 5530 · Processo Penal > Procedimento Ordinário

<details><summary>decisão do ensemble</summary>revisar → 5530 · Processo Penal > Procedimento Ordinário (conf 0.41) ramo certo, subtema incerto (claude-opus: nível 1); confiança abaixo do limiar</details>


---

## Q0020  (origem: Processo Penal / Ação Penal (Parte 02))

```
Assinale com V (verdadeiro) ou com F (falso) as seguintes afirmações sobre posições jurisprudenciais do Superior Tribunal de Justiça.
( ) Segundo jurisprudência dominante do Superior Tribunal de Justiça, é possível o reconhecimento do concurso material entre as condutas previstas nos artigos 241-A ( artigo 241-A Oferecer, trocar, disponibilizar, transmitir, distribuir, publicar ou divulgar por qualquer meio, inclusive por meio de sistema de informática ou telemático, fotografia, vídeo ou outro registro que contenha cena de sexo explícito ou pornografia envolvendo criança ou adolescente ) e artigo 241-B ( Adquirir, possuir ou armazenar, por qualquer meio, fotografia, vídeo ou outra forma de registro que contenha cena de sexo explícito ou pornográfica envolvendo criança ou adolescente ) do Estatuto da Criança e do Adolescente, uma vez os tipos penais são autônomos, com verbos e condutas distintas, sendo que o crime previsto no artigo 241-B do ECA não configura fase normal, tampouco meio de execução, para o crime previsto no artigo 241-A do ECA.
( ) Segundo jurisprudência dominante do Superior Tribunal de Justiça, é possível, na segunda fase da dosimetria da pena, a compensação integral da atenuante da confissão espontânea com a agravante da reincidência, mesmo que esta seja específica.
( ) Segundo jurisprudência dominante do Superior Tribunal de Justiça, atribuir-se falsa identidade perante a Autoridade Policial com a finalidade de ocultar maus antecedentes constitui o crime previsto no artigo 307, caput, do Código Penal ( atribuir-se ou atribuir a terceiro falsa identidade para obter vantagem, em proveito próprio ou alheio, ou para causar dano a outrem ). Esse tipo de conduta não é protegido pelo princípio constitucional da autodefesa (artigo 5 o , inciso LXIII, CF).
( ) Segundo jurisprudência dominante do Superior Tribunal de Justiça, a causa de aumento de pena relativa ao crime de furto pelo repouso noturno não se aplica em nenhuma das hipóteses do furto qualificado.
( ) Segundo jurisprudência dominante do Superior Tribunal de Justiça, é cabível a suspensão condicional do processo e a transação penal aos delitos que preveem a pena de multa alternativamente à pena privativa de liberdade, ainda que o preceito secundário da norma legal ultrapasse os parâmetros mínimos e máximos exigidos em lei para a incidência dos institutos em comento.
A sequência correta do preenchimento dos parênteses, de cima para baixo, é

(A) V – F – V – V – F.
(B) F – V – F – V – F.
(C) F – F – V – F – V.
(D) V – V – F – F – V.
(E) Nenhuma das alternativas anteriores está correta.
```

Candidatos (em ordem aleatória):

- 5157 · Penal > Dos Crimes Contra o Patrimônio
- 5199 · Penal > Teoria da Pena

<details><summary>decisão do ensemble</summary>revisar → 5199 · Penal > Teoria da Pena (conf 0.16) questão multi-tema (alternativas sobre institutos diferentes); ramo Teoria da Pena</details>


---

## Q0028  (origem: Processo Penal / Comunicação dos atos processuais)

```
O Código de Processo Penal, em seu art. 406, estabelece que o juiz, ao receber a denúncia ou a queixa, ordenará a citação do acusado para responder a acusação, por escrito, no prazo de dez dias.
O art. 409, do mesmo diploma legal, determina que, apresentada a defesa, o juiz ouvirá o Ministério Público ou o querelante sobre preliminares e documentos, em cinco dias.
Por sua vez, segundo o parágrafo primeiro, do art. 421, do referido Estatuto Processual, ainda que preclusa a decisão de pronúncia, havendo circunstância superveniente que altere a classificação do crime, o juiz ordenará a remessa dos autos ao Ministério Público.

(C) Certo
(E) Errado
```

Candidatos (em ordem aleatória):

- 5524 · Processo Penal > Procedimento do Tribunal do Júri
- 5526 · Processo Penal > Procedimento do Tribunal do Júri > Procedimento Bifásico do Tribunal do Júri
- 5527 · Processo Penal > Procedimento do Tribunal do Júri > Impronúncia, Desclassificação, Absolvição Sumária e Pronúncia

<details><summary>decisão do ensemble</summary>publicar → 5524 · Processo Penal > Procedimento do Tribunal do Júri (conf 0.93) </details>


---

## Q0039  (origem: Direito Penal - Legislação Especial / Concurso de Crimes)

```
Suponha que todos os revendedores de gás liquefeito de petróleo (GLP) ajustem artificialmente preço final de venda do produto em determinada localidade. A esse respeito, é correto afirmar que

(A) o ajuste é comum e em nada influencia na concorrência entre as empresas.
(B) há, em princípio, um ilícito penal a ser apurado que se subsumi ao crime contra o consumidor.
(C) o fato descrito encarta-se como crime contra a ordem econômica.
(D) a relação de consumo é afetada pela conduta descrita; portanto, há contravenção praticada contra a economia popular.
(E) a investigação a respeito do caso ficará a cargo da Polícia Federal, em virtude de que a União possui o monopólio de distribuição do GLP no Brasil.
```

Candidatos (em ordem aleatória):

- 4687 · Direito Penal - Legislação Especial > Crimes contra a Economia Popular
- 4695 · Direito Penal - Legislação Especial > Crimes Tributários

<details><summary>decisão do ensemble</summary>revisar → 4687 · Direito Penal - Legislação Especial > Crimes contra a Economia Popular (conf 0.45) ramo certo, subtema incerto (claude-opus: nível 1); confiança abaixo do limiar</details>


---

## Q0045  (origem: Penal / Concussão e Excesso de Exação , Crimes contra a administração pública)

```
No crime de excesso de exação, o crime é qualificado se

(A) praticado por funcionário público.
(B) cometido por meio vexatório ou gravoso, que a lei não autoriza.
(C) resulta dano para a Administração Pública ou para o administrado.
(D) o funcionário pratica ato de ofício, com infração de dever funcional, cedendo a pedido ou influência de outrem.
(E) o funcionário desvia, em proveito próprio ou de outrem, o que recebeu indevidamente para recolher aos cofres públicos.
```

Candidatos (em ordem aleatória):

- 5087 · Penal > Dos Crimes Contra a Administração Pública
- 5091 · Penal > Dos Crimes Contra a Administração Pública > Concussão e Excesso de Exação

<details><summary>decisão do ensemble</summary>publicar → 5091 · Penal > Dos Crimes Contra a Administração Pública > Concussão e Excesso de Exação (conf 0.95) </details>


---

## Q0052  (origem: Direito Penal - Legislação Especial / Teoria da Pena (Parte 02))

```
Uma pessoa presa em regime fechado, definitivamente condenada, prestou 300 dias de trabalho prisional intra muros , bem como, simultaneamente, teve frequência escolar de 200 horas, concluindo atividade de ensino médio ao longo do cumprimento da pena. Cada 12 (doze) horas foram divididas em 3 (três) dias de estudo.
Esse indivíduo
I. tem direito à remição de pena, à razão de 1 (um) dia de pena a cada 3 (três) dias de trabalho.
II. tem direito à remição de pena, à razão de 1 (um) dia de pena a cada 12 (doze) horas de frequência escolar.
III. tem direito à remição de pena, com o acréscimo de 1/3 (um terço) de toda a remição conquistada durante o cumprimento da pena devido à conclusão do ensino médio.
IV. em caso da prática de falta grave, obrigatoriamente, perderá 1/3 (um terço) da remição conquistada, recomeçando a contagem a partir da data da infração disciplinar.

(A) II, III e IV.
(B) I e III.
(C) I e II.
(D) III e IV.
(E) I, II e IV.
```

Candidatos (em ordem aleatória):

- 4703 · Direito Penal - Legislação Especial > Lei de Execução Penal
- 5201 · Penal > Teoria da Pena > Penas Privativas de Liberdade

<details><summary>decisão do ensemble</summary>publicar → 4703 · Direito Penal - Legislação Especial > Lei de Execução Penal (conf 0.93) </details>


---

## Q0059  (origem: Criminologia / Teorias Legitimidoras da Pena)

```
Sobre a relação entre o preso e a sociedade, segundo Alessandro Baratta, é CORRETO afirmar:

(A) A reinserção do preso na sociedade, após o cumprimento da pena, é assegurada\na partir do momento em que, no cárcere, o preso absorve um conjunto de\nvalores e modelos de comportamento desejados socialmente.
(B) É necessário primeiro modificar os excluídos, para que eles possam voltar ao\nconvívio social na sociedade que está apta a acolhê-los.
(C) O cárcere não reflete as características negativas da sociedade, em razão do\nisolamento a que são submetidos os presos.
(D) São relações sociais baseadas no egoísmo e na violência ilegal, no interior\ndas quais os indivíduos socialmente mais débeis são constrangidos a papéis\nde submissão e de exploração.
```

Candidatos (em ordem aleatória):

- 4385 · Criminologia > Teorias Sociológicas Explicativas da Criminalidade
- 4384 · Criminologia > Teorias Legitimidoras da Pena
- 4388 · Criminologia > Teorias Sociológicas Explicativas da Criminalidade > Teorias Criminológicas em Espécie

<details><summary>decisão do ensemble</summary>revisar → 4388 · Criminologia > Teorias Sociológicas Explicativas da Criminalidade > Teorias Criminológicas em Espécie (conf 0.45) ramo certo, subtema incerto (claude-opus: Teorias Criminológicas em Espécie); confiança abaixo do limiar</details>


---

## Q0075  (origem: Direito Penal / Causas de extinção da punibilidade)

```
Quanto à comunicabilidade da extinção da punibilidade, é INCORRETO afirmar:

(A) A extinção da punibilidade de crime que é circunstância agravante de outro não se estende a este.
(B) Nos crimes conexos, a extinção da punibilidade de um deles não impede, quanto aos outros, a agravação da pena resultante da conexão.
(C) A extinção da punibilidade de crime que é pressuposto de outro não se estende a este.
(D) A extinção da punibilidade de crime que é elemento constitutivo de outro não se estende a este.
(E) Nos crimes conexos, a extinção da punibilidade de um deles impede, quanto aos outros, a agravação da pena resultante da conexão.
```

Candidatos (em ordem aleatória):

- 5191 · Penal > Punibilidade
- 5066 · Penal > Concurso de Crimes

<details><summary>decisão do ensemble</summary>publicar → 5191 · Penal > Punibilidade (conf 0.9) </details>


---

## Q0076  (origem: Criminologia / Conceitos Gerais de Criminologia)

```
A Criminologia é definida tradicionalmente como a ciência que estuda de forma empírica o delito, o delinquente, a vítima e os mecanismos de controle social.
Os autores que fundaram a Criminologia (Positivista) são:

(A) Cesare Lombroso, Enrico Ferri e Raffaele Garofalo.
(B) Franz Von Liszt, Edmund Mezger e Marquês de Beccaria.
(C) Marquês de Beccaria, Cesare Lombroso e Michel Foucault.
(D) Cesare Lombroso, Enrico Ferri e Michel Foucault.
(E) Enrico Ferri, Michel Foucault e Nina Rodrigues.
```

Candidatos (em ordem aleatória):

- 4380 · Criminologia > Teoria Geral da Criminologia
- 4373 · Criminologia > Etapas Evolutivas e Escolas Criminológicas > Escolas Crimonológicas
- 4371 · Criminologia > Etapas Evolutivas e Escolas Criminológicas

<details><summary>decisão do ensemble</summary>publicar → 4371 · Criminologia > Etapas Evolutivas e Escolas Criminológicas (conf 0.85) </details>


---

## Q0087  (origem: Direito Penal / Legislação Penal Especial)

```
De acordo com a jurisprudência do Superior Tribunal de Justiça, a prisão domiciliar na execução penal

(A) possui rol taxativo previsto no art. 117 da Lei de Execução Penal.
(B) é cabível apenas para sentenciado que cumpre pena no regime aberto.
(C) depende de exame criminológico favorável para condenados reincidentes.
(D) deve utilizar o marco etário de 60 anos em razão do disposto no Estatuto do Idoso.
(E) é cabível excepcionalmente em regime fechado para mãe cujo cuidado do filho seja imprescindível.
```

Candidatos (em ordem aleatória):

- 4703 · Direito Penal - Legislação Especial > Lei de Execução Penal
- 5201 · Penal > Teoria da Pena > Penas Privativas de Liberdade

<details><summary>decisão do ensemble</summary>publicar → 4703 · Direito Penal - Legislação Especial > Lei de Execução Penal (conf 0.88) </details>


---

## Q0089  (origem: Direito Penal / Teoria do Crime (Ilicitude))

```
De acordo com o Glossário Jurídico do Supremo Tribunal Federal, “o princípio da insignificância tem o sentido de excluir ou de afastar a própria tipicidade penal, ou seja, não considera o ato praticado como um crime, por isso, sua aplicação resulta na absolvição do réu e não apenas na diminuição e substituição da pena ou não sua não aplicação”. Sobre o tema princípio da insignificância, assinale a resposta correta.

(A) Buscando sua origem, de acordo com certa vertente doutrinária, no Direito Romano, o princípio da insignificância vem sendo objeto de recorrentes decisões do STF, nas quais são estabelecidos dois parâmetros para sua determinação: reduzidíssimo grau de reprovabi l idade do compor tamento e inexpressividade da lesão jurídica provocada.
(B) O princípio da insignificância, decorrência do caráter fragmentário do Direito Penal, tem base em uma orientação utilitarista, tem origem controversa, encontrando, na atual jurisprudência do STF, os seguintes requisitos de configuração: a mínima ofensividade da conduta do agente; nenhuma periculosidade social da ação; o reduzidíssimo grau de reprovabilidade do comportamento; e a inexpressividade da lesão jurídica provocada.
(C) Sua atual elaboração deita raízes na doutrina de Claus Roxin e, no Direito Penal brasileiro, consoante jurisprudência atual do STF, se limita à avaliação da inexpressividade da lesão jurídica provocada, ou seja, observa-se se a ofensa ao bem jurídico tutelado é relevante ou banal.
(D) Surgindo como uma consequência lógica do princípio da individualização das penas, a insignificância penal não aceita a periculosidade social da ação como parâmetro, de acordo com o posicionamento atual do STF, em razão da elevada abstração desse conceito, mas apresenta como requisi tos: a mínima ofensividade da conduta do agente; o reduzidíssimo grau de reprovabilidade do comportamento; e a inexpressividade da lesão jurídica provocada.
(E) Inserida no princípio da intervenção mínima, embora já mencionada anteriormente por Welzel como uma faceta do princípio da adequação social, a insignificância determina a inexistência do crime quando a conduta praticada apresentar a simultânea presença dos seguintes requisitos, exigidos pela atual jurisprudência do STF: a mínima ofensividade da conduta do agente; nenhuma periculosidade social da ação; o reduzidíssimo grau de reprovabilidade do comportamento; a inexpressividade da lesão jurídica provocada; e a inexistência de um especial fim de agir.
```

Candidatos (em ordem aleatória):

- 5172 · Penal > Introdução ao Estudo do Direito Penal > Princípios do Direito Penal
- 5170 · Penal > Introdução ao Estudo do Direito Penal
- 5227 · Penal > Teoria do Crime: Fato Típico > Tipicidade

<details><summary>decisão do ensemble</summary>revisar → 5172 · Penal > Introdução ao Estudo do Direito Penal > Princípios do Direito Penal (conf 0.68) ramo certo, subtema incerto (claude-opus: Princípios do Direito Penal); confiança abaixo do limiar</details>


---

## Q0090  (origem: Processo Penal / Ação Penal (Parte 01))

```
Assinale a alternativa CORRETA.

(A) Em havendo reunião de processos perante o juízo comum ou o tribunal do júri, decorrentes da aplicação das regras de conexão e continência, não serão observados os institutos da transação penal e da composição dos danos civis, em relação aos crimes de menor potencial ofensivo.
(B) Em razão de a Lei n° 9.099/95 admitir a aplicação subsidiária das disposições do Código de Processo Penal, o juiz determinará a suspensão do processo e do curso do prazo prescricional sempre que, nos crimes submetidos ao procedimento traçado por aquela lei, o acusado, citado por edital, não comparecer e nem constituir advogado.
(C) No direito processual penal brasileiro, a réplica à resposta à acusação não se constitui em uma regra prevista expressamente para todas as modalidades de procedimentos existentes, podendo ser encontrada no procedimento aplicável aos processos de competência do Tribunal do Júri e no procedimento para os processos perante o Superior Tribunal de Justiça e o Supremo Tribunal Federal.
(D) De acordo com o Código de Processo Penal, nos processos submetidos ao rito comum ordinário, a denúncia ou queixa serão rejeitadas quando forem manifestamente ineptas, quando faltar pressuposto processual ou condição da ação para o exercício da ação penal, quando faltar justa causa para o oferecimento da ação penal e quando o fato narrado evidentemente não constitui crime.
(E) Tendo o funcionário público cometido o crime de racismo no exercício de sua função, e estando a denúncia ou queixa em devida ordem, o juiz mandará autuá-la e ordenará a notificação do acusado, para responder por escrito, dentro do prazo de quinze dias.
```

Candidatos (em ordem aleatória):

- 5539 · Processo Penal > Procedimento Sumaríssimo
- 5530 · Processo Penal > Procedimento Ordinário

<details><summary>decisão do ensemble</summary>revisar → 5530 · Processo Penal > Procedimento Ordinário (conf 0.32) questão multi-tema (alternativas sobre institutos diferentes); ramo Procedimento Ordinário</details>


---

## Q0103  (origem: Processo Penal / Ação Penal (Parte 01))

```
A respeito da revisão criminal, julgue os próximos itens.
A revisão criminal, que é um dos aspectos diferenciadores do mero direito à defesa e do direito à ampla defesa, este caracterizador do direito processual penal, tem por finalidade o reexame do processo já alcançado pela coisa julgada, de forma a possibilitar ao condenado a absolvição, a melhora de sua situação jurídica ou a anulação do processo.

(C) Certo
(E) Errado
```

Candidatos (em ordem aleatória):

- 5478 · Processo Penal > Ações Autônomas de Impugnação > Revisão Criminal
- 5476 · Processo Penal > Ações Autônomas de Impugnação
- 5582 · Processo Penal > Sistemas e Princípios Processuais Penais > Princípios do Processo Penal

<details><summary>decisão do ensemble</summary>publicar → 5478 · Processo Penal > Ações Autônomas de Impugnação > Revisão Criminal (conf 0.93) </details>


---

## Q0106  (origem: Direito Penal / Crimes contra o patrimônio)

```
Que delito praticam os estudantes de Direito com o chamado “pendura”, nas comemorações da instalação dos cursos jurídicos no País?

(A) Nenhum crime foi praticado, por se tratar de fato atípico.
(B) Crime de dano qualificado, por motivo egoístico.
(C) Delito de fraude, consistente em tomar refeições em restaurante, sem dispor de recursos para pagar as despesas.
(D) Estelionato privilegiado, devido ao pequeno valor do prejuízo causado à vítima.
```

Candidatos (em ordem aleatória):

- 5157 · Penal > Dos Crimes Contra o Patrimônio
- 5166 · Penal > Dos Crimes Contra o Patrimônio > Estelionato

<details><summary>decisão do ensemble</summary>publicar → 5157 · Penal > Dos Crimes Contra o Patrimônio (conf 0.95) </details>


---

## Q0107  (origem: Penal / Outras falsidades, Crimes contra a fé pública)

```
À luz das disposições legais de direito penal e da jurisprudência correlata, julgue o próximo item.

(C) Certo
(E) Errado
```

Candidatos (em ordem aleatória):

- 5118 · Penal > Dos Crimes Contra a Fé Pública e de Falsidade Documental > Da Falsidade Documental
- 5116 · Penal > Dos Crimes Contra a Fé Pública e de Falsidade Documental
- 5119 · Penal > Dos Crimes Contra a Fé Pública e de Falsidade Documental > De outras falsidades

<details><summary>decisão do ensemble</summary>revisar → 5119 · Penal > Dos Crimes Contra a Fé Pública e de Falsidade Documental > De outras falsidades (conf 0.41) ramo certo, subtema incerto (claude-opus: De outras falsidades); confiança abaixo do limiar</details>


---

## Q0111  (origem: Criminologia / Teorias Legitimidoras da Pena)

```
Sobre a escola positivista da criminologia, é correto afirmar:

(A) A escola positivista ainda não chega a considerar a concepção da pena como meio de defesa social, que é própria de\nescolas mais modernas da criminologia.
(B) Sua recepção no Brasil recebeu contornos racistas, notadamente no trabalho antropológico de Nina Rodrigues.
(C) É uma escola criminológica ultrapassada e que já influenciou a legislação penal brasileira, mas que após a Constituição\nFederal de 1988 não conta mais com institutos penais influenciados por esta corrente.
(D) Por ter enveredado pela sociologia criminal, Enrico Ferri não é considerado um autor da escola positivista, que possui viés\nmédico e antropológico.
(E) O método positivista negava a importância da pesquisa empírica, que possivelmente a levaria a resultados diversos\ndaqueles encontrados pelos seus autores.
```

Candidatos (em ordem aleatória):

- 4371 · Criminologia > Etapas Evolutivas e Escolas Criminológicas
- 4386 · Criminologia > Teorias Sociológicas Explicativas da Criminalidade > Teorias de Nível Individual
- 4373 · Criminologia > Etapas Evolutivas e Escolas Criminológicas > Escolas Crimonológicas

<details><summary>decisão do ensemble</summary>publicar → 4371 · Criminologia > Etapas Evolutivas e Escolas Criminológicas (conf 0.88) </details>


---

## Q0120  (origem: Processo Penal / Sistemas e Princípios Processuais Penais)

```
Acerca das provas, das sentenças e dos princípios do direito processual penal, julgue o item a seguir.
No processo penal, o momento adequado para a especificação de provas pelo réu é a apresentação da resposta à acusação. Entretanto, isso não impede que, por ocasião de seu interrogatório, o réu indique outros meios de prova que deseje produzir.

(C) Certo
(E) Errado
```

Candidatos (em ordem aleatória):

- 5530 · Processo Penal > Procedimento Ordinário
- 5533 · Processo Penal > Procedimento Ordinário > Defesa Preliminar
- 5547 · Processo Penal > Provas em Espécies > Interrogatório Judicial

<details><summary>decisão do ensemble</summary>revisar → 5533 · Processo Penal > Procedimento Ordinário > Defesa Preliminar (conf 0.45) ramo certo, subtema incerto (claude-opus: Defesa Preliminar); confiança abaixo do limiar</details>


---

## Q0125  (origem: Direito Penal - Legislação Especial / Teoria da Pena (Parte 02))

```
A Lei Antitóxicos (Lei n o 11.343/06) estabelece diminuição de pena no caso de agente primário, de bons antecedentes e que não se dedique às atividades criminosas ou integre organização criminosa.
Em um processo de execução, cuja condenação de tráfico o sentenciado preenche os requisitos acima enumerados e que fora preso anteriormente à edição da lei, o defensor público deverá requerer a aplicação de novatio legis in mellius

(A) para o Tribunal ou o juízo da Vara das Execuções Criminais, indistintamente, por força da imediatidade desta decisão.
(B) perante o juízo da Vara das Execuções Criminais independentemente do trânsito em julgado da decisão do processo de conhecimento.
(C) perante o juízo da Vara de Execuções Criminais no caso de trânsito em julgado da decisão do processo de conhecimento.
(D) perante o Tribunal, único competente para a decisão de diminuição de pena no processo de execução em andamento.
(E) perante o juízo da condenação para não haver risco de supressão de instância.
```

Candidatos (em ordem aleatória):

- 5181 · Penal > Lei Penal no Tempo e no Espaço > Lei penal no Tempo
- 4703 · Direito Penal - Legislação Especial > Lei de Execução Penal
- 5180 · Penal > Lei Penal no Tempo e no Espaço

<details><summary>decisão do ensemble</summary>revisar → 5181 · Penal > Lei Penal no Tempo e no Espaço > Lei penal no Tempo (conf 0.54) ramo certo, subtema incerto (claude-opus: Lei penal no Tempo); confiança abaixo do limiar</details>


---

## Q0128  (origem: Processo Penal / Ação Penal (Parte 01))

```
A ação de prevenção penal é aquela ajuizada com a finalidade de se aplicar medida de segurança a acusado que, em virtude de doença mental ou de desenvolvimento mental incompleto ou retardado, era, ao tempo da ação ou omissão, absolutamente incapaz de entender o caráter ilícito do fato ou de determinar-se de acordo com esse entendimento.

(C) Certo
(E) Errado
```

Candidatos (em ordem aleatória):

- 5466 · Processo Penal > Ação Penal
- 5468 · Processo Penal > Ação Penal > Classificação da Ação Penal
- 5184 · Penal > Medida de Segurança

<details><summary>decisão do ensemble</summary>revisar → 5468 · Processo Penal > Ação Penal > Classificação da Ação Penal (conf 0.72) ramo certo, subtema incerto (claude-opus: Classificação da Ação Penal); confiança abaixo do limiar</details>


---

## Q0129  (origem: Processo Penal / Comunicação dos atos processuais)

```
Em virtude de desavença familiar no interior de uma residência, um marido agrediu, mediante socos e chutes, sua esposa, na presença de familiares (pais, irmãos, filhos e primos) que lá se encontravam para a comemoração de um aniversário. Ao elaborar a denúncia, o promotor de justiça arrolou, além da vítima, as demais pessoas presentes como testemunhas.
O magistrado, ao deliberar sobre a designação de audiência de instrução e julgamento, deverá:

(A) indeferir a oitiva, pois a oitiva de depoimento testemunhal de\nparente do envolvido não é admitida em nosso ordenamento\njurídico;
(B) deferir a oitiva, pois o depoimento testemunhal de parente\ndo envolvido é admitido em nosso ordenamento e\nnotadamente relevante em casos nos quais a conduta foi\npraticada no âmbito doméstico dos familiares;
(C) indeferir a oitiva, pois a oitiva de depoimento testemunhal de\nparente do envolvido é expressamente vedada em nosso\nordenamento;
(D) deferir a oitiva, pois a legislação brasileira é expressa em\nadmitir toda pessoa como testemunha, não fazendo vedação\nà qualidade ou proximidade com os envolvidos no fato;
(E) indeferir a oitiva, pois a comprovação da conduta delituosa,\nnesse caso específico, pode ser feita por outros elementos,\ndependendo o depoimento testemunhal de expressa\nanuência da testemunha.
```

Candidatos (em ordem aleatória):

- 5550 · Processo Penal > Provas em Espécies > Prova Testemunhal
- 5543 · Processo Penal > Provas em Espécies
- 5590 · Processo Penal > Teoria Geral das Provas

<details><summary>decisão do ensemble</summary>publicar → 5550 · Processo Penal > Provas em Espécies > Prova Testemunhal (conf 0.88) </details>


---

## Q0143  (origem: Processo Penal / Lei Processual Penal no tempo e no espaço)

```
No que diz respeito à norma processual penal, aos sistemas processuais penais e à investigação criminal, julgue o item subsequente.
No ordenamento jurídico brasileiro, em regra, a lei processual penal será aplicada com fulcro no princípio do tempus delicti .

(C) Certo
(E) Errado
```

Candidatos (em ordem aleatória):

- 5505 · Processo Penal > Lei Processual no Tempo e no Espaço
- 5507 · Processo Penal > Lei Processual no Tempo e no Espaço > Lei processual no Tempo

<details><summary>decisão do ensemble</summary>publicar → 5507 · Processo Penal > Lei Processual no Tempo e no Espaço > Lei processual no Tempo (conf 0.92) </details>


---

## Q0149  (origem: Processo Penal / Inquérito Policial)

```
Relativamente ao inquérito policial e às diligências neste levadas a efeito, é correto afirmar que:

(A) na busca domiciliar fundada em ordem judicial, quando\nencontrada a arma objeto do crime de roubo, a não\nespecificação no mandado judicial para a busca pessoal\nimpedirá a realização desta;
(B) o delegado de polícia, apurando crime de extorsão mediante\nsequestro, necessita de prévia autorização judicial para\nrequisitar, de quaisquer órgãos do poder público, dados e\ninformações cadastrais dos suspeitos;
(C) após representação do delegado de polícia, nos crimes\nrelacionados ao tráfico de pessoas, sobre a disponibilização\ndos meios técnicos que permitam a localização da vítima, se\nnão houver manifestação judicial no prazo de doze horas,\npoderá aquele proceder às requisições, comunicando-se\nimediatamente ao juiz;
(D) nos crimes relacionados ao tráfico de pessoas, o delegado de\npolícia poderá requisitar, independentemente de autorização\njudicial, às empresas prestadoras de serviço de\ntelecomunicações que disponibilizem imediatamente os\nmeios técnicos adequados que permitam a localização dos\nsuspeitos;
(E) dar-se-á prioridade à realização de exame de corpo de delito,\nna fase do inquérito policial, quando se tratar de crime que\nenvolva criança ou adolescente, idoso, pessoa com\ndeficiência, indígena ou gestante.
```

Candidatos (em ordem aleatória):

- 5500 · Processo Penal > Inquérito Policial > Procedimento do Inquérito Policial
- 5498 · Processo Penal > Inquérito Policial
- 5554 · Processo Penal > Provas em Espécies > Busca e Apreensão

<details><summary>decisão do ensemble</summary>publicar → 5498 · Processo Penal > Inquérito Policial (conf 0.9) </details>


---

## Q0151  (origem: Processo Penal / Ação Penal (Parte 02))

```
No que diz respeito às prisões e medidas cautelares no processo penal, assinale a alternativa CORRETA:

(A) O juiz poderá substituir a prisão preventiva pela domiciliar quando o suposto autor do fato delituoso for maior de 70 (setenta) anos de idade ou estiver extremamente debilitado por motivo de doença grave.
(B) Em respeito ao princípio da proporcionalidade das medidas cautelares, a fiança, segundo as regras do Código de Processo Penal, quando estabelecida em seu valor máximo, não poderá ser cumulada com outras medidas cautelares diversas da prisão preventiva.
(C) Se assim recomendar a situação econômica do preso, a fiança poderá ser aumentada em até 1.000 (mil) vezes.
(D) De acordo com o novo regramento destinado à prisão cautelar, o Código de Processo Penal passou a estabelecer a prisão temporária como uma das hipóteses das denominadas prisões cautelares estritamente processuais.
(E) É pacífico o entendimento da doutrina quanto à natureza jurídica precautelar da prisão em flagrante, o que tem sido confirmado pela jurisprudência do Superior Tribunal de Justiça.
```

Candidatos (em ordem aleatória):

- 5517 · Processo Penal > Prisões em Espécie
- 5523 · Processo Penal > Prisões em Espécie > Liberdade Provisória

<details><summary>decisão do ensemble</summary>revisar → 5517 · Processo Penal > Prisões em Espécie (conf 0.64) questão multi-tema (alternativas sobre institutos diferentes); ramo Prisões em Espécie</details>


---

## Q0152  (origem: Processo Penal / Ação Penal)

```
Nos crimes de ação privada, se comparecer mais de uma pessoa com direito de queixa, terá preferência, numa ordem legal estabelecida pelo artigo 31 do Código de Processo Penal,

(A) o parente mais próximo na ordem de vocação sucessória.
(B) o cônjuge, que poderá prosseguir na ação penal.
(C) a figura do ascendente, em face dos vínculos fraternos.
(D) a figura do descendente, com o direito de apenas prosseguir.
(E) o representante legalmente constituído para o fim.
```

Candidatos (em ordem aleatória):

- 5474 · Processo Penal > Ação Penal > Queixa Crime
- 5472 · Processo Penal > Ação Penal > Ação Penal de Iniciativa Privada
- 5466 · Processo Penal > Ação Penal

<details><summary>decisão do ensemble</summary>publicar → 5466 · Processo Penal > Ação Penal (conf 0.85) </details>


---

## Q0162  (origem: Criminologia / Conceitos Gerais de Criminologia)

```
A moderna criminologia se dedica, também, ao estudo do controle social do delito, tendo este objeto representado um giro metodológico de grande importância.

(A) a família, a escola, a opinião pública, por exemplo, são instituições encarregadas de exercer o\ncontrole social primário.
(B) a polícia, o Judiciário, a administração penitenciária, por exemplo, são instituições\nencarregadas de exercer o controle social informal.
(C) a polícia, o Judiciário, a administração penitenciária, por exemplo, são instituições\nencarregadas de exercer o controle social formal.
(D) a família, a escola, a opinião pública, por exemplo, são instituições encarregadas de exercer o\ncontrole social terciário.
(E) a família, a escola, a opinião pública, por exemplo, são instituições encarregadas de exercer o\ncontrole social secundário.
```

Candidatos (em ordem aleatória):

- 4368 · Criminologia > Criminologia no Estado Democrático de Direito
- 4380 · Criminologia > Teoria Geral da Criminologia
- 4381 · Criminologia > Teoria Geral da Criminologia > Conceito e objeto da Criminologia

<details><summary>decisão do ensemble</summary>revisar → 4381 · Criminologia > Teoria Geral da Criminologia > Conceito e objeto da Criminologia (conf 0.63) ramo certo, subtema incerto (claude-opus: Conceito e objeto da Criminologia); confiança abaixo do limiar</details>


---

## Q0178  (origem: Penal / Legislação Penal Especial, Lei de Armas (Estatuto do Desarmamento) – Lei nº 10.826 de 2003 e Decretos Regulamentares)

```
A Resolução CNJ nº 467/2022 regulamentou o inciso XI do artigo 6º da Lei nº 10.826/2003 e prevê que o porte de arma de fogo de servidores dos quadros pessoais do Poder Judiciário é:

(A) defeso aos servidores do Poder Judiciário, enquadrados como agentes e inspetores da especialidade Polícia Judicial, ainda que efetivamente estejam no exercício do poder de polícia, em todo o território nacional, sendo permitido somente no Estado em que está lotado para o exercício de suas funções.
(B) autorizado aos servidores do Poder Judiciário, enquadrados como agentes e inspetores da especialidade Polícia Judicial, independentemente de estarem no exercício do poder de polícia, somente no Estado em que estejam lotados.
(C) defeso aos servidores do Poder Judiciário, enquadrados como agentes e inspetores da especialidade Polícia Judicial, ainda que efetivamente estejam no exercício do poder de polícia, em todo o território nacional.
(D) autorizado aos servidores do Poder Judiciário, enquadrados como agentes e inspetores da especialidade Polícia Judicial, e que efetivamente estejam no exercício do poder de polícia, em todo o território nacional.
(E) autorizado aos servidores do Poder Judiciário, enquadrados como agentes e inspetores da especialidade Polícia Judicial, e que efetivamente estejam no exercício do poder de polícia, somente no Estado em que estejam lotado para os exercícios de suas funções.
```

Candidatos (em ordem aleatória):

- 4697 · Direito Penal - Legislação Especial > Estatuto do Desarmamento

<details><summary>decisão do ensemble</summary>publicar → 4697 · Direito Penal - Legislação Especial > Estatuto do Desarmamento (conf 0.93) </details>


---

## Q0181  (origem: Direito Penal - Legislação Especial / Concurso de Crimes)

```
Identifique o que constitui crime contra a ordem tributária e assinale a alternativa correta .
I Adquirir, distribuir e revender derivados de petróleo, gás natural e suas frações recuperáveis, álcool etílico, hidratado carburante e demais combustíveis líquidos carburantes, em desacordo com as normas estabelecidas na forma da lei .
II Usar gás liquefeito de petróleo em motores de qualquer espécie, saunas, caldeiras e aquecimento de piscinas, ou para fins automotivos, em desacordo com as normas estabelecidas na forma da lei .
III Negar ou deixar de fornecer, quando obrigatório, nota fiscal ou documento equivalente, relativa a venda de mercadoria ou prestação de serviço, efetivamente realizada, ou fornecê-la em desacordo com a legislação .
IV Sem autorização legal, produzir, adquirir, transportar, industrializar, ter consigo, consumir ou comercializar produtos ou matéria-prima pertencentes à União .

(A) Apenas II e III estão corretas.
(B) Apenas a afirmação III está correta.
(C) Apenas II e IV estão corretas.
(D) Apenas I, II e IV estão corretas.
(E) Todas as afirmações estão corretas.
```

Candidatos (em ordem aleatória):

- 4695 · Direito Penal - Legislação Especial > Crimes Tributários
- 4687 · Direito Penal - Legislação Especial > Crimes contra a Economia Popular

<details><summary>decisão do ensemble</summary>publicar → 4695 · Direito Penal - Legislação Especial > Crimes Tributários (conf 0.88) </details>


---

## Q0182  (origem: Direito Penal / Concurso de Crimes)

```
Analise os itens e assinale a quantidade de itens errados .
I - A instigação da gestante para permitir que terceiro lhe provoque aborto, em se consumando o crime, enseja para o instigador a participação no crime de aborto consensual, descrito no artigo 126 do CP.
II - O crime de perigo de contágio de moléstia venérea tipificado no artigo 130 do CP exige o perigo concreto para a sua consumação.
III - O rixoso que sofre a lesão corporal de natureza grave, causa de aumento de pena no crime em questão, não responde por esta circunstância.
IV - Descoberto o autor da morte ocorrida durante uma rixa, imputa-se a este o crime de acordo com o elemento volitivo que informou a sua conduta, excluindo-se os demais rixosos que passam a responder pela forma simples do crime de rixa prevista no artigo 137 do CP.
V - É incorreto afirmar que um indivíduo que chega à sala do seu chefe, numa conversa a dois, e assevera que este está subtraindo verba da empresa onde trabalham, comete, caso seja falsa a afirmação e tendo ciência desta falsidade, o crime de calúnia.

(A) Um.
(B) Dois.
(C) Três.
(D) Quatro.
(E) Cinco.
```

Candidatos (em ordem aleatória):

- 5149 · Penal > Dos Crimes Contra a Vida
- 5138 · Penal > Dos Crimes Contra a Periclitação da Vida e da Saúde

<details><summary>decisão do ensemble</summary>revisar → 5138 · Penal > Dos Crimes Contra a Periclitação da Vida e da Saúde (conf 0.24) questão multi-tema (alternativas sobre institutos diferentes); ramo Dos Crimes Contra a Periclitação da Vida e da Saúde</details>


---

## Q0188  (origem: Direito Penal / Teoria do Crime (Ilicitude))

```
Segundo sua classificação doutrinária dominante, o chamado ofendículo pode mais precisamente caracterizar situação de exclusão de

(A) antijuridicidade.
(B) tipicidade.
(C) periculosidade.
(D) culpabilidade.
(E) punibilidade.
```

Candidatos (em ordem aleatória):

- 5229 · Penal > Teoria do Crime: Ilicitude > Conceito e Elementos da Ilicitude
- 5228 · Penal > Teoria do Crime: Ilicitude
- 5231 · Penal > Teoria do Crime: Ilicitude > Legítima Defesa

<details><summary>decisão do ensemble</summary>publicar → 5228 · Penal > Teoria do Crime: Ilicitude (conf 0.93) </details>


---

## Q0189  (origem: Processo Penal / Ação Penal)

```
Acerca do direito processual penal, julgue o item subseqüente.
A desistência da ação penal privada pode ocorrer a qualquer momento, somente surgindo óbice intransponível quando já existente decisão condenatória transitada em julgado.

(C) Certo
(E) Errado
```

Candidatos (em ordem aleatória):

- 5196 · Penal > Punibilidade > Renúncia, Perdão do Ofendido e Retratação
- 5466 · Processo Penal > Ação Penal
- 5472 · Processo Penal > Ação Penal > Ação Penal de Iniciativa Privada

<details><summary>decisão do ensemble</summary>revisar → 5472 · Processo Penal > Ação Penal > Ação Penal de Iniciativa Privada (conf 0.63) ramo certo, subtema incerto (claude-opus: Ação Penal de Iniciativa Privada); confiança abaixo do limiar</details>


---

## Q0190  (origem: Processo Penal / Rito Sumaríssimo)

```
Considerando a temática dos Juizados Especiais Criminais, assinale a alternativa correta.

(A) A competência do Juizado será determinada pelo lugar em que foi praticada a infração penal.
(B) Consideram-se infrações penais de menor potencial ofensivo as contravenções penais e os crimes a que a lei comine pena mínima não superior a 2 (dois) anos, cumulada ou não com multa.
(C) Nos crimes em que a pena mínima cominada for igual ou inferior a um ano, o Ministério Público, ao oferecer a denúncia, poderá propor a suspensão do processo, por um a quatro anos, desde que o acusado não esteja sendo processado ou não tenha sido condenado por outro crime, presentes os demais requisitos que autorizariam a suspensão condicional da pena (art. 77 do Código Penal).
(D) A composição civil, estabelecida nos arts. 74 e 75 da Lei, é uma causa de extinção da punibilidade nos crimes de menor potencial ofensivo, quando a ação for pública incondicionada.
(E) A proposta de Transação Penal (art. 76) deve ser feita pelo Juiz na presença do Ministério Público.
```

Candidatos (em ordem aleatória):

- 5539 · Processo Penal > Procedimento Sumaríssimo
- 4701 · Direito Penal - Legislação Especial > Juizado Especial Criminal

<details><summary>decisão do ensemble</summary>revisar → 4701 · Direito Penal - Legislação Especial > Juizado Especial Criminal (conf 0.45) ramo certo, subtema incerto (claude-opus: nível 1); confiança abaixo do limiar</details>


---

## Q0200  (origem: Processo Penal / Ação Penal (Parte 02))

```
No que diz respeito às organizações criminosas, assinale a opção correta.

(A) O líder de organização criminosa condenado pelo crime de integrar tal organização deverá iniciar o cumprimento da pena necessariamente em estabelecimento penal de segurança máxima.
(B) A definição legal de organização criminosa promovida pela\nLei n.º 12.850/2013 internaliza na legislação nacional a\ndefinição de grupo criminoso organizado constante da\nConvenção de Palermo.
(C) O concurso de funcionário público é qualificadora do crime\nde integrar organização criminosa.
(D) Havendo indício de participação de funcionário público na\norganização criminosa, é cabível a determinação judicial de\nafastamento cautelar do cargo, do emprego ou da função, sem\nremuneração, quando necessária à investigação ou instrução\nprocessual.
(E) Para que seja possível nova acusação pelo crime de integrar\norganização criminosa contra os mesmos agentes por novo\ncrime de mesma espécie, sem configurar bis in idem, deve ser\nconsiderada cessada a permanência da conduta com o\nrecebimento da denúncia.
```

Candidatos (em ordem aleatória):

- 4705 · Direito Penal - Legislação Especial > Organizações Criminosas
- 5146 · Penal > Dos Crimes Contra a Saúde Pública e Dos Crimes Contra à Paz Pública > Crimes Contra à Paz Pública

<details><summary>decisão do ensemble</summary>publicar → 4705 · Direito Penal - Legislação Especial > Organizações Criminosas (conf 0.95) </details>


---

## Q0209  (origem: Processo Penal / Inquérito Policial)

```
Acerca das provas, das sentenças e dos princípios do direito processual penal, julgue o item a seguir.
Em razão do princípio constitucional da presunção de inocência, é vedado à autoridade policial mencionar anotações referentes à instauração de inquérito nos atestados de antecedentes que lhe forem solicitados.

(C) Certo
(E) Errado
```

Candidatos (em ordem aleatória):

- 5499 · Processo Penal > Inquérito Policial > Conceito, Finalidade e Caractéristas do Inquérito Policial
- 5498 · Processo Penal > Inquérito Policial
- 5582 · Processo Penal > Sistemas e Princípios Processuais Penais > Princípios do Processo Penal

<details><summary>decisão do ensemble</summary>revisar → 5499 · Processo Penal > Inquérito Policial > Conceito, Finalidade e Caractéristas do Inquérito Policial (conf 0.59) ramo certo, subtema incerto (claude-opus: Conceito, Finalidade e Caractéristas do Inquérito Policial); confiança abaixo do limiar</details>


---

## Q0217  (origem: Criminologia / Teorias Legitimidoras da Pena)

```
Para Michel Foucault, em Vigiar e punir , as razões de ser essenciais da reforma penal no século XVIII, também denominada Reforma Humanista do Direito penal, são constituir uma nova economia e uma nova tecnologia do poder de:

(A) recuperar.
(B) ressocializar.
(C) humanizar.
(D) punir.
(E) descriminalizar.
```

Candidatos (em ordem aleatória):

- 4371 · Criminologia > Etapas Evolutivas e Escolas Criminológicas
- 4372 · Criminologia > Etapas Evolutivas e Escolas Criminológicas > Etapas Evolutivas da Criminologia (Antiguidade, Idade Média e Idade Moderna)
- 4384 · Criminologia > Teorias Legitimidoras da Pena

<details><summary>decisão do ensemble</summary>revisar → 4372 · Criminologia > Etapas Evolutivas e Escolas Criminológicas > Etapas Evolutivas da Criminologia (Antiguidade, Idade Média e Idade Moderna) (conf 0.41) ramo certo, subtema incerto (claude-opus: Etapas Evolutivas da Criminologia (Antiguidade, Idade Média e Idade Moderna)); confiança abaixo do limiar</details>


---

## Q0222  (origem: Direito Penal / Ação Penal)

```
Assinale a alternativa correta.

(A) O denominado direito penal do inimigo, que tem como expoente Günther Jakobs,\npode ser entendido como um direito penal de segunda velocidade, restringindo\ngarantias penais e processuais.
(B) A terceira velocidade do direito penal, ligada à ideia de aplicação de penas\nalternativas, encontra amparo no ordenamento penal brasileiro na Lei n.\n9.099/1995.
(C) A quarta velocidade do direito penal refere-se ao neopunitivismo, abrangendo\naquelas pessoas que violaram tratados e convenções internacionais de direitos\nhumanos, ostentando a condição de Chefes de Estado, devendo sofrer a incidência\nde normas internacionais.
(D) A teoria da primeira velocidade do direito penal, fundada no respeito às garantias\nindividuais, tinha a ideia de um direito penal de mínima intervenção e sanções não\nprivativas de liberdade.
(E) A ideia de velocidades do direito penal foi concebida e sistematizada pelo professor\nManuel Cancio Meliá.
```

Candidatos (em ordem aleatória):

- 4376 · Criminologia > Política Criminal > Direito Penal do Inimigo
- 4374 · Criminologia > Política Criminal

<details><summary>decisão do ensemble</summary>revisar → 4374 · Criminologia > Política Criminal (conf 0.5) ramo certo, subtema incerto (claude-opus: nível 1); confiança abaixo do limiar</details>


---

## Q0228  (origem: Processo Penal / Ação Penal (Parte 02))

```
Se o defensor de um condenado preso entender que ele faz jus ao livramento condicional, deverá:

(A) Solicitar ao Tribunal, mediante a\nimpetração de habeas corpus;
(B) Solicitar ao Tribunal, mediante a\npropositura de Revisão Criminal;
(C) Solicitar ao Juiz da Execução, mediante\nAgravo em Execução;
(D) Solicitar ao Juiz da Execução, mediante\npetição.
```

Candidatos (em ordem aleatória):

- 5208 · Penal > Teoria da Pena > Livramento Condicional
- 4703 · Direito Penal - Legislação Especial > Lei de Execução Penal

<details><summary>decisão do ensemble</summary>revisar → 4703 · Direito Penal - Legislação Especial > Lei de Execução Penal (conf 0.54) ramo certo, subtema incerto (claude-opus: nível 1); confiança abaixo do limiar</details>


---

## Q0250  (origem: Direito Penal / Teoria da Pena (Parte 02))

```
Sobre a determinação do regime inicial de cumprimento de pena, é correto afirmar que

(A) em virtude do princípio da individualização da pena, a primeira fase de aplicação da pena não pode influenciar na\ndeterminação do regime.
(B) a pena de detenção deve ser cumprida em regime aberto ou semiaberto, salvo caso de reincidência.
(C) segundo a jurisprudência dominante do STJ, a reincidência impede o cumprimento de pena em regime semiaberto,\nindependentemente da quantidade de pena e das circunstâncias judiciais.
(D) em caso de condenação por crime de extorsão mediante sequestro consumado, é possível a aplicação do regime\nsemiaberto.
(E) por ser cometido com violência ou grave ameaça contra a pessoa, a condenação por roubo consumado impede a\naplicação do regime aberto.
```

Candidatos (em ordem aleatória):

- 5199 · Penal > Teoria da Pena
- 5201 · Penal > Teoria da Pena > Penas Privativas de Liberdade
- 5576 · Processo Penal > Sentença Penal > Fixação da Pena e do Regime Penitenciário

<details><summary>decisão do ensemble</summary>publicar → 5199 · Penal > Teoria da Pena (conf 0.93) </details>


---

## Q0252  (origem: Processo Penal / Ação Penal (Parte 02))

```
João, maior de setenta anos de idade ao tempo do fato, foi condenado pelo crime de estelionato à pena privativa de liberdade de quatro anos e três meses de reclusão em regime inicial semiaberto e, ainda, ao pagamento de cinquenta dias-multa, fixado o valor de um vinte avos do salário mínimo vigente.
Nessa situação hipotética, conforme o CPP,

(A) caso o presidente da República conceda a João graça parcial,\no benefício não poderá ser recusado.
(B) o juiz poderá, a requerimento do réu, demonstradas as\ncircunstâncias que o justifiquem, permitir que o pagamento da\npena de multa se faça em parcelas mensais.
(C) João terá direito ao livramento condicional, preenchidos os\nrequisitos, e somente este ou o seu advogado poderá requerê-lo\nao juízo da execução penal, tendo em vista a natureza\npersonalíssima da pena.
(D) o requisito temporal do livramento condicional será reduzido\npela metade, em razão de João contar com mais de setenta anos\nde idade na data do fato.
```

Candidatos (em ordem aleatória):

- 5199 · Penal > Teoria da Pena
- 4703 · Direito Penal - Legislação Especial > Lei de Execução Penal

<details><summary>decisão do ensemble</summary>revisar → 4703 · Direito Penal - Legislação Especial > Lei de Execução Penal (conf 0.44) questão multi-tema (alternativas sobre institutos diferentes); ramo Lei de Execução Penal</details>


---

## Q0263  (origem: Processo Penal / Procedimento do Júri)

```
O juiz dar-se-á por suspeito e, se não o fizer, poderá ser recusado por qualquer das partes:
I. Se ele próprio ou seu cônjuge ou parente, consanguíneo ou afim, em linha reta ou colateral até o terceiro grau, inclusive, for parte ou diretamente interessado no feito.
II. Se ele, seu cônjuge, ascendente ou descendente, estiver respondendo a processo por fato análogo, sobre cujo caráter criminoso haja controvérsia.
III. Se ele, seu cônjuge, ou parente, consanguíneo, ou afim, até o terceiro grau, inclusive, sustentar demanda ou responder a processo que tenha de ser julgado por qualquer das partes.
IV. Ele próprio houver desempenhado qualquer dessas funções (defensor ou advogado, órgão do Ministério Público, autoridade policial, auxiliar da justiça ou perito) ou servido como testemunha.

(A) Apenas as assertivas I e IV estão corretas.
(B) Apenas as assertivas I, II e III estão corretas.
(C) Apenas as assertivas II e III estão corretas.
(D) Todas as assertivas estão corretas.
```

Candidatos (em ordem aleatória):

- 5583 · Processo Penal > Sujeitos do Processo
- 5492 · Processo Penal > Das Questões e Processos Incidentes > Exceção de Suspeição, de Impedimento ou de Incompatibilidade
- 5490 · Processo Penal > Das Questões e Processos Incidentes

<details><summary>decisão do ensemble</summary>revisar → 5492 · Processo Penal > Das Questões e Processos Incidentes > Exceção de Suspeição, de Impedimento ou de Incompatibilidade (conf 0.72) ramo certo, subtema incerto (claude-opus: Exceção de Suspeição, de Impedimento ou de Incompatibilidade); confiança abaixo do limiar</details>


---

## Q0267  (origem: Processo Penal / Procedimento especial da Lei nº 11.343 de 2006, Procedimento Penal)

```
Matheus, caminhoneiro, foi capturado em flagrante enquanto transportava, na fronteira entre a República Federativa do Brasil e a Colômbia, cem quilos de cocaína. Em assim sendo, o indivíduo foi encaminhado à presença do delegado de polícia federal, que constatou que, na unidade policial, inexistia perito oficial para firmar o laudo de constatação da natureza e quantidade da droga. Dessa forma, o laudo pericial foi lavrado por uma pessoa idônea. Nesse cenário, considerando as disposições da Lei n o 11.343/2006, é correto afirmar que:

(A) recebida cópia do auto de prisão em flagrante, o juiz, no prazo de dez dias, certificará a regularidade formal do laudo de constatação e determinará a destruição das drogas apreendidas, guardando-se amostra necessária à realização do laudo definitivo;
(B) com a ratificação da prisão em flagrante de Matheus, o delegado de polícia fará, imediatamente, comunicação ao juiz competente, ao Ministério Público e à Defensoria Pública, remetendo-lhes cópia do auto lavrado;
(C) o local da destruição das drogas será vistoriado antes e depois de efetivada a medida, sendo lavrado auto circunstanciado pela autoridade sanitária, certificando-se neste a destruição total do material;
(D) a constatação da natureza e quantidade da droga se deu de forma irregular, pois não é possível suprir a ausência de perito oficial, substituindo-o por pessoa idônea, por ausência de previsão legal;
(E) a destruição das drogas será executada pelo delegado de polícia competente, na presença do Ministério Público, da autoridade sanitária e do juiz que ordenar a adoção da medida.
```

Candidatos (em ordem aleatória):

- 4708 · Direito Penal - Legislação Especial > Tráfico de Drogas
- 5545 · Processo Penal > Provas em Espécies > Exame de Corpo de Delito

<details><summary>decisão do ensemble</summary>publicar → 4708 · Direito Penal - Legislação Especial > Tráfico de Drogas (conf 0.85) </details>


---

## Q0268  (origem: Direito Penal / Teoria do Crime (Ilicitude))

```
Assinale a alternativa correta:

(A) São requisitos do tipo, no crime de falsidade ideológica: 1) alteração da verdade sobre fato juridicamente relevante; 2) imitação da verdade; 3) potencialidade do dano; 4) dolo.
(B) O uso de documento falso não é crime formal e sua caracterização depende da ocorrência de um resultado naturalístico específico e determinado.
(C) A persecução do crime de "abuso de autoridade" somente se procede mediante queixa do ofendido.
(D) Não é punível a calúnia contra os mortos.
(E) A exceção da verdade, nos crimes contra a honra, é cabível, indistintamente, tanto na calúnia, quanto na injúria e na difamação.
```

Candidatos (em ordem aleatória):

- 5120 · Penal > Dos Crimes Contra a Honra
- 5116 · Penal > Dos Crimes Contra a Fé Pública e de Falsidade Documental

<details><summary>decisão do ensemble</summary>revisar → 5116 · Penal > Dos Crimes Contra a Fé Pública e de Falsidade Documental (conf 0.32) questão multi-tema (alternativas sobre institutos diferentes); ramo Dos Crimes Contra a Fé Pública e de Falsidade Documental</details>


---

## Q0274  (origem: Penal / Roubo, Crimes contra o patrimônio)

```
Tendo como referência a jurisprudência sumulada dos tribunais superiores, julgue o item a seguir, acerca de crimes, penas, imputabilidade penal, aplicação da lei penal e institutos. Na hipótese de tentativa de subtração patrimonial e morte consumada, o agente responderá pelo crime de latrocínio consumado.

(C) Certo
(E) Errado
```

Candidatos (em ordem aleatória):

- 5177 · Penal > Iter Criminis > Crime Consumado e Tentado
- 5157 · Penal > Dos Crimes Contra o Patrimônio
- 5160 · Penal > Dos Crimes Contra o Patrimônio > Roubo

<details><summary>decisão do ensemble</summary>publicar → 5157 · Penal > Dos Crimes Contra o Patrimônio (conf 0.85) </details>


---

## Q0300  (origem: Penal / Crimes contra a administração pública, Favorecimento pessoal)

```
Àquele que oculta uma arma de fogo utilizada por terceiro para a prática anterior de um roubo, consignando-se não haver qualquer vínculo de parentesco entre ambos, pode-se atribuir o crime de ______. Assinale a alternativa que preencha corretamente a lacuna.

(A) favorecimento pessoal
(B) favorecimento real
(C) coautoria do crime de roubo
(D) participação do crime de roubo
```

Candidatos (em ordem aleatória):

- 5071 · Penal > Concurso de Pessoas
- 5084 · Penal > Dos Crimes Contra a Administração Judicial > Favorecimento Pessoal e Real
- 5079 · Penal > Dos Crimes Contra a Administração Judicial

<details><summary>decisão do ensemble</summary>publicar → 5084 · Penal > Dos Crimes Contra a Administração Judicial > Favorecimento Pessoal e Real (conf 0.9) </details>


---

## Q0303  (origem: Direito Penal / Ação Penal)

```
Com relação à aplicação da lei penal, assinale a opção correta.

(A) As frações de dia são computadas como um dia integral de pena nas penas privativas de liberdade e nas restritivas de direitos.
(B) O direito penal, quanto ao tempo do crime, considera praticado o crime no momento do seu resultado.
(C) A sentença estrangeira, quando a aplicação da lei brasileira produz as mesmas consequências, poderá ser homologada no Brasil para todos os efeitos, exceto para obrigar o condenado à reparação do dano.
(D) Ficam sujeitos à lei brasileira os crimes contra o patrimônio ou a fé pública do DF, de estado, de município, de empresa pública, sociedade de economia mista, autarquia ou fundação instituída pelo poder público, embora cometidos no estrangeiro, sendo o agente punido segundo a lei brasileira, ainda que absolvido no estrangeiro.
(E) Não é aplicável a lei brasileira aos crimes praticados a bordo de aeronaves ou embarcações estrangeiras de propriedade privada, ainda que achando-se aquelas em pouso no território nacional ou em vôo no espaço aéreo correspondente, e estas em porto ou mar territorial do Brasil.
```

Candidatos (em ordem aleatória):

- 5181 · Penal > Lei Penal no Tempo e no Espaço > Lei penal no Tempo
- 5182 · Penal > Lei Penal no Tempo e no Espaço > Lei penal no Espaço
- 5180 · Penal > Lei Penal no Tempo e no Espaço

<details><summary>decisão do ensemble</summary>publicar → 5180 · Penal > Lei Penal no Tempo e no Espaço (conf 0.93) </details>


---

## Q0313  (origem: Direito Penal / Teoria da Pena (Parte 02))

```
A condenação tem como efeito genérico tornar certa a obrigação de reparar o dano. Esse efeito é automático, não precisa ser expressamente pronunciado pelo juiz na sentença condenatória e destina-se a formar título executivo judicial para a propositura de ação civil ex delicto.

(C) Certo
(E) Errado
```

Candidatos (em ordem aleatória):

- 5199 · Penal > Teoria da Pena
- 5209 · Penal > Teoria da Pena > Efeitos da Condenação Penais e Extrapenais
- 5577 · Processo Penal > Sentença Penal > Efeitos Decorrentes da Sentença Penal Condenatória

<details><summary>decisão do ensemble</summary>publicar → 5199 · Penal > Teoria da Pena (conf 0.88) </details>


---

## Q0318  (origem: Penal / -)

```
Com intenção de matar Mário, Lúcio adquiriu, de forma clandestina, uma arma de fogo e munições. Após monitorar a rotina da vítima, Lúcio aguardou Mário sair do trabalho e, enquanto ele caminhava em direção ao seu veículo, Lúcio sacou a arma e disparou uma única vez, atingindo-o. Mesmo possuindo ainda quatro projéteis intactos na arma, Lúcio sentiu repentino remorso, guardou a arma e ligou para o serviço de emergência. Mário foi socorrido, mas, apesar de todo o esforço médico empregado, veio a falecer dias depois no hospital em decorrência exclusiva dos ferimentos causados pelos disparos. Diante de tal situação hipotética, assinale a afirmativa correta.

(A) O caso narrado configura desistência voluntária, uma vez que Lúcio interrompeu voluntariamente a execução do homicídio quando ainda dispunha de meios para prosseguir, devendo, portanto, responder apenas pelo delito de lesão corporal.
(B) O caso narrado configura arrependimento eficaz, pois Lúcio exauriu os meios de execução que seriam suficientes para atingir o resultado almejado, contudo, agiu positivamente para evitá-lo, devendo, portanto, responder apenas pela tentativa de homicídio.
(C) A intervenção de Lúcio ao chamar o socorro não exclui a tipicidade, uma vez que o resultado morte efetivamente ocorreu por consequência direta de sua conduta, devendo ele responder por homicídio consumado, sem prejuízo da aplicação de atenuante genérica.
(D) O caso narrado configura arrependimento posterior, pois Lúcio buscou minimizar as consequências do crime praticado logo após a sua consumação ao chamar o socorro médico, o que enseja a redução da pena do homicídio de um a dois terços.
(E) O caso narrado configura crime impossível por ineficácia relativa do meio empregado, pois a intervenção médica quase evitou o resultado, demonstrando que a conduta do agente não era inequivocamente apta a garantir a consumação inicialmente pretendida.
```

Candidatos (em ordem aleatória):

- 5175 · Penal > Iter Criminis
- 5178 · Penal > Iter Criminis > Desistência Voluntária, Arrependimento Eficaz e Arrependimento posterior
- 5177 · Penal > Iter Criminis > Crime Consumado e Tentado

<details><summary>decisão do ensemble</summary>publicar → 5175 · Penal > Iter Criminis (conf 0.9) </details>


---

## Q0320  (origem: Processo Penal / Inquérito Policial)

```
O Direito Processual Penal, doutrinariamente, elenca as espécies de testemunhas. Dentre elas há a chamada testemunha fedatária.

(A) é a testemunha que depõe sobre algum fato que ouviu dizer.
(B) é a testemunha que depõe sobre a regularidade de algum ato praticado no inquérito ou no processo.
(C) é a pessoa que foi indicada por outra testemunha, não sendo computada no número máximo de testemunhas.
(D) trata-se dos casos em que a Lei de Drogas e a Lei do crime organizado autorizam os agentes de polícia a se infiltrarem para obterem informações acerca desses crimes.
```

Candidatos (em ordem aleatória):

- 5550 · Processo Penal > Provas em Espécies > Prova Testemunhal
- 5543 · Processo Penal > Provas em Espécies

<details><summary>decisão do ensemble</summary>publicar → 5550 · Processo Penal > Provas em Espécies > Prova Testemunhal (conf 0.88) </details>


---

## Q0322  (origem: Processo Penal / Procedimento Ordinário)

```
Delegado Mário foi denunciado pelo delito de abuso de autoridade, tendo em vista a prática de conduta que se enquadra na seguinte descrição típica: “deixar injustificadamente de comunicar prisão em flagrante à autoridade judiciária no prazo legal.”
O Magistrado competente para a análise da inicial acusatória entendeu por bem rejeitá-la.
Inconformado, o Ministério Público resolve recorrer de tal decisão.

(A) Apelação, no prazo de 5 dias.
(B) Apelação, no prazo de 10 dias.
(C) Recurso em Sentido Estrito, no prazo de 20 dias.
(D) Recurso em Sentido Estrito, no prazo de 2 dias.
(E) Recurso em Sentido Estrito, no prazo de 5 dias.
```

Candidatos (em ordem aleatória):

- 5561 · Processo Penal > Recursos em Espécies > Recurso em sentido estrito (RESE)
- 5560 · Processo Penal > Recursos em Espécies
- 5531 · Processo Penal > Procedimento Ordinário > 2 Oferecimento, Rejeição e Recebimento da Peça Acusatória

<details><summary>decisão do ensemble</summary>publicar → 5561 · Processo Penal > Recursos em Espécies > Recurso em sentido estrito (RESE) (conf 0.85) </details>


---

## Q0324  (origem: Direito Penal - Legislação Especial / Teoria da Pena (Parte 02))

```
É certo afirmar:
I. A pena de prisão simples deve ser cumprida, sem rigor penitenciário, em estabelecimento especial ou seção especial de prisão comum, em regime semiaberto ou aberto.
II. As penas acessórias previstas no Código Penal são a perda da função pública eletiva ou de nomeação, as interdições de direitos e a publicidade da sentença.
III. No caso da semi-imputabilidade, a periculosidade é presumida a partir da verificação, por meio da realização de exame pericial, do estado de doença ou perturbação mental, bem como de desenvolvimento mental incompleto ou retardado do indivíduo no instante da prática do fato delituoso. Nesse caso, o juiz pode aplicar medida de segurança, devendo fundamentar a sua decisão demonstrando a existência da periculosidade.
IV. O trabalho do preso será remunerado, não podendo ser inferior a três quartos do salário mínimo, estando sujeito ao regime da Consolidação das Leis do Trabalho.

(A) Todas as proposições estão corretas.
(B) Somente as proposições II e III estão corretas.
(C) Somente as proposições I e III estão corretas.
(D) Somente as proposições I e IV estão corretas.
```

Candidatos (em ordem aleatória):

- 5184 · Penal > Medida de Segurança
- 5199 · Penal > Teoria da Pena

<details><summary>decisão do ensemble</summary>revisar → 5199 · Penal > Teoria da Pena (conf 0.52) questão multi-tema (alternativas sobre institutos diferentes); ramo Teoria da Pena</details>


---

## Q0329  (origem: Processo Penal / Ação Penal (Parte 01))

```
Em determinado estado brasileiro, uma investigação revelou um esquema criminoso que envolvia a competição futebolística estadual: Cavalcante, empresário no ramo do futebol, dono do time Tapauense, conseguia cooptar árbitros e jogadores de clubes de outros municípios para criar situações em momentos críticos durante as partidas, com o objetivo de manipular resultados. A promessa era de que, após os jogos, o empresário faria investimentos para ajudar os envolvidos a migrar para o mercado de futebol no Sudeste do país. Quanto à comissão de arbitragem, constatou-se que seu presidente simulava os sorteios com um assistente e, assim, conseguia indicar árbitros que se alinhavam ao esquema. Aos árbitros honestos eram destinados os mais distantes jogos e as piores condições de trabalho. Para os jogadores, a vantagem prometida ou a transferência em dinheiro nunca eram realizadas, ao passo que aos árbitros era pago o dinheiro mediante a sua contratação falsa como professores de treino de uma escolinha particular de futebol, que sequer existia. Everton respondia pela escolinha e era professor aposentado da secretaria de educação e desporto do estado. A investigação avançou devido à colaboração do jogador de futebol Kiko Jr., que havia participado do esquema por indicação de Alves, um dos árbitros. Segundo o próprio jogador, Alves combinara com ele a marcação de um pênalti resultante de falta provocada pelo zagueiro Kiko Jr. em determinado momento da partida contra o Tapauense, o que foi feito. No entanto, como não fora atendido nas promessas feitas dentro do esquema, Kiko Jr. se revoltou e, então, procurou a polícia, revelando os fatos até então desconhecidos.

(A) O MP poderá deixar de oferecer denúncia a Kiko Jr., desde\nque o jogador tenha contribuído efetivamente para a\nidentificação dos envolvidos da organização criminosa.
\n
(B) A conduta de Kiko Jr. é atípica.
(C) Kiko Jr. foi vítima do crime de estelionato.
(D) No âmbito da investigação, o testemunho de Kiko Jr. tem\nnatureza de meio de prova e pode servir-lhe de atenuante por\nconfissão espontânea.
\n
(E) A colaboração de Kiko Jr. não o exime da pena pelo crime\npraticado, porém sua pena pode ser reduzida em até 2/3.
\n
```

Candidatos (em ordem aleatória):

- 5557 · Processo Penal > Provas em Espécies > Colaboração Premiada
- 4705 · Direito Penal - Legislação Especial > Organizações Criminosas

<details><summary>decisão do ensemble</summary>revisar → 4705 · Direito Penal - Legislação Especial > Organizações Criminosas (conf 0.54) ramo certo, subtema incerto (claude-opus: nível 1); confiança abaixo do limiar</details>


---

## Q0332  (origem: Processo Penal / Ação Penal (Parte 02))

```
Acolhendo a proposta do Ministério Público aceita pelo autor da infração, o Juiz aplicará a pena restritiva de direitos ou de multa, que não importará em reincidência, sendo registrada apenas para impedir novamente o mesmo benefício no prazo de cinco anos.
Assim sendo, enquadra-se nesse caso, a pessoa que,

(A) tendo aceito a proposta de transação penal, pela\nprática de lesão corporal, com o cumprimento de\n72 horas de prestação de serviços à comunidade\nem dezembro ano de 2012, não terá sob qualquer\nhipótese, direito a nova transação penal antes de\ndezembro de 2017.
(B) tendo aceito a proposta de transação penal, pela\nprática de constrangimento ilegal, com o\npagamento de multa em dezembro de 2012, e\nhistórico de prática de lesão corporal em setembro\nde 2017, terá direito a nova transação penal.
(C) tendo aceito a proposta de transação penal, pela\nprática de desacato, e não cumprido o acordo da\nproposta, poderá em audiência conciliatória, ter\nfeita nova proposta de transação penal.
(D) tendo cumprida a proposta de transação penal\npela prática do crime de ameaça, praticado em\n2014, poderá, ter proposta nova transação penal\nem crime praticado em 2017.
(E) tendo praticado o crime de homicídio em agosto\nde 2012 seguindo de prática de crime de lesão\ncorporal leve após saída em livramento\ncondicional, terá proposta de transação penal em\nrelação ao segundo crime.
```

Candidatos (em ordem aleatória):

- 5539 · Processo Penal > Procedimento Sumaríssimo
- 4701 · Direito Penal - Legislação Especial > Juizado Especial Criminal
- 5541 · Processo Penal > Procedimento Sumaríssimo > Transação Penal

<details><summary>decisão do ensemble</summary>revisar → 5541 · Processo Penal > Procedimento Sumaríssimo > Transação Penal (conf 0.5) ramo certo, subtema incerto (claude-opus: Transação Penal); confiança abaixo do limiar</details>


---

## Q0333  (origem: Direito Penal / Iter Criminis)

```
Assinale a alternativa CORRETA.

(A) A pessoa pode ser, ao mesmo tempo, sujeito ativo e passivo de um delito em face de sua própria conduta.
(B) O agente responderá tão-somente por tentativa de crime se ocorrer a desistência voluntária ou o arrependimento eficaz.
(C) O condenado não reincidente, cuja pena não exceda a doze anos, poderá, desde o princípio, cumpri-la em regime semiaberto.
(D) O positivismo criminológico utiliza método empírico-intuitivo experimental, contrapondo-se à análise filosófico-metafísica da escola clássica.
(E) Na contagem dos prazos, leva-se em consideração o dia do final, excluindo-se o do começo.
```

Candidatos (em ordem aleatória):

- 5175 · Penal > Iter Criminis
- 4373 · Criminologia > Etapas Evolutivas e Escolas Criminológicas > Escolas Crimonológicas

<details><summary>decisão do ensemble</summary>revisar → 5175 · Penal > Iter Criminis (conf 0.24) questão multi-tema (alternativas sobre institutos diferentes); ramo Iter Criminis</details>


---

## Q0336  (origem: Penal / Crimes contra o patrimônio, Furto)

```
Em 05 de junho de 2022, Mariana entrou em um restaurante estilo “self-service” e apoiou sua bolsa em uma cadeira. Enquanto conversava distraidamente com seu marido, José, Mariana esqueceu sua bolsa aberta. Diogo, outro cliente que estava no estabelecimento, terminou o almoço, levantou-se de onde estava sentado e foi em direção ao caixa para efetuar o pagamento da conta. Nesse momento, Diogo percebeu a bolsa de Mariana aberta e, sorrateiramente, pegou o aparelho celular dela. Logo em seguida, Mariana e José deram falta do aparelho e iniciaram a procura no local, tendo José visto Diogo na fila do caixa com o celular de Mariana. Imediatamente, José interpelou Diogo e restou comprovado que se tratava realmente do celular de Mariana. De acordo com jurisprudência consolidada dos Tribunais Superiores, em relação à conduta de Diogo, pode-se afirmar que

(A) praticou o crime de roubo consumado, previsto no art. 157, caput, do CP.
(B) praticou o crime de furto, na sua forma tentada, previsto no art. 155, caput, c/c art. 14, II, ambos do CP.
(C) praticou o crime de roubo, na sua forma tentada, previsto no art. 157, caput c/c art. 14, II, ambos do CP.
(D) praticou o crime de furto consumado, previsto no art. 155, caput, do CP.
(E) praticou o crime de apropriação indébita, previsto no art. 168, caput, do CP.
```

Candidatos (em ordem aleatória):

- 5157 · Penal > Dos Crimes Contra o Patrimônio
- 5177 · Penal > Iter Criminis > Crime Consumado e Tentado
- 5159 · Penal > Dos Crimes Contra o Patrimônio > Furto

<details><summary>decisão do ensemble</summary>revisar → 5159 · Penal > Dos Crimes Contra o Patrimônio > Furto (conf 0.72) ramo certo, subtema incerto (claude-opus: Furto); confiança abaixo do limiar</details>


---

## Q0341  (origem: Direito Penal / Concurso de Crimes)

```
Quanto aos crimes contra o patrimônio, possível assegurar que

(A) é pública condicionada a ação penal no caso de dano cometido por motivo egoístico ou com prejuízo considerável para a vítima.
(B) é causa de aumento da pena no roubo o fato de a vítima estar em serviço de transporte de valores, independentemente de o agente conhecer a circunstância.
(C) é admissível no furto praticado em concurso de pessoas o acréscimo de um terço até metade sobre a pena prevista para a forma simples do delito, por aplicação analógica do disposto para o roubo majorado pela mesma circunstância.
(D) o crime de duplicata simulada é de natureza formal, não exigindo a ocorrência de resultado naturalístico.
(E) cabível o perdão judicial na receptação dolosa simples, se primário o agente e de pequeno valor a coisa.
```

Candidatos (em ordem aleatória):

- 5157 · Penal > Dos Crimes Contra o Patrimônio
- 5166 · Penal > Dos Crimes Contra o Patrimônio > Estelionato

<details><summary>decisão do ensemble</summary>publicar → 5157 · Penal > Dos Crimes Contra o Patrimônio (conf 0.93) </details>


---

## Q0355  (origem: Direito Penal / Concurso de Crimes)

```
À luz da recente decisão do Supremo Tribunal Federal com repercussão geral a respeito do Art. 28 da Lei nº 11.343/2006, é correto afirmar que:

(A) são atípicas as condutas de adquirir, guardar, ter em\ndepósito, transportar ou trazer consigo, para consumo\npessoal, 1g da substância entorpecente cocaína, distribuído\nem duas cápsulas plásticas;
(B) a transação penal firmada, em dezembro de 2023, pela\nprática do crime de trazer consigo maconha, para consumo\npessoal, configura obstáculo ao oferecimento de acordo de\nnão persecução penal, caso praticado o crime de furto\nsimples, em janeiro de 2025;
(C) pratica crime de abuso de autoridade o delegado de polícia\nque lavrar auto de prisão em flagrante contra o cidadão\nsurpreendido com um tablete de 10g de maconha\nacondicionados em um sacolé, uma balança de precisão e\num caderno com anotações relativas a datas, valores e\nnomes;
(D) as condutas de adquirir, guardar, ter em depósito,\ntransportar ou trazer consigo até 40g de maconha ou seis\nplantas fêmeas, para consumo próprio, são indiferentes para\no ordenamento jurídico;
(E) não se admite a imposição de prestação de serviços à\ncomunidade em virtude da prática das condutas de adquirir,\nguardar, ter em depósito, transportar ou trazer consigo até\n40g de maconha ou seis plantas fêmeas, para consumo\npróprio.
```

Candidatos (em ordem aleatória):

- 4708 · Direito Penal - Legislação Especial > Tráfico de Drogas
- 4684 · Direito Penal - Legislação Especial > Abuso de Autoridade

<details><summary>decisão do ensemble</summary>publicar → 4708 · Direito Penal - Legislação Especial > Tráfico de Drogas (conf 0.93) </details>


---

## Q0359  (origem: Processo Penal / Ação Penal (Parte 02))

```
Aos crimes cometidos contra idosos, cuja pena máxima privativa de liberdade não ultrapasse quatro anos, aplica-se o procedimento previsto na Lei nº 9.099/1995, e, subsidiariamente, no que couber, as disposições do Código Penal e do Código de Processo Penal.
O STF, contudo, vedou, nesses casos, a possibilidade de que fossem aplicadas quaisquer das medidas despenalizadoras previstas na Lei nº 9.099/1995.

(C) Certo
(E) Errado
```

Candidatos (em ordem aleatória):

- 4701 · Direito Penal - Legislação Especial > Juizado Especial Criminal
- 4696 · Direito Penal - Legislação Especial > Estaturo de Idoso - Crimes

<details><summary>decisão do ensemble</summary>revisar → 4696 · Direito Penal - Legislação Especial > Estaturo de Idoso - Crimes (conf 0.65) ramo certo, subtema incerto (claude-opus: nível 1); confiança abaixo do limiar</details>
