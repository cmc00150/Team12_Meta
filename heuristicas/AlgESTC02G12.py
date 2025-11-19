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
    flujos = data.flujos
    distancias = data.distancias

    log.registrarPoblacionInicial(poblacion)

    while(ev < maxEvaluaciones and time.time() < TiempoFin):
        # -- SELECCIÓN --
        padres = poblacion.seleccion(kBest, numPadres) # Seleccionamos 2 padres para el cruce
        log.iniciarCiclo(padres)

        # -- CRUCE --
        n = len(padres)
        for i in range(0, n - (n%2), 2): # Vamos cogiendo de dos en dos

            # -- CRUCE --
            h1, h2 = Individuo.cruce(padres[i], padres[i+1], cruce, flujos, distancias)

            # -- MUTACIÓN INDIVIDUO 1 --
            if random.randint(0, 100) < prcMutacion:
                h1.mutar(flujos, distancias)
                log.registrarMutacion(i)
            # -- MUTACIÓN INDIVIDUO 2 --
            if random.randint(0, 100) < prcMutacion:
                h2.mutar(flujos, distancias)
                log.registrarMutacion(i + 1)
        
            # -- EVALUACIÓN --
            if not h1.getCosto: h1.setCosto(flujos, distancias); ev+=1 # Si no tiene costo es porque es un hijo, por lo que evaluamos
            if not h2.getCosto: h2.setCosto(flujos, distancias); ev+=1
        
            log.registrarCruce(h1, h2)

            # -- REEMPLAZO --
            poblacion.reemplazo(kWorst, h1) # Hacemos el reemplazo
            poblacion.reemplazo(kWorst, h2) # Hacemos el reemplazo
        
        log.finalizarCruceMutacion()
        log.registrarReemplazo(padres)
    
    log.registrarSolucion((poblacion.getMejor, time.time() - TiempoInicio), ev if ev>=maxEvaluaciones else None)