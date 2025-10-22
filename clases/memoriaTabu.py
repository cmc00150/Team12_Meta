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

    for u, l in enumerate(perm):     # Actualizamos la memoria a largo plazo (u - unidad y l - localización)
      self.__larga[u][l] += 1        # Indicamos que a la unidad se le ha asignado la localización l una vez más

  def tabu(self, i, j) -> bool:
    return (i,j) in self.__corta or (j,i) in self.__corta

  def reiniciar_corto_plazo(self):
    self.__corta.clear()

  def menosFrecuente(self) -> list[int]:
    n = len(self.__larga)
    perm = [-1] * n
    incluido = [0] * n
    
    for i in range(n):
        menosFrec = maxsize

        for j in range(n):
          if incluido[j] == 0 and self.__larga[i][j] > 0:   # SI la localización no ha sido incluida y la casilla es mayor que 0 (sino nos quedariamos con el 0 todo el rato)
            if self.__larga[i][j] < menosFrec:              # SI la localización actual es la que menos veces ha estado hastas ahora en la unidad i
              menosFrec = self.__larga[i][j]                # Actualizamos el valor del menos frecuente
              perm[i] = j       
        
        if menosFrec != maxsize:        # SI no se ha modificado la variable es porque no se ha escogido a ninguno (porque el menor ya estaria )
            incluido[perm[i]] = 1
    
    disponibles = [j for j in range(n) if incluido[j] == 0]
    for i in range(n):
        if perm[i] == -1 and disponibles:
            perm[i] = disponibles.pop(0)
            incluido[perm[i]] = 1

    return perm

  def masFrecuente(self) -> list[int]:
    n = len(self.__larga)
    perm = [-1] * n
    incluido = [0] * n
    
    # 1. Primera pasada: asignar según frecuencia máxima
    for i in range(n):
        masFrec = -1
        
        for j in range(n):
            if incluido[j] == 0:  # Solo considerar localizaciones disponibles
                if self.__larga[i][j] > masFrec:
                    masFrec = self.__larga[i][j]
                    perm[i] = j
        
        # Solo marcar como incluido si realmente se asignó
        if masFrec != -1:
            incluido[perm[i]] = 1

    disponibles = [j for j in range(n) if incluido[j] == 0]
    for i in range(n):
        if perm[i] == -1 and disponibles:
            perm[i] = disponibles.pop(0)
            incluido[perm[i]] = 1
            
    return perm
