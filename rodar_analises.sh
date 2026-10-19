#!/usr/bin/env bash
# Refaz todas as análises e entregáveis a partir das saídas brutas em runs/ (não chama nenhum LLM).
set -euo pipefail
export PYTHONIOENCODING=utf-8
python src/42_comparar_metodos.py > /dev/null
python src/45_confiabilidade.py > /dev/null
# variantes: híbrido (subtema quando a evidência é forte) e sem os temas com gêmeo 67xx
python src/47_decisao.py --modo hibrido --saida publicacao_subtema.csv --saida_jsonl data/decisoes_subtema.jsonl > /dev/null
python src/47_decisao.py --evitar_duplicados --saida publicacao_sem_duplicados.csv --saida_jsonl data/decisoes_sem_duplicados.jsonl > /dev/null
python src/60_previsao.py --decisoes data/decisoes_subtema.jsonl --saida_json runs/previsao_subtema.json > /dev/null
python src/60_previsao.py --decisoes data/decisoes_sem_duplicados.jsonl --saida_json runs/previsao_sem_duplicados.json > /dev/null
python src/49_sensibilidade.py > /dev/null
python src/47_decisao.py                                   # entrega principal: nível 1 -> publicacao.csv
python src/60_previsao.py > /dev/null
python src/61_escrever_previsao.py > /dev/null
python src/44_diagnostico.py > /dev/null
python src/43_embeddings.py avaliar > /dev/null 2>&1 || echo "aviso: avaliação de embeddings não rodou (faltam os vetores em data/embeddings)"
python src/62_preencher_relatorio.py | head -1
python src/64_gerar_pdf.py
head -4 previsao.txt
python src/63_validar_entrega.py
