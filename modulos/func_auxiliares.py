import sys
from clases.logs import Log

def fact(i, j, perm, f, d):
    total = 0
    for k, elem in enumerate(perm):
        if k == i or k == j:
            continue
        total += f[i][k]*(d[perm[j]][elem] - d[perm[i]][elem])*2 + f[j][k]*(d[perm[i]][elem] - d[perm[j]][elem])*2
    return total

def DLB(sol: list, costo, flujos, distancias, max_iteraciones, log: Log): # Encontrar 
    factible = [0 for e in sol]
    it = 0
    n_factibles = len(sol)
    i=0

    # Con iteraciones se refiere al numero de veces que se ejecuta el algoritmo dlb o la cantidad de i
    while it <= max_iteraciones and n_factibles > 0:
        #dlb
        menor_actual = 0 # Como solo buscamos numeros negativos (porque queremos minimizar), nos quedamos con los <0.
        if factible[i] == 0: # Si hay posibilidad de mejor entro
            improve = False # Lo ponemos a falso
            for j in range(i+1, len(sol)+i): # Opt-2, revisamos las posibles combinaciones
                j = j % len(sol) # Hacemos el modulo para que no se pase
                efic = fact(i, j, sol, flujos, distancias) # Miramos si mejora esta combinacion
                costoAux=costo # Hago una copia del costo hasta el momento para comparar sin perder su valor

                if efic + menor_actual < menor_actual: # Si el delta es negativo (mejora):
                    costoAux+=efic+menor_actual # Se guarda el nuevo costo para poder mostrarlo en logs
                    # Hacemos el intercambio
                    aux = sol[i]
                    sol[i] = sol[j]
                    sol[j] = aux
                    
                    if factible[j] == 1: # Si hemos recuperado un no factible, ahora tenemos uno más
                        n_factibles += 1
                    factible[i] = factible[j] = 0 # Indicamos que por estas dos unidades se puede seguir buscando

                    it += 1

                    log.registraCambioBLocal(i,j,sol,costoAux,it)

                    menor_actual = efic # Escogemos este vecino (guardamos las posiciones que se cambian)
                    improve = True # Indicamos que se ha encontrado
                    break  # Salir del bucle j una vez que encontramos una mejora

            costo=costoAux # Tras pasar por todas las opciones, actualizo el costo para quedarme con el mejor

            if not improve: # Si no se ha encontrado ninguna que mejora, vetamos esta posición poniendo un 1
                factible[i] = 1
                n_factibles -= 1
                if n_factibles == 0:
                    break

        i=(i+1)%len(sol)

        if(it==max_iteraciones):
            break
        
