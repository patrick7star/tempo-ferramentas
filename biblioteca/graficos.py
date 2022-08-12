

# biblioteca do Python:
from curses import *
#from .python_utilitarios.utilitarios.texto import constroi_str
from biblioteca.python_utilitarios.utilitarios import texto


class LED:
   def __init__(self, janela, horas, minutos, segundos):
      (lin, col) = janela.getmaxyx()
      # posições centralizadoras:
      meio_y = lin // 2 - 5
      meio_x = col // 2

      self._hour = newwin(8, 20, meio_y, 0)
      self._min  = newwin(8, 20, meio_y, 20)
      self._sec  = newwin(8, 20, meio_y, 40)

      # valores atuais.
      self._hora_atual = horas
      self._minuto_atual = minutos

      # construindo uma tela inicial.
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
...


def desenha_janela(janela, matriz):
   (max_Y, max_X) = matriz.dimensao()
   # limpa janela primeiramente.
   janela.erase()
   # desenha novo valor.
   for y in range(max_Y):
      for x in range(max_X):
         char = matriz[y][x]
         try:
            janela.addch(y, x, char)
         except: pass
      ...
   ...
...
