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
    mejora_global = 0                                       # Empezamos con una mejora de 0 (buscamos negativos)
    factible = [0] * len(solInicial)                        # Inicializamos el vector de factibles
    n_factibles=len(solInicial)                             # Inicializamos el vector de factibles

    while it <= maxIteraciones and n_factibles > 0:
        if factible[i] == 0:                                # Si hay posibilidad de mejora entro
            improve = False
            for j in range(i+1, len(solInicial)+i):             # Opt-2, revisamos las posibles combinaciones
                j = j % len(solInicial)                             # Hacemos el modulo para que no se pase
                mejora = fact(i, j, solInicial, flujos, distancias) # Miramos si mejora esta combinacion

                if mejora_global + mejora < mejora_global:          # SI la mejora hasta ahora mejor que lo que teniamos lo devolvemos
                    dos_opt(solInicial, i, j)                           # Hacemos el intercambio
                    
                    if factible[j] == 1:                                # SI hemos recuperado un no factible, ahora tenemos uno más
                        n_factibles += 1
                    factible[i] = factible[j] = 0                       # Indicamos que por estas dos unidades se puede seguir buscando

                    improve = True
                    it+=1
                    costoInicial += mejora
                    mejora_global += mejora
                    logBusqueda.registraCambioBLocal(i, j, solInicial, costoInicial, it)

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
    mejora_global = costoInicial                                # Empezamos en 0 porque nos interesan los que resten el coste actual
    mejor_global = []                                           # Mejor movimiento hasta ahora
    mem = MemTabu(tenencia=tenencia, n=len(solInicial))         # Inicialización de la memoria tabú
    factible = [0] * len(solInicial)                            # Inicializamos el vector de factibles
    n_factibles=len(solInicial)                                 # Número de unidades factibles

    while it <= maxIteraciones:
        print("Incial:", solInicial, "i:", i, "mejor global:", mejora_global, "costoActual:", costoInicial, "factibles:", factible)

        if factible[i] == 0:                                    # Si i tiene posibilidad de mejora buscamos con explorar_vecinos()
            mejora_local = maxsize
            mejor_local = ()
            for j in range(i+1, len(solInicial)+i):                 # Opt-2, revisamos las posibles combinaciones
                j = j % len(solInicial)                                 # Hacemos el modulo para que no se pase
                mejora = fact(i, j, solInicial, flujos, distancias)     # Miramos si mejora esta combinacion

                if mejor_global == (i,j) or mejor_global == (j,i):
                    continue
                if mem.tabu(i,j) and mejora >= mejora_global:           # SI es tabu y no mejora la puntuación global lo omitimos
                    continue

                if mejora < mejora_local:                               # SI este vecino mejora es el más pequeño actual:
                    mejor_local = (i, j)                                    # Guardamos el intercambio
                    mejora_local = mejora                                   # Guardamos la cantidad de mejora
                print("\tmejora: ", mejora, "cambio: ", (i,j), end="")
            
            if mejor_global + mejora_local < mejora_global:        # SI el mejor de los vecinos mejora el valor actual nos movemos a él
                dos_opt(solInicial, i, j)                               # Hacemos el intercambio
                
                if factible[j] == 1:                                    # SI hemos recuperado un no factible, ahora tenemos uno más
                    n_factibles += 1
                factible[i] = factible[j] = 0                           # Indicamos que por estas dos unidades se puede seguir buscando

                mejora_global += mejora_local                            # Actualizamos la mejora
                mejor_global = solInicial
                mem.push(i, j)                                          # La añadimos a la memoria tabú (si ya estaba se elimina y se vuelve a insertar automáticamente)

                print(" - MEJORA")
                it+=1
                sin_mejora = 0                                          # Hemos tenido una mejora
                mejor_peores = ()
                mejora_peores = maxsize
                logBusqueda.registraCambioBTabu(i,j,solInicial,coste_actual,mejora_global,it)
            else:                                                   # SI no se ha encontrado ninguna que mejora
                factible[i] = 1                                         # Vetamos esta unidad poniendo un 1
                n_factibles -= 1                                        # Reducimos el número de casillas factibles
                print(" - NO")

        if n_factibles == 0:                                    # SI no nos quedan más unidades factibles
            factible = [0] * len(solInicial)                        # Reiniciamos el vector de posiciones factibles
            n_factibles = len(solInicial)
            i, j = mejor_local                                      # Sacamos el intercambio del mejor de los vecinos
            mem.push(i, j)                                          # Como nos hemos movido, insertamos la solución
            dos_opt(solInicial, i, j)                               # Nos movemos a este vecino (aunque no mejore la global)
            sin_mejora+=1                                           # Aumentamos el número de iteraciones sin mejora
            it+=1
            logBusqueda.registraCambioBTabu(i,j,solInicial,coste_actual,mejora_global,it)

        i=(i+1)%len(solInicial)                                         # Pasamos al siguiente elemento
        # La mem a largo plazo debe devolver una permutación
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
            mejor_global = (nueva_perm[0], nueva_perm[1])
            it+=1
    fin=time.time()                                                 # Fin del contador del tiempo
    tiempo=fin-inicio                                               # Tiempo empleado en obtener el resultado
    return (mejor_global, tiempo)                                   # Permutación solución + tiempo de ejecución
