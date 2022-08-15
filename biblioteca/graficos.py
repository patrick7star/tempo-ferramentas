

# biblioteca do Python:
from curses import *
from biblioteca.python_utilitarios.utilitarios import texto
from sys import stderr

# margem de cada seção da LED.
MARGEM = 5
# largura e altura padrão da LED.
LARGURA = 19
ALTURA = 8

class LED:
   def __init__(self, janela, horas, minutos, segundos):
      (max_Y, max_X) = janela.getmaxyx()
      # posições centralizadoras:
      y = max_Y // 2 - ALTURA//2
      x = max_X // 2 - (3*LARGURA + 2*MARGEM)//2

      # sub-janelas de cada peso na contagem
      # do "horário".
      self._hour = newwin(ALTURA, LARGURA, y, x)
      x += LARGURA + MARGEM
      self._min = newwin(ALTURA, LARGURA, y, x)
      x += LARGURA + MARGEM
      self._sec = newwin(ALTURA, LARGURA, y, x)

      # valores atuais.
      self._hora_atual = horas
      self._minuto_atual = minutos

      # construindo uma tela inicial.
      self._desenha_delimitador(janela)
      self._tela_inicial(horas, minutos, segundos)
   ...

   def _tela_inicial(self, hora, minuto, segundo):
      matriz_hora = texto.constroi_str("%2.2i"% hora)
      matriz_minuto = texto.constroi_str("%2.2i"% minuto)
      matriz_segundo = texto.constroi_str("%2.2i"% segundo)

      desenha_janela(self._hour, matriz_hora)
      desenha_janela(self._min, matriz_minuto)
      desenha_janela(self._sec, matriz_segundo)

      self._hour.refresh()
      self._min.refresh()
      self._sec.refresh()
   ...

   def __call__(self, hora, minuto, segundo):
      matriz_hora = texto.constroi_str("%2.2i"% hora)
      matriz_minuto = texto.constroi_str("%2.2i"% minuto)
      matriz_segundo = texto.constroi_str("%2.2i"% segundo)

      desenha_janela(self._hour, matriz_hora)
      desenha_janela(self._min, matriz_minuto)
      desenha_janela(self._sec, matriz_segundo)

      if self._hora_atual != hora:
         self._hour.refresh()
      if self._minuto_atual != minuto:
         self._min.refresh()

      # os segundos atualizada a cada meio-segundo.
      self._sec.refresh()
      napms(500)
   ...

   def _desenha_delimitador(self, janela):
      delimitador = texto.constroi_str(':')
      (max_Y, max_X) = janela.getmaxyx()
      # posições centralizadoras:
      yM = max_Y // 2 - ALTURA//2
      xM = max_X // 2 - (3*LARGURA + 2*MARGEM)//2
      # incrementos para 'x' e 'y'.
      incremento_y = ALTURA//3
      incremento_x = LARGURA + MARGEM//2
      # recuando posições dos delimitadores
      # verticalmente e horizontalmente ...
      xM += incremento_x-1
      yM += incremento_y-1
      add_mt(janela, yM, xM, delimitador)
      # pula a parte do LED central.
      xM += incremento_x + 3
      add_mt(janela, yM, xM, delimitador)
      # NOTA: Como nada é perfeito, foi ajustado
      # manulamente, acrescentando e decrementando,
      # com literais, os incrementos.¨\(´-´)/¨
   ...
...

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

class UmLED:
   def __init__(self, y, x, valor_inicial):
      self._atual = valor_inicial
      self._janela = newwin(ALTURA, LARGURA, y, x)
      self.posicao = (y, x)
   ...

   def __call__(self, novo_valor):
      if self._atual == novo_valor:
         return False 
      self._atual = novo_valor
      molde = "%2.2i" % novo_valor
      matriz = constroi_str(molde)
      desenha_janela(self._janela, matriz)
      self._janela.refresh()
      return True
   ...
...

class LEDs:
   def __init__(self, janela, horas, minutos, segundos):
      (max_Y, max_X) = janela.getmaxyx()
      (self.max_X, self.max_Y) = (max_X, max_Y)
      # posições centralizadoras:
      y = max_Y // 2 - ALTURA//2
      x = max_X // 2 - (3*LARGURA + 2*MARGEM)//2

      # construindo uma tela inicial.
      #self._desenha_delimitador(janela)
      # sub-janelas de cada peso na contagem
      # do "horário".
      if horas is not None:
         x = max_X // 2 - (3*LARGURA + 2*MARGEM)//2
         self._hour = newwin(ALTURA, LARGURA, y, x)
         x += LARGURA + MARGEM
         self._atualiza_hora(horas)
      else:
         self._hour = None
      ...
      self._hora_atual = horas

      if minutos is not None:
         x = max_X // 2 - (2*LARGURA + MARGEM)//2
         self._min = newwin(ALTURA, LARGURA, y, x)
         x += LARGURA + MARGEM
         self._atualiza_minuto(minutos)
      else:
         self._min = None
      ...
      self._minuto_atual = minutos
      # desenho inicial.
      self._sec = newwin(ALTURA, LARGURA, y, x)
      self._atualiza_segundo(segundos)
      janela.refresh()
   ...

   def _atualiza_hora(self, hora):
      # abandona a função.
      if self._hour is None:
         if __debug__:
            from sys import stderr
            print("sem display hora!", file=stderr)
         return None
      matriz = texto.constroi_str("%2.2i"% hora)
      desenha_janela(self._hour, matriz)
      self._hour.refresh()
   ...

   def _atualiza_minuto(self, minuto):
      if self._min is None:
         if __debug__:
            print("sem display minutos!")
         return None
      matriz = texto.constroi_str("%2.2i"% minuto)
      desenha_janela(self._min, matriz)
      self._min.refresh()
   ...

   def _atualiza_segundo(self, segundo):
      # executa sempre o desenha na seção do LED.
      matriz = texto.constroi_str("%2.2i"% segundo)
      desenha_janela(self._sec, matriz)
      self._sec.refresh()
   ...

   def __call__(self, hora, minuto, segundo):
      # se tais seções do LED estão ativados.
      hora_existe = self._hour is not None
      minuto_existe = self._min is not None

      if hora_existe:
         if self._hora_atual != hora:
            self._atualiza_hora(hora)
      ...
      if minuto_existe:
         if self._minuto_atual != minuto:
            self._atualiza_minuto(minuto)
      ...
      self._atualiza_segundo(segundo)
      napms(500)
   ...

   def _desenha_delimitador(self, janela):
      delimitador = texto.constroi_str(':')
      (max_Y, max_X) = janela.getmaxyx()
      # incrementos para 'x' e 'y'.
      incremento_y = ALTURA//3
      incremento_x = LARGURA + MARGEM//2

      # posições centralizadoras:
      yM = max_Y // 2 - ALTURA//2
      if self._hour is not None:
         xM = max_X // 2 - (3*LARGURA + 2*MARGEM)//2
         # recuando posições dos delimitadores
         # verticalmente e horizontalmente ...
         xM += incremento_x-1
         yM += incremento_y-1
         add_mt(janela, yM, xM, delimitador)
      ...
      if self._min is not None:
         # pula a parte do LED central.
         xM = max_X // 2 - (2*LARGURA + MARGEM)//2
         xM += incremento_x + 3
         add_mt(janela, yM, xM, delimitador)
      ...
   ...
...

