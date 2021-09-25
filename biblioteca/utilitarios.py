# módulos do Python:
import copy, os.path
# módulos necessários:
from .externa.moldura_str import matriciar, imprime


# dicionário contendo todos algarismos, e 
# acrônimos, com representação matricial.
algs_e_mais = {} # vázia inicialmente.
# o caminho para o diretório contendo 
# números, acrônimos e outros símbolos 
# desenhados com caractéres.
caminho_numeros = r'./símbolos/números'
caminhos_acron = r'./símbolos/acronimos'
caminho_outros = r'./símbolos/'

def numero_desenho(numero):
   global algs_e_mais

   # se for a primeira vez de acesso, então
   # obter dados do disco, e gravar também 
   # na memória.
   if numero not in algs_e_mais:
      # proposições:
      if type(numero) == int and (numero >= 0 and numero <= 9):
         if numero == 0:
            numero_str = 'zero.txt'
         elif numero == 1:
            numero_str = 'um.txt'
         elif numero == 2:
            numero_str = 'dois.txt'
         elif numero == 3:
            numero_str = 'três.txt'
         elif numero == 4:
            numero_str = 'quatro.txt'
         elif numero == 5:
            numero_str = 'cinco.txt'
         elif numero == 6:
            numero_str = 'seis.txt'
         elif numero == 7:
            numero_str = 'sete.txt'
         elif numero == 8:
            numero_str = 'oito.txt'
         else:
            numero_str = 'nove.txt'
         with open(os.path.join(caminho_numeros,numero_str), 'rt') as arq:
            dados = matriciar(arq.read())
            algs_e_mais[numero] = dados
            return dados

      elif type(numero) == str and numero in ('am','pm'):
         # conteúdo do arquivo.
         with open(os.path.join(caminhos_acron,numero+'.txt'), 'rt') as arq:
            dados = matriciar(arq.read())
            algs_e_mais[numero] = dados
            return dados
   else:
      return algs_e_mais[numero]


# mesclador de matrizes com a mesma 
# quantia de linhas.
def mescla_matrizes(*matrizes):
   # cópia de primeira.
   geral = copy.deepcopy(matrizes[0]) 
 
   # lendo outros símbolos, como o separador
   # dos "algarismos" do horário.' Lê o disco
   # inicialmente, na próxima execução, guarda
   # em memória.
   if 'sep'.upper() not in algs_e_mais:
      with open(os.path.join(caminho_outros,'separador.txt'),'rt') as arq:
         SEPARADOR = matriciar(arq.read())
         # adicionando "separador" também a memória.
         algs_e_mais['SEP'] = SEPARADOR
   else: SEPARADOR = algs_e_mais['SEP']

   # verifica se tal matriz não é um dos
   # acrônimos.
   def nao_acronimo(matriz):
      global algs_e_mais
      # adicionando na memória os acrônimos para 
      # evitar erros, caso não foram carregados ainda.
      caminho1 = os.path.join(caminhos_acron,'am.txt')
      caminho2 = os.path.join(caminhos_acron, 'pm.txt')
      with open(caminho1,'rt') as arq, open (caminho2, 'rt') as arq_i:
         dados = matriciar(arq.read())
         algs_e_mais['am'] = dados
         dados = matriciar(arq_i.read())
         algs_e_mais['pm'] = dados

      # proposições:
      p1 = matriz != algs_e_mais['am']
      p2 = matriz != algs_e_mais['pm']
      return p1 and p2

   # junta com as demais.
   k = 1 # contador de pares e contador de vezes.
   for M in matrizes[1:]:

      if k % 2 == 0:
         for (i, linha) in enumerate(SEPARADOR):
            if nao_acronimo(M):
               geral[i].extend(linha)
            else:
               geral[i].extend([' ', ' '])
      for (i, linha) in enumerate(M):
         geral[i].extend(linha)
      k += 1

   # retorno da matriz geral mesclada.
   return geral
