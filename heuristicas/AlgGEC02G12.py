import time # Para medir cuánto tarda cada función en ejecutarsey poder comparar rendimientos

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