from dataclasses import dataclass
from sys import maxsize
    
@dataclass
class Modificables:
    n_factibles: int
    it: int

@dataclass
class ReturnDLB:
    mejor_encontrado: tuple[int, int]
    mejora: int

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