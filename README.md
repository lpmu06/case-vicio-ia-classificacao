# Case Vício / Método VDE — classificação de tópicos

Entrega do processo seletivo da área de IA. Classifica 359 questões de concurso (Penal, Processo Penal, Legislação Penal Especial e Criminologia) em uma árvore de 377 temas, decidindo entre **publicar**, **revisar** e **fora**, com a meta de ≥ 95% de precisão nas publicadas.

| Entregável | Onde |
|---|---|
| Decisões por questão | [`publicacao.csv`](publicacao.csv) |
| Previsão de precisão e cobertura | [`previsao.txt`](previsao.txt) |
| Relatório (raciocínio, diagnóstico, produção) | [`docs/relatorio.md`](docs/relatorio.md) |
| Memo para o professor | [`docs/memo_professor.md`](docs/memo_professor.md) |
| Diário de bordo: entendimento, plano e registro de decisões | [`docs/00_entendimento_e_plano.md`](docs/00_entendimento_e_plano.md) |
| Enunciado original | [`case-ia-classificacao-de-topicos.pdf`](case-ia-classificacao-de-topicos.pdf), [`docs/enunciado_README_original.md`](docs/enunciado_README_original.md) |

## Como rodar

Requisitos: Python 3.10+, `pip install anthropic openai rapidfuzz`. Chaves em `keys.txt` (não versionado; formato `openai = sk-...`, `claude = sk-ant-...`) ou nas variáveis `OPENAI_API_KEY` / `ANTHROPIC_API_KEY`. O provedor `claude_cli` usa o Claude Code instalado e logado (`claude -p`), sem chave.

```bash
python src/00_preparo.py                      # limpa o HTML -> data/questoes_limpas.jsonl
python src/10_arvore.py                       # árvore de temas -> data/temas.json, data/arvore.txt
python src/11_enriquecer_temas.py --provedor openai --modelo gpt-5.5     # metadados dos temas (uma vez)
python src/20_baseline_origem.py              # baseline "copiar a origem" -> data/baseline_origem.jsonl
python src/30_classificar.py --provedor openai --modelo gpt-5.5          # runs/gpt-5.5/*.json
python src/30_classificar.py --provedor claude_cli --modelo opus --rotulo claude-opus   # runs/claude-opus/*.json
python src/40_ensemble.py --rotulos gpt-5.5,claude-opus --t_sub 0.85 --t_ramo 0.85     # -> publicacao.csv, data/ensemble.jsonl
python src/50_amostra.py --n 60               # caderno de rotulagem -> docs/amostra_rotulagem.md, data/rotulos_humanos.csv
python src/51_calibracao.py                   # precisão na amostra, intervalos -> runs/calibracao.json
```

O `publicacao.csv` é gerado pelo passo `40_ensemble.py` a partir das saídas brutas em `runs/`. Todas as chamadas a modelos ficam gravadas em `runs/<modelo>/<id>.json` (resposta, justificativa, uso de tokens), e o uso agregado em `runs/<modelo>/_usage.json`. Reexecutar um passo pula o que já existe.

## Como a classificação é feita (resumo)

1. **Limpeza**: enunciado + alternativas, sem HTML (uma questão trazia 100 mil caracteres de lixo do Word).
2. **Taxonomia enriquecida**: um LLM escreve, uma vez, descrição, palavras-chave, dispositivos legais e "não confundir com" para cada tema ativo. Temas inativos e os 20 "buckets de curso" (ids 67xx, "(Parte N)") nunca recebem publicação.
3. **Classificação**: uma chamada por questão, com a árvore e os metadados no system prompt (cacheado), saída JSON: tema de nível 1, subtema de nível 2 (ou null quando genérica/incerta), confianças, segunda opção, extras, flag multi-tema. Dois modelos de famílias diferentes.
4. **Ensemble e regras**: fora só se todos dizem fora; publicar no subtema se todos concordam e a menor confiança ≥ limiar; publicar no tema de nível 1 se concordam no ramo (backoff hierárquico, correto pela régua do case); senão revisar, com a sugestão e o motivo.
5. **Estimativa de precisão**: amostra rotulada à mão, precisão por faixa de confiança, intervalo de Wilson/bootstrap → `previsao.txt`.

## Decisões tomadas à mão

Registradas com data e motivo em [`docs/00_entendimento_e_plano.md`](docs/00_entendimento_e_plano.md) (seção 10). As principais: buckets 67xx e temas inativos nunca são usados; nos títulos duplicados, o nó da Legislação Especial é o alvo; evidência externa (bancos de questões na web) foi testada e descartada; backoff hierárquico adotado.

## Modelos, custo e tempo

[PREENCHER a partir de runs/*/_usage.json]
