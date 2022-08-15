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

   (altura, largura) = (
      len(matriz) + 1,
      len(matriz[0]) + 4
   )
   (Y,X) = (
      (LINHAS-altura)//2, 
      (COLUNAS-largura)//2
   )
   sub_janela.resize(altura, largura)
   sub_janela.mvwin(Y,X)

   return matriz  # matriz contendo molde processado.


def barra_status(janela, *strings):
   """ cria uma barra de status, independente
   do monitor(janela) passada, aceita um monte
   de strings, onde computa suas posições baseado
   no seus comprimentos e espaços disponíveis. """
   obtem_dimensoes(janela)  # atualiza dimensões.
   (linhas, colunas) = janela.getmaxyx()
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
   """ 
   pega um tempo passado em segundos e o
   converte para o formato de hora, posteriormente
   retorna uma tupla contendo todos seus 'inteiros'
   como, o primeiro elemento sendo as horas, o
   segundo os minutos, e o terceiro os segundos.
   """
   return (
      # horas:
      T // 3600,
      # minutos:
      (T % 3600) // 60,
      # segundos:
      (T % 3600) % 60
   )
...

def horario_em_segundos(H):
   """ pega a tupla contendo três valores, horas
   minutos e segundos, e a computa em segundos.  """
   if type(H) == tuple and len(H) == 3:
      return H[0]*3600 + H[1]*60 + H[2]


def contagem_regressiva(tempo):
   """ 
   uma 'bound function' que armazena o valor
   inicial dado em segundos e, em cada chamada
   verifica se a contagem chegou à zero;o retorno
   sempre é o atual valor da contagem, e se passado
   de tal, levanta uma exceção terminando o programa. 
   """
   # marca um tempo inicial à partir
   # da primeira chamada feita.
   # marca argumento passado para
   tempo_inicial = int(time())
   # próximas chamadas da função.
   tempo = tempo + tempo_inicial

   def func():
      # baseado no tempo de próximas chamadas,
      # computa a diferença restante.
      restante = tempo - int(time())
      if restante >= 0:
         return abs(tempo-int(time()))
      else:
         # quando termina uma contagem, sobre
         # uma exceção para terminar o programa.
         raise ContagemLimiteError()

   # diferença restante.
   return func
...

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
...

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

   # para sair do programa.
   tecla = janela.getch()
   # função temporizadora, dado um valor
   # a "temporizar"....
   global TEMPO
   contador = contagem_regressiva(TEMPO)
   cronometro_ligado = False
   dispara_horario = False

   # sub-janela; monitor do relógio.
   tempo = segundos_em_horario(contador()) 
   if tempo[1] == 0:
      h = None
   else:
      h = tempo[1]
   if m:=tempo[2] == 0:
      m = None
   s = tempo[2]
   janela_flutuante = graficos.LED_II(janela, h, m, s)

   while tecla != ord('s'):
      tecla = janela.getch()
      # alterna moldes do relógio.
      if tecla == curses.KEY_RESIZE:
         obtem_dimensoes(janela) # atualiza dimensões.
         janela.refresh()
      elif tecla == ord('c'):
         cronometro_ligado=True
         break
      elif tecla == ord('h'):
         dispara_horario = True
         break
      ...

      tempo = segundos_em_horario(contador())
      janela_flutuante(tempo[2], tempo[1], tempo[0])

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

   #janela_flutuante.clearok(True) # para sair do programa.
   tecla = janela.getch()
   # função temporizadora, dado um valor
   # a "temporizar"....
   contador = contagem_crescente()
   # acionou temporizador.
   temporizador_ligado=False
   dispara_horario = False

   janela_flutuante = graficos.LED(janela, 0, 20, 0)

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
         break
      elif tecla == ord('h'):
         dispara_horario = True
         break
      ...

      tempo = segundos_em_horario(contador())
      janela_flutuante(*tempo)

      # mensagem para sair.
      barra_status(
         janela, '<S> sai do programa',
         '<R> resetar', '<M> marcar registro',
         '<T> temporizador', '<H> horário'
      )
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
   janela_flutuante = graficos.LED(janela, 0, 0, 0)
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

      # matriz contendo molde selecionado.
      horario = gmtime(time())
      janela_flutuante(
         horario.tm_hour,
         horario.tm_min,
         horario.tm_sec
      )
      # mensagem para sair.
      barra_status(
         janela, '<S> sai do programa',
         '<T> temporizador', '<C> conômetro',
         '<F> formato'
      )
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
