# biblioteca padrão do Python:
import curses, curses.ascii
from curses import color_pair, A_BLINK, napms
from time import gmtime, time, localtime
import pprint
# meus módulos:
from .utilitarios import *
import biblioteca.graficos as graficos

# o que pode ser importado.
__all__ = [
   "TEMPO", "registros", "ContagemLimiteError",
   "CronometroLimiteError","monitor_temporizador"
   ,"monitor_cronometro"
]

# atributos básicos:
LINHAS,COLUNAS = (0,0)
# tempo atual que será contando regressivamente,
# ou de forma crescente.
TEMPO = 120  # inicialmente dois minutos.
# limite máximo do cronômetro é de um dia/24h.
limite_cronometro = 24 * 3600
# lista de registros marcados durante a cronometragem.
registros = []


# exceções do programa.
class ContagemLimiteError(BaseException):
   def __str__(self):
      return (
         """não se pode mais continuar a partir,
         \rdaqui, pois ou a contagem estora a
         \r\"memória\" possível, ou vai para valores não físicos!"""
      )
   ...
...

class CronometroLimiteError(Exception):
   def __str__(self):
      return (
         "o tempo máximo que tal 'contador' suporta"+
         "\né um dia/24h, no formato 23:59:59"
      )
   ...
...

# computa dimensões de todas janelas.
def obtem_dimensoes(J):
   global LINHAS,COLUNAS
   LINHAS,COLUNAS = J.getmaxyx()

# marca hora.
def molde(sub_janela, tempo):
   """ molde do temporizador; como será mostrador
   ou, quando será mostrado os dígitos do 'relógio'."""
   horas = str(tempo[0])      # primeira parte, horas.
   minutos = str(tempo[1])    # segunda, minutos.
   segundos = str(tempo[2])   # terceira, segundos.

   if len(horas) == 2:
      hora_i = numero_desenho(int(horas[0]))
      hora_ii = numero_desenho(int(horas[1]))
   else:
      hora_i = numero_desenho(0)
      hora_ii = numero_desenho(int(horas[0]))

   if len(minutos) == 2:
      min_i = numero_desenho(int(minutos[0]))
      min_ii = numero_desenho(int(minutos[1]))
   else:
      min_i = numero_desenho(0)
      min_ii = numero_desenho(int(minutos[0]))

   if len(segundos) == 2:
      seg_i = numero_desenho(int(segundos[0]))
      seg_ii = numero_desenho(int(segundos[1]))
   else:
      seg_i = numero_desenho(0)
      seg_ii = numero_desenho(int(segundos[0]))

   # removendo dígitos inúteis.
   # convertendo tempo novamente em segundos.
   T_seg = tempo[0]*3600 + tempo[1]*60 + tempo[2]
   if T_seg > 3600:
      # se houver mais de uma hora deixa todos dígitos.
      matriz = mescla_matrizes(hora_i, hora_ii,
                               min_i, min_ii,
                               seg_i, seg_ii)
   elif 60 < T_seg < 3600:
      # se não estiver na faixa das horas, corta
      # o "dígito horas".
      matriz = mescla_matrizes( min_i, min_ii,
                                seg_i, seg_ii)
   else:
      # se não estiver nem na faixa dos minutos
      # então corta dos "dígitos" minutos e horas.
      matriz = mescla_matrizes(seg_i, seg_ii)

   (altura, largura) = len(matriz)+1,len(matriz[0])+4
   (Y,X) = ((LINHAS-altura)/2, (COLUNAS-largura)/2)
   sub_janela.resize(altura, largura)
   sub_janela.mvwin(int(Y),int(X))

   return matriz  # matriz contendo molde processado.

# marca hora.
def molde_cronometro(sub_janela, tempo):
   """ molde do cronômetro mostra todos
   dígitos de um relógio 24h. Não oculta algum
   em nenhum momento. """
   horas = "%2.2i" % tempo[0]
   minutos = "%2.2i" % tempo[1]
   segundos = "%2.2i" % tempo[2]

   if len(horas) == 2:
      hora_i = numero_desenho(int(horas[0]))
      hora_ii = numero_desenho(int(horas[1]))
   else:
      hora_i = numero_desenho(0)
      hora_ii = numero_desenho(int(horas[0]))

   if len(minutos) == 2:
      min_i = numero_desenho(int(minutos[0]))
      min_ii = numero_desenho(int(minutos[1]))
   else:
      min_i = numero_desenho(0)
      min_ii = numero_desenho(int(minutos[0]))

   if len(segundos) == 2:
      seg_i = numero_desenho(int(segundos[0]))
      seg_ii = numero_desenho(int(segundos[1]))
   else:
      seg_i = numero_desenho(0)
      seg_ii = numero_desenho(int(segundos[0]))
   matriz = mescla_matrizes(hora_i,hora_ii,
                            min_i, min_ii,
                            seg_i, seg_ii)
   (altura, largura) = len(matriz)+1,len(matriz[0])+4
   (Y,X) = ((LINHAS-altura)/2, (COLUNAS-largura)/2)
   sub_janela.resize(altura, largura)
   sub_janela.mvwin(int(Y),int(X))

   return matriz  # matriz contendo molde processado.


def barra_status(janela, *strings):
   """ cria uma barra de status, independente
   do monitor(janela) passada, aceita um monte
   de strings, onde computa suas posições baseado
   no seus comprimentos e espaços disponíveis. """
   obtem_dimensoes(janela)  # atualiza dimensões.
   # comprimento das strings.
   # espaços intermediários.
   E = int((COLUNAS - sum(len(s) for s in strings)) / len(strings))
   espaco = ' '*E # quantia de espaços entre legendas.
   meio_espaco = ' '*int(E/2-2) # espaço das pontas.

   # condições especiaís e genéricas.
   if len(strings) == 1:
      texto = meio_espaco + strings[0] + meio_espaco
   else:
      texto = meio_espaco # meio-espaço inicial.
      texto += espaco.join(strings)
      # subtraindo espaço indesejado.
      texto[0:len(texto)-len(espaco)]
      # colocando meio espaço no lugar.
      texto += meio_espaco
   # escrevendo barra de status.
   janela.addstr(LINHAS-2, 0, texto)


def segundos_em_horario(T):
   """ pega um tempo passado em segundos e o
   converte para o formato de hora, posteriormente
   retorna uma tupla contendo todos seus 'inteiros'
   como, o primeiro elemento sendo as horas, o
   segundo os minutos, e o terceiro os segundos."""
   # quantas grupos de "hora" posso
   # arranjar todos estes segundos.
   horas = T/3600
   # tirando a parte fracionária das horas,
   # e, contabilizando em minutos.
   minutos = abs(int(horas)-(T/3600)) * 60
   # tirando a parte fracionária dos minutos
   # e contabilizando-o em segundos.
   segundos = abs(int(minutos)-minutos) * 60

   # convertendo todas contagens para inteiros.
   return (int(horas),int(minutos), int(segundos))


def horario_em_segundos(H):
   """ pega a tupla contendo três valores, horas
   minutos e segundos, e a computa em segundos.  """
   if type(H) == tuple and len(H) == 3:
      return H[0]*3600 + H[1]*60 + H[2]


def contagem_regressiva(tempo):
   """ uma 'bound function' que armazena o valor
   inicial dado em segundos e, em cada chamada
   verifica se a contagem chegou à zero;o retorno
   sempre é o atual valor da contagem, e se passado
   de tal, levanta uma exceção terminando o programa. """
   # marca um tempo inicial à partir
   # da primeira chamada feita.
   # marca argumento passado para
   tempo_inicial = time()
   # próximas chamadas da função.
   tempo = tempo + tempo_inicial

   def func():
      # baseado no tempo de próximas chamadas,
      # computa a diferença restante.
      restante = tempo-time()
      if restante >= 0:
         return abs(tempo-time())
      else:
         # quando termina uma contagem, sobre
         # uma exceção para terminar o programa.
         raise ContagemLimiteError()

   # diferença restante.
   return func


def contagem_crescente():
   """ uma função que armazena informação de um
   valor passado com argumento e, conta a
   passagem de tempo até determinado valor; o
   retorno é uma tupla contendo o valor das horas
   minutos e segundos, nesta respectiva ordem da
   contagem crescente, ou seja, cada vez maior.
   O argumento passado é em segundos. """
   # marca um tempo ínicial desde a
   # primeira chamada.
   ti = time()
   def auxiliar():
      # para debug, menos de um minuto do fim.
      tf = time()+(3600*23+59*60+3)
      tf = time() # tempo registrado a cada chamada.
      decorrido = tf-ti
      if decorrido < limite_cronometro:
         return decorrido
      else:
         raise CronometroLimiteError()
   return auxiliar


# para horário e temporizador, uso em comum.
def desenha_LED(janela, matriz, tempo):
   em_segundos = (
      3600 * tempo[0] +
      60 * tempo[1] +
      tempo[2]
   )
   for i in range(len(matriz)):
      for j in range(len(matriz[0])):
         (y, x) = (i+1, j+2)
         cor = None
         char = matriz[i][j]
         if em_segundos < 10:
            cor = 2
         else:
            cor = 1
         janela.addch(y, x, char, color_pair(cor))
      ...
   ...
...


# tela que mostra e atualiza o relógio.
def monitor_temporizador(janela):
   """ constrói uma interface gráfica de um
   temporizador, que faz uma contagem regressiva
   baseado no valor da variável global TEMPO. """
   # atualiza atual dimensão da janela.
   obtem_dimensoes(janela)
   curses.curs_set(False)  # oculta cursor do teclado.
   janela.nodelay(True)   # não bloqueia com o input.
   janela.keypad(True)  # ativa teclas especiais.

   # paleta de cores.
   curses.init_pair(1, curses.COLOR_GREEN, 0)
   curses.init_pair(2, curses.COLOR_RED, 0)

   # sub-janela; monitor do relógio.
   janela_flutuante = curses.newwin(5,5)
   janela_flutuante.keypad(True)
   #janela_flutuante.clearok(True)
   # para sair do programa.
   tecla = janela.getch()
   # função temporizadora, dado um valor
   # a "temporizar"....
   global TEMPO
   contador = contagem_regressiva(TEMPO)
   cronometro_ligado = False
   dispara_horario = False

   # limpa tela antes de começar.
   janela.erase()
   janela.refresh()

   while tecla != ord('s'):
      tecla = janela.getch()
      # alterna moldes do relógio.
      if tecla == curses.KEY_RESIZE:
         obtem_dimensoes(janela) # atualiza dimensões.
         janela.refresh()
      elif tecla == ord('c'):
         cronometro_ligado=True
         janela_flutuante.erase()
         break
      elif tecla == ord('h'):
         dispara_horario = True
         break
      ...

      # apaga possível molde anterior.
      janela_flutuante.erase()
      # matriz contendo molde selecionado.
      tempo = segundos_em_horario(contador())
      matriz = molde(janela_flutuante,tempo)
      desenha_LED(janela_flutuante, matriz, tempo)
      janela_flutuante.refresh() # atualiza após desenhar.

      # mensagem para sair.
      barra_status(
         janela, '<S> sai do programa',
         '<N> nova contagem', '<C> conômetro',
         '<H> horário'
      )
      janela.refresh()
   ...

   curses.endwin()  # fim da interface.

   # mensagem caso a contagem não tenha sido finalizada.
   if sum(tempo) > 0:
      # função que modela string de acordo com o
      # necessário.
      def molda_tempo_str(tempo):
         if tempo[0] == 0 and tempo[1] > 0:
            return "%0.2imin %0.2iseg"%(tempo[1:])
         elif tempo[0] == 0 and tempo[1] == 0:
            return "%0.2iseg"%(tempo[-1])
         else:
            return "%0.2ih %0.2imin %0.2iseg"%tempo

      restante_str = molda_tempo_str(tempo)
      string = ("você finalizou o programa "+
                "há %s do termino!"%restante_str)
      print(string)

   # chama nova função do programa.
   if cronometro_ligado:
      curses.wrapper(monitor_cronometro)
   if dispara_horario:
      curses.wrapper(monitor_horario)
...

def monitor_cronometro(janela):
   """ constrói a interface gráfica do cronômetro
   que conta até quando for possível, na verdade
   o tempo total que ele suporta é 24h em ponto. """
   obtem_dimensoes(janela) # atualizando dimensão.
   curses.curs_set(False)  # oculta cursor do teclado.
   janela.nodelay(True)   # não bloqueia com o input.
   janela.keypad(True)  # ativa teclas especiais.

   # paleta de cores.
   curses.init_pair(1, curses.COLOR_GREEN, 0)
   curses.init_pair(2, curses.COLOR_RED, 0)

   # sub janela; monitor do relógio.
   janela_flutuante = curses.newwin(5,5)
   janela_flutuante.keypad(True)
   #janela_flutuante.clearok(True) # para sair do programa.
   tecla = janela.getch()
   # função temporizadora, dado um valor
   # a "temporizar"....
   contador = contagem_crescente()
   # acionou temporizador.
   temporizador_ligado=False
   dispara_horario = False

   # limpa tela antes de começar.
   janela.erase()
   janela.refresh()

   while tecla != ord('s'):
      # entrada para alguma tecla pressionada.
      tecla = janela.getch()
      # alterna moldes do relógio.
      if tecla == curses.KEY_RESIZE:
         obtem_dimensoes(janela) # atualiza dimensões.
         janela.refresh()
      elif tecla == ord('r'):
         contador = contagem_crescente()
      elif tecla == ord('m'):
         registros.append(tempo)
      elif tecla == ord('t'):
         temporizador_ligado=True
         janela_flutuante.erase()
         janela_flutuante.refresh()
         break
      elif tecla == ord('h'):
         dispara_horario = True
         break
      ...

      janela_flutuante.erase()  # apaga possível molde anterior.
      # matriz contendo molde selecionado.
      tempo = segundos_em_horario(contador())
      matriz = molde_cronometro(janela_flutuante,tempo)
      desenha_LED(janela_flutuante, matriz, tempo)
      janela_flutuante.refresh() # atualiza após desenhar.

      # mensagem para sair.
      barra_status(
         janela, '<S> sai do programa',
         '<R> resetar', '<M> marcar registro',
         '<T> temporizador', '<H> horário'
      )
      # à cada meio segundo refresca tela.
      napms(500)
      janela.refresh()  # refresca janela.
   ...
   curses.endwin()  # fim da interface.
   for (ordem, T) in enumerate(registros):
      print(
         "%iª ==> %2.2i:%2.2i:%2.2i"
         %(1 + ordem, T[0],T[1],T[2])
      )

   # se o temporizador foi acionado, então...
   if temporizador_ligado:
      curses.wrapper(monitor_temporizador)
   elif dispara_horario:
      curses.wrapper(monitor_horario)
   ...
...

def monitor_cronometro(janela):
   """ constrói a interface gráfica do cronômetro
   que conta até quando for possível, na verdade
   o tempo total que ele suporta é 24h em ponto. """
   obtem_dimensoes(janela) # atualizando dimensão.
   curses.curs_set(False)  # oculta cursor do teclado.
   janela.nodelay(True)   # não bloqueia com o input.
   janela.keypad(True)  # ativa teclas especiais.

   # paleta de cores.
   curses.init_pair(1, curses.COLOR_GREEN, 0)
   curses.init_pair(2, curses.COLOR_RED, 0)

   # sub janela; monitor do relógio.
   janela_flutuante = curses.newwin(5,5)
   janela_flutuante.keypad(True)
   #janela_flutuante.clearok(True) # para sair do programa.
   tecla = janela.getch()
   # função temporizadora, dado um valor
   # a "temporizar"....
   contador = contagem_crescente()
   # acionou temporizador.
   temporizador_ligado=False
   dispara_horario = False

   # limpa tela antes de começar.
   janela.erase()
   janela.refresh()

   janela_flutuante = graficos.LED(janela, 0, 0, 0)

   while tecla != ord('s'):
      # entrada para alguma tecla pressionada.
      tecla = janela.getch()
      # alterna moldes do relógio.
      if tecla == curses.KEY_RESIZE:
         obtem_dimensoes(janela) # atualiza dimensões.
         janela.refresh()
      elif tecla == ord('r'):
         contador = contagem_crescente()
      elif tecla == ord('m'):
         registros.append(tempo)
      elif tecla == ord('t'):
         temporizador_ligado=True
         janela_flutuante.erase()
         janela_flutuante.refresh()
         break
      elif tecla == ord('h'):
         dispara_horario = True
         break
      ...

      """
      janela_flutuante.erase()  # apaga possível molde anterior.
      # matriz contendo molde selecionado.
      tempo = segundos_em_horario(contador())
      matriz = molde_cronometro(janela_flutuante,tempo)
      desenha_LED(janela_flutuante, matriz, tempo)
      janela_flutuante.refresh() # atualiza após desenhar.
      """
      tempo = segundos_em_horario(contador())
      janela_flutuante(*tempo)

      # mensagem para sair.
      barra_status(
         janela, '<S> sai do programa',
         '<R> resetar', '<M> marcar registro',
         '<T> temporizador', '<H> horário'
      )
      # à cada meio segundo refresca tela.
      napms(500)
      janela.refresh()  # refresca janela.
   ...
   curses.endwin()  # fim da interface.
   for (ordem, T) in enumerate(registros):
      print(
         "%iª ==> %2.2i:%2.2i:%2.2i"
         %(1 + ordem, T[0],T[1],T[2])
      )

   # se o temporizador foi acionado, então...
   if temporizador_ligado:
      curses.wrapper(monitor_temporizador)
   elif dispara_horario:
      curses.wrapper(monitor_horario)
   ...
...

def molde_horario(sub_janela, tempo):
   """
   molde do temporizador; como será mostrador
   ou, quando será mostrado os dígitos do 'relógio'.
   """

   horas = str(tempo[0])      # horas.
   minutos = str(tempo[1])    # minutos.
   segundos = str(tempo[2])   # segundos.

   if len(horas) == 2:
      hora_i = numero_desenho(int(horas[0]))
      hora_ii = numero_desenho(int(horas[1]))
   else:
      hora_i = numero_desenho(0)
      hora_ii = numero_desenho(int(horas[0]))

   if len(minutos) == 2:
      min_i = numero_desenho(int(minutos[0]))
      min_ii = numero_desenho(int(minutos[1]))
   else:
      min_i = numero_desenho(0)
      min_ii = numero_desenho(int(minutos[0]))

   if len(segundos) == 2:
      seg_i = numero_desenho(int(segundos[0]))
      seg_ii = numero_desenho(int(segundos[1]))
   else:
      seg_i = numero_desenho(0)
      seg_ii = numero_desenho(int(segundos[0]))

   # removendo dígitos inúteis.
   # convertendo tempo novamente em segundos.
   T_seg = tempo[0]*3600 + tempo[1]*60 + tempo[2]
   if T_seg > 3600:
      # se houver mais de uma hora deixa todos dígitos.
      matriz = mescla_matrizes(
         hora_i, hora_ii,
         min_i, min_ii,
         seg_i, seg_ii
      )
   elif 60 < T_seg < 3600:
      # se não estiver na faixa das horas, corta
      # o "dígito horas".
      matriz = mescla_matrizes(
         min_i, min_ii,
         seg_i, seg_ii
      )
   else:
      # se não estiver nem na faixa dos minutos
      # então corta dos "dígitos" minutos e horas.
      matriz = mescla_matrizes(seg_i, seg_ii)
   ...

   (altura, largura) = (
      len(matriz) + 1,
      len(matriz[0]) + 4
   )
   (Y, X) = (
      (LINHAS - altura) / 2,
      (COLUNAS - largura) / 2
   )
   sub_janela.resize(altura, largura)
   sub_janela.mvwin(int(Y),int(X))

   # matriz contendo molde processado.
   return matriz
...

def monitor_horario(janela):
   """
   constrói uma interface para visualizar o
   horário atual.
   """
   # atualiza atual dimensão da janela.
   obtem_dimensoes(janela)
   curses.curs_set(False)  # oculta cursor do teclado.
   janela.nodelay(True)   # não bloqueia com o input.
   janela.keypad(True)  # ativa teclas especiais.

   # paleta de cores.
   curses.init_pair(1, curses.COLOR_GREEN, 0)
   curses.init_pair(2, curses.COLOR_RED, 0)

   # sub-janela; monitor do relógio.
   janela_flutuante = curses.newwin(5,5)
   janela_flutuante.keypad(True)
   #janela_flutuante.clearok(True)
   # para sair do programa.
   tecla = janela.getch()
   # programas a acionar:
   dispara_temporizador = False
   dispara_cronometro = False

   while tecla != ord('s'):
      tecla = janela.getch()
      # alterna moldes do relógio.
      if tecla == curses.KEY_RESIZE:
         obtem_dimensoes(janela) # atualiza dimensões.
         janela.refresh()
      elif tecla == ord('t'):
         dispara_temporizador = True
         break
      elif tecla == ord('c'):
         dispara_cronometro = True
         break
      ...

      # apaga possível molde anterior.
      janela_flutuante.erase()
      # matriz contendo molde selecionado.
      horario = gmtime(time())
      tempo = (
         horario.tm_hour,
         horario.tm_min,
         horario.tm_sec
      )
      matriz = molde_horario(janela_flutuante, tempo)
      desenha_LED(janela_flutuante, matriz, tempo)
      # atualiza após desenhar.
      janela_flutuante.refresh()

      # mensagem para sair.
      barra_status(
         janela, '<S> sai do programa',
         '<T> temporizador', '<C> conômetro',
         '<F> formato'
      )
      janela.refresh()
   ...
   # fim da interface.
   curses.endwin()

   # possívelmente inicial novo programa.
   if dispara_cronometro:
      curses.wrapper(monitor_cronometro)
   elif dispara_temporizador:
      curses.wrapper(monitor_temporizador)
   else:
      print("apenas abandonou o programa.")
...

