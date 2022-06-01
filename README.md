# temporizador-cronometro
um programa simples feito em "ncurses" que dá duas funções de tempo importantes: crônometro e temporizador. Ambas podem ser ativadas via terminal, se nenhuma opção for escolhida, o temporizador é ativado por padrão.

## temporizador detalhes:
Ele é ativado como padrão se nenhum argumeto for dado por terminal, ou simplesmente clicado para execução; com um porêm é claro, no caso da ativação por terminal, geralmente pede-se um tempo em segundos para a contagem regressiva, neste caso será por padrão apenas um minuto. Ele vai do valor em segundos dado até zero.
Suas opções são as seguintes: 

  - sair do programa... [pressionar S]
  - começar uma nova contagem-regressiva, de onde disparou inicialmente, é claro... [pressionar N]
  - ir para o outro modo, o crônometro... [pressionar C]

## cronômetro detalhes:
Este mode é o crônometro comum, vai de "00h 00min 00seg" até "23h 59min 59seg", ativado por terminal pelo parâmetro '-c', mas não recebe nenhum argumento, como já dito, pode ser também ativado pela a funcionalidade de alternância do temporizador. Suas opções são as seguintes:

  - sair do programa...[pressionar S]
  - resetar a contagem à 00:00:00
  - mudar de modo, ou seja, ir ao temporizador...[pressionar T]


## como mexer no programa?
Como mexer no programa pode ser facilitado disparando sua ajuda, os seguintes comandos: './tempo --ajuda', ou se não colocou o arquivo "tempo.py" para execução "python tempo.py --ajuda", a seguinte informação aparecerá abaixo:
```
SOBRE:
   É um programa, com uma biblioteca "semi-gráfica(ncurses)" que 
dá duas fucionalidades importantes de tempo: temporizadores e
cronômetros. Cada uma têm suas opções específicas para melhor 
se utilizar dela. Ao acionar uma escolhendo uma opção abaixo, pode-se
alternar para próxima em plena execução.
USO:
  tempo [-options<args>]
     --temporizador SEG  faz uma contagem regressiva dado determinado 
                         valor.
     --cronômetro, -c      conta até ser parado, pode ser registrado 
                           também alguns marcos na contagem.
NOTA: Nenhuma opção colocada, ele inicialização
por opção o "temporizador".
```
