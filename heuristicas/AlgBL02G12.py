import time # Para medir cuánto tarda cada función en ejecutarsey poder comparar rendimientos
import random
from sys import maxsize
from modulos.func_auxiliares import (dos_opt, fact)
from clases.logs import Log
from clases.memoriaTabu import MemTabu

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