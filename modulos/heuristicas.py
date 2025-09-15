def greedy(flujos: list[list[int]], distancias: list[list[int]], candidatos: int) -> tuple[list[int], int]:
    v_flujos = [(i, sum(row)) for i, row in enumerate(flujos)]
    v_distancias = [(i, sum(row)) for i, row in enumerate(distancias)]

    sorted_flujos = sorted(v_flujos, key=lambda tuple: tuple[1], reverse=True)
    sorted_distancias = sorted(v_distancias, key=lambda tuple: tuple[1])

    print(sorted_flujos, sorted_distancias)

    permutacion = [0] * candidatos
    for index in range(1, candidatos+1):
        permutacion[sorted_flujos.pop(0)[0]] = sorted_distancias.pop(0)[0]

    costo = 0
    for i, target in enumerate(permutacion):
        aux = 0
        for j, it in enumerate(permutacion): 
            if i == j:
                continue
            #print(flujos[i][j], "(" ,i,j ,")*", distancias[target][it], "(", target,it, ")+ ", end="", flush=True)
            print(flujos[i][j], "*", distancias[target][it], "+ ", end="", flush=True)
            aux += flujos[i][j] * distancias[target][it]
        print("")
        costo += aux
    return (permutacion, costo)