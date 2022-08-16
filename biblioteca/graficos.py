

# biblioteca do Python:
from curses import *
from biblioteca.python_utilitarios.utilitarios import texto
from sys import stderr

# margem de cada seção da LED.
MARGEM = 4
# largura e altura padrão da LED.
LARGURA = 19
ALTURA = 8

# um "pseudo-método" assim como todos os 
# existentes na 'lib' curses, porém este
# ao invés de strings e caractéres, desenha
# "matrizes-texto" na tela, dado a posição,
# e, é claro, a "matriz".
def add_mt(janela, y, x, matriz_texto, atributo=None):
   (altura, largura) = matriz_texto.dimensao()
   for lin in range(altura):
      for col in range(largura):
         char = matriz_texto[lin][col]
         try:
            if atributo is not None:
               janela.addch(y+lin, x+col, char, atributo)
            else:
               janela.addch(y+lin, x+col, char)
         except:
            pass
      ...
   ...
...

def desenha_janela(janela, matriz):
   (max_Y, max_X) = matriz.dimensao()
   # limpa janela primeiramente.
   janela.erase()
   add_mt(janela, 0, 0, matriz, atributo=color_pair(1))
...

class LEDs:
   def __init__(self, janela, horas, minutos, segundos):
      (max_Y, max_X) = janela.getmaxyx()
      # proposições:
      horas_OFF = horas is None
      minutos_OFF = (minutos is None) and horas_OFF

      # valores no canto-superior-esquerdo, para daí
      # fazer um desenho centralizado na tela.
      # só se alteram ao redimensionar janela.
      self._yM = (max_Y-ALTURA)//2

      if horas_OFF:
         container = 2*LARGURA + MARGEM
      elif minutos_OFF:
         container = LARGURA
      else:
         container = 3*LARGURA + 2*MARGEM
      self._xM = (max_X - container)//2

      # se pedido, ativar horas.
      if horas is not None:
         x = self._xM
         self._horas = newwin(ALTURA, LARGURA, self._yM, x)
         # valor de inicialização das horas.
         self._valor_horas = horas
      else:
         self._horas = None
      # se pedido, ativa minutos.
      if minutos is not None:
         if horas_OFF:
            x = self._xM
         else:
            x = self._xM + LARGURA + MARGEM
         self._minutos = newwin(ALTURA, LARGURA, self._yM, x)
         # valor de inicialização dos minutos.
         self._valor_min = minutos
      else:
         self._minutos = None
      # sempre inicializa os segundos.
      if minutos_OFF:
         x = self._xM + 2*MARGEM
      elif horas_OFF:
         x = self._xM + LARGURA + MARGEM
      else:
         x = self._xM + 2*(LARGURA + MARGEM)
      self._segundos = newwin(ALTURA, LARGURA, self._yM, x)

      self._esboco_inicial()
   ...

   def _atualiza_segundos(self, s):
      self._segundos.erase()
      matriz = texto.constroi_str("%2.2i"%s)
      desenha_janela(self._segundos, matriz)
      self._segundos.refresh()
   ...

   def _atualiza_minutos(self, m):
      if self._minutos is None:
         return False
      # só muda texto-desenhado se, e somente
      # se, houve atualização de valor real.
      if self._valor_min != m:
         self._minutos.erase()
         matriz = texto.constroi_str("%2.2i"%m)
         desenha_janela(self._minutos, matriz)
         self._minutos.refresh()
      # confirma atualização
      return True
   ...

   def _atualiza_horas(self, h):
      if self._horas is None:
         return False
      # só muda texto-desenhado se, e somente
      # se, houve atualização de valor real.
      if self._valor_horas != h:
         self._horas.erase()
         matriz = texto.constroi_str("%2.2i"%h)
         desenha_janela(self._horas, matriz)
         self._horas.refresh()
      # confirma atualização
      return True
   ...

   # atualiza cada sub-janela, se ela existir é claro.
   def _esboco_inicial(self):
      if self._minutos is not None:
         matriz = texto.constroi_str("%2.2i"%self._valor_min)
         desenha_janela(self._minutos, matriz)
         self._minutos.refresh()
      ...
      if self._horas is not None:
         matriz = texto.constroi_str("%2.2i"%self._valor_horas)
         desenha_janela(self._horas, matriz)
         self._horas.refresh()
      ...
      matriz = texto.constroi_str("%2.2i"%0)
      desenha_janela(self._segundos, matriz)
      self._segundos.refresh()
   ...

   def __call__(self, h, min, seg):
      self._atualiza_horas(h)
      self._atualiza_minutos(min)
      self._atualiza_segundos(seg)
      # taxa de atualização das sub-janelas.
      napms(500)
   ...
...

# apenas abrindo um novo bloco na classe
# para inserir novos métodos.
class LEDs(LEDs):
   def esboca_delimitadores(self, janela):
      separador = texto.constroi_str(":")
      # proposições:
      horas_OFF = self._horas is None
      minutos_OFF = (self._minutos is None) and horas_OFF

      # posições dos delimitadores iniciais.
      y = self._yM + 1

      if minutos_OFF:
         pass
      elif horas_OFF:
         x = self._xM + LARGURA + MARGEM//2 - 1
         add_mt(janela, y, x, separador)
      else:
         # primeiro.
         x = self._xM + LARGURA + MARGEM//2 - 1
         add_mt(janela, y, x, separador)
         # segundo.
         x = self._xM + 2*LARGURA + MARGEM +  MARGEM//2 - 3
         add_mt(janela, y, x, separador)
      ...
   ...
...
