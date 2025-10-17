import time # Para medir cuánto tarda cada función en ejecutarsey poder comparar rendimientos
import random
from modulos.func_auxiliares import *
from clases.logs import Log

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

def busqueda_local_dlb(flujos: list[list[int]], distancias: list[list[int]], solInicial:list[int], costoInicial: int, maxIteraciones: int, logBusqueda: Log) -> tuple [list[int], float]:
    inicio = time.time()
    
    modf = Modificables(improve=False, n_factibles=len(solInicial), menor_actual=0, it=0, costo=costoInicial)
    i = 0
    factible = [0 for _ in solInicial]

    while modf.it <= maxIteraciones and modf.n_factibles > 0:
        modf.improve = False
        if factible[i] == 0: # Si hay posibilidad de mejor entro
            dlb_primer_mejor(solInicial, factible, i, modf, flujos, distancias, logBusqueda)

        if not modf.improve: # Si no se ha encontrado ninguna que mejora, vetamos esta posición poniendo un 1
            factible[i] = 1
            modf.n_factibles -= 1
            if modf.n_factibles == 0:
                break

        i=(i+1)%len(solInicial) # Pasamos al siguiente elemento

    fin=time.time() # Fin del contador del tiempo
    tiempo=fin-inicio # Tiempo empleado en obtener el resultado
    return (solInicial, tiempo) # Permutación solución + tiempo de ejecución

def busqueda_tabu(flujos: list[list[int]], distancias: list[list[int]], solInicial:list[int], costoInicial: int, maxIteraciones: int, tenencia: int, oscilacion: float, estancamiento: float, logBusqueda: Log) -> tuple [list[int], float]:
    inicio = time.time()
    
    modf = Modificables(improve=False, n_factibles=len(solInicial), menor_actual=0, it=0, costo=costoInicial)
    cortoPlazo=[0,0,0]
    posCortoPlazo=0
    largoPlazo=[[0 for _ in len(sol)] for _ in len(sol)]

    menorGlobal=solInicial
    menorCosteGlobal=costo
    
    while modf.it <= maxIteraciones and modf.n_factibles > 0:
        modf.improve = False
        if factible[i] == 0: # Si hay posibilidad de mejor entro
            dlb_tabu(solInicial, factible, i, modf, flujos, distancias, logBusqueda)

        if not modf.improve: # Si no se ha encontrado ninguna que mejora, vetamos esta posición poniendo un 1
            factible[i] = 1
            modf.n_factibles -= 1
            if modf.n_factibles == 0:
                break

        i=(i+1)%len(solInicial) # Pasamos al siguiente elemento

    fin=time.time() # Fin del contador del tiempo
    tiempo=fin-inicio # Tiempo empleado en obtener el resultado
    return (solInicial, tiempo) # Permutación solución + tiempo de ejecución
