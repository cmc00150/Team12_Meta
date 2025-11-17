import sys, random
from heuristicas.AlgESTC02G12 import evolutivo_estacionario
from heuristicas.AlgGENC02G12 import evolutivo_generacional
from modulos.func_auxiliares import (error, finPrograma)
from clases.extractor import Extractor
from clases.configurador import (Configurador, supportedAlg)
from clases.logs import (LogEstacionario, LogGeneracional)
from itertools import product


if len(sys.argv) != 2: # Se comprueba que se ha introducido solo el archivo de configuración
    error("Seleccione un archivo para abrir")
    exit(1)

config = Configurador(sys.argv[1]) # Guardamos la información de configuración
config.mostrarInfo()

dataset = [Extractor(archivo) for archivo in config.data] # Obtenemos los datos de cada problema

combinaciones = product(
    config.alg,
    zip(config.data, dataset),
    config.seed,
    config.k,
    config.prcAleatorio,
    config.tampoblacion,
    config.numElites,
    config.kBest,
    config.prcCruce,
    config.cruce,
    config.prcMutacion,
    config.kWorst,
    config.maxEvaluaciones,
    config.maxSegundos,
    config.numPadres
)

for (alg, (ruta_data, data), seed, k, prcAleatorio, tamPoblacion, numElites, 
     kBest, prcCruce, cruce, prcMutacion, kWorst, maxEvaluaciones, maxSegundos, numPadres) in combinaciones:

    random.seed()

    match alg:
        case supportedAlg.GEN: # Usar el Enum para mayor seguridad y claridad
            logGen = LogGeneracional(ruta_data, alg, seed, k, prcAleatorio, tamPoblacion, numElites, kBest, prcCruce, cruce, prcMutacion, kWorst, maxEvaluaciones, maxSegundos)
            if(prcAleatorio <= 0):
                error('El porcentaje de generación de individuos mediante aleatorizado debe ser mayor a 0')
            evolutivo_generacional(numElites, tamPoblacion, prcAleatorio, prcCruce, prcMutacion, cruce, maxEvaluaciones, k, kBest, kWorst, data, logGen, maxSegundos)
            logGen.generaLogs()
        case supportedAlg.EST:
            logEst = LogEstacionario(ruta_data, alg, seed, k, prcAleatorio, tamPoblacion, kBest, prcCruce, cruce, prcMutacion, kWorst, maxEvaluaciones, maxSegundos)
            if(prcAleatorio <= 0):
                error('El porcentaje de generación de individuos mediante aleatorizado debe ser mayor a 0')
            evolutivo_estacionario(tamPoblacion, prcAleatorio, prcMutacion, numPadres, cruce, maxEvaluaciones, k, kBest, kWorst, data, logEst, maxSegundos)
            logEst.generaLogs()

finPrograma()