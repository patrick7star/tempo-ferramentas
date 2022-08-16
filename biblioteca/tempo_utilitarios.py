
# o que pode ser importado.
__all__ = [
   "TEMPO", "registros",
   "ContagemLimiteError",
   "CronometroLimiteError",
   "segundos_em_horario",
   "horario_em_segundos",
   "contagem_regressiva",
   "contagem_crescente"
]

from time import gmtime, time, localtime

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
