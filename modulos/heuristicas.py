import time # Para medir cuánto tarda cada función en ejecutarsey poder comparar rendimientos
import random
from sys import maxsize
from .func_auxiliares import (explorar_vecinos, Modificables, dos_opt, fact)
from clases.logs import Log
from clases.memoriaTabu import MemTabu

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
    
    i = 0
    mejora_global = 0 # Empezamos en 0 porque nos interesan solo los negativos (los que disminuyan el coste actual)
    factible = [0] * len(solInicial) # Inicializamos el vector de factibles
    n_factibles=len(solInicial), 
    it=0

    while it <= maxIteraciones and n_factibles > 0:
        if factible[i] == 0: # Si hay posibilidad de mejora entro
            mejor_local = ()
            mejora_local = maxsize

            for j in range(i+1, len(solInicial)+i): # Opt-2, revisamos las posibles combinaciones
                j = j % len(solInicial) # Hacemos el modulo para que no se pase
                mejora = fact(i, j, solInicial, flujos, distancias) # Miramos si mejora esta combinacion

                if mejora < mejora_local: # Guardamos el mejor hasta ahora
                    mejor_local = (i, j)
                    mejora_local = mejora

                if mejora_local < mejora_global: # Si la mejora hasta ahora es menor que lo que teniamos lo devolvemos
                    dos_opt(solInicial, i, j) # Hacemos el intercambio
                    
                    if factible[j] == 1: # Si hemos recuperado un no factible, ahora tenemos uno más
                        n_factibles += 1
                    factible[i] = factible[j] = 0 # Indicamos que por estas dos unidades se puede seguir buscando

                    it+=1
                    break # Salir del dlb una vez que encontramos una mejora

        if mejora < mejora_global: # Si ha habido mejora actualizamos
            mejora_global = mejora
            i, j = mejor_local
            costoInicial+= mejora_local
            logBusqueda.registraCambioBLocal(i, j, solInicial, costoInicial, it)
        else: # Si no se ha encontrado ninguna que mejora, vetamos esta posición poniendo un 1
            factible[i] = 1
            n_factibles -= 1
            if n_factibles == 0:
                break

        i=(i+1)%len(solInicial) # Pasamos al siguiente elemento

    fin=time.time() # Fin del contador del tiempo
    tiempo=fin-inicio # Tiempo empleado en obtener el resultado
    return (solInicial, tiempo) # Permutación solución + tiempo de ejecución

def busqueda_tabu(flujos: list[list[int]], distancias: list[list[int]], solInicial:list[int], costoInicial: int, maxIteraciones: int, tenencia: int, oscilacion: float, estancamiento: float, logBusqueda: Log) -> tuple [list[int], float]:
    inicio = time.time()

    i = 0
    mejora_global = 0 # Empezamos en 0 porque nos interesan solo los negativos (los que disminuyan el coste actual)
    factible = [0] * len(solInicial) # Inicializamos el vector de factibles
    n_factibles=len(solInicial)
    it=0
    mem = MemTabu(tenencia=tenencia, n=len(solInicial))

    while it <= maxIteraciones:
        if factible[i] == 0: # Si i tiene posibilidad de mejora buscamos con explorar_vecinos()
            mejor_local = ()
            mejora_local = maxsize
            improve = False

            for j in range(i+1, len(solInicial)+i): # Opt-2, revisamos las posibles combinaciones
                j = j % len(solInicial) # Hacemos el modulo para que no se pase
                mejora = fact(i, j, solInicial, flujos, distancias) # Miramos si mejora esta combinacion
                tabu = mem.tabu(i, j)

                if tabu and mejora >= mejora_global: #  
                    continue

                if mejora < mejora_global: # Si la mejora encontrada es mejor que la global, nos movemos
                    dos_opt(solInicial, i, j) # Hacemos el intercambio
                    
                    if factible[j] == 1: # Si hemos recuperado un no factible, ahora tenemos uno más
                        n_factibles += 1
                    factible[i] = factible[j] = 0 # Indicamos que por estas dos unidades se puede seguir buscando

                    mejora_global = mejora
                    if tabu:
                        mem.eliminar(i,j) # Si ya estaba en la list lo quitamos
                    mem.push(i, j) # La añadimos a la memoria tabú
                    logBusqueda.registraCambioBLocal(i, j, solInicial, costoInicial - mejora_global, it)
                    improve = True
                    it+=1
                    break # Salir del for una vez que encontramos una mejora

                if mejora < mejora_local: # Guardamos el mejor hasta ahora
                    mejor_local = (i, j)
                    mejora_local = mejora

            if not improve: # Si no se ha encontrado ninguna que mejora, vetamos esta posición poniendo un 1
                factible[i] = 1
                n_factibles -= 1
                if n_factibles == 0: # Si no nos quedan más posiciones factibles
                    factible = [0] * len(solInicial) # Reiniciamos el vector de posiciones factibles
                    i, j = mejor_local
                    solInicial = dos_opt(solInicial, i, j) # Intercambiamos para quedarnos con el mejor de los vecinos encontrados (aunque no mejore la global)

        i=(i+1)%len(solInicial) # Pasamos al siguiente elemento

    fin=time.time() # Fin del contador del tiempo
    tiempo=fin-inicio # Tiempo empleado en obtener el resultado
    return (solInicial, tiempo) # Permutación solución + tiempo de ejecución
