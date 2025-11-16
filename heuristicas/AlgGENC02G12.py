from clases.poblacion import (PoblacionGEN, Extractor, Individuo)
from clases.logs import Log
import time
import random

# TODO Temporizador
def evolutivo_generacional(numElites, tamPoblacion, prcAleatorio, prcCruce, prcMutacion, cruce, maxEvaluaciones, k, kBest, kWorst, data: Extractor, log: Log, maxSegundos: int):

    TiempoInicio = time.time()
    TiempoFin = time.time() + maxSegundos
    # -- GENERACIÓN Y EVALUACIÓN --
    poblacion = PoblacionGEN(numElites, tamPoblacion, prcAleatorio, k, data)
    log.registrarGeneracion(poblacion,1)
    numGeneracion = 1

    ev = len(poblacion) # Contamos las evaluaciones al inicializar los individuos
    p_cruce = prcCruce
    p_mutacion = prcMutacion
    t_cruce = cruce
    mejorGlobal = Individuo()
    mejorGlobal.copiarIndividuo(poblacion[0])

    while(ev < maxEvaluaciones and time.time() < TiempoFin):
        # -- SELECCIÓN --
        pobl_tmp = poblacion.seleccion(kBest) # Preparamos la población para su cruce
        mejorelitepob = poblacion.getElites[0][0]
        if mejorelitepob.getCosto < mejorGlobal.getCosto:
            mejorGlobal.copiarIndividuo(mejorelitepob)

        # -- CRUCE --
        n = len(pobl_tmp)
        for i in range(0, n - (n%2), 2): # Vamos cogiendo de dos en dos
            if random.randint(0, 100) < p_cruce: # Cae dentro de la probabilidad de cruce, los cruzamos
                # 1. Cogemos a los padres
                padre1 = pobl_tmp[i]
                padre2 = pobl_tmp[i+1] 
                # 2. Los reproducimos para obtener a sus hijos
                hijos = Individuo.cruce(padre1, padre2, t_cruce, data.flujos, data.distancias)
                log.registrarCruce(padre1,padre2,hijos)
                # 3. Sustituimos a los padres a los hijos
                pobl_tmp[i] = hijos[0]
                pobl_tmp[i+1] = hijos[1]
                # 4. Anotamos dos evaluaciónes (una por cada hijo)
                ev+= 2

            if ev >= maxEvaluaciones or time.time() >= TiempoFin: # Sale del for
                break

        if ev >= maxEvaluaciones or time.time() >= TiempoFin: # Sale del while
                break
        
        # -- MUTACION --
        for i in pobl_tmp:
            if random.randint(0, 100) < p_mutacion: # Si cae dentro lo mutamos, sino no hacemos nada
                posiciones=i.mutar(data.flujos, data.distancias)
                log.registrarMutacion(posiciones[0]+1,posiciones[1]+1,i)
                # Anotamos una evaluación al individuo mutado
                ev+=1 
            
            if ev >= maxEvaluaciones or time.time() >= TiempoFin: # Sale del for
                break   

        if ev >= maxEvaluaciones or time.time() >= TiempoFin: # Sale del while
                break
        
        poblacion.reemplazo(kWorst, pobl_tmp) # Hacemos el reemplazo
        log.registrarReemplazo();

        numGeneracion += 1
        log.registrarGeneracion(poblacion,numGeneracion)

    if ev>=maxEvaluaciones:
        log.registrarSolucion((mejorGlobal, time.time() - TiempoInicio), ev)
    else:
        log.registrarSolucion((mejorGlobal, time.time() - TiempoInicio))