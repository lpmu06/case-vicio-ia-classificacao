#!/usr/bin/env bash
# Refaz todas as análises e entregáveis a partir das saídas brutas em runs/ (não chama nenhum LLM).
set -euo pipefail
export PYTHONIOENCODING=utf-8
python src/42_comparar_metodos.py > /dev/null
python src/45_confiabilidade.py > /dev/null
python src/47_decisao.py --modo n1 --saida publicacao_nivel1.csv --saida_jsonl data/decisoes_nivel1.jsonl > /dev/null
python src/47_decisao.py --evitar_duplicados --saida publicacao_sem_duplicados.csv --saida_jsonl data/decisoes_sem_duplicados.jsonl > /dev/null
python src/60_previsao.py --decisoes data/decisoes_nivel1.jsonl --saida_json runs/previsao_nivel1.json > /dev/null
python src/60_previsao.py --decisoes data/decisoes_sem_duplicados.jsonl --saida_json runs/previsao_sem_duplicados.json > /dev/null
python src/49_sensibilidade.py > /dev/null
python src/47_decisao.py                                   # versão principal -> publicacao.csv
python src/60_previsao.py > /dev/null
python src/61_escrever_previsao.py > /dev/null
python src/44_diagnostico.py > /dev/null
python src/43_embeddings.py avaliar > /dev/null 2>&1 || echo "aviso: avaliação de embeddings não rodou (faltam os vetores em data/embeddings)"
python src/62_preencher_relatorio.py | head -1
head -4 previsao.txt
