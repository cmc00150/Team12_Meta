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

  def menosFrecuente(self) -> tuple[int, int]: 
    perm = [-1] * len(self.__larga)
    incluido = [0] * len(self.__larga)
    
    for i, _ in enumerate(self.__larga):          # Recorremos las unidades (filas)
      menosFrec = maxsize
      for j, frec in enumerate(self.__larga[i]):    # Por cada unidada, miramos las locailzaciones donde ha estado menos (columnas)
        if frec > 0 and frec < menosFrec and incluido[j] == 0:             # SI la frecuencia es menor que el mínimo hasta ahora y es mayor que 0 (porque sino es una casilla inactiva)
          menosFrec = frec                              # Asignamos de nuevo
          perm[i] = j
      incluido[perm[i]] = 1

    return perm

  def masFrecuente(self) -> tuple[int, int]: 
    perm = [-1] * len(self.__larga)
    incluido = [0] * len(self.__larga)

    for i, _ in enumerate(self.__larga):          # Recorremos las unidades (filas)
      masFrec = 0
      for j, frec in enumerate(self.__larga[i]):    # Por cada unidada, miramos las locailzaciones donde ha estado menos (columnas)
        if frec > masFrec and incluido[1] == 0:                            # SI la frecuencia es menor que el mínimo hasta ahora y es mayor que 0 (porque sino es una casilla inactiva)
          masFrec = frec                              # Asignamos de nuevo
          perm[i] = j                                   # Le asignamos la localización a esa unidad
          incluido[j] = 1

    return perm
