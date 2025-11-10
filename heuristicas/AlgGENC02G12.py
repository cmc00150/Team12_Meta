from clases.poblacion import (Poblacion, Configurador, Extractor, Individuo)
from modulos.func_auxiliares import (fact, dos_opt)
import random
from multiprocessing import Process

# TODO Temporizador
def evolutivo_generacional(config: Configurador, data: Extractor):
    poblacion = Poblacion(config, data)

    ev = 0
    p_cruce = config.prcCruce
    p_mutacion = config.prcMutacion
    t_cruce = config.cruce

    while(ev < config.maxEvaluaciones):
        # -- SELECCIÓN --
        poblacion.seleccion(config.kBest) # Preparamos la población para su cruce

        # -- CRUCE --
        n = len(poblacion)
        for i in range(0, n - (n%2), 2): # Vamos cogiendo de dos en dos
            if random.random() < p_cruce: # Cae dentro de la probabilidad de cruce, los cruzamos
                # 1. Cogemos a los padres
                padre1 = poblacion[i]
                padre2 = poblacion[i+1] 
                # 2. Los reproducimos para obtener a sus hijos
                hijos = Individuo.cruce(padre1, padre2)
                # 3. Sustituimos a los padres a los hijos
                poblacion[i] = hijos[0]
                poblacion[i+1] = hijos[1]
                # 4. Vemos si es mejor que alguno de los élites
                poblacion.considerarElite(i)
                poblacion.considerarElite(i+1)
                # 5. Anotamos dos evaluaciónes (una por cada hijo)
                ev+= 2
        
        if (ev == config.maxEvaluaciones):
            break
        
        # -- MUTACION --
        for i in range(n):
            if random.random() < p_mutacion: # Si cae dentro lo mutamos, sino no hacemos nada
                # 1. Cogemos la permutación
                perm = poblacion[i].getPermutacion()       
                # 2. Selecciono los genes a mutar
                posiciones = random.choices(range(len(perm)), k=2) # Cojo dos posiciones de esta permutación
                # 3. Le hago la mutación
                nuevaPerm = dos_opt(perm, posiciones[0], posiciones[1]) # Los intercambio
                # 4. Calculo el costo (parcialmente)
                variacion = fact(posiciones[0], posiciones[1], perm, data.flujos, data.data.distancias)
                # 5. Creo el nuevo individuo
                poblacion[i] = Individuo(nuevaPerm, poblacion[i].getCosto() + variacion, poblacion[i].getGeneracion()+1)
                # 6. Vemos si puede añadirse como élite
                poblacion.considerarElite(i)
                # 7. Anotamos una evaluación al individuo mutado
                ev+=1 
            
        if (ev == config.maxEvaluaciones):
            break

    return poblacion.getMejor()
