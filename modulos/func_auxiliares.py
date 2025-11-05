import random
from clases.individuo import Individuo

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
        total += (f[i][k]*(d[perm[j]][elem] - d[perm[i]][elem])*2) + (f[j][k]*(d[perm[i]][elem] - d[perm[j]][elem])*2)
    return total

def dos_opt (perm, i, j):
    aux = perm[i]
    perm[i] = perm[j]
    perm[j] = aux

def error(mensaje:str):
      print('[!] Error -',mensaje)
      exit(1)

def finPrograma():
    print(' o'*50,
        '\n',
        f" FIN DEL PROGRAMA, CONSULTE LOS LOGS PARA OBTENER LOS RESULTADOS ".center(100, " "),
        '\n',
        ' o'*50)
    
def greedy_aleatorizado(flujos: list[list[int]], distancias: list[list[int]], candidatos: int, k: int) -> Individuo:
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

    costoPermutacion=costo(permutacion,flujos,distancias)
    ind=Individuo(permutacion,costoPermutacion,1)
    return ind # Individuo generado

def aleatorio(flujos: list[list[int]], distancias: list[list[int]], tam: int) -> Individuo:
    permutacion = list(range(tam)) # Crea una lista con el rango proporcionado
    random.shuffle(permutacion) # Barajamos la permutación, de forma que nos aseguramos de que se cumple el factor aleatorio y no se repiten números
    costoPermutacion=costo(permutacion, flujos, distancias)
    ind=Individuo(permutacion,costoPermutacion,1)
    return ind