import sys, random
from heuristicas.AlgMEMC02G12 import memetico_generacional, GenData, TabuData
from modulos.func_auxiliares import (error, finPrograma)
from clases.extractor import Extractor
from clases.configurador import (Configurador, supportedAlg)
from clases.logs import Log
from itertools import product


if len(sys.argv) != 2: # Se comprueba que se ha introducido solo el archivo de configuración
    error("Seleccione un archivo para abrir")
    exit(1)

config = Configurador(sys.argv[1]) # Guardamos la información de configuración
config.mostrarInfo()

dataset = [Extractor(archivo) for archivo in config.data] # Obtenemos los datos de cada problema

combinaciones = product(
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
    config.iteracionesBL,
    config.evaluaciones,
    config.tenencia
)

for ((ruta_data, data), seed, k, prcAleatorio, tamPoblacion, numElites, 
     kBest, prcCruce, cruce, prcMutacion, kWorst, maxEvaluaciones, maxSegundos, iteracionesBL, evaluaciones, tenencia) in combinaciones:

    random.seed(seed)
    log = Log(ruta_data, seed, k, prcAleatorio, tamPoblacion, numElites, kBest, prcCruce, cruce, prcMutacion, kWorst, maxEvaluaciones, maxSegundos)
    if(prcAleatorio <= 0):
        error('El porcentaje de generación de individuos mediante aleatorizado debe ser mayor a 0')

    genData = GenData(numElites, tamPoblacion, prcAleatorio, prcCruce, prcMutacion, cruce, maxEvaluaciones, k, kBest, kWorst)
    tabuData = TabuData(evaluaciones, iteracionesBL)
    memetico_generacional(genData, tabuData, data, log, maxSegundos)
    log.generaLogs()

finPrograma()