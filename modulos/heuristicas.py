def greedy(flujos: list[list[int]], distancias: list[list[int]], candidatos: int) -> tuple[list[int], int]:
    # Obtenemos los vectores
    v_flujos = [(i, sum(row)) for i, row in enumerate(flujos)]
    v_distancias = [(i, sum(row)) for i, row in enumerate(distancias)]

    # Los ordenamos
    sorted_flujos = sorted(v_flujos, key=lambda tuple: tuple[1], reverse=True) # Mayor a menor
    sorted_distancias = sorted(v_distancias, key=lambda tuple: tuple[1]) # Menor a mayor

    print(sorted_flujos, sorted_distancias)

    permutacion = [0] * candidatos
    for _ in range(candidatos):
        permutacion[sorted_flujos.pop(0)[0]] = sorted_distancias.pop(0)[0]

    costo = 0
    for i, main in enumerate(permutacion):
        aux = 0
        for j, it in range(i+1, len(permutacion)):
            #print(flujos[i][j], "(" ,i,j ,")*", distancias[target][it], "(", target,it, ")+ ", end="", flush=True)
            it = permutacion[j]
            print(flujos[i][j], "*", distancias[main][it], "+ ", end="", flush=True)
            aux += flujos[i][j] * distancias[main][it]
        print("")
        costo += aux
    return (permutacion, costo)