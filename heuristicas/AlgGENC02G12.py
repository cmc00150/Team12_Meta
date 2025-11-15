from clases.poblacion import (Poblacion, Extractor, Individuo)
from modulos.func_auxiliares import (fact, dos_opt)
from clases.logs import Log
import time
import random

# TODO Temporizador
def evolutivo_generacional(numElites, tamPoblacion, prcAleatorio, prcCruce, prcMutacion, cruce, maxEvaluaciones, k, kBest, kWorst, data: Extractor, log: Log):

    Itime = time.time()
    # -- GENERACIÓN Y EVALUACIÓN --
    poblacion = Poblacion(numElites, tamPoblacion, prcAleatorio, k, data)
    log.registrarGeneracion(poblacion,1)

    ev = len(poblacion) # Contamos las evaluaciones al inicializar los individuos
    p_cruce = prcCruce
    p_mutacion = prcMutacion
    t_cruce = cruce

    while(ev < maxEvaluaciones):
        # -- SELECCIÓN --
        pobl_tmp = poblacion.seleccion(kBest) # Preparamos la población para su cruce

        # -- CRUCE --
        n = len(pobl_tmp)
        for i in range(0, n - (n%2), 2): # Vamos cogiendo de dos en dos
            if random.randint(0, 100) < p_cruce: # Cae dentro de la probabilidad de cruce, los cruzamos
                # 1. Cogemos a los padres
                padre1 = pobl_tmp[i]
                padre2 = pobl_tmp[i+1] 
                # 2. Los reproducimos para obtener a sus hijos
                hijos = Individuo.cruce(padre1, padre2, t_cruce, data.flujos, data.distancias)
                # 3. Sustituimos a los padres a los hijos
                pobl_tmp[i] = hijos[0]
                pobl_tmp[i+1] = hijos[1]
                # 4. Anotamos dos evaluaciónes (una por cada hijo)
                ev+= 2

        if (ev == maxEvaluaciones):
            break
        
        # -- MUTACION --
        for i in pobl_tmp:
            if random.randint(0, 100) < p_mutacion: # Si cae dentro lo mutamos, sino no hacemos nada
                i.mutar(data.flujos, data.distancias)
                # Anotamos una evaluación al individuo mutado
                ev+=1 
            
        if (ev == maxEvaluaciones):
            break   
        
        poblacion.reemplazo(kWorst, pobl_tmp) # Hacemos el reemplazo
        log.registrarGeneracion(poblacion,poblacion[0].getGeneracion)
    
    mejor = poblacion.getMejor()
    log.registrarSolucion((mejor, time.time() - Itime))