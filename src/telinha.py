# Biblioteca do Python:
from curses import *
from sys import stderr
import unittest
from datetime import (timedelta)
from queue import (SimpleQueue)
# Importa demais módulos:
from utilitarios import texto

# margem de cada seção da LED.
MARGEM = 4
# largura e altura padrão da LED.
LARGURA = 19
ALTURA = 8


# Um "pseudo-método" assim como todos os existentes na 'lib' curses, porém 
# este ao invés de strings e caractéres, desenha "matrizes-texto" na tela, 
# dado a posição, e, é claro, a "matriz".
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

def desenha_janela(janela, matriz):
   (max_Y, max_X) = matriz.dimensao()
   # limpa janela primeiramente.
   janela.erase()
   add_mt(janela, 0, 0, matriz, atributo=color_pair(1))

def cria_separador() -> texto.MatrizTexto:
   separador = texto.constroi_str(":")

   separador.margem(2, texto.Lados.DIREITO)
   separador.margem(2, texto.Lados.SUPERIOR)

   return separador


# Muito desorganizado o código, então será todo reescrito. Se chegar com algo
# com mais linhas do que a primeira versão, então falhei.
class CronometroLED():
   # Objeto totalmente compartilhado, um para ser usado no desenho geral,
   # o outro para servir de medida pro calcula da dimensão do objeto.
   SEP = cria_separador()
   ZERO = ZERO = texto.constroi_str("00")

   def __init__(self, janela: window, h: int, _min: int, seg:int) -> None:
      # Segue restrições a rígido.
      if (h is not None) and (_min is not None) and (seg is not None):
         assert(0 <= h <= 23)
         assert(0 <= _min <= 59)
         assert(0 <= seg <= 59)
      assert(isinstance(janela, window) and (janela is not None))
      assert(any(map(lambda x: x is not None, [h, _min, seg])))

      self.digitos = [h, _min, seg]
      self.tela = janela
      self.posicao = (3, 3)
      self.grade = SimpleQueue()

   def _dimensao(self) -> (int, int):
      "Computa uma estimativa da dimensão do objeto concatenado."
      ZERO = CronometroLED.ZERO
      DIGITOS_LENGTH = ZERO.dimensao()[1]
      DIGITOS_HEIGHT = ZERO.dimensao()[0]
      SEP_LENGTH = CronometroLED.SEP.dimensao()[1]
      LARGURA = 3 * DIGITOS_LENGTH + 2 * SEP_LENGTH

      return (DIGITOS_HEIGHT, LARGURA)

   def _constroi(self) -> None:
      (horas, minutos, segundos) = self.digitos
      # Formatação string das partes:
      h_str    = ("%02d" % horas)
      min_str  = ("%02d" % minutos)
      seg_str  = ("%02d" % segundos)
      # Onde começar a desenhar o objeto na tela.
      (y, x)   = self.posicao
      # Cores usadas.
      COR_PADRAO = color_pair(1)
      COR_SEP    = color_pair(4)
      COR_RESTO  = color_pair(2)

      hora_desenho = texto.constroi_str(h_str)
      min_desenho  = texto.constroi_str(min_str)
      seg_desenho  = texto.constroi_str(seg_str)
      separador    = CronometroLED.SEP
      # Total de itens a remover e re-inserir no final.
      # Cursor do final do desenhado iterado na grade.
      CURSOR       = 0

      # Ajusta o separador antes de concatenar.
      #esvazia_fila(self.grade)
      self.grade.put(hora_desenho)
      self.grade.put(separador)
      self.grade.put(min_desenho)
      self.grade.put(separador)
      self.grade.put(seg_desenho)

      # Desenhando pixel-por-pixel ...
      while (not self.grade.empty()):
         desenho = self.grade.get()
         (ALTURA, LARGURA) = desenho.dimensao()
         # Proposições evaluadas:
         os_segundos_finais = (
            # Esta nos segundos determinados:
            horas == 0 and minutos == 0 and
            (segundos >= 0 and segundos <= 49) and
            # Tem que ser o dígito dos segundos:
            (desenho is seg_desenho)
         )
         e_um_separador = (desenho is CronometroLED.SEP)

         # Definindo cor dos separadores, e quando estiver em contagem
         # regressiva, algo entre menos que um minuto.
         if e_um_separador:
            cor = COR_SEP
         elif os_segundos_finais:
            cor = COR_RESTO
         else:
            cor = COR_PADRAO

         # Marca pixel-por-pixel na posição correta.
         for i in range(ALTURA):
            for j in range(LARGURA):
               pixel = desenho[i][j]
               (py, px) = (y + i, x + j + CURSOR)
               self.tela.addch(py, px, pixel, cor)
         CURSOR += LARGURA 

   def _atualiza(self, hora: int, minuto: int, segundo: int) -> None:
      if hora is not None:
         self.digitos[0] = hora

      if minuto is not None:
         self.digitos[1] = minuto

      if segundo is not None:
         self.digitos[2] = segundo

   def __call__(self, *args):
      if len(args) == 3:
         (h, _min, seg) = args
         self._atualiza(h, _min, seg)
         self._constroi()

      elif len(args) == 1:
         assert(isinstance(args[0],timedelta))

         t = args[0]
         hours = int(t.total_seconds()) // 3600
         mins = int(t.total_seconds() // 60)
         self.__call__(hours, mins, t.seconds % 60)

      else:
         if __debug__:
            print("Quantia de parâmetros: %d" % len(args))
         raise ValueError("argumento não válido!")

   def posiciona(self, y: int, x: int) -> None:
      (MAX_Y, MAX_X) = self.tela.getmaxyx()
      (H, C) = self._dimensao()
      # Proposições:
      NAO_TRANSBORDA_OBJETO = (y + H < MAX_Y) and (x + C < MAX_X)
      COORDENADAS_FORA_DA_TELA = (0 <= y <= MAX_Y) and (0 <= x <= MAX_X)

      if (not NAO_TRANSBORDA_OBJETO):
         raise IndexError("coordenadas transbordam objeto da tela")

      if COORDENADAS_FORA_DA_TELA:
         self.posicao = (y, x)
      else:
         raise IndexError("coordenadas transbordam a tela") 

   def centraliza(self) -> None:
      # Dimensões da tela e do objeto, respectivamente:
      (H, L) = self.tela.getmaxyx()
      (h, l) = self._dimensao()
      # Calcula uma centralização pensando no ponto esquerdo superior.
      (y, x) = ((H - h) // 2, (L - l) // 2)

      self.posiciona(y, x - 10)
...


class CronometroLedUnitarios(unittest.TestCase):
   def simples_instanciacao(self):
      janela = initscr()

      try:
         start_color()
         print("Cor do terminal iniciada com sucesso.")
      except _curses.error:
         print("Erro ao tentar iniciar cores!")


      objeto = CronometroLED(janela, 5, 20, 30)
      objeto(timedelta(hours=9, minutes=35, seconds=12))
      janela.refresh()
      napms(1200)
      endwin()

   def atributo_e_criado_em_runtime(self):
      objeto = CronometroLED(initscr(), 1, 2, 3)
      objeto._constroi()
      print("\rCampo digitos:",hasattr(objeto, "digitos"))
      print("\rCampo tela:",hasattr(objeto, "tela"))
      print("\rCampo posição:",hasattr(objeto, "posicao"))
      print("\rCampo grade:",hasattr(objeto, "grade"))
      endwin()
