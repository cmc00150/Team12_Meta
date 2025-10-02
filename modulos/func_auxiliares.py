def fact(i, j, perm, f, d):
    total = 0
    for k, elem in enumerate(perm):
        if k == i or k == j:
            pass
        total += f[i][k]*(d[perm[j]][elem] - d[perm[i]][elem])*2 + f[k][j]*(d[perm[i]][elem] - d[perm[j]][elem])*2
    return total



def DBL(sol: list, factible:list, flujos, distancias): # Encontrar 
    mejor_actual = (0, 0, 0)
    improve_flag 

    for i in range(len(sol)): # Miramos cada elemento
        if factible[i] == 0: # Si hay posibilidad de mejor entro
            improve_flag = False # Lo ponemos a falso
            for j in range(i+1, len(sol)): # Opt-2, revisamos las posibles convinaciones
                efic = fact(i, j, sol, flujos, distancias) # Miramos si mejora esta convinacion
                if efic > mejor_actual: # Si mejora:
                    mejor_actual = (i, j, efic) # Escogemos este vecino (guardamos las posiciones que se cambian)
                    factible[i] = factible[j] = 0 # Indicamos que por estas dos unidades se puede seguir buscando
                    improve_flag = True # Indicamos que se ha encontrado
            if not improve_flag: # Si no se ha encontrado ninguna que mejore, vetamos esta posición poniendo un 1
                factible[i] = 1
            
    aux = sol(mejor_actual[0])
    sol(mejor_actual[0]) = sol(mejor_actual[1])
    sol(mejor_actual[1]) = aux