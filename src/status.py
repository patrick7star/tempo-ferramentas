from curses import (window)
import curses


class BarraStatus:
   """
   Objeto que serve como barra de status para qualquer tela. Ele também é uma
   menu que mostra foco em qualquer seleção.
   """
   def __init__(self, janela: window, *menus) -> None:
      (y, _) = janela.getmaxyx()

      self.tela = janela
      self.posicao = (y - 1, 0)
      self.menus = list(menus)
      self.tocado = None 

   def _constroi_formatacao(self) -> str:
      QTD = len(self.menus)
      (_, COL) = self.tela.getmaxyx()
      E = int((COL - sum(len(s) for s in self.menus)) / QTD)
      # Quantia de espaços entre legendas.
      espaco = ' '*E 
      # Espaço das pontas.
      meio_espaco = ' '*int(E / 2 - 2) 

      # condições especiaís e genéricas.
      if QTD == 1:
         texto = meio_espaco + strings[0] + meio_espaco
      else:
         texto = meio_espaco # meio-espaço inicial.
         texto += espaco.join(self.menus)
         # subtraindo espaço indesejado.
         texto[0:len(texto)-len(espaco)]
         # colocando meio espaço no lugar.
         texto += meio_espaco
      return texto

   def _desenha_na_tela(self) -> None:
      (LINHAS, _) = self.tela.getmaxyx()
      fmt = self._constroi_formatacao()
      PONTO = (LINHAS - 2, 0)

      # Primeiro esboço, inicialmente sem cor, da barra de status.
      self.tela.addstr(*PONTO, fmt)

      # Pinta a feature atualmente selecionada. Se houver algum menu é claro.
      if self.menus is not [] and (self.tocado is not None):
         selecionado = self.menus[self.tocado]
         self.tela.addstr(0, 15, selecionado)
         indice = fmt.index(selecionado)
         cor = curses.color_pair(12)
         self.tela.addstr(LINHAS - 2, indice, selecionado, cor)
      
   def __call__(self):
      self._desenha_na_tela()

   def tocar(self, menu: str) -> bool:
      for (posicao, item) in enumerate(self.menus):
         # Registra posição que tal menu assume na lista de menus.
         if item == menu:
            self.tocado = posicao
            return True 
      return False
         
   def _indice(self, obj: str) -> int:
      assert(isinstance(obj, str))

      for (p, item) in enumerate(array):
         if item == obj:
            return p
      raise ValueError("não objeto tal objeto na array")

   def muda_pra_direita(self) -> bool:
      if self.tocado is None:
         return False

      try:
         total = len(self.menus)
         atual = self.tocado
         self.tocado = (atual + 1) % total

      except ValueError:
         return False
      finally:
         return True

   def muda_a_esquerda(self) -> bool:
      if self.tocado is None:
         return False

      try:
         total = len(self.menus)
         atual = self.tocado
         self.tocado = (atual - 1) % total
      except ValueError:
         return False
      finally:
         return True

