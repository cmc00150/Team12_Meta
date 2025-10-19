from collections import deque
from sys import maxsize 

class MemTabu: 
  def __init__(self, tenencia: int, n: int):
    self.__viejo = 0
    self.__nuevo = 0
    self.__tenencia = tenencia
    self.__corta = [0] * tenencia
    self.__larga = [[0 for _ in range(n)] for _ in range(n)]
  
  def eliminar(self, i, j):          
    if (self.__nuevo - self.__viejo)**2 > 1:
      sust = 0
      guardo = self.__corta[self.__viejo]
      self.__viejo = self.__viejo % self.__tenencia
      while not (guardo == (i, j) or guardo == (j, i)):
        guardo = self.__corta[i+1]
        i %= self.__tenencia
        self.__corta[i+1] = sust
        sust = guardo
    elif self.__nuevo < self.__viejo:
        self.__corta.pop(self.__viejo)
        self.__viejo = self.__viejo % self.__tenencia
  
  def push(self, i, j):
    self.__corta.insert(self.__nuevo, (i,j))
    self.__nuevo = self.__nuevo % self.__tenencia
    if self.__nuevo > self.__viejo:
      self.__viejo = self.__viejo + 1 % self.__tenencia
    self.__larga[i][j] += 1

  def tabu(self, i, j) -> bool:
    tabu = False
    for t in self.__corta:
      if (i, j) == t or (j, i) == t:
        tabu = True
        break
    return tabu

  def menosFrecuente(self) -> tuple[int, int]: 
    menosFrec = ((), maxsize)
    for i, _ in enumerate(self.larga):
      for j in range(i+1, len(self.larga)):
        elem = self.__larga[i][j]
        if elem < menosFrec[1] and elem != 0:
          menosFrec = ((i, j), elem)
    return menosFrec[0]

  def masFrecuente(self) -> tuple[int, int]: 
    masFrec = ((), 0)
    for i, _ in enumerate(self.larga):
      for j in range(i+1, len(self.larga)):
        elem = self.__larga[i][j]
        if elem > masFrec[1] and elem != 0:
          masFrec = ((i, j), elem)
    return masFrec[0]