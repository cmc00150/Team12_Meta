import sys, random
from heuristicas.AlgESTC02G12 import evolutivo_estacionario
from heuristicas.AlgGENC02G12 import evolutivo_generacional
from modulos.func_auxiliares import (error, finPrograma)
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

for (algoritmo, (archivoDatos, data), semilla, k, prcAleatorio, tamPoblacion, numElites,kBest, prcCruce, tipoCruce, prcMutacion, kWorst, maxEvaluaciones, 
    maxSegundos, extra) in product (config.alg, zip(config.data, dataset),config.seed,config.k,config.prcAleatorio,config.tampoblacion,config.numElites 
    if config.numElites else [None],config.kBest,config.prcCruce,config.cruce,config.prcMutacion,config.kWorst, config.maxEvaluaciones,config.maxSegundos,
    config.extra if config.extra else [None]):

    random.seed(semilla)

    match algoritmo:
        case 'evolutivo_generacional':
            logEvolutivoGen = Log(algoritmo,archivoDatos,semilla,k,prcAleatorio,tamPoblacion,kBest,prcCruce,tipoCruce,prcMutacion,kWorst,maxEvaluaciones,maxSegundos,numElites)
            if(prcAleatorio <= 0):
                error('El porcentaje de generación de individuos mediante aleatorizado debe ser mayor a 0')
            evolutivo_generacional(numElites, tamPoblacion, prcAleatorio, prcCruce, prcMutacion, tipoCruce, maxEvaluaciones, k, kBest, kWorst, data, logEvolutivoGen)
            logEvolutivoGen.generaLogs()

finPrograma()