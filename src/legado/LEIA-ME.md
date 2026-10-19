# Scripts substituídos (mantidos como registro do caminho)

- `40_ensemble_v1.py` e `41_estatisticas_v1.py`: primeira versão do ensemble, com dois modelos de famílias diferentes (GPT-5.5 e Claude). Foi abandonada quando os créditos da OpenAI acabaram; a decisão final está em `src/47_decisao.py`.
- `50_amostra_rotulagem_humana.py`, `51_calibracao_com_rotulos.py`, `amostra_rotulagem.md` e `rotulos_humanos_vazio.csv`: o plano original de calibrar a previsão com 60 questões rotuladas por uma pessoa. Foi descartado porque não havia quem rotulasse com conhecimento jurídico; a estimativa passou a ser cega (`src/45_confiabilidade.py`, `src/48_auditoria.py`, `src/60_previsao.py`).

Estes scripts podem não rodar mais com a estrutura atual de `data/` e `runs/`.
