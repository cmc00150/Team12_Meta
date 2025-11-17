from clases.extractor import Extractor
from clases.logs import LogEstacionario
from clases.poblacion import PoblacionEST
from clases.individuo import Individuo
from copy import deepcopy
import random
import time

def evolutivo_estacionario(tamPoblacion, prcAleatorio, prcMutacion, numPadres, cruce, maxEvaluaciones, k, kBest, kWorst, data: Extractor, log: LogEstacionario, maxSegundos: int):

    TiempoInicio = time.time()
    TiempoFin = time.time() + maxSegundos
    # -- GENERACIÓN Y EVALUACIÓN --
    poblacion = PoblacionEST(tamPoblacion, prcAleatorio, k, data)

    ev = len(poblacion) # Contamos las evaluaciones al inicializar los individuos
    mejorGlobal = deepcopy(poblacion[0])

    log.registrarPoblacion(poblacion)

    while(ev < maxEvaluaciones and time.time() < TiempoFin):
        # -- SELECCIÓN --
        padres = poblacion.seleccion(kBest, numPadres) # Seleccionamos 2 padres para el cruce
        log.registrarSeleccion(padres)
        mejorpob = poblacion.getMejor()
        if mejorpob.getCosto < mejorGlobal.getCosto:
            mejorGlobal = deepcopy(mejorpob)

        # -- CRUCE --
        hijos: list[Individuo] = []
        n = len(padres)
        for i in range(0, n - (n%2), 2): # Vamos cogiendo de dos en dos
            # Los reproducimos para obtener a sus hijos
            h1, h2 = Individuo.cruce(padres[i], padres[i+1], cruce, data.flujos, data.distancias)
            hijos.append(h1)
            hijos.append(h2)
            # Anotamos dos evaluaciónes (una por cada hijo)
            ev+= 2
            log.registrarCruce(padres[i], padres[i+1], hijos)
            if ev >= maxEvaluaciones or time.time() >= TiempoFin: break

        if ev >= maxEvaluaciones or time.time() >= TiempoFin: break
        
        # -- MUTACION --
        for i in hijos:
            if random.randint(0, 100) < prcMutacion: # Si cae dentro lo mutamos, sino no hacemos nada
                costoAnterior = i.getCosto
                posiciones = i.mutar(data.flujos, data.distancias)
                log.registrarMutacion(i, (posiciones[0]+1,posiciones[1]+1), costoAnterior)
                # Anotamos una evaluación al individuo mutado
                ev+=1 
            
            if ev >= maxEvaluaciones or time.time() >= TiempoFin: break

        if ev >= maxEvaluaciones or time.time() >= TiempoFin: break
        
        poblacion.reemplazo(kWorst, hijos) # Hacemos el reemplazo
        log.registrarReemplazo(hijos)
    
    log.registrarPoblacion(poblacion)
    
    if ev>=maxEvaluaciones:
        log.registrarSolucion((mejorGlobal, time.time() - TiempoInicio), ev)
    else:
        log.registrarSolucion((mejorGlobal, time.time() - TiempoInicio))