import sys, random
from heuristicas.AlgESTC02G12 import evolutivo_estacionario
from heuristicas.AlgGENC02G12 import evolutivo_generacional
from modulos.func_auxiliares import (error, finPrograma, greedy_aleatorizado, aleatorio)
from clases.extractor import Extractor
from clases.configurador import Configurador
from clases.logs import Log
from clases.poblacion import Poblacion
from itertools import product # Para no tener que estar anidando los bucles


if len(sys.argv) != 2: # Se comprueba que se ha introducido solo el archivo de configuración
    error("Seleccione un archivo para abrir")
    exit(1)

config = Configurador(sys.argv[1]) # Guardamos la información de configuración
config.mostrarInfo()

dataset = [Extractor(archivo) for archivo in config.data] # Obtenemos los datos de cada problema

for (algoritmo, (archivoDatos, data), semilla, k, prc_greedyAleat, tamPoblacion, numElites,kBest, prcCruce, tipoCruce, prcMutacion, kWorst, maxEvaluaciones, 
    maxSegundos, extra) in product (config.alg, zip(config.data, dataset),config.seed,config.k,config.prcGreedyAleat,config.tampoblacion,config.numElites 
    if config.numElites else [None],config.kBest,config.prcCruce,config.cruce,config.prcMutacion,config.kWorst, config.maxEvaluaciones,config.maxSegundos,
    config.extra if config.extra else [None]):

    random.seed(semilla)


    match algoritmo:
        case 'evolutivo_generacional':
            logEvolutivoGen = Log(algoritmo,archivoDatos,semilla,k,prc_greedyAleat,tamPoblacion,kBest,prcCruce,tipoCruce,prcMutacion,kWorst,maxEvaluaciones,maxSegundos,numElites)
            poblacionInicial = Poblacion(tamPoblacion, numElites)
            if(prc_greedyAleat <= 0):
                error('El porcentaje de generación de individuos mediante greedy aleatorizado debe ser mayor a 0')
            poblacionInicial.generarPoblacionInicial(k,prc_greedyAleat,data.flujos,data.distancias,data.dimension)
            logEvolutivoGen.registrarGeneracion(poblacionInicial,1) 
            logEvolutivoGen.generaLogs()             

finPrograma()