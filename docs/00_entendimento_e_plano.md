# 00 — Entendimento do case e plano de abordagens

> Rascunho v0, escrito em 16/10/2026 (sexta). Este documento é o "diário de bordo" do raciocínio antes do código: o que entendemos, o que achamos nos dados, as abordagens candidatas e as decisões em aberto. Ele vai evoluir e, no fim, alimenta a seção (a) do relatório.

---

## 1. O desafio em uma frase

Classificar 359 questões reais de concurso (Penal, Processo Penal, Legislação Penal Especial e Criminologia) em uma árvore de 377 temas, decidindo para cada uma entre **publicar** (vai direto ao aluno), **revisar** (fila do professor, com sugestão) e **fora** (nenhum tema serve), de modo que **pelo menos 95% das publicadas estejam certas** e, dentro disso, o maior número possível seja publicado. Sem gabarito: estimar a própria precisão faz parte do problema.

## 2. Regras do jogo (lidas do PDF, README e LEIA-ME)

### 2.1 O que conta como acerto

- Acerta quem publica **no tema que a equipe de especialistas atribuiu** à questão, **ou em um nó do mesmo ramo (pai ou filho dele)**, porque o aluno que estuda um tema também vê as questões dos subtemas.
- Publicar em **outro subtema do mesmo tema (irmão) conta como erro**.
- Só as questões **publicadas** entram na conta da precisão. `revisar` e `fora` não penalizam a precisão, apenas reduzem a cobertura.

Implicação estratégica (a confirmar em conjunto, ver §9): quando temos certeza do tema de nível 1 mas dúvida entre dois subtemas irmãos de nível 2, **publicar no nível 1 é correto pela régua** e também é honesto para o produto (o aluno vê a questão ao estudar o tema). Publicar na raiz (nível 0 = disciplina) seria tecnicamente "pai de tudo", mas é jogar contra o espírito do case; não faremos isso e vamos registrar a escolha no relatório.

### 2.2 Entregáveis

| Entregável | Conteúdo | Observações |
|---|---|---|
| `publicacao.csv` | 359 linhas: `id, decisao, tema_central_id, extras_ids, confianca, motivo` | `tema_central_id` obrigatório em publicar e revisar; vazio em fora. `motivo` obrigatório em revisar e fora |
| `previsao.txt` | precisão prevista e cobertura prevista, cada uma com intervalo, e a explicação | Comparam com o resultado real: previsão honesta pesa na avaliação |
| Relatório (≤ 5 páginas) | (a) como pensamos, inclusive becos sem saída; (b) diagnóstico dos dados e dos temas; (c) desenho para produção (50 mil questões/semana): tipos de IA, custo por questão, medição contínua, encaixe no fluxo; (d) memo de 1 página para o professor | PDF ou Markdown |
| Código | Pipeline completo, prompts, chamadas a modelos, regras de decisão, estimativa de precisão, README de como rodar; modelos usados, custo aproximado e tempo; decisões tomadas à mão | "Mesmo que esteja bagunçado" |

Prazo: **domingo, 18/10/2026**. Entrega: repositório público no GitHub, link para carla@viciodeumaestudante.com.br.

### 2.3 O que pesa e o que não pesa

Pesa: cobertura com precisão ≥ 95%; o quanto a previsão acerta o próprio resultado; raciocínio, diagnóstico e desenho de produção; clareza com quem não é técnico.
Não pesa: código bonito, infraestrutura sofisticada, usar o modelo mais caro, volume de páginas, saber Direito Penal de cor.

Leitura: o case avalia **julgamento**. A solução "LLM classifica tudo" é o ponto de partida, não o fim. O diferencial está em (i) saber quando não confiar, (ii) estimar a própria precisão sem gabarito e (iii) explicar.

## 3. O que encontramos nos dados (diagnóstico inicial)

### 3.1 As 359 questões

| Aspecto | Achado |
|---|---|
| Estrutura | 359 registros, ids únicos Q0001–Q0359, todos com os 6 campos |
| `disciplina_origem` | Processo Penal 131 · Direito Penal 129 · Legislação Especial 32 · Criminologia 31 · Penal 27 · **9 fora do recorte** (Constitucional 2, Civil-Leg. Especial 2, Tributário 1, Ambiental 1, "Disciplina Unificada" 1, "Direito Processual Penal" 1, vazia 1) |
| `assunto_origem` | 95 valores distintos; 18 vazios; nomes de "aula de curso" como "Ação Penal (Parte 01)", "Teoria da Pena (Parte 02)"; **"Concurso de Crimes" tem 43 questões, a maioria sem relação com o assunto** (meio ambiente, racismo, terrorismo, concussão…). Ou seja, a origem é um sinal fraco e às vezes enganoso |
| `comando` | vazio em 94; "<br>" em 7; em alguns casos é um texto gerado ("Explique o que é a prisão preventiva.") que não faz parte da questão |
| `enunciado_html` | HTML cru: `<br>` em 125, `<i>`/`<b>` em ~60, `\n` literal em 26, sem imagens. Tamanho: mediana 207 caracteres, p90 956, máx. 2.542 |
| Alternativas | 5 alternativas: 255 · Certo/Errado: 58 · 4 alternativas: 46 |
| "Duplicatas" | 11 questões cujo enunciado é só "Assinale a alternativa correta/incorreta": **o conteúdo está inteiramente nas alternativas**. Nenhuma duplicata real |
| Lixo de Word | **Q0099**: três alternativas com ~35 mil caracteres cada de HTML/XML do Microsoft Word (comentários condicionais, `<xml>`, estilos); o texto útil tem ~800 caracteres por alternativa. A limpeza precisa remover comentários, `<xml>`/`<style>` e tags, não só `<br>` |

Consequências para o pipeline: o texto classificável precisa ser **enunciado + alternativas** (limpos de HTML); `comando` é dispensável; `disciplina_origem` e `assunto_origem` entram só como sinal auxiliar.

### 3.2 A árvore de 377 temas

| Aspecto | Achado |
|---|---|
| Forma | 4 raízes (nível 0), 111 temas (nível 1), 262 subtemas (nível 2). Penal 186 · Processo Penal 138 · Leg. Especial 27 (sem nível 2) · Criminologia 26 |
| Status | 2 inativos (Direito penal econômico; Tratados e convenções em matéria criminal) |
| Descrições | 337/377 são boilerplate ("Subtema de X. N questões no source."), sem conteúdo semântico; 20 têm texto de verdade; 20 estão vazias |
| Temas "novos" (ids 67xx) | 20 temas sem descrição e sem contagem: cópias de temas da Legislação Especial dentro de Penal (Lei Maria da Penha, Tráfico de Drogas, Lavagem, Org. Criminosas, Abuso de Autoridade, Meio ambiente, Estatuto do Idoso) e **buckets não semânticos "(Parte 1)/(Parte 2)"** (Teoria da Pena, Crimes contra a Administração, Patrimônio, Competência, Sentença Penal, Recursos (Parte 03)). Nomes de aula, não de tema |
| Títulos duplicados entre disciplinas | 8: Abuso de Autoridade, Crimes contra o meio ambiente, Lavagem de Dinheiro, Lei Maria da Penha, Lei de Execução Penal (Leg. Especial × Processo Penal), Organizações Criminosas, Tráfico de Drogas, Ação Penal (Penal × Processo Penal) |
| "Lixeiras" (contagem de origem muito alta em temas genéricos) | Sistemas e Princípios Processuais Penais (538) · Introdução ao Estudo do Direito Penal (424; "Conceito e Fontes" sozinho tem 310) · Teoria Geral das Prisões (359; "Conceitos e Espécies de Prisão" 209) · Inquérito Policial > Conceito/Finalidade (164) · Características e Condições da Ação Penal (212) · Noções gerais dos crimes contra a adm. pública (100) · Sanção Penal: Conceito (107) · Conceito e Elementos da Culpabilidade (100) |
| Qualidade editorial | Erros de digitação nos títulos ("Escolas Crimonológicas", "Estaturo de Idoso", "Comeptência Territorial", "Caractéristas", "Crimescontra"), números residuais ("12 Disposições Gerais…", "2 Oferecimento…"), 7 temas com 0 questões, 60 temas de nível 1 sem filhos |

### 3.3 Cruzamento `assunto_origem` × títulos da árvore

- 225/359 assuntos de origem têm um título **idêntico** na árvore; mas só 123 na mesma disciplina, e 82 são ambíguos (o mesmo título existe em mais de um lugar).
- 134 não têm match exato; 71 assuntos distintos. Muitos são concatenações de vários tópicos ("Corrupção ativa, Corrupção passiva, Peculato") ou nomes de aula.
- Logo, um baseline "copia a origem" teria no máximo ~1/3 de cobertura segura, e mesmo esse terço precisa ser verificado porque a origem erra (ex.: "Comunicação dos atos processuais" rotulando questões de desaforamento, direito ao silêncio e habeas corpus).

### 3.4 Hipóteses sobre o que é difícil (para validar durante o trabalho)

1. **Questões "multi-tema"**: cada alternativa trata de um crime diferente (ex.: Q0268: falsidade ideológica, uso de documento falso, abuso de autoridade, calúnia, exceção da verdade). Não há tema central óbvio. Candidatas naturais a `revisar` ou a um nível 1 abrangente.
2. **Fronteira Penal × Processo Penal × Execução**: ação penal, prescrição, execução penal, habeas corpus, Lei Maria da Penha existem em mais de um ramo. Errar o ramo é erro, mesmo com o assunto certo.
3. **Irmãos de nível 2 com fronteira difusa**: "Fato Típico" × "Tipicidade" × "Conduta"; "Conceito e Elementos da Culpabilidade" × "Inimputabilidade"; "Princípios do Direito Penal" × "Tipicidade" (princípio da insignificância). É exatamente onde o backoff para o nível 1 vale ouro.
4. **Legislação Especial vs. tema equivalente em Penal (67xx)**: qual dos dois o especialista usou? Provavelmente o da Legislação Especial (tem histórico e contagem); o de Penal é cópia recente e vazia. Decisão a registrar.
5. **Certo/Errado (58)**: itens curtos, uma afirmação só, frequentemente precedidos de contexto amplo ("julgue os itens sobre prisão…"). Pouco texto para decidir.
6. **Criminologia**: perguntas sobre autores e escolas; a árvore tem subtemas finos (Teorias de Nível Sociológico × Teorias Criminológicas em Espécie) que até humanos confundiriam.
7. **Fora do recorte**: ~5–10 questões (ITCD/Direito Tributário, ECA/medidas socioeducativas, Lei 9.029/95, suborno no futebol…). Algumas parecem fora mas têm tema (Lei 9.605 → Crimes contra o meio ambiente; crimes contra idoso → Estatuto do Idoso).

## 4. Ambiente disponível (levantado em 16/10)

| Recurso | Situação |
|---|---|
| Python | 3.10.11, `uv` 0.9.3; instalados: numpy, polars, scikit-learn, torch (CPU), matplotlib, httpx, pydantic. Faltam: anthropic/openai/google-genai, sentence-transformers, pandas |
| Modelos locais | Ollama com gemma3:4b, qwen2.5vl:3b e mxbai-embed-large (embeddings). GPU RTX 3050 4 GB, 16 GB RAM |
| APIs de LLM | Nenhuma chave de API nas variáveis de ambiente. O Claude Code está logado com **assinatura Max** (claude.ai) e o modo headless funciona: `claude -p "<prompt>" --model haiku\|sonnet\|opus --output-format json` devolve JSON com uso de tokens e custo a preço de lista. Serve como motor reprodutível (um script Python chama a CLI), com a ressalva de que cada chamada carrega ~37 mil tokens de contexto do próprio Claude Code (cacheados por 1 h), o que pede processar várias questões por chamada. Só cobre a família Anthropic; para concordância entre famílias (E2) falta um segundo provedor (ver §9, decisão 1) |
| GitHub | `gh` autenticado como lpmu06; git configurado |
| Web | Busca web encontra as questões (ex.: Q0002 no QConcursos), mas a página retorna 403 para acesso automatizado |

## 5. Abordagens candidatas, do simples ao complexo

A ideia é construir uma escada: cada degrau é um pipeline completo que gera um `publicacao.csv`, e o relatório compara os degraus. Nem todos precisam ir até o fim; os que forem descartados viram "becos sem saída" documentados.

### Degrau A — sem LLM (baratos, explicáveis, servem de baseline e de diagnóstico)

| # | Abordagem | Como | Custo | Para que serve |
|---|---|---|---|---|
| A0 | **Copiar a origem** | `assunto_origem` → tema por match de título (restrito à disciplina) | zero | Mostrar que a origem é ruidosa; sinal auxiliar no ensemble |
| A1 | **Lexical (BM25/TF-IDF)** | texto da questão × texto do tema | zero | Quase inútil com descrições boilerplate; melhora muito com a taxonomia enriquecida (C) |
| A2 | **Embeddings** | questão × tema enriquecido, similaridade de cosseno, top-k | zero (local, mxbai) ou centavos (API) | Pré-seleção de candidatos para o LLM (L3) e segunda opinião barata |

Limite estrutural: sem rótulos não há classificador supervisionado. Em produção, os rótulos do LLM + revisão humana viram dados de treino (destilação). Vale citar na seção (c).

### Degrau B — enriquecer a taxonomia (habilitador de tudo)

| # | Abordagem | Como |
|---|---|---|
| C | **Descrever os 377 temas uma vez** | LLM gera, por tema: descrição de 2–3 linhas, palavras-chave, dispositivos legais cobertos (ex.: Furto → art. 155 CP), fronteiras com irmãos ("não confundir com…"). Custo único, ~377 chamadas curtas |

Sem isso, nem humano nem máquina distingue "Fato Típico" de "Tipicidade" a partir do título. O resultado também é matéria-prima para o memo ao professor (temas duplicados, lixeiras, erros de grafia).

### Degrau C — LLM como classificador (o núcleo)

| # | Abordagem | Como | Prós | Contras |
|---|---|---|---|---|
| L1 | **Árvore inteira no prompt** | prompt fixo com os 377 temas (cabe em ~10–15 mil tokens, cacheável) + questão → `tema_central`, `extras`, `confianca`, `justificativa`, em saída estruturada | simples, um passo, cache barateia | o modelo vê 377 opções; irmãos confundem |
| L2 | **Hierárquico em 2 estágios** | 1º: disciplina + tema nível 1; 2º: subtema dentro do ramo (ou "fica no nível 1") | espelha a régua; backoff natural; menos distração | duas chamadas; erro no 1º estágio é fatal |
| L3 | **Retrieval + LLM** | embeddings/BM25 selecionam top-10 temas; LLM escolhe entre eles | barato e escalável (produção) | depende do recall do retrieval |

### Degrau D — confiança sem gabarito (o "pulo do gato")

| # | Técnica | Ideia |
|---|---|---|
| E1 | Auto-consistência | N amostras do mesmo modelo; concordância = confiança. Barato, mas erros do mesmo modelo são correlacionados |
| E2 | **Concordância entre modelos diferentes** | 2–3 modelos de famílias distintas classificam de forma independente; concordância forte → publicar; divergência → revisar. Erros menos correlacionados que E1 |
| E3 | Juiz adversarial | Segundo passo tenta refutar: "há um irmão melhor? o ramo está certo? a questão tem tema central?" |
| E4 | Concordância com a origem | `assunto_origem`/`disciplina_origem` como voto fraco (concorda → sobe confiança; discorda → não derruba sozinho) |
| E5 | Pivô por dispositivos legais | questão → artigos/leis testados → tema (via mapa artigo→tema da taxonomia enriquecida). Explicável e verificável pelo professor |

### Degrau E — evidência externa (pensar fora da caixa; a decidir)

As questões são reais e indexadas (QConcursos etc.). Em tese, a classificação de outros sites é um "votante" independente. Na prática: o QConcursos bloqueia acesso automatizado (403), há questão de termos de uso, as taxonomias não batem com a nossa, e o custo de tempo é alto para 2 dias. Proposta: **não entra no pipeline**; no máximo, consulta manual em meia dúzia de casos de dúvida, registrada como decisão à mão, e discussão no relatório como caminho testado e limitado.

## 6. Regras de decisão (proposta inicial)

Score de confiança por questão = combinação de: concordância entre modelos (E2), confiança auto-reportada, margem entre 1ª e 2ª opção, nível hierárquico escolhido, e flags de risco (multi-tema, texto curto, disciplina fora do recorte, tema "lixeira" ou 67xx, disputa Penal × Leg. Especial).

| Situação | Decisão |
|---|---|
| Modelos concordam no nível 2 e confiança alta | publicar no nível 2 |
| Concordam no nível 1, divergem no nível 2 | publicar no nível 1 (backoff) |
| Divergem no nível 1 ou no ramo | revisar, com a sugestão majoritária e o motivo |
| Nenhum tema cobre (disciplina fora, lei sem tema) | fora, com motivo |
| Tema escolhido é inativo ou bucket "(Parte N)" | nunca publicar ali; redirecionar para o nó semântico ou revisar |

Os limiares (thresholds) não são chutados: são escolhidos na amostra rotulada (§7) para mirar ~97% internos e sobrar margem para os 95%.

## 7. Como estimar a precisão sem gabarito (proposta)

1. **Amostra rotulada por nós** (estratificada por faixa de confiança e disciplina, ~60–80 questões): leitura humana (Luis) com apoio de pesquisa, registrando o tema e o grau de certeza. Vira nosso "gabarito interno".
2. **Calibração**: precisão observada por faixa de confiança na amostra → escolha dos limiares → precisão esperada do conjunto publicado (média ponderada) com intervalo (Wilson/bootstrap).
3. **Checagem cruzada**: a taxa de concordância entre modelos no conjunto todo deve bater com a da amostra; se não bater, a amostra não é representativa.
4. **Previsão final**: ponto + intervalo para precisão e cobertura, com margem de segurança explícita e os motivos (nosso gabarito também erra; a equipe pode ter usado convenções que não conhecemos, ex.: qual "Lei Maria da Penha").

## 8. Plano de execução (prazo: domingo 18/10)

| Quando | O quê |
|---|---|
| Sex 16/10 (hoje) | Entendimento e plano (este doc) · decisões do §9 · estrutura do repo · preparo dos dados (limpeza de HTML, dataset único) · taxonomia enriquecida (C) · baselines A0/A2 · primeira passada LLM (L1 ou L2) com um modelo |
| Sáb 17/10 | Segundo/terceiro modelo (E2) · juiz (E3) · regras de decisão · amostra rotulada (§7) · calibração · `publicacao.csv` v1 · rascunho do relatório e do memo |
| Dom 18/10 | Iteração final · `previsao.txt` · README (como rodar, custo, tempo, decisões à mão) · revisão do relatório · repositório público · e-mail |

Estrutura prevista do repositório:

```
README.md                 como rodar; o que gera publicacao.csv; modelos, custo, tempo
anexos/                   dados originais, intocados
docs/                     00_entendimento_e_plano.md · 01_decisoes.md · relatorio.md · memo_professor.md
prompts/                  todos os prompts, versionados
src/                      00_preparo · 10_taxonomia · 20_baselines · 30_llm · 40_ensemble · 50_calibracao · 60_exportar
runs/                     saídas brutas de cada modelo (JSON), com custo e tempo
publicacao.csv · previsao.txt
```

## 9. Decisões em aberto (precisam do Luis)

1. **Acesso a modelos.** Confirmado: família Anthropic via assinatura Max (Haiku 4.5, Sonnet, Opus) pelo `claude -p`. Falta decidir o **segundo provedor** para a concordância entre famílias (E2): chave da API do Gemini (a camada gratuita cobre 359 questões), OpenAI, OpenRouter, ou só o Gemma 3 4B local (fraco, mas independente). Se preferir não criar chave nenhuma, E2 vira auto-consistência (E1) + juiz (E3) dentro da mesma família, e dizemos isso no relatório.
2. **"Jev".** Qual modelo é esse (na transcrição ficou "Jev")? Entra como um dos votantes?
3. **Backoff hierárquico.** Adotar "publicar no nível 1 quando o nível 2 é incerto"? (Recomendo sim, com transparência no relatório.)
4. **Evidência externa.** Descartar, usar só manualmente em casos de dúvida, ou investir?
5. **Amostra rotulada.** Luis topa rotular ~60–80 questões no sábado (2–3 h) com meu apoio? É o método mais defensável para a previsão.
6. **Repositório.** Nome e momento de criar o repo público (sugiro criar já privado e abrir no domingo).
7. **Orçamento.** Teto de gasto em API para o case (estimativa: uma passada completa com um modelo da família Opus custa na casa de dezenas de dólares com cache; com Sonnet/Haiku, poucos dólares; a confirmar com contagem de tokens antes de rodar).

## 10. Registro de decisões

| Data | Decisão | Motivo |
|---|---|---|
| 16/10 | Arquivos locais conferidos contra o GitHub (README, PDF e os 4 anexos do ZIP: idênticos byte a byte) | Garantir que trabalhamos com os dados oficiais |
| 16/10 | Texto classificável = enunciado + alternativas, limpos de HTML; `comando` ignorado | 11 questões só têm conteúdo nas alternativas; `comando` é vazio ou gerado |
| 16/10 | Limpeza de HTML robusta (comentários, `<xml>`, `<style>`, entidades) antes de qualquer modelo | Q0099 carrega ~100 mil caracteres de lixo do Word que estourariam prompt e custo |
| 18/10 | Segunda família de modelos = OpenAI (GPT-5.x), via chave do Luis; Anthropic via chave de API (Opus/Sonnet/Haiku 5.5). Jev (typesafe.ai) é opcional: até 255 opções por pergunta, caberia como votante hierárquico | Concordância entre famílias (E2) exige provedores independentes |
| 18/10 | Evidência externa (QConcursos etc.) descartada | Luis: acessar conteúdo de um concorrente pode parecer irregular; o ganho não compensa |
| 18/10 | Backoff hierárquico adotado: publicar no nível 1 quando o nível 2 é incerto | Conta como certo pela régua e é honesto para o aluno |
| 18/10 | Temas 67xx ("(Parte N)" e cópias vazias dentro de Penal/Processo Penal) e inativos marcados como "não usar"; o equivalente da Legislação Especial é o alvo (ex.: Lei Maria da Penha 4704, não 6724) | São buckets de curso, sem histórico; o especialista provavelmente usou o nó semântico |
| 18/10 | Prazo caiu para hoje (18/10): escada reduzida ao essencial: baseline de origem, taxonomia enriquecida, classificação LLM com 2 famílias, ensemble, amostra rotulada pequena, relatório | Tempo |
| 19/10 | Só modelos Anthropic pela assinatura Max (`claude -p`); OpenAI descartada depois de esgotar os créditos em 47 questões com o prompt plano de 131 mil tokens | Luis: "não é necessário usar Opus para classificar questões; usar modelos menores". Erro nosso: começar pelo modelo mais caro e pelo prompt maior |
| 19/10 | Comparar três profundidades com o mesmo modelo: plano (árvore inteira + metadados em uma chamada), 2 estágios (tema -> subtema) e 3 estágios (grupo artificial -> tema -> subtema), medindo tokens e concordância; e um modelo menor (Haiku) na versão hierárquica | Luis pediu a comparação "por camadas"; é também o desenho de produção |
| 19/10 | Grupos artificiais de temas de nível 1 definidos à mão em data/grupos_n1.json (23 grupos) | Necessário para o estágio A do classificador de 3 níveis; não existem na plataforma |
| 19/10 | Prazo de 18/10 passou; entregar mesmo assim, priorizando trabalho bem feito | Decisão do Luis |
