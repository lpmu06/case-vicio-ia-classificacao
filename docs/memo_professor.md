# Memo para o professor

*O que encontramos nas 359 questões, o que recomendamos mudar nos temas e do que precisamos de você.*

**O que fizemos.** Vários "leitores" automáticos, de tamanhos e estratégias diferentes, indicaram o tema de cada questão e explicaram por quê. Um leitor mais cuidadoso revisou tudo sem saber o que os outros disseram. Só publicamos quando todos convergem com segurança; o resto vai para a sua fila, com sugestão e motivo.

| Publicadas para o aluno | Na sua fila, com sugestão | Sem tema na árvore |
|---|---|---|
| 218 | 139 | 2 |

Estimamos que cerca de 96% das publicadas estão no tema certo. Sem gabarito, é uma estimativa; o relatório explica como chegamos a ela.

**O que atrapalha a classificação, sua e da máquina.**
1. **Temas duplicados.** Lei Maria da Penha, Tráfico de Drogas, Lavagem de Dinheiro, Lei de Execução Penal e outros existem em dois lugares. Quem estuda um não vê as questões do outro. Usamos sempre o da Legislação Especial; se a equipe usa as cópias criadas em Penal, essa é a informação que mais muda o resultado: são 38 das 218 publicadas.
2. **Assuntos com dois endereços.** Prisão está em "Teoria Geral das Prisões" e em "Prisões em Espécie"; ação penal, em Penal e em Processo Penal; juizados, em Legislação Especial e em "Procedimento Sumaríssimo". Foi onde mais tivemos dúvida.
3. **Fronteiras sem regra escrita.** Progressão de regime vai em Execução Penal ou em Teoria da Pena? Uma questão que compara erro de tipo e erro de proibição vai em qual dos dois? Essas convenções são a principal fonte de erro que não conseguimos medir.
4. **Temas com nome de aula.** "Teoria da Pena (Parte 1)", "Competência (Parte 2)" e outros 18 não dizem o que o aluno vai estudar. Não publicamos nada neles.
5. **Temas-lixeira.** "Sistemas e Princípios Processuais Penais" e "Introdução ao Estudo do Direito Penal" acumulavam centenas de questões que não são sobre princípios nem introdução. Na nossa classificação, só 8 questões ficaram em temas desse tipo.
6. **Temas sem descrição.** 337 dos 377 não dizem o que entra e o que não entra. Escrevemos uma proposta para cada um, com artigos de lei e "não confundir com", em `data/temas_enriquecidos.json`.
7. **Questões sem tema central.** Em 44 questões, cada alternativa cobra um crime diferente. Hoje vão para a sua fila.
8. **Erros de grafia** nos títulos, como "Crimonológicas", "Estaturo de Idoso" e "Comeptência".

**O que recomendamos mudar.**
- Manter um único tema por assunto e desativar os temas "(Parte N)" e as cópias.
- Escrever uma regra de uma linha para cada fronteira dos itens 2 e 3. Vale para a máquina e para a consistência entre professores.
- Revisar as descrições propostas, começando pelos temas de fronteira.
- Decidir o destino das questões sem tema central: tema mais amplo ou uma marcação "miscelânea".

**Do que precisamos de você.**

| Pedido | Tempo |
|---|---|
| Dizer qual dos temas duplicados a equipe usa | 10 minutos |
| Responder as regras de fronteira dos itens 2 e 3 | 30 minutos |
| Revisar a fila de 139 questões, cada uma com sugestão e motivo | cerca de 1 minuto por questão |
| Validar as descrições dos temas de fronteira | 1 hora |

Com essas respostas, a próxima rodada publica mais questões com a mesma segurança, e a sua fila fica menor.
