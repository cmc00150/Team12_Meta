import time # Para medir cuánto tarda cada función en ejecutarsey poder comparar rendimientos
import random
from sys import maxsize
from .func_auxiliares import (dos_opt, fact, costo)
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
    
    i = 0                                                   # Posición inicial a investigar en la permutación
    it=0                                                    # Número de soluciones a las que nos movemos (iterador)
    mejora_global = 0                                       # Empezamos en 0 porque nos interesan solo los negativos (los que disminuyan el coste actual)
    factible = [0] * len(solInicial)                        # Inicializamos el vector de factibles
    n_factibles=len(solInicial)                             # Inicializamos el vector de factibles

    while it <= maxIteraciones and n_factibles > 0:
        if factible[i] == 0:                                # Si hay posibilidad de mejora entro
            improve = False
            for j in range(i+1, len(solInicial)+i):             # Opt-2, revisamos las posibles combinaciones
                j = j % len(solInicial)                             # Hacemos el modulo para que no se pase
                mejora = fact(i, j, solInicial, flujos, distancias) # Miramos si mejora esta combinacion

                if mejora < mejora_global:                          # SI la mejora hasta ahora es menor que lo que teniamos lo devolvemos
                    dos_opt(solInicial, i, j)                           # Hacemos el intercambio
                    
                    if factible[j] == 1:                                # SI hemos recuperado un no factible, ahora tenemos uno más
                        n_factibles += 1
                    factible[i] = factible[j] = 0                       # Indicamos que por estas dos unidades se puede seguir buscando

                    improve = True
                    it+=1
                    logBusqueda.registraCambioBLocal(i, j, solInicial, costoInicial + mejora, it)

                    break                                               # Salir del dlb una vez que encontramos una mejora
            
            if not improve:                                      # SI no se ha encontrado ninguna que mejora, vetamos esta posición poniendo un 1
                factible[i] = 1
                n_factibles -= 1

        i=(i+1)%len(solInicial)                               # Pasamos al siguiente elemento

    fin=time.time()                                         # Fin del contador del tiempo
    tiempo=fin-inicio                                       # Tiempo empleado en obtener el resultado
    return (solInicial, tiempo)                             # Permutación solución + tiempo de ejecución

def busqueda_tabu(flujos: list[list[int]], distancias: list[list[int]], solInicial:list[int], costoInicial: int, maxIteraciones: int, tenencia: int, oscilacion: float, estancamiento: float, logBusqueda: Log) -> tuple [list[int], float]:
    inicio = time.time()

    i = 0                                                       # Posición inicial a investigar en la permutación
    it=0                                                        # Número de soluciones a las que nos movemos (iterador)
    sin_mejora = 0                                              # Número de iteraciones sin mejora
    mejora_global = 0                                           # Empezamos en 0 porque nos interesan los que resten el coste actual
    mem = MemTabu(tenencia=tenencia, n=len(solInicial))         # Inicialización de la memoria tabú
    factible = [0] * len(solInicial)                            # Inicializamos el vector de factibles
    n_factibles=len(solInicial)                                 # Número de unidades factibles
    print(costo([3, 0, 1, 2], flujos, distancias))

    while it <= maxIteraciones:
        if factible[i] == 0:                                    # Si i tiene posibilidad de mejora buscamos con explorar_vecinos()
            mejor_local = ()
            mejora_local = maxsize
            tabu = False

            for j in range(i+1, len(solInicial)+i):                 # Opt-2, revisamos las posibles combinaciones
                j = j % len(solInicial)                                 # Hacemos el modulo para que no se pase
                mejora = fact(i, j, solInicial, flujos, distancias)     # Miramos si mejora esta combinacion
                act_tabu = mem.tabu(i, j)                               # Almacenamos el valor tabú del vecino actual

                if act_tabu and mejora >= mejora_global:                # SI es tabu y no mejora la puntuación global lo omitimos
                    continue

                if mejora < mejora_local:                               # SI este vecino mejora el valor actual lo apuntamos
                    tabu = act_tabu                                         # Indicamos que es tabú
                    mejor_local = (i, j)                                    # Guardamos el intercambio
                    mejora_local = mejora                                   # Guardamos la cantidad de mejora
            
            if mejora_local < mejora_global:                         # SI el mejor de los vecinos mejora el global lo escogemos
                    dos_opt(solInicial, i, j)                          # Hacemos el intercambio, nos movemos a él
                    
                    if factible[j] == 1:                               # SI hemos recuperado un no factible, ahora tenemos uno más
                        n_factibles += 1
                    factible[i] = factible[j] = 0                      # Indicamos que por estas dos unidades se puede seguir buscando

                    mejora_global = mejora                             # Actualizamos la mejora
                    if tabu:                                              # SI el vecino escogido es tabú
                        mem.eliminar(i,j)                                       # Lo quitamos de la lista
                    mem.push(i, j)                                        # La añadimos a la memoria tabú

                    logBusqueda.registraCambioBLocal(i, j, solInicial, costoInicial + mejora_global, it)
                    it+=1

            else:                                                      # SI no se ha encontrado ninguna que mejora
                factible[i] = 1                                            # Vetamos esta unidad poniendo un 1
                n_factibles -= 1                                           # Reducimos el número de casillas factibles
                sin_mejora+=1                                              # Aumentamos el número de iteraciones sin mejora
                if n_factibles == 0:                                       # SI no nos quedan más unidades factibles
                    factible = [0] * len(solInicial)                          # Reiniciamos el vector de posiciones factibles
                    i, j = mejor_local                                        # Sacamos el intercambio del mejor de los vecinos
                    dos_opt(solInicial, i, j)                    # Nos movemos a este vecino (aunque no mejore la global)

        i=(i+1)%len(solInicial)                                         # Pasamos al siguiente elemento
        if sin_mejora == maxIteraciones * estancamiento:                # SI el número de iteraciones sin mejoras es el 5% del máximo de iteraciones
            sin_mejora = 0                                                  # Reiniciamos el contador de mejora
            r = random() % 100 + 1                                          # Sacamos un número del 1 al 100
            nueva_perm = ()                                                 # Preparamos el nuevo cambio
            if r <= oscilacion * 100:                                       # SI está por debajo de la oscilación DIVERSIFICAMOS
                nueva_perm = mem.menosFrecuente()
            else:                                                           # De lo contrario INTENSIFICAMOS
                nueva_perm = mem.masFrecuente()
            dos_opt(solInicial, nueva_perm[0], nueva_perm[1])               # Hacemos el cambio

    fin=time.time()                                                 # Fin del contador del tiempo
    tiempo=fin-inicio                                               # Tiempo empleado en obtener el resultado
    return (solInicial, tiempo)                                     # Permutación solución + tiempo de ejecución
