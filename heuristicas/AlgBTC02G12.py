from sys import maxsize
from modulos.func_auxiliares import (dos_opt, fact, costo)
from clases.logs import Log

from collections import deque
from sys import maxsize 

class MemTabu: 
  def __init__(self, tenencia: int):
    self.__corta = deque(maxlen=tenencia) 
  
  def push(self, i, j):
    try:       
      self.__corta.remove((i,j))        # Intenta borrarlo por si ya estaba
    except:
      try:
        self.__corta.remove((j,i))      # Si no estaba mira el inverso
      except:
        pass

    self.__corta.append((i,j))          # Siempre lo añade (estuviera o no)    # Indicamos que a la unidad se le ha asignado la localización l una vez más

  def tabu(self, i, j) -> bool:
    return (i,j) in self.__corta or (j,i) in self.__corta

  def reiniciar_corto_plazo(self):
    self.__corta.clear()

def busqueda_tabu(flujos: list[list[int]], distancias: list[list[int]], solInicial:list[int], costoInicial: int, maxIteraciones: int, tenencia: int, log: Log) -> tuple [list[int], float]:

    i = 0                                                       # Posición inicial a investigar en la permutación
    it=0                                                        # Número de soluciones a las que nos movemos (iterador)
    mejor_global = solInicial.copy()                            # Mejor movimiento hasta ahora
    mejora_global = costoInicial                                # Empezamos con el costo inicial
    coste_actual = costoInicial                                 # Costo de las soluciones hacia las que nos movemos
    mejor_peores = ()
    mejora_peores = maxsize
    mem = MemTabu(tenencia=tenencia)         # Inicialización de la memoria tabú
    factible = [0] * len(solInicial)                            # Inicializamos el vector de factibles
    n_factibles=len(solInicial)                                 # Número de unidades factibles

    while it <= maxIteraciones:
      if factible[i] == 0:                                    # Si i tiene posibilidad de mejora buscamos con explorar_vecinos()
        mejor_local = ()
        mejora_local = maxsize
        for j in range(i+1, len(solInicial)+i):                 # Revisamos las posibles combinaciones
          j = j % len(solInicial)                                 # Hacemos el modulo para que no se pase
          mejora = fact(i, j, solInicial, flujos, distancias)     # Miramos si mejora esta combinacion

          if mem.tabu(i,j) and mejora + coste_actual >= mejora_global: # SI es tabu y no mejora la puntuación global lo omitimos
              continue

          if mejora < mejora_local:                               # Si es el mejor vecino lo apuntamos
              mejora_local = mejora
              mejor_local = (i,j)
        
        if coste_actual + mejora_local < coste_actual:         # SI el mejor de los vecinos mejora el valor actual nos movemos a él
          dos_opt(solInicial, mejor_local[0], mejor_local[1])                               # Hacemos el intercambio
          if factible[mejor_local[1]] == 1:                                    # SI hemos recuperado un no factible, ahora tenemos uno más
              n_factibles += 1
          factible[mejor_local[0]] = factible[mejor_local[1]] = 0                           # Indicamos que por estas dos unidades se puede seguir buscando
          coste_actual += mejora_local

          if coste_actual < mejora_global:
              mejor_global = solInicial.copy()
              mejora_global = coste_actual                       # Actualizamos la mejora

          mem.push(i, j)                              # La añadimos a la memoria tabú (si ya estaba se elimina y se vuelve a insertar automáticamente)
          it+=1
          mejor_peores = ()
          mejora_peores = maxsize
        else:                                                   # SI no se ha encontrado ninguna que mejora
          factible[i] = 1                                         # Vetamos esta unidad poniendo un 1
          n_factibles -= 1                                        # Reducimos el número de casillas factibles
          if mejora_local < mejora_peores:                        # Si este nuevo vecino supera al vecino encontrado
            mejor_peores = mejor_local                              # Guardamos el vecino que es mejor aunque no mejore la global
            mejora_peores = mejora_local                            # Guardamos su mejora también

      if n_factibles == 0:                                    # SI no nos quedan más unidades factibles
        factible = [0] * len(solInicial)                        # Reiniciamos el vector de posiciones factibles
        n_factibles = len(solInicial)
        k, l = mejor_peores                                     # Sacamos el intercambio del mejor de los vecinos encontrados hasta ahora
        dos_opt(solInicial, k, l)                               # Nos movemos a este vecino (aunque no mejore la global)
        mem.push(k, l)                                          # Como nos hemos movido, insertamos la solución
        coste_actual+= mejora_peores
        mejor_peores = ()
        mejora_peores = maxsize
        it+=1
      
      log.registraCambioBTabu(i,j,solInicial,coste_actual,mejora_global,it)
      i=(i+1)%len(solInicial)                                         # Pasamos al siguiente elemento

      if it == maxIteraciones:
        break

    return mejor_global                                     # Permutación solución + tiempo de ejecución