# Memo para o professor: o que encontramos nos temas e do que precisamos de você

*Uma página, sem jargão técnico. Escrito por Luis Paulo em 18/10/2026.*

## O que fizemos

Pegamos 359 questões de Penal, Processo Penal, Legislação Especial e Criminologia e pedimos a dois "leitores" de inteligência artificial, de empresas diferentes, que dissessem em qual tema da nossa árvore cada questão deveria entrar, explicando o porquê. Só publicamos quando os dois concordam e têm alta certeza; quando discordam ou hesitam, a questão vai para a sua fila com as duas sugestões. Resultado: [PREENCHER: N publicadas, N para sua revisão, N sem tema].

## O que atrapalha a classificação (sua e da máquina)

1. **Temas duplicados.** Existem dois "Lei Maria da Penha" (um em Penal, outro em Legislação Especial), dois "Tráfico de Drogas", dois "Lavagem de Dinheiro", duas "Ação Penal" (Penal e Processo Penal), duas "Lei de Execução Penal". Hoje a mesma questão pode cair em qualquer um, e o aluno que estuda um deles não vê as questões do outro. Adotamos o da Legislação Especial e precisamos que você confirme.
2. **Temas que são nomes de aula, não de assunto.** "Teoria da Pena (Parte 1)", "(Parte 2)", "Competência (Parte 1)", "Recursos (Parte 03)" e mais 20 parecidos vieram de uma importação e não dizem ao aluno o que ele vai estudar. Sugerimos desativá-los e mover as questões para os temas de verdade.
3. **Temas-lixeira.** "Sistemas e Princípios Processuais Penais" (538 questões), "Introdução ao Estudo do Direito Penal" (424, das quais 310 em "Conceito e Fontes") e "Teoria Geral das Prisões" (359) acumulam questões que não são sobre princípios nem sobre introdução. Elas estão lá porque era o lugar "menos errado". Vale uma passada sua nesses três.
4. **Temas sem descrição.** 337 dos 377 temas não têm uma linha dizendo o que entra e o que não entra. Escrevemos uma proposta de descrição, palavras-chave, artigos de lei e "não confundir com" para cada um (arquivo `data/temas_enriquecidos.json`). Precisa da sua revisão, principalmente nas fronteiras difíceis: "Fato Típico" × "Tipicidade"; "Culpabilidade" × "Inimputabilidade"; "Princípios do Direito Penal" × "Tipicidade" (princípio da insignificância); em Criminologia, "Teorias de Nível Sociológico" × "Teorias Criminológicas em Espécie".
5. **Questões sem tema central.** Algumas questões têm cada alternativa sobre um crime diferente (falsidade, abuso de autoridade, calúnia...). Não existe tema certo para elas. Proposta: publicar no tema mais amplo (nível 1) ou criar uma marcação "miscelânea" para o aluno saber o que esperar.
6. **Pequenos erros de grafia** nos títulos ("Escolas Crimonológicas", "Estaturo de Idoso", "Comeptência Territorial", "Caractéristas", "Crimescontra"), e títulos com números soltos ("12 Disposições Gerais…", "2 Oferecimento…").

## O que recomendamos mudar

- Desativar os temas "(Parte N)" e as cópias duplicadas; manter um único nó por assunto.
- Adotar a regra "o aluno que estuda o tema vê os subtemas" também na classificação: quando a questão é genérica do tema, ela fica no tema, não forçada em um subtema.
- Aprovar as descrições propostas (ou corrigi-las) para os temas de fronteira difícil. Isso melhora tanto a máquina quanto a consistência entre professores.
- Olhar primeiro as três lixeiras: são as que mais confundem o aluno.

## Do que precisamos de você

| Pedido | Tempo estimado |
|---|---|
| Confirmar a escolha "Legislação Especial" para os temas duplicados | 10 min |
| Revisar a fila de [PREENCHER N] questões marcadas "revisar", cada uma com duas sugestões e o motivo da dúvida | ~1 min por questão |
| Validar as descrições dos [PREENCHER] temas de fronteira difícil | 1 h |
| Decidir o destino das questões "multi-tema" | 15 min |

Com isso, a próxima rodada publica mais questões com a mesma segurança, e a sua fila fica menor.
