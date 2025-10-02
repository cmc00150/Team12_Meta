def fact(i, j, perm, f, d):
    total = 0
    for k, elem in enumerate(perm):
        if k == i or k == j:
            pass
        total += f[i][k]*(d[perm[j]][elem] - d[perm[i]][elem])*2 + f[k][j]*(d[perm[i]][elem] - d[perm[j]][elem])*2
    return total

def DLB(sol: list, flujos, distancias, max_iteraciones): # Encontrar 
    mejor_actual = 0
    factible = [0 for e in sol]
    it = 0
    n_factibles = len(sol)

    while it <= max_iteraciones and n_factibles > 0:
        for i in range(len(sol)): # Miramos cada elemento
            if factible[i] == 0: # Si hay posibilidad de mejor entro
                improve = False # Lo ponemos a falso
                for j in range(i+1, len(sol)+i+1): # Opt-2, revisamos las posibles convinaciones
                    j%= len(sol) # Hacemos el modulo para que no se pase
                    efic = fact(i, j, sol, flujos, distancias) # Miramos si mejora esta convinacion
                    if efic > mejor_actual: # Si mejora:
                        # Hacemos el intercambio
                        aux = sol[i]
                        sol[i] = sol[j]
                        sol[j] = aux

                        it += 1
                        mejor_actual = efic # Escogemos este vecino (guardamos las posiciones que se cambian)
                        if factible[j] == 1: # Si hemos recuperado un no factible, ahora tenemos uno más
                            n_factibles += 1
                        factible[i] = factible[j] = 0 # Indicamos que por estas dos unidades se puede seguir buscando
                        improve = True # Indicamos que se ha encontrado
                if not improve: # Si no se ha encontrado ninguna que mejora, vetamos esta posición poniendo un 1
                    factible[i] = 1
                    n_factibles -= 1