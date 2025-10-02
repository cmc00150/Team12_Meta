def fact(i, j, perm, f, d):
    total = 0
    for k, elem in enumerate(perm):
        if k == i or k == j:
            pass
        total += f[i][k]*(d[perm[j]][elem] - d[perm[i]][elem])*2 + f[k][j]*(d[perm[i]][elem] - d[perm[j]][elem])*2
    return total



def DLB(sol: list, flujos, distancias):
    factible = [0 for u in list]
    mejor_actual = 0
    improve_flag 

    for i in range(len(sol)):
        if factible[i] == 0:
            improve_flag = False
            for j in range(i+1, len(sol)):
                efic = fact(i, j, sol, flujos, distancias)
                if efic > mejor_actual:
                    mejor_actual = efic
                    factible[i] = factible[j] = 0