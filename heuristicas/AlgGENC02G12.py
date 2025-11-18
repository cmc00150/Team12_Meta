from copy import deepcopy
from clases.poblacion import (PoblacionGEN, Extractor, Individuo)
from clases.logs import LogGeneracional
from modulos.func_auxiliares import costo ,fact

import time
import random

def evolutivo_generacional(numElites, tamPoblacion, prcAleatorio, prcCruce, prcMutacion, cruce, maxEvaluaciones, k, kBest, kWorst, data: Extractor, log: LogGeneracional, maxSegundos: int):

    TiempoInicio = time.time()
    TiempoFin = time.time() + maxSegundos
    
    # -- GENERACIÓN Y EVALUACIÓN --
    poblacion = PoblacionGEN(numElites, tamPoblacion, prcAleatorio, k, data)
    numGeneracion = 1
    ev = len(poblacion) # Contamos las evaluaciones al inicializar los individuos
    # Cacheamos las estructuras para mas eficiencia
    flujos = data.flujos
    distancias = data.distancias
    log.registrarGeneracion(poblacion,1, numGeneracion)

    while(ev < maxEvaluaciones and time.time() < TiempoFin):
        # -- SELECCIÓN --
        pobl_tmp = poblacion.seleccion(kBest)
        log.iniciarCiclo(pobl_tmp)  # ← Iniciar ciclo

        n = len(pobl_tmp)
        for i in range(0, n - (n%2), 2): # Vamos cogiendo de dos en dos
            idv1 = pobl_tmp[i]
            idv2 = pobl_tmp[i+1]

            # -- CRUCE --
            if random.randint(0, 100) < prcCruce: # Cae dentro de la probabilidad de cruce, los cruzamos                
                h1, h2 = Individuo.cruce(idv1, idv2, cruce, flujos, distancias)
                log.registrarCruce(i, i+1)

                idv1 = pobl_tmp[i] = h1
                idv2 = pobl_tmp[i+1] = h2

            # -- MUTACIÓN INDIVIDUO 1 --
            if random.randint(0, 100) < prcMutacion:
                if idv1.getCosto: ev+=1 # Si tiene coste es porque no se ha cruzado, contabiliza el fact() de dentro de mutar()
                idv1.mutar(flujos, distancias)
                log.registrarMutacion(i)
            # -- MUTACIÓN INDIVIDUO 2 --
            if random.randint(0, 100) < prcMutacion:
                if idv2.getCosto: ev+=1 # Si tiene coste es porque no se ha cruzado
                idv2.mutar(flujos, distancias)
                log.registrarMutacion(i+1)
        
            # -- EVALUACIÓN --
            if not idv1.getCosto: pobl_tmp[i].setCosto(flujos, distancias); ev+=1 # Si no tiene costo es porque es un hijo, por lo que evaluamos
            if not idv2.getCosto: pobl_tmp[i+1].setCosto(flujos, distancias); ev+=1
        
        log.finalizarSeleccion()
        log.registrarReemplazo(pobl_tmp)
        poblacion.reemplazo(kWorst, pobl_tmp) # Hacemos el reemplazo

        numGeneracion += 1
        log.registrarGeneracion(poblacion,numGeneracion, ev)

    log.registrarSolucion((poblacion.getMejor, time.time() - TiempoInicio), ev if ev>=maxEvaluaciones else None)