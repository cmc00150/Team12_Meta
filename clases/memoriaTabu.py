from collections import deque
from sys import maxsize

class MemTabu: 
  def __init__(self, tenencia: int, n: int):
    self.__corta = deque(maxlen=tenencia)
    self.__larga = [0 for _ in range(n) for _ in range(n)]
  
  def pop(self):
    return self.__corta.popleft()
  
  def push(self, i, j):
    self.__corta.append((i, j))
    self.__larga[i][j] += 1

  def menosFrecuente(self): 
    menosFrec = ((), maxsize)
    for i, _ in enumerate(self.larga):
      for j in range(i+1, len(self.larga)):
        elem = self.__larga[i][j]
        if elem < menosFrec[1] and elem != 0:
          menosFrec = ((i, j), elem)

  def masFrecuente(self): 
    masFrec = ((), 0)
    for i, _ in enumerate(self.larga):
      for j in range(i+1, len(self.larga)):
        elem = self.__larga[i][j]
        if elem > masFrec[1] and elem != 0:
          masFrec = ((i, j), elem)