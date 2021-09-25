# temporizador-cronometro
um programa simples feito em "ncurses" que dá duas funções de tempo importantes: crônometro e temporizador. Ambas podem ser ativadas via terminal, se nenhuma opção for escolhida, o temporizador é ativado por padrão.

# temporizador detalhes:
Ele é ativado como padrão se nenhum argumeto for dado por terminal, ou simplesmente clicado para execução; com um porêm é claro, no caso da ativação por terminal, geralmente pede-se um tempo em segundos para a contagem regressiva, neste caso será por padrão apenas um minuto. Ele vai do valor em segundos dado até zero.
Suas opções são as seguintes: 

  - sair do programa... [pressionar S]
  - começar uma nova contagem-regressiva, de onde disparou inicialmente, é claro... [pressionar N]
  - ir para o outro modo, o crônometro... [pressionar C]

# cronômetro detalhes:
Este mode é o crônometro comum, vai de "00h 00min 00seg" até "23h 59min 59seg", ativado por terminal pelo parâmetro '-c', mas não recebe nenhum argumento, como já dito, pode ser também ativado pela a funcionalidade de alternância do temporizador. Suas opções são as seguintes:

  - sair do programa...[pressionar S]
  - resetar a contagem à 00:00:00
  - mudar de modo, ou seja, ir ao temporizador...[pressionar T]
