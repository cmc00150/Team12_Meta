import sys, random
from heuristicas.AlgESTC02G12 import evolutivo_estacionario
from heuristicas.AlgGENC02G12 import evolutivo_generacional
from modulos.func_auxiliares import (error, finPrograma)
from clases.extractor import Extractor
from clases.configurador import Configurador
from clases.logs import Log

if len(sys.argv) != 2: # Se comprueba que se ha introducido solo el archivo de configuración
    error("Seleccione un archivo para abrir")
    exit(1)

config = Configurador(sys.argv[1]) # Guardamos la información de configuración
config.mostrarInfo()

dataset = [Extractor(archivo) for archivo in config.data] # Obtenemos los datos de cada problema

for algoritmo in config.alg: # Obtengo los diferentes algoritmos del archivo de configuración
    for archivoDatos, data in zip(config.data, dataset):
        match algoritmo:
            case 'evolutivo_generacional':
                evolutivo_generacional()
            case 'evolutivo_estacional':
                evolutivo_estacionario()
            case _:
                error('El algoritmo',algoritmo,'no ha sido programado, no se han obtenido resultados\n')

    finPrograma()