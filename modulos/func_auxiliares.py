from dataclasses import dataclass
from clases.logs import Log
    
@dataclass
class Modificables:
    improve: bool
    n_factibles: int
    menor_actual: int
    it: int
    costo: int

def costo(permutacion, flujos: list[list[int]], distancias: list[list[int]]): # Función de evaluación de los diferentes algoritmos
    costo = 0
    for i, main in enumerate(permutacion):
        aux = 0
        for j in range(i+1, len(permutacion)): # Para no repetir valores, vamos de i hasta el final
            it = permutacion[j]
            aux += flujos[i][j] * distancias[main][it] * 2 # Sabiendo que es simetrica
        costo += aux
    return costo

def fact(i, j, perm, f, d):
    total = 0
    for k, elem in enumerate(perm):
        if k == i or k == j:
            continue
        total += f[i][k]*(d[perm[j]][elem] - d[perm[i]][elem])*2 + f[j][k]*(d[perm[i]][elem] - d[perm[j]][elem])*2
    return total

def dos_opt (perm, i, j):
    aux = perm[i]
    perm[i] = perm[j]
    perm[j] = aux

def dlb_primer_mejor(sol: list[int], factible: list[int], i, modificables: Modificables, flujos, distancias, log: Log):    
    for j in range(i+1, len(sol)+i): # Opt-2, revisamos las posibles combinaciones
        j = j % len(sol) # Hacemos el modulo para que no se pase
        mejora = fact(i, j, sol, flujos, distancias) # Miramos si mejora esta combinacion

        if mejora < modificables.menor_actual: # Si el delta es negativo (mejora):
            modificables.menor_actual = mejora # Escogemos este vecino
            modificables.costo+=modificables.menor_actual # Se guarda el nuevo costo para poder mostrarlo en logs

            dos_opt(sol, i, j) # Hacemos el intercambio
            
            if factible[j] == 1: # Si hemos recuperado un no factible, ahora tenemos uno más
                modificables.n_factibles += 1
            factible[i] = factible[j] = 0 # Indicamos que por estas dos unidades se puede seguir buscando

            modificables.it+=1
            log.registraCambioBLocal(i, j, sol, modificables.costo, modificables.it)
            modificables.improve = True
            return # Salir del dlb una vez que encontramos una mejora
        
def dlb_tabu(sol: list[int], factible: list[int], i, modificables: Modificables, flujos, distancias, log: Log):    
    for j in range(i+1, len(sol)+i): # Opt-2, revisamos las posibles combinaciones
        j = j % len(sol) # Hacemos el modulo para que no se pase
        mejora = fact(i, j, sol, flujos, distancias) # Miramos si mejora esta combinacion

        if mejora < modificables.menor_actual: # Si el delta es negativo (mejora):
            modificables.menor_actual = mejora # Escogemos este vecino
            modificables.costo+=modificables.menor_actual # Se guarda el nuevo costo para poder mostrarlo en logs

            dos_opt(sol, i, j) # Hacemos el intercambio
            
            if factible[j] == 1: # Si hemos recuperado un no factible, ahora tenemos uno más
                modificables.n_factibles += 1
            factible[i] = factible[j] = 0 # Indicamos que por estas dos unidades se puede seguir buscando

            modificables.it+=1
            log.registraCambioBLocal(i, j, sol, modificables.costo, modificables.it)
            modificables.improve = True
            return # Salir del dlb una vez que encontramos una mejora        