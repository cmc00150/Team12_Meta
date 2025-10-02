import time # Para medir cuánto tarda cada función en ejecutarsey poder comparar rendimientos
import random
from modulos.func_auxiliares import *

def greedy(flujos: list[list[int]], distancias: list[list[int]], candidatos: int) -> tuple [list[int], float]:
    inicio = time.time() # Inicio el contador del tiempo

    # Obtenemos los vectores
    v_flujos = [(i, sum(row)) for i, row in enumerate(flujos)]
    v_distancias = [(i, sum(row)) for i, row in enumerate(distancias)]

    # Los ordenamos
    sorted_flujos = sorted(v_flujos, key=lambda tuple: tuple[1], reverse=True) # Mayor a menor
    sorted_distancias = sorted(v_distancias, key=lambda tuple: tuple[1]) # Menor a mayor

    permutacion = [0] * candidatos
    for _ in range(candidatos):
        permutacion[sorted_flujos.pop(0)[0]] = sorted_distancias.pop(0)[0]

    fin=time.time() # Fin del contador del tiempo
    tiempo=fin-inicio # Tiempo empleado en obtener el resultado
    return (permutacion, tiempo) # Permutación solución + tiempo de ejecución

def greedy_aleatorizado(flujos: list[list[int]], distancias: list[list[int]], candidatos: int, k: int) -> tuple [list[int], float]:
    inicio = time.time() # Inicio el contador del tiempo

    # Obtenemos los vectores
    v_flujos = [(i, sum(row)) for i, row in enumerate(flujos)]
    v_distancias = [(i, sum(row)) for i, row in enumerate(distancias)]

    # Los ordenamos
    sorted_flujos = sorted(v_flujos, key=lambda tuple: tuple[1], reverse=True) # Mayor a menor
    sorted_distancias = sorted(v_distancias, key=lambda tuple: tuple[1]) # Menor a mayor

    permutacion = [0] * candidatos
    for _ in range(candidatos):
        aleatorioFlujos=random.randint(0,min(k,len(sorted_flujos)-1)) # El aleatorio tiene que ser entre 0 y k o entre 0 y el tamaño del vector en caso de que haya menos de k elementos
        aleatorioDistancias=random.randint(0,min(k,len(sorted_distancias)-1))

        permutacion[sorted_flujos.pop(aleatorioFlujos)[0]] = sorted_distancias.pop(aleatorioDistancias)[0]

    fin=time.time() # Fin del contador del tiempo
    tiempo=fin-inicio # Tiempo empleado en obtener el resultado
    return (permutacion, tiempo) # Permutación solución + tiempo de ejecución
    
def costo(permutacion, flujos: list[list[int]], distancias: list[list[int]]): # Función de evaluación de los diferentes algoritmos
    costo = 0
    for i, main in enumerate(permutacion):
        aux = 0
        for j in range(i+1, len(permutacion)): # Para no repetir valores, vamos de i hasta el final
            it = permutacion[j]
            aux += flujos[i][j] * distancias[main][it] * 2 # Sabiendo que es simetrica
        costo += aux
    return costo

def busqueda_local_dlb(flujos: list[list[int]], distancias: list[list[int]], candidatos: int, k: int) -> tuple [list[int], float]:
    inicio = time.time()

    solucion_1 = greedy_aleatorizado(flujos, distancias, candidatos, k)[0]
    DLB(solucion_1, flujos, distancias, 5000)

    fin=time.time() # Fin del contador del tiempo
    tiempo=fin-inicio # Tiempo empleado en obtener el resultado
    return (solucion_1, tiempo) # Permutación solución + tiempo de ejecución
