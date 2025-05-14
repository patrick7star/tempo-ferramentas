# Biblioteca padrão do Python:
from curses import (window)
import curses
from time import (localtime, time)
# Módulos deste projeto: 
import telinha
from status import (BarraStatus)
from tempotools import *


# computa dimensões de todas janelas.
def obtem_dimensoes(J: window) -> None:
   global LINHAS,COLUNAS
   LINHAS,COLUNAS = J.getmaxyx()

def barra_status(janela: window, *strings) -> None:
   """ 
   Cria uma barra de status, independente do monitor(janela) passada, 
   aceita um monte de strings, onde computa suas posições baseado no seus 
   comprimentos e espaços disponíveis. 
   """
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

def define_cores_e_configuracao(janela: window) -> None:
   curses.curs_set(False)     # oculta cursor do teclado.
   janela.nodelay(True)       # não bloqueia com o input.
   janela.keypad(True)        # ativa teclas especiais.

   # Paleta de cores:
   curses.init_pair(1, curses.COLOR_GREEN, 0)
   curses.init_pair(2, curses.COLOR_RED, 0)
   curses.init_pair(3, curses.COLOR_YELLOW, 0)
   curses.init_pair(4, curses.COLOR_WHITE, 0)
   curses.init_pair(13, curses.COLOR_WHITE, curses.COLOR_RED)
   curses.init_pair(12, curses.COLOR_WHITE, curses.COLOR_YELLOW)

def painel_de_controle(janela: window) -> None:
   pass

class Interruptor:
   """
   Variável do tipo boleano, entretanto em forma de objeto para manipulação
   como uma referência.
   """
   def __init__(self, ligado: bool) -> None:
      self.estado = ligado

   def __bool__(self) -> bool:
      return self.estado

   def liga(self) -> bool:
      if self.estado:
      # Se já estiver ativado, informa que a chamada não foi necessária.
         return False

      self.estado = True
      return True

   def desliga(self) -> bool:
      if (not self.estado):
         return False

      self.estado = False
      return True


def monitor_do_temporizador(janela: window) -> None:
   """
   Constrói uma interface gráfica de um temporizador, que faz uma contagem 
   regressiva baseado no valor da variável global TEMPO.
   """
   # atualiza atual dimensão da janela.
   obtem_dimensoes(janela)
   define_cores_e_configuracao(janela)

   # Para sair do programa.
   tecla = janela.getch()
   # Função temporizadora, dado um valor a "temporizar"....
   global TEMPO
   contador = contagem_regressiva(TEMPO)
   # Nova versão de interruptores:
   cronometro_ligado = Interruptor(False)
   dispara_horario = Interruptor(False)
   # Objetos da tela:
   status = BarraStatus(
      janela, '<S> sai do programa',
      '<N> nova contagem', '<C> conômetro',
      '<H> horário', '<Z> Cores'
   )

   # sub-janela; monitor do relógio.
   def desabilitador(hora, minuto, segundo):
      if hora == 0 and minuto != 0:
         hora = None
      if hora == 0 and minuto == 0:
         hora = None
         minuto = None
      return (hora, minuto, segundo)
   ...

   # Limpando a tela para renovação:
   tempo = segundos_em_horario(contador())
   (h, m, s) = desabilitador(*tempo)
   ledizinho = telinha.CronometroLED(janela, h, m, s)

   assert(status.tocar("<N> nova contagem"))

   while tecla != ord('s'):
      tecla = janela.getch()

      # alterna moldes do relógio.
      if tecla == curses.KEY_RESIZE:
         obtem_dimensoes(janela) # atualiza dimensões.
         janela.refresh()
      elif tecla == ord('c'):
         cronometro_ligado.liga()
         break
      elif tecla == ord('h'):
         dispara_horario.liga()
         break
      elif tecla == curses.KEY_RIGHT:
         status.muda_pra_direita()
      elif tecla == curses.KEY_LEFT:
         status.muda_a_esquerda()
      ...

      try:
         tempo = segundos_em_horario(contador())
      except ContagemLimiteError:
         print("o 'contador' está esgotado!")
         break
      finally:
         janela.erase()
         ledizinho.centraliza()
         ledizinho(*tempo)
         # Instruções na barra de status.
         status(); curses.napms(200)

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

def monitor_cronometro(janela):
   """
   constrói a interface gráfica do cronômetro
   que conta até quando for possível, na verdade
   o tempo total que ele suporta é 24h em ponto.
   """
   pass

def monitor_horario(janela):
   """
   constrói uma interface para visualizar o
   horário atual.
   """
   pass
