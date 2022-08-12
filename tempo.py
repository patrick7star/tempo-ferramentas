#!/bin/python3.8
""" simulação de um relógio analógico, que
no terminal. """

# biblioteca do Python:
from os import listdir, get_terminal_size
import copy, sys, getopt
from curses import wrapper
# meus módulos:
import biblioteca.monitor as BM


# analisando sintaxe do argumento.
conteudo = getopt.gnu_getopt(
   sys.argv[1:], shortopts='t:ch', 
   longopts=[
      'temporizador=',
      'cronômetro',
      'ajuda',
      'horario'
   ]
)

# descrição da ajuda:
ajuda = ('''
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

     --horario       mostra o horário.


NOTA: Nenhuma opção colocada, ele inicialização
por opção o "temporizador".
''')


# executando opções.
for (opcao, valor) in conteudo[0]:
   if opcao == '--temporizador' or opcao == '-t':
      BM.TEMPO = int(valor)
      wrapper(BM.monitor_temporizador)
      break

   elif opcao == '--cronômetro' or opcao == '-c':
      wrapper(BM.monitor_cronometro)
      break
   
   elif opcao == '--horario' or opcao == '-H':
      wrapper(BM.monitor_horario)
      break

   elif opcao == '--ajuda' or opcao == '-h':
      print(ajuda)
      break
else:
   # se nenhum argumento for detectado apenas aciona
   # o temporizador, já que é possível alterna entre
   # as funções do programa, não importa qual começa.
   wrapper(BM.monitor_temporizador)
...
