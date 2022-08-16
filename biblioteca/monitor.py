# biblioteca padrão do Python:
import curses, curses.ascii
from curses import color_pair, A_BLINK, napms
# meus módulos:
import biblioteca.graficos as graficos
from .tempo_utilitarios import *


# computa dimensões de todas janelas.
def obtem_dimensoes(J):
   global LINHAS,COLUNAS
   LINHAS,COLUNAS = J.getmaxyx()

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

# tela que mostra e atualiza o relógio.
def monitor_temporizador(janela):
   """
   constrói uma interface gráfica de um
   temporizador, que faz uma contagem regressiva
   baseado no valor da variável global TEMPO.
   """
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
   def desabilitador(hora, minuto, segundo):
      if hora == 0 and minuto != 0:
         hora = None
      if hora == 0 and minuto == 0:
         hora = None
         minuto = None
      ...
      return (hora, minuto, segundo)
   ...

   # limpando a tela para renovação:
   janela.erase()
   janela.refresh()
   tempo = segundos_em_horario(contador())
   (h, m, s) = desabilitador(*tempo)
   janela_flutuante = graficos.LEDs(janela, h, m, s)
   janela_flutuante.esboca_delimitadores(janela)

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
      janela_flutuante(*tempo)

      # mensagem para sair.
      barra_status(
         janela, '<S> sai do programa',
         '<N> nova contagem', '<C> conômetro',
         '<H> horário'
      )
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
   """
   constrói a interface gráfica do cronômetro
   que conta até quando for possível, na verdade
   o tempo total que ele suporta é 24h em ponto.
   """
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

   # limpando a tela para renovação:
   janela.erase()
   janela.refresh()
   janela_flutuante = graficos.LEDs(janela, 0, 0, 0)
   janela_flutuante.esboca_delimitadores(janela)

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

   # limpando a tela para renovação:
   janela.erase()
   janela.refresh()
   # sub-janela; monitor do relógio.
   janela_flutuante = graficos.LEDs(janela, 0, 0, 0)
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
      horario = localtime(time())
      janela_flutuante(
         horario.tm_hour,
         horario.tm_min,
         horario.tm_sec
      )
      janela_flutuante.esboca_delimitadores(janela)
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
