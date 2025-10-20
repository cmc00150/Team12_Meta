from collections import deque
from sys import maxsize 

class MemTabu: 
  def __init__(self, tenencia: int, n: int):
    self.__corta = deque(maxlen=tenencia)
    self.__larga = [[0 for _ in range(n)] for _ in range(n)]    
  
  def push(self, i, j, perm: list[int]):
    try:       
      self.__corta.remove((i,j))        # Intenta borrarlo por si ya estaba
    except:
      try:
        self.__corta.remove((j,i))      # Si no estaba mira el inverso
      except:
        pass

    self.__corta.append((i,j))          # Siempre lo añade (estuviera o no)

    for i, elem in enumerate(perm):     # Actualizamos la memoria a largo plazo (fila - unidad y col - localización)
      self.__larga[i][elem] += 1

  def tabu(self, i, j) -> bool:
    return (i,j) in self.__corta or (j,i) in self.__corta

  def reiniciar_corto_plazo(self):
    self.__corta.clear()

  def menosFrecuente(self) -> tuple[int, int]: 
    perm = []
    menosFrec = maxsize
    for i, _ in enumerate(self.__larga):
      for j in range(0, len(self.__larga)):
        elem = self.__larga[i][j]
        if elem < menosFrec and elem != 0:
          menosFrec = elem
          perm[i] = j
    return menosFrec[0]

  def masFrecuente(self) -> tuple[int, int]: 
    masFrec = ((), 0)
    for i, _ in enumerate(self.__larga):
      for j in range(i+1, len(self.__larga)):
        elem = self.__larga[i][j]
        if elem > masFrec[1] and elem != 0:
          masFrec = ((i, j), elem)
    return masFrec[0]
