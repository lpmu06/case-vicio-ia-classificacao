# Relatório — Case "Classificação de tópicos" (Vício / Método VDE)

Autor: Luis Paulo (lpmu06@gmail.com) · Data: 18/10/2026 · Repositório: github.com/lpmu06/case-vicio-ia-classificacao

> Resultado em uma linha: **[PREENCHER: N publicadas de 359 (X%), precisão prevista Y% (intervalo), com dois modelos de famílias diferentes concordando e backoff hierárquico].**

## a) Como pensamos

**O problema não é classificar; é saber quando não confiar.** Um LLM classifica questões "razoavelmente bem" em minutos, mas a régua do case é de precisão nas publicadas (≥ 95%), não de acurácia média. Isso muda o desenho: o objetivo passa a ser separar as questões em que a classificação é quase certa das que precisam de um professor, e estimar a própria taxa de erro sem gabarito.

**Três leituras da régua guiaram tudo.** (1) Só as publicadas contam; `revisar` e `fora` não penalizam a precisão, só a cobertura. (2) Acerto inclui pai e filho do tema atribuído pelo especialista, mas não o irmão. Logo, quando há certeza do tema de nível 1 e dúvida entre subtemas, publicar no nível 1 é correto pela régua e honesto para o aluno (ele vê a questão ao estudar o tema). Chamamos isso de *backoff hierárquico*. Publicar na raiz (disciplina) seria "pai de tudo" e não fizemos. (3) O que pesa é o julgamento: a previsão da própria precisão é avaliada, então ela precisa ser conservadora e explicada.

**Escada de abordagens, do simples ao complexo.** Planejamos uma escada e subimos só até onde o prazo permitiu:

| Degrau | O que é | O que aconteceu |
|---|---|---|
| A0 · copiar a origem | `assunto_origem` → tema por título | 225/359 têm título idêntico na árvore, mas a origem erra muito ("Concurso de Crimes" rotula 43 questões, a maioria sem relação). Ficou como sinal fraco e como diagnóstico |
| A1/A2 · lexical e embeddings | BM25 / vetores questão × tema | Descartado por tempo e porque as descrições dos temas eram boilerplate (337/377); só faria sentido depois do enriquecimento. Fica como desenho de produção |
| B · enriquecer a taxonomia | LLM escreve, uma vez, descrição, palavras-chave, dispositivos legais e "não confundir com" para cada tema | Feito com GPT-5.5 (89 chamadas, uma por tema de nível 1 com seus subtemas). É o que permite distinguir "Fato Típico" de "Tipicidade" |
| C · LLM classificador | Uma chamada por questão com a árvore + metadados no prompt (cacheado), saída JSON com tema, subtema, confianças, segunda opção, multi-tema | Feito com dois modelos de famílias diferentes: GPT-5.5 (OpenAI) e Claude [PREENCHER modelo] (Anthropic) |
| D · confiança sem gabarito | Concordância entre famílias + confiança auto-reportada + flags de risco → regras publicar/revisar/fora | Feito. Divergência no ramo → revisar; concordância no ramo mas não no subtema → publicar no nível 1 |
| E · evidência externa | Procurar a questão em bancos públicos e usar a classificação deles como voto | Testado e descartado: as questões existem na web (QConcursos), mas o site bloqueia acesso automatizado, as taxonomias não batem e, principalmente, não pareceu correto usar conteúdo de um concorrente |

**Becos sem saída e surpresas.** A chave de API da Anthropic estava sem créditos; resolvemos chamando o Claude Code em modo headless pela assinatura (`claude -p`), o que funciona mas carrega ~45 mil tokens de contexto do próprio Claude Code por chamada. Na primeira rodada os dois modelos puseram a *disciplina* no campo "tema de nível 1"; corrigimos rotulando os níveis na própria árvore do prompt. Uma questão (Q0099) tinha 100 mil caracteres de HTML do Word nas alternativas e teria estourado prompt e custo sem uma limpeza robusta.

## b) Diagnóstico: o que atrapalha máquina e humano

**Nos dados das questões.**
- O texto classificável precisa incluir as alternativas: 11 questões têm enunciado igual a "Assinale a alternativa correta", e tudo está nas alternativas.
- `assunto_origem` e `disciplina_origem` são pistas fracas: 18 assuntos vazios, 9 disciplinas fora do recorte (Tributário, Constitucional, Civil...), nomes de aula ("Ação Penal (Parte 01)", "Teoria da Pena (Parte 02)") e rótulos errados ("Comunicação dos atos processuais" em questões de desaforamento, direito ao silêncio e habeas corpus).
- HTML cru com `<br>`, `\n` literal, entidades e, em um caso, lixo do Word.
- 58 questões Certo/Errado: uma afirmação curta, pouco contexto.

**Na árvore de temas.**
- 20 temas criados depois (ids 67xx) com nomes de aula, "(Parte 1)/(Parte 2)", sem descrição e sem histórico, duplicando temas semânticos. Tratamos como "não usar".
- 8 títulos duplicados entre disciplinas (Lei Maria da Penha, Tráfico de Drogas, Lavagem, Organizações Criminosas, Abuso de Autoridade, Meio ambiente em Penal × Legislação Especial; Lei de Execução Penal em Legislação Especial × Processo Penal; Ação Penal em Penal × Processo Penal). Errar o ramo é erro mesmo com o assunto certo.
- "Lixeiras": temas genéricos com centenas de questões de origem (Sistemas e Princípios Processuais Penais 538; Introdução ao Estudo do Direito Penal 424, sendo 310 em "Conceito e Fontes"; Teoria Geral das Prisões 359; "Noções gerais dos crimes contra a administração pública" 100). São o destino natural de classificações preguiçosas.
- 337 de 377 descrições são boilerplate ("Subtema de X. N questões no source."); 2 temas inativos; erros de grafia nos títulos ("Crimonológicas", "Estaturo de Idoso", "Comeptência", "Caractéristas").

**Que tipo de questão é difícil.**
1. Multi-tema: cada alternativa trata de um crime diferente (ex.: Q0268 mistura falsidade ideológica, abuso de autoridade e crimes contra a honra). Não há tema central; o melhor é o nível 1 mais abrangente ou revisão.
2. Fronteira Penal × Processo Penal × Execução Penal: ação penal, prescrição, habeas corpus, LEP.
3. Irmãos de fronteira difusa: "Fato Típico" × "Tipicidade" × "Conduta"; "Conceito e Elementos da Culpabilidade" × "Inimputabilidade"; "Princípios do Direito Penal" × "Tipicidade" (insignificância).
4. Legislação Especial × cópia em Penal: qual nó o especialista usou? Apostamos no da Legislação Especial e registramos.
5. Criminologia: autores e escolas com subtemas finos ("Teorias de Nível Sociológico" × "Teorias Criminológicas em Espécie").

[PREENCHER: tabela de concordância entre modelos por disciplina e os principais pontos de divergência observados.]

## c) Produção: 50 mil questões por semana

[PREENCHER com números medidos: custo por questão de cada modelo, tempo, taxa de revisão.]

Desenho proposto, em camadas:

1. **Importação.** Limpeza de HTML, deduplicação por hash do texto, extração de "dispositivos citados" (artigos, leis, súmulas) por regex. Questão entra com `assunto_origem` como metadado, nunca como rótulo.
2. **Taxonomia como produto.** Cada tema tem descrição, palavras-chave, dispositivos e "não confundir com", mantidos pelo professor com ajuda do LLM. Temas-lixeira e duplicados são bloqueados para publicação automática. Mudanças na árvore disparam reclassificação só das questões dos ramos afetados.
3. **Classificação em dois estágios.** (i) Embeddings (texto da questão × metadados dos temas) selecionam os 10 temas candidatos: custo quase zero, serve de filtro e de sanidade. (ii) Um modelo rápido (classe Haiku/GPT-mini) escolhe entre os candidatos com saída estruturada; só as questões com confiança abaixo do limiar vão a um modelo forte de outra família. Concordância entre os dois → publica; divergência → fila de revisão com as duas sugestões. Ordem de grandeza: [PREENCHER] por questão no caminho rápido e [PREENCHER] no caminho forte; com 20–30% indo ao caminho forte, [PREENCHER] por semana.
4. **Classificador destilado.** Os rótulos confirmados por professores viram dados de treino de um classificador leve (regressão sobre embeddings) que substitui o estágio (ii) para os ramos onde ele já atinge a precisão alvo, e serve de terceiro voto nos demais.
5. **Qualidade contínua.** Amostra semanal de 100 publicadas auditadas por professor (precisão com intervalo); monitoramento de drift (distribuição por tema, taxa de revisão, concordância entre modelos); reportes de alunos entram como rótulos negativos com prioridade; temas que recebem reportes acima do normal são bloqueados para publicação automática até revisão.
6. **Fila do professor.** Ordenada por valor: questões com maior probabilidade de uso (temas mais estudados) e menor confiança primeiro; cada decisão humana realimenta a taxonomia (descrições) e o classificador.

## d) Memo para o professor

Ver `docs/memo_professor.md` (1 página).

## Anexo: modelos, custo e tempo

[PREENCHER a partir de runs/*/_usage.json]
