from clases.poblacion import (Poblacion, Extractor, Individuo)
from clases.logs import Log
from dataclasses import dataclass
import time
import random

@dataclass
class GenData:
    numElites: int
    tamPoblacion: int
    prcAleatorio: int
    prcCruce: int
    prcMutacion: int
    cruce: str
    maxEvaluaciones: int
    k: int
    kBest: int
    kWorst: int

@dataclass
class TabuData:
    evaluaciones: int
    iteracionesBL: int
    tenencia: int

def memetico_generacional(gendata: GenData, tabuData: TabuData,data: Extractor, log: Log, maxSegundos: int):

    TiempoInicio = time.time()
    TiempoFin = TiempoInicio + maxSegundos
    
    # -- GENERACIÓN Y EVALUACIÓN --
    poblacion = Poblacion(gendata.tamPoblacion, gendata.prcAleatorio, gendata.k, gendata.numElites, data)
    numGeneracion = 1
    ev = len(poblacion) # Contamos las evaluaciones al inicializar los individuos
    # Cacheamos las estructuras para mas eficiencia
    flujos = data.flujos
    distancias = data.distancias
    log.registrarPoblacionInicial(poblacion)
    log.registrarGeneracion(poblacion,1, ev)

    # --- FUNCIÓN AUXILIAR PARA GESTIONAR EVALUACIONES ---
    def registrar_evaluacion():
        nonlocal ev # Permite modificar la variable 'ev' de la función padre
        ev += 1
        
        # 1. Chequeo de Tabú
        #if ev % tabuData.evaluaciones == 0:
         #   poblacion.busquedaTabu(flujos, distancias, tabuData.iteracionesBL, tabuData.tenencia, log)
        
        # 2. Chequeo de Parada (devuelve True si hay que parar)
        return ev >= gendata.maxEvaluaciones or time.time() >= TiempoFin
    # ----------------------------------------------------

    while(ev < gendata.maxEvaluaciones and time.time() < TiempoFin):
        # -- SELECCIÓN --
        pobl_tmp = poblacion.seleccion(gendata.kBest)
        log.iniciarCiclo(pobl_tmp)  # ← Iniciar ciclo

        n = len(pobl_tmp)
        for i in range(0, n - (n%2), 2): # Vamos cogiendo de dos en dos
            idv1 = pobl_tmp[i]
            idv2 = pobl_tmp[i+1]

            # -- CRUCE --
            cruzar = random.randint(0, 100) < gendata.prcCruce

            if cruzar: # Cae dentro de la probabilidad de cruce, los cruzamos                
                h1, h2 = Individuo.cruce(idv1, idv2, gendata.cruce)
                log.registrarCruce(i, i+1)

                idv1 = pobl_tmp[i] = h1
                idv2 = pobl_tmp[i+1] = h2

            # -- MUTACIÓN INDIVIDUO 1 --
            if random.randint(0, 100) < gendata.prcMutacion:
                idv1.mutar(flujos, distancias) # Si tiene costo (no se ha cruzado) se evalua dentro.
                if not cruzar: # Como se ha evaluado en mutar sumamos
                    if registrar_evaluacion(): break # Si al registrar se ha pasado el máximo paramos
                log.registrarMutacion(i)
            # -- MUTACIÓN INDIVIDUO 2 --
            if random.randint(0, 100) < gendata.prcMutacion:
                idv2.mutar(flujos, distancias)
                if not cruzar:
                    if registrar_evaluacion(): break
                log.registrarMutacion(i+1)
        
            # -- EVALUACIÓN --
            if cruzar: # Si se ha cruzado, entonces no tiene costo y no se ha evaluado en mutar
                pobl_tmp[i].setCosto(flujos, distancias)
                if registrar_evaluacion(): break
            
            if cruzar: 
                pobl_tmp[i+1].setCosto(flujos, distancias)
                if registrar_evaluacion(): break          
        
        log.finalizarSeleccion()
        log.registrarReemplazo(pobl_tmp)
        poblacion.reemplazo(gendata.kWorst, pobl_tmp) # Hacemos el reemplazo

        numGeneracion += 1
        log.registrarGeneracion(poblacion,numGeneracion, ev)

    log.registrarSolucion((poblacion.getMejor, time.time() - TiempoInicio), ev if ev>=gendata.maxEvaluaciones else None)