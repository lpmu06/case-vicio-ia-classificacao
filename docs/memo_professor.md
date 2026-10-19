# Memo para o professor

*O que encontramos nas 359 questões, o que recomendamos mudar nos temas e do que precisamos de você. Uma página, sem jargão técnico.*

## O que fizemos

Pedimos a vários "leitores" automáticos, de tamanhos e estratégias diferentes, que dissessem em qual tema cada questão deveria entrar e por quê. Um leitor mais cuidadoso fez a revisão final, sem saber o que os outros tinham dito. Só publicamos quando todos convergem com segurança. Quando hesitam ou discordam, a questão vai para a sua fila com uma sugestão e o motivo da dúvida.

| Resultado | Questões |
|---|---|
| Publicadas direto para o aluno | 218 |
| Na sua fila de revisão, com sugestão | 139 |
| Sem tema na árvore atual | 2 |

Estimamos que cerca de 96% das publicadas estão no tema certo. Não tínhamos gabarito, então essa é uma estimativa, e a explicamos no relatório.

## O que atrapalha a classificação, sua e da máquina

1. **Temas duplicados.** Há dois "Lei Maria da Penha", dois "Tráfico de Drogas", dois "Lavagem de Dinheiro", duas "Ação Penal" e duas "Lei de Execução Penal". O aluno que estuda um não vê as questões do outro. Usamos sempre o da Legislação Especial. Se a equipe usa as cópias criadas em Penal, essa é a informação que mais muda o nosso resultado: são 38 das 218 publicadas.
2. **Temas com nome de aula.** "Teoria da Pena (Parte 1)", "Competência (Parte 2)", "Recursos (Parte 03)" e outros 17 vieram de uma importação e não dizem o que o aluno vai estudar. Não publicamos nada neles.
3. **Temas-lixeira.** "Sistemas e Princípios Processuais Penais", "Introdução ao Estudo do Direito Penal" e "Teoria Geral das Prisões" acumulavam centenas de questões que não são sobre princípios nem introdução. Elas estavam lá por ser o lugar menos errado.
4. **Fronteiras que confundem.** Os leitores automáticos divergiram sempre nos mesmos pares: Juizado Especial Criminal (Legislação Especial) × Procedimento Sumaríssimo; Lei de Execução Penal × Teoria da Pena; prisões em "Teoria Geral das Prisões" × "Prisões em Espécie"; ação penal e decadência em Penal × Processo Penal; erro de tipo × erro de proibição. Onde você guarda, por exemplo, uma questão de progressão de regime: em Execução Penal ou em Teoria da Pena? Essas convenções não estão escritas em lugar nenhum, e são a principal fonte de erro que não conseguimos medir.
5. **Temas sem descrição.** 337 dos 377 temas não dizem o que entra e o que não entra. Escrevemos uma proposta para cada um, com descrição, palavras-chave, artigos de lei e "não confundir com", no arquivo `data/temas_enriquecidos.json`.
6. **Questões sem tema central.** Em 44 questões, cada alternativa cobra um crime diferente. Não existe tema certo para elas; hoje vão para a sua fila.
7. **Pequenos erros de grafia** nos títulos: "Escolas Crimonológicas", "Estaturo de Idoso", "Comeptência Territorial", "Caractéristas", "Crimescontra", e números soltos como "12 Disposições Gerais".

## O que recomendamos mudar

- Desativar os temas "(Parte N)" e as cópias duplicadas, mantendo um único tema por assunto.
- Escrever, para cada fronteira da lista do item 4, uma regra de uma linha ("progressão de regime vai em Execução Penal"). Isso vale para a máquina e para a consistência entre professores.
- Revisar as descrições propostas, começando pelos temas de fronteira.
- Criar uma marcação "miscelânea" para as questões sem tema central, ou decidir que elas ficam no tema mais amplo.

## Do que precisamos de você

| Pedido | Tempo estimado |
|---|---|
| Confirmar a escolha da Legislação Especial nos temas duplicados | 10 minutos |
| Responder as regras de fronteira do item 4 | 30 minutos |
| Revisar a fila de 139 questões, cada uma com sugestão e motivo | cerca de 1 minuto por questão |
| Validar as descrições dos temas de fronteira | 1 hora |

Com essas respostas, a próxima rodada publica mais questões com a mesma segurança, e a sua fila fica menor.
