# Plano de melhorias — 19/10/2026, 18h15 → meia-noite

Origem: `docs/90_avaliacao_simulada.md` (avaliação simulada, lida e aceita com os ajustes anotados abaixo). Este arquivo é a lista de trabalho. Marque o status de cada item aqui mesmo (`[ ]` → `[x]`) e registre as decisões no diário (`docs/00_entendimento_e_plano.md`, seção 10).

## Status em 19/10 às 19h30

Blocos A, B, C, D e E executados e commitados (um commit por bloco). Bloco F executado: entrega final commitada e enviada ao repositório privado. Bloco G executado em 19/10 à noite, com a chave do Jev: o Jev entra só como estudo (relatório, comparação de métodos e `docs/jev.md`), fora da regra de publicação e da previsão. Pendentes: tornar o repositório público, enviar o e-mail, revogar as chaves.

## Regras de execução (valem para todos os itens)

1. Antes de começar: ler este arquivo inteiro e a seção 2 de `docs/90_avaliacao_simulada.md`.
2. Não alterar `anexos/`. Não rodar classificação em lote com LLM (as rodadas em `runs/` estão completas). A única chamada a modelo é a auditoria cega (bloco B), feita por um agente com contexto limpo.
3. Depois de cada bloco: `bash rodar_analises.sh`, depois `python src/63_validar_entrega.py` (três CSVs OK), depois `pdfinfo docs/relatorio.pdf | grep Pages` (= 5). Um commit por bloco, mensagem "melhorias bloco X: ...".
4. Os números do relatório vêm de `src/modelos/relatorio.md` + `src/62_preencher_relatorio.py`; os do `previsao.txt`, de `src/61_escrever_previsao.py`. Nunca editar `docs/relatorio.md` ou `previsao.txt` à mão.
5. Cada decisão tomada entra no diário com data e motivo.
6. Se o tempo apertar, a ordem de corte é: G → F → E → D → C → B → A (A é o que mais muda a nota; F fecha a entrega e não pode faltar; G depende de chave externa e roda quando ela existir, mesmo depois do fechamento).

## Decisões do Luis (tomadas em 19/10 às 18h30)

| # | Decisão | Opções | Recomendação | Decisão |
|---|---|---|---|---|
| D1 | Entrega principal | nível 1 (tudo no tema) / híbrido (69 no subtema) | nível 1: mesma cobertura, zero risco de irmão; híbrido vira `publicacao_subtema.csv` | **nível 1** (Luis, 19/10 18h30). O híbrido entra no relatório como comparação: a versão ótima pela régua (nível 1) e a tentativa que não compensou (subtema: mesmo número de publicadas, risco de irmão a mais) |
| D2 | Risco dos gêmeos "(Parte N)" (12 temas 67xx, 47 publicadas expostas a mais) | incluir com p = 10% como as cópias / incluir com p menor (5%) / só justificar por escrito | incluir com p = 5% e mostrar sensibilidade (5, 10, 25%); argumento: nome de aula sem significado para quem rotula à mão; as 8 cópias têm título idêntico ao tema real, por isso 10% | **5% com sensibilidade** (Luis, 19/10 18h30) |
| D3 | Auditoria cega nova | fazer (50 questões, agente separado, sem acesso às conclusões) / não fazer | fazer; é o item de maior valor | **fazer** (Luis, 19/10 18h30) |
| D4 | `estudo_movai.md` e id da OpenAI no histórico do git | reescrever o histórico (git filter-repo + force push; repo privado, só o Luis) / manter | reescrever: `git rm --cached` não tira do histórico, e o repo vai ficar público | **reescrever** (Luis, 19/10 18h30) |
| D5 | Escopo | 13 itens / lista curta (1, 2, 6, 7, 12, 13) | 13 itens: ~3 h de relógio | **13 itens** (Luis, 19/10 18h30) |
| D6 | Perguntar à Carla sobre as cópias 67xx | no e-mail de entrega / antes / não perguntar | no e-mail de entrega, como pergunta aberta | **não perguntar** (Luis, 19/10 18h30): não temos acesso à equipe; trabalhar só com o que temos. O risco fica modelado na previsão (A5) e como pergunta aberta no memo |

## Bloco A — código que muda o resultado (fazer primeiro)

### A1. Nível 1 como entrega principal (item 1 da avaliação) — depende de D1
- Mudança: `src/47_decisao.py`, padrão de `--modo` passa a `n1`. No modelo do relatório (seção a), apresentar as duas versões lado a lado como comparação: nível 1 = ótima pela régua; híbrido/subtema = tentativa que não compensou (mesmas publicadas, risco de irmão a mais, previsão igual ou menor); manter o argumento de produto como trabalho futuro. `rodar_analises.sh`: `publicacao.csv` = nível 1; `publicacao_subtema.csv` = `--modo hibrido`; manter `publicacao_sem_duplicados.csv` (nível 1 + `--evitar_duplicados`). `src/60_previsao.py`: `runs/previsao_subtema.json` para a variante. README, modelo do relatório e `61_escrever_previsao.py`: trocar as referências (`publicacao_nivel1.csv` deixa de existir).
- Verificação: `python -c "import csv,json;A={json.loads(l)['tema_id']:json.loads(l) for l in open('data/temas.json')}"` não serve (temas.json é dict); usar: `python - <<EOF` que lê `publicacao.csv` e confere que todo `tema_central_id` de `publicar` tem `nivel == 1` em `data/temas.json`. Resultado esperado: 0 publicadas no nível 2; total de publicadas igual ao da variante subtema.
- [x] feito

### A2. `fora` só com evidência forte (item 4)
- Mudança: `src/47_decisao.py`, ramo `if ramo_a == "FORA" and frac_fora >= 0.5` → exigir `va["c_ramo"] >= 0.80` e `cont.get("FORA", 0) == n_mod` (os dois votantes). Senão `revisar` com motivo "dúvida entre 'fora' (nenhum tema serve) e X".
- Verificação: `grep -c ",fora," publicacao.csv` = 1 (só Q0142); Q0168 em `revisar` com motivo começando por "dúvida entre 'fora'".
- [x] feito

### A3. Unanimidade com critério igual para todas as questões (item 5)
- Mudança: `src/47_decisao.py`, linha `unanime = all(rod[q][0]["ramo"] == ramo_a for rod in todas.values() ...)`: trocar `todas` por `completas` = rodadas com 359 questões (hoje: claude-opus, claude-sonnet-h, claude-sonnet-3n) mais o árbitro. Imprimir quantas questões mudam de decisão em relação ao `data/decisoes.jsonl` anterior (salvar cópia antes em `runs/decisoes_antes_A3.jsonl`).
- Verificação: a impressão mostra a contagem; registrar no diário. Os pares confundíveis continuam calculados com todas as rodadas (isso é só diagnóstico).
- [x] feito

### A4. Coluna `confianca` que separa as decisões (seção 4, item 5)
- Mudança: `src/47_decisao.py`, bloco "confiança = média...": em `publicar`, subtrair o risco por questão (p das cópias, de `--p_copias`, quando o ramo tem gêmeo 67xx; usar o mesmo mapa de gêmeos de A5); em `revisar`, usar só a confiança do árbitro no nó sugerido (sem a média com Dawid-Skene); em `fora`, manter.
- Verificação: `python -c` que imprime min/max da confiança por decisão: publicadas abaixo de qualquer revisar com o mesmo ramo? Não precisa ser perfeito; esperado: nenhuma `revisar` com confiança ≥ 0,93, e publicadas expostas às cópias com confiança ~0,10 menor que as demais.
- [x] feito

### A5. Gêmeos "(Parte N)" no risco 67xx (item 2) — depende de D2
- Mudança: `src/60_previsao.py`: substituir o conjunto fixo `dup` por um mapa construído da árvore: para cada tema bucket ativo (ids 67xx), achar o tema usável correspondente: título idêntico (normalizado) ou título com "(Parte N)" removido, na mesma disciplina ou em Legislação Especial; incluir à mão `4696` (Estaturo/Estatuto do Idoso). Dois grupos: `copias` (título idêntico, p = `--p_copias`, padrão 0,10) e `partes` (nome de aula, p = `--p_partes`, padrão conforme D2). Perda esperada = soma de p × exposição por grupo. Gravar em `runs/previsao.json` a tabela por tema (gêmeo, publicadas) e uma grade de sensibilidade: p_copias ∈ {5, 10, 25%} × peso da dúvida ∈ {1/3, 1/2, 1}. `src/47_decisao.py --evitar_duplicados` passa a usar o mesmo mapa (os dois grupos).
- Verificação: `runs/previsao.json` mostra exposição das cópias = 38 publicadas e dos "(Parte N)" ≈ 47 (números podem mudar com A2/A3); a grade tem 9 células; `publicacao_sem_duplicados.csv` tem menos publicadas que antes (≈ 130).
- [x] feito

### A6. Motivos sem corte no meio da palavra (item 11)
- Mudança: `src/47_decisao.py`: função `cortar(texto, n=240)` que corta no fim da última frase completa (ponto, ponto e vírgula ou parêntese fechado) antes de n; aplicar ao motivo e à justificativa do `fora` (hoje `[:150]`).
- Verificação: `python -c` que confere que nenhum motivo tem 240 caracteres exatos nem termina sem pontuação/parêntese; os dois `fora` terminam em frase completa.
- [x] feito

Fechamento do bloco A: regras de execução, item 3. Commit "melhorias bloco A: nível 1 principal, fora, unanimidade, confiança, gêmeos 67xx, motivos".

## Bloco B — auditoria cega (item 3) — depende de D3

### B1. Caderno cego
- Mudança: `src/48_auditoria.py`: flags `--cego` (omite votos e justificativa do árbitro), `--excluir data/auditoria_ia.csv` (não repete as 60), `--semente 2026`, `--n 50`, `--saida data/auditoria_ia_v2.csv`, caderno em `docs/auditoria_cega_caderno.md`. Cada questão no caderno: id, texto completo, tema publicado com caminho, descrição e "não confundir" do tema, lista de irmãos (se nível 2) ou subtemas (se nível 1), e os 3 ramos de nível 1 mais parecidos por título (sem dizer de onde vêm). Nada de votos, confiança ou argumento do pipeline.
- Verificação: `grep -c "^## Q" docs/auditoria_cega_caderno.md` = 50; `grep -c "árbitro\|votos de ramo" docs/auditoria_cega_caderno.md` = 0; nenhum id em comum com `data/auditoria_ia.csv`.
- [x] feito

### B2. Auditoria por agente com contexto limpo
- Como: um agente Claude Opus separado, com o prompt de `prompts/auditoria_cega.md` (criar): "você é um professor cético; para cada questão, primeiro escreva o melhor argumento a favor de OUTRO tema da árvore (`data/arvore.txt`), depois dê o veredito: ok / duvidoso / erro, tema_sugerido, tipo_duvida (ramo/subtema), comentário". O agente lê só o caderno e `data/arvore.txt`; não lê `docs/`, `runs/`, `data/decisoes.jsonl` nem este plano. Ele grava `data/auditoria_ia_v2.csv` (colunas iguais à v1: id, tema_publicado, veredito, tipo_duvida, tema_sugerido, comentario).
- Verificação: 50 linhas preenchidas; distribuição de vereditos impressa; ler os "erro" e "duvidoso" e conferir se o argumento faz sentido (anotar no diário quantos são convenção e quantos são erro real).
- [x] feito

### B3. E3 com a auditoria cega
- Mudança: `src/60_previsao.py`: se `data/auditoria_ia_v2.csv` existir, E3 usa a v2 (restrita às publicadas atuais) e a v1 é reportada à parte como "auditoria ancorada, usada para escolher os limiares". `src/61_escrever_previsao.py` e o modelo do relatório: texto correspondente. Se a v2 mostrar erros reais acima de ~5%, voltar ao bloco A e reavaliar o limiar (0,95) antes de fechar; registrar.
- Verificação: `runs/previsao.json` tem `E3_auditoria` com n ≈ 50 e `E3_ancorada` com n = 46; `previsao.txt` cita as duas.
- [x] feito

## Bloco C — textos (itens 6, 7, 9, 10 e memo)

### C1. Bloco de precisão do `previsao.txt` (item 6)
- `src/61_escrever_previsao.py`: tirar "independentes entre si" (→ "três estimadores com fontes de erro diferentes" + uma frase sobre a correlação: todos Claude, GPT escreveu a taxonomia); tirar "árbitro" da lista do Dawid-Skene; dizer que os limiares foram escolhidos com a auditoria v1 e que E3 vem da v2 (ou, se B não foi feito, que E3 é otimista por isso); tabela de sensibilidade de A5; E1 descrito como teto do modelo, usado só como limite superior do intervalo; ponto = mediana de E2 e E3 ajustados (ou média, se só dois) — ajustar `60_previsao.py`.
- Verificação: `grep -c "independentes entre si" previsao.txt` = 0; `grep -c "árbitro" previsao.txt` só nas frases sobre a regra de publicação; a tabela aparece.
- [x] feito

### C2. Afirmações a corrigir (item 7; tabela da seção 5 da avaliação)
- README: "quase todas" → 359; tempo de máquina e de calendário (16/10 a 19/10); `pip install` inclui `markdown`; Chrome e poppler como requisitos do PDF; aviso de que `11_enriquecer_temas.py` não precisa rodar; `requirements.txt` com versões (`pip freeze | grep -iE "anthropic|openai|httpx|numpy|scikit|sentence|markdown|torch"`).
- Diário: "47 questões" → 63; registrar a prorrogação até meia-noite de 19/10; decisões D1–D6 com data.
- Modelo do relatório: "20 temas 67xx … tratamos todos como não utilizáveis" + frase sobre o desconto cobrir os dois grupos (A5); linha do Haiku 3 estágios com tokens e custo (marcadores `TOK_HAIKU_3N`, `USD_HAIKU_3N` em `62_preencher_relatorio.py`); "Nenhum erro claro" → "com acesso aos votos" (v1) e o resultado da v2.
- Memo: "sem saber o que os outros disseram" → "sem saber qual era a maioria"; "cerca de 96%" → "entre 85% e 99%, mais provavelmente perto de 96%"; total da fila (140 questões ≈ 2,5 h, ordenada); pedir decisão também sobre os "(Parte N)"; item 8 (grafia) vira uma linha dentro do item 6. Manter uma página.
- Verificação: `grep -n "quase todas" README.md` vazio; `grep -n "47 questões" docs/00_entendimento_e_plano.md` vazio; `grep -c "sem saber o que os outros" docs/memo_professor.md` = 0; PDF com 5 páginas.
- [x] feito

### C3. Seção c) do relatório: fila do professor (item 9)
- Modelo do relatório, seção c): parágrafo "Fila do professor" com marcador `FILA_SEMANA` (taxa de revisão atual × 50 mil, horas a 1 min); só importações novas passam pela cascata; meta: taxa de revisão < 10% em três meses (regras de fronteira escritas pelo professor, segunda família em todas, destilação); ordem da fila (fronteira primeiro, multi-tema por último, com as contagens `REV_FRONTEIRA`, `REV_MULTI`, `REV_DISCORDAM` calculadas de `data/decisoes.jsonl`); reportes de alunos com regra concreta; versionamento da árvore; auditoria semanal de 100 com intervalo de ±4 pontos; latência da API em lote (até 24 h).
- `62_preencher_relatorio.py`: novos marcadores.
- Verificação: `docs/relatorio.md` contém o parágrafo com números; PDF ainda com 5 páginas (cortar prosa em a) se passar).
- [x] feito

### C4. Glossário e clareza (item 10)
- Modelo do relatório: meia frase na primeira ocorrência de Dawid-Skene, Wilson, leave-one-out e cache; números em prosa com mais de três valores viram tabela; frase sobre o que foi julgamento humano (busca em concorrentes descartada, modelos menores, nível 1, não rotular sem conhecimento jurídico, limiares) na seção a).
- Verificação: leitura do PDF; 5 páginas.
- [x] feito

## Bloco D — custo reconstruível (item 8)

### D1. Árbitro na comparação de métodos
- `src/42_comparar_metodos.py`: rodada `arbitro-opus` como método "árbitro": prompt = sistema do árbitro (`prompts/arbitro_sistema.md` com a árvore resumida, como em `46_arbitragem.py`) + blocos dos ramos candidatos (`candidatos_ramos` gravados em cada JSON, via `c31.bloco_ramo`) + pedido da questão; tokens de saída do `uso`. Adicionar a `RODADAS` e a `MODELO_REAL` (`claude-opus-5-5`).
- `62_preencher_relatorio.py`: marcador `CUSTO_PIPELINE` = soma (Opus plano + Sonnet 2 estágios + árbitro) × 359 com cache, e `CUSTO_PIPELINE_LOTE` = metade; substituir o "US$ 48" / "US$ 24" fixos no modelo do relatório e no README.
- Verificação: `docs/comparacao_metodos.md` tem a linha do árbitro; o valor de `CUSTO_PIPELINE` aparece no relatório e no README (README é editado à mão com o mesmo número).
- [x] feito

## Bloco E — repositório (item 12) — depende de D4

### E1. Tirar o que não pode ser público
- `estudo_movai.md`: `git rm --cached estudo_movai.md`, adicionar ao `.gitignore` (o arquivo fica no disco). O relatório mantém só a frase "estudo anterior com andamentos processuais, 38%".
- `runs/gpt-5.5/_usage.json`: esvaziar a lista `erros` (ou trocar `org-...` por `org-REDACTED`), e no `src/30_classificar.py` truncar mensagens de erro sem ids.
- `runs/faltam.py`: apagar.
- `docs/90_avaliacao_simulada.md` e `docs/91_plano_melhorias.md`: decidir se ficam públicos. Recomendação: ficam, renomeados para `docs/90_avaliacao_simulada.md` e `docs/91_plano_melhorias.md`, porque mostram o caminho; o diário cita os dois.
- Título do PDF: `<title>Relatório — Case Classificação de tópicos</title>` em `64_gerar_pdf.py`.
- Verificação: `git ls-files | grep -E "estudo_movai|faltam.py"` vazio; `runs/gpt-5.5/_usage.json` só com `org-REDACTED`; `pdfinfo docs/relatorio.pdf | grep Title`.
- [x] feito

### E2. Reescrever o histórico (só se D4 = sim)
- `pip install git-filter-repo`; `git filter-repo --invert-paths --path estudo_movai.md --path runs/faltam.py --replace-text <(echo "org-<id da organização OpenAI>==>org-REDACTED")` (criar o arquivo de substituição em `runs/` temporário e apagar depois); o filter-repo remove o remote: `git remote add origin git@github.com:lpmu06/case-vicio-ia-classificacao.git`; `git push --force origin main`.
- Verificação: `git log --all --oneline -- estudo_movai.md` vazio; `git grep -c "org-<id da organização OpenAI>" $(git rev-list --all)` vazio; `git log --oneline | wc -l` igual ao de antes; `gh repo view` ainda privado.
- [x] feito

## Bloco G — Jev (TypeSafe) como classificador adicional — decisão do Luis, 19/10 18h40

Motivo: o Jev é uma tecnologia nova feita para classificação estruturada, com probabilidades calibradas, aplicada a um problema que é exatamente de classificação. Mesmo que o resultado não seja o melhor, testá-lo demonstra pesquisa e domínio de tecnologias novas; o resultado entra no relatório como está, bom ou ruim. O Luis providencia a chave (console.typesafe.ai); até lá, o bloco não roda.

### G1. Rodada do Jev
- Pré-requisito: linha `typesafe = ...` em `keys.txt` (não versionado).
- Como: `python src/33_classificar_jev.py` (integração pronta: 2 estágios, tema de nível 1 entre até 255 opções com descrição, depois subtema; saída em `runs/jev-h/`). Testar primeiro com `--limite 3`, conferir o JSON de uma questão (escolha, probabilidades, confiança), depois rodar as 359. Registrar tokens e custo (preço de lista: entrada quase zero, saída grátis).
- Verificação: `ls runs/jev-h | grep -c '^Q'` = 359; `_usage.json` com erros = 0.
- [x] feito (19/10 22h). Além da base, quatro variantes de um fator cada, todas nas 359 (decisão do Luis): `jev-preview`, critérios ricos, beam K=3 e 5 ordens embaralhadas, em `runs/jev-h*`. 0 erros; US$ 1,82 no total. Só os critérios ricos ajudam (85,8% contra 79,7% de concordância com a maioria dos não-Jev).

### G2. Jev na comparação e nas estimativas
- `42_comparar_metodos.py`, `45_confiabilidade.py` e `47_decisao.py` já listam `jev-h`; ele entra automaticamente na tabela de métodos, no Dawid-Skene e nos pares confundíveis. Não entra como votante da regra de publicação (a regra fecha com Opus plano, Sonnet 2 estágios e árbitro); fica como anotador de outra família.
- Medir e escrever no relatório: concordância do Jev com o consenso (leave-one-out na amostra 2×2 e nas 359), calibração das probabilidades dele (acurácia contra o consenso por faixa de confiança, em `docs/jev.md`), custo por questão. Se a calibração for boa, propor na seção c) o Jev como "segunda opinião de outra família" na cascata, no lugar do modelo pequeno.
- `src/modelos/relatorio.md`: parágrafo na seção a) (o que é, por que testamos, o que deu) e marcadores `LOO_JEV`, `JEV_CALIB` em `62_preencher_relatorio.py`.
- Verificação: `docs/comparacao_metodos.md` tem a linha `jev-h`; `docs/jev.md` existe; PDF segue com 5 páginas.
- [x] feito, com desvio (19/10 22h50). Medido o efeito do previsto acima: com o `jev-h` no Dawid-Skene e nos pares confundíveis, 7 publicadas iriam para revisão e a precisão prevista passaria de 0,95 a 0,96. Decisão do Luis: o Jev entra só como estudo; sai das listas do 45 e do 47 e da média de subtema do 60, e na comparação de métodos entra a variante de critérios ricos (`jev-h-ricos`), com tokens reais da API e fora da maioria dos outros. Avaliação em `src/50_avaliar_jev.py` → `docs/jev.md` (variantes, calibração, ruído, viés de ordem, cascata). Teste extra, ideia do Luis: o Jev como desempate entre os candidatos das questões em revisão (`src/51_jev_desempate.py`), com regra fixada antes e auditoria cega com 40 controles: 26 de 39 promovidas passaram contra 39 de 40 controles; descartado. Relatório: linha na tabela da seção a), frase em becos sem saída, Jev como segunda opinião na cascata da seção c) (total de US$ 0,03 para 0,025 por questão). Entregáveis idênticos aos do bloco F; PDF com 5 páginas.

### G3. Se a chave não chegar antes do fechamento
- O relatório mantém o parágrafo "o que faríamos com mais tempo" citando o Jev com a integração pronta, e a seção 8 da avaliação registra a frente. Nada mais.

## Bloco F — fechamento (item 13)

1. `bash rodar_analises.sh`; `python src/63_validar_entrega.py`; `pdfinfo docs/relatorio.pdf | grep Pages` = 5; abrir o PDF renderizado (pdftoppm) e conferir a tabela de custo e o memo na última página.
2. `python - <<EOF` conferindo `anexos/` contra os hashes oficiais: README 07096ab7…, PDF 4f384b9a…, LEIA-ME d28b4b53…, entrega_modelo 7f1ad400…, questoes 808f07c3…, temas b8ff7bee… (`git hash-object`).
3. Atualizar o diário (seção 10) e este plano (status). Commit "entrega final 19/10".
4. E-mail de entrega para carla@viciodeumaestudante.com.br com o link do repositório.
5. Tornar o repositório público: **ação do Luis** (`gh repo edit lpmu06/case-vicio-ia-classificacao --visibility public --accept-visibility-change-consequences`), depois abrir o link numa janela anônima.
6. Revogar as chaves do `keys.txt` (OpenAI e Anthropic): **ação do Luis**.

## Orçamento de tempo (relógio, 19/10)

| Bloco | Estimativa | Até |
|---|---|---|
| A | 50 min | 19h30 |
| B | 60 min (caderno 15, auditoria 30, integração 15) | 20h30 |
| C | 60 min | 21h30 |
| D | 25 min | 22h00 |
| E | 25 min | 22h30 |
| F | 30 min + ações do Luis | 23h00 |
| G | 45 min, quando a chave do Jev existir | sem prazo |

Folga de uma hora para imprevistos.
