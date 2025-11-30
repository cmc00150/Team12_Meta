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
    log.registrarGeneracion(poblacion,1, numGeneracion)

    # --- FUNCIÓN AUXILIAR PARA GESTIONAR EVALUACIONES ---
    def registrar_evaluacion():
        nonlocal ev # Permite modificar la variable 'ev' de la función padre
        ev += 1
        
        # 1. Chequeo de Tabú
        if ev % tabuData.evaluaciones == 0:
            poblacion.busquedaTabu(flujos, distancias, tabuData.iteracionesBL, tabuData.tenencia, log)
        
        # 2. Chequeo de Parada (devuelve True si hay que parar)
        return ev >= gendata.maxEvaluaciones or time.time() - TiempoInicio >= TiempoFin
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
            cruce = random.randint(0, 100) < gendata.prcCruce
            mutacion1 = random.randint(0, 100) < gendata.prcMutacion
            mutacion2 = random.randint(0, 100) < gendata.prcMutacion

            if cruce: # Cae dentro de la probabilidad de cruce, los cruzamos                
                h1, h2 = Individuo.cruce(idv1, idv2, gendata.cruce)
                log.registrarCruce(i, i+1)

                idv1 = pobl_tmp[i] = h1
                idv2 = pobl_tmp[i+1] = h2

            # -- MUTACIÓN INDIVIDUO 1 --
            if mutacion1:
                idv1.mutar(flujos, distancias) # Si no tiene costo (no cruzado) se evalua dentro.
                log.registrarMutacion(i)
            # -- MUTACIÓN INDIVIDUO 2 --
            if mutacion1:
                idv2.mutar(flujos, distancias)
                log.registrarMutacion(i+1)
        
            # -- EVALUACIÓN --
            if not idv2.getCosto: # Si no tiene costo es porque es un hijo, por lo que evaluamos
                pobl_tmp[i].setCosto(flujos, distancias)
            
            if not idv2.getCosto: 
                pobl_tmp[i+1].setCosto(flujos, distancias)

            if cruce or mutacion1:
                if registrar_evaluacion(): break # Si al registrar se ha pasado el máximo paramos
            
            if cruce or mutacion2:
                if registrar_evaluacion(): break          
        
        log.finalizarSeleccion()
        log.registrarReemplazo(pobl_tmp)
        poblacion.reemplazo(gendata.kWorst, pobl_tmp) # Hacemos el reemplazo

        numGeneracion += 1
        log.registrarGeneracion(poblacion,numGeneracion, ev)

    log.registrarSolucion((poblacion.getMejor, time.time() - TiempoInicio), ev if ev>=gendata.maxEvaluaciones else None)