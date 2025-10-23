import time # Para medir cuánto tarda cada función en ejecutarsey poder comparar rendimientos
import random
from sys import maxsize
from modulos.func_auxiliares import (dos_opt, fact, costo)
from clases.logs import Log
# from clases.memoriaTabu import MemTabu

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

def busqueda_tabu(flujos: list[list[int]], distancias: list[list[int]], solInicial:list[int], costoInicial: int, maxIteraciones: int, tenencia: int, oscilacion: float, estancamiento: float, logBusqueda: Log) -> tuple [list[int], float]:
    inicio = time.time()

    i = 0                                                       # Posición inicial a investigar en la permutación
    it=0                                                        # Número de soluciones a las que nos movemos (iterador)
    sin_mejora = 0                                              # Número de iteraciones sin mejora
    mejor_global = solInicial.copy()                            # Mejor movimiento hasta ahora
    mejora_global = costoInicial                                # Empezamos con el costo inicial
    coste_actual = costoInicial                                 # Costo de las soluciones hacia las que nos movemos
    mejor_peores = ()
    mejora_peores = maxsize
    mem = MemTabu(tenencia=tenencia, n=len(solInicial))         # Inicialización de la memoria tabú
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

                mem.push(i, j, solInicial)                              # La añadimos a la memoria tabú (si ya estaba se elimina y se vuelve a insertar automáticamente)
                it+=1
                sin_mejora = 0                                          # Hemos tenido una mejora
                mejor_peores = ()
                mejora_peores = maxsize
                logBusqueda.registraCambioBTabu(i,j,solInicial,coste_actual,mejora_global,it)
            else:                                                   # SI no se ha encontrado ninguna que mejora
                factible[i] = 1                                         # Vetamos esta unidad poniendo un 1
                n_factibles -= 1                                        # Reducimos el número de casillas factibles
                if mejora_local < mejora_peores:                        # Si este nuevo vecino supera al vecino encontrado
                    mejor_peores = mejor_local                              # Guardamos el vecino que es mejor aunque no mejore la global
                    mejora_peores = mejora_local                            # Guardamos su mejora también

        if it == maxIteraciones:
            break

        if n_factibles == 0:                                    # SI no nos quedan más unidades factibles
            factible = [0] * len(solInicial)                        # Reiniciamos el vector de posiciones factibles
            n_factibles = len(solInicial)
            k, l = mejor_peores                                     # Sacamos el intercambio del mejor de los vecinos encontrados hasta ahora
            dos_opt(solInicial, k, l)                               # Nos movemos a este vecino (aunque no mejore la global)
            mem.push(k, l, solInicial)                                          # Como nos hemos movido, insertamos la solución
            sin_mejora+=1                                           # Aumentamos el número de iteraciones sin mejora
            coste_actual+= mejora_peores
            mejor_peores = ()
            mejora_peores = maxsize
            it+=1
            logBusqueda.registraCambioBTabu(k,l,solInicial,coste_actual,mejora_global,it)

        i=(i+1)%len(solInicial)                                         # Pasamos al siguiente elemento

        if sin_mejora == maxIteraciones * estancamiento:                # SI el número de iteraciones sin mejoras es el 5% del máximo de iteraciones
            sin_mejora = 0                                                  # Reiniciamos el contador de mejora
            r = random.randint(1,100)                                     # Sacamos un número del 1 al 100
            nueva_perm = []                                                 # Preparamos el nuevo cambio
            intensificar=0
            if r <= oscilacion * 100:                                       # SI está por debajo de la oscilación DIVERSIFICAMOS
                nueva_perm = mem.menosFrecuente()
            else:                                                           # De lo contrario INTENSIFICAMOS
                nueva_perm = mem.masFrecuente()
                intensificar=1
            solInicial = nueva_perm                                 # Hacemos el cambio
            coste_actual = costo(nueva_perm, flujos, distancias)
            it+=1                                                   # Suma una iteración
            logBusqueda.registrarReinicializacionIntensificar(nueva_perm,coste_actual, it, intensificar) # Se registra en el log la reinicialización
            factible = [0] * len(solInicial)                        # Reiniciamos el vector de posiciones factibles
            n_factibles = len(solInicial)

    fin=time.time()                                                 # Fin del contador del tiempo
    tiempo=fin-inicio                                               # Tiempo empleado en obtener el resultado
    return (mejor_global, tiempo)                                     # Permutación solución + tiempo de ejecución