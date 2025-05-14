#!/bin/python3.8
"""
   Alguns utilitários referentes ao tempo: temporizador, cronômetro e o
 próprio relógio, tanta a versão 12 AM/PM quanto a 24h. A interface dele é
 via o ncurses. Como é próprio do Python, não é preciso instalar nenhum
 programa terceiro para funcionar, sem falar que por isso, faz dele uma
 aplicação multiplataforma.
 """

# Biblioteca do Python:
from os import ( listdir, get_terminal_size, getenv, environ as EnvironVars)
import copy, sys, getopt
from curses import wrapper
from sys import (path as PathSearch)
from pathlib import (Path)

# Demais módulos destes projeto:
DIR_SOURCE     = PathSearch[0]
DIR_DO_PROJETO = Path(DIR_SOURCE).resolve().parent
SUBDIR_LIB     = "lib/python-utilitarios"
LIB_EXTERNA    = DIR_DO_PROJETO.joinpath(SUBDIR_LIB)
SIMBOLOS_DATA  = DIR_DO_PROJETO.joinpath("simbolos")

#putenv("SIMBOLOS_DO_TEXTO", str(SIMBOLOS_DATA))
EnvironVars["SIMBOLOS_DO_TEXTO"] = str(SIMBOLOS_DATA)
PathSearch.append(str(LIB_EXTERNA))

import monitor as BM
from utilitarios import texto

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
      BM.monitor_temporizador
   elif opcao == '--cronômetro' or opcao == '-c':
      wrapper(BM.monitor_cronometro)
   elif opcao == '--horário' or opcao == '-H':
      wrapper(BM.monitor_horario)
   elif opcao == '--ajuda' or opcao == '-h':
      print(ajuda)
else:
   # se nenhum argumento for detectado apenas aciona
   # o temporizador, já que é possível alterna entre
   # as funções do programa, não importa qual começa.
   wrapper(BM.monitor_do_temporizador)
...

