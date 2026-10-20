# Rascunho do e-mail de entrega

Para: carla@viciodeumaestudante.com.br
Assunto: Case de IA — Classificação de tópicos — Luis Paulo

Olá, Carla,

Segue a entrega do case "Classificação de tópicos":

https://github.com/lpmu06/case-vicio-ia-classificacao

O que está lá:

- `publicacao.csv`: a decisão para cada uma das 359 questões. Publicamos 218 (61%), todas no tema de nível 1; 140 vão para revisão do professor, cada uma com a sugestão de tema e o motivo da dúvida; 1 ficou fora da árvore.
- `previsao.txt`: precisão prevista de 0,95 nas publicadas, com intervalo de 0,86 a 0,99, e cobertura de 0,61. O arquivo explica como chegamos a cada número sem gabarito: três estimadores com hipóteses declaradas, dois descontos e uma tabela de sensibilidade.
- `docs/relatorio.pdf` (5 páginas): raciocínio e caminhos testados, diagnóstico das questões e da árvore, desenho para 50 mil questões por semana, e o memo de uma página para o professor na última página.
- Código e README com os comandos para reproduzir tudo. As saídas brutas de todas as chamadas a modelos estão em `runs/`, então os entregáveis se refazem sem chamar nenhum modelo (`bash rodar_analises.sh`).
- Duas variantes do CSV, para comparação: `publicacao_subtema.csv` (desce ao subtema quando a evidência é forte) e `publicacao_sem_duplicados.csv` (manda para revisão os temas que têm um gêmeo recente na árvore).
- O diário de bordo (`docs/00_entendimento_e_plano.md`) registra todas as decisões, com data e motivo, inclusive os caminhos que não deram certo.

Sobre o prazo: combinamos a prorrogação até a meia-noite de 19/10, e a entrega está dentro dela. Obrigado pela flexibilidade.

Fico à disposição para conversar sobre qualquer parte do trabalho.

Abraço,
Luis Paulo
lpmu06@gmail.com
