from clases.extractor import Extractor
from clases.logs import Log
from clases.poblacion import PoblacionEST
from clases.individuo import Individuo
from random import random
import time

def evolutivo_estacionario(tamPoblacion, prcAleatorio, prcMutacion, numPades, cruce, maxEvaluaciones, k, kBest, kWorst, data: Extractor, log: Log):

    Itime = time.time()
    # -- GENERACIÓN Y EVALUACIÓN --
    poblacion = PoblacionEST(tamPoblacion, prcAleatorio, k, data)
    log.registrarGeneracion(poblacion,1)

    ev = len(poblacion) # Contamos las evaluaciones al inicializar los individuos
    p_mutacion = prcMutacion
    t_cruce = cruce

    while(ev < maxEvaluaciones):
        # -- SELECCIÓN --
        padres = poblacion.seleccion(kBest) # Preparamos la población para su cruce

        # -- CRUCE --
        hijos = []
        n = len(padres)
        for i in range(0, n - (n%2), 2): # Vamos cogiendo de dos en dos
            # Los reproducimos para obtener a sus hijos
            h1, h2 = Individuo.cruce(padres[i], padres[i], t_cruce, data.flujos, data.distancias)
            hijos.append(h1)
            hijos.append(h2)
            # Anotamos dos evaluaciónes (una por cada hijo)
            ev+= 2

        if (ev == maxEvaluaciones):
            break
        
        # -- MUTACION --
        for i in range(len(hijos)):
            if random.randint(0, 100) < p_mutacion: # Si cae dentro lo mutamos, sino no hacemos nada
                i.mutar(data.flujos, data.distancias)
                # Anotamos una evaluación al individuo mutado
                ev+=1 
            
        if (ev == maxEvaluaciones):
            break   
        
        poblacion.reemplazo(kWorst, hijos) # Hacemos el reemplazo
        log.registrarGeneracion(poblacion,poblacion[0].getGeneracion)
    
    mejor = poblacion.getMejor()
    log.registrarSolucion((mejor, time.time() - Itime))