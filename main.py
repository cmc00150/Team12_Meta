import sys, random
from heuristicas.AlgGE02G12 import greedy
from heuristicas.AlgGA02G12 import greedy_aleatorizado
from heuristicas.AlgBL02G12 import busqueda_local_dlb
from heuristicas.AlgBT02G12 import busqueda_tabu
from modulos.prints import *
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
            case 'greedy':
                logGreedy=Log(algoritmo,archivoDatos)
                result = greedy(data.flujos, data.distancias, data.dimension)
                logGreedy.registrarSolucion(result, costo(result[0],data.flujos, data.distancias))
                logGreedy.generaLogs()

            case 'greedy_aleatorizado':
                if len(config.seed) == 0 or len(config.extra) == 0:
                    error(f'Para utilizar el algoritmo {algoritmo.upper()} debe incluir al menos una semilla y argumento extra (rango en el que aplicar el aleatorio, k)')
                    continue

                for k in config.extra[0]: # Bucle de ejecución dependiendo del número de k que haya en config
                    for semilla in config.seed: # Bucle de ejecución dependiendo del número de semillas que haya en config
                        logGreedyAleatorizado=Log(algoritmo,archivoDatos,semilla,k)
                        random.seed(semilla)  # Actualizo la semilla
                        result = greedy_aleatorizado(data.flujos, data.distancias, data.dimension, int(k))
                        logGreedyAleatorizado.registrarSolucion(result,costo(result[0],data.flujos,data.distancias))
                        logGreedyAleatorizado.generaLogs()

            case 'busqueda_local_dlb':
                if len(config.seed) == 0 or len(config.extra) < 2:
                    error(f'Para utilizar el algoritmo {algoritmo.upper()} debe incluir al menos una semilla y dos argumentos extra (rango en el que aplicar el aleatorio, k, número máximo de iteraciones)')
                    continue

                for k in config.extra[0]: # Bucle de ejecución dependiendo del número de k que haya en config
                    for semilla in config.seed: # Bucle de ejecución dependiendo del número de semillas que haya en config
                        for maxIteraciones in config.extra[1]:
                            logBusqueda = Log(algoritmo, archivoDatos, semilla, k,maxIteraciones)

                            random.seed(semilla)  # Actualizo la semilla
                            solInicial = greedy_aleatorizado(data.flujos, data.distancias, data.dimension, int(k))[0]
                            costoInicial = costo(solInicial,data.flujos,data.distancias)
                            logBusqueda.registrarSolucionInicial(solInicial,costoInicial)

                            result = busqueda_local_dlb(data.flujos, data.distancias, solInicial, costoInicial, int(maxIteraciones), logBusqueda)

                            logBusqueda.registrarSolucion(result, costo(result[0], data.flujos, data.distancias))
                            logBusqueda.generaLogs()
                            if(config.extra[5][0] == '1'): # Si generacionImagen = 1 en config, se genera un gráfico de la evolución del coste del algoritmo a lo largo de las iteraciones
                                logBusqueda.dibujarGrafica()
            
            case 'busqueda_tabu':
                if len(config.seed) == 0 or len(config.extra) < 5:
                    error(f'Para utilizar el algoritmo {algoritmo.upper()} debe incluir al menos una semilla y dos argumentos extra (rango en el que aplicar el aleatorio, k, número máximo de iteraciones, tenencia, oscilación, estancamiento)')
                    continue
                for k in config.extra[0]: # Bucle de ejecución dependiendo del número de k que haya en config
                    for semilla in config.seed: # Bucle de ejecución dependiendo del número de semillas que haya en config
                        for maxIteraciones in config.extra[1]:
                            for tenencia in config.extra[2]:
                                for oscilacion in config.extra[3]:
                                    for estancamiento in config.extra[4]:
                                        logTabu = Log(algoritmo, archivoDatos, semilla, k,maxIteraciones,tenencia,oscilacion,estancamiento)

                                        random.seed(semilla)  # Actualizo la semilla
                                        solInicial = greedy_aleatorizado(data.flujos, data.distancias, data.dimension, int(k))[0]
                                        costoInicial = costo(solInicial,data.flujos,data.distancias)
                                        logTabu.registrarSolucionInicial(solInicial,costoInicial)

                                        result = busqueda_tabu(data.flujos, data.distancias, solInicial, costoInicial, int(maxIteraciones), int(tenencia), float(oscilacion), float(estancamiento), logTabu)

                                        logTabu.registrarSolucion(result, costo(result[0], data.flujos, data.distancias))
                                        logTabu.generaLogs()
                                        if(config.extra[5][0] == '1'): # Si generacionImagen = 1 en config, se genera un gráfico de la evolución del coste del algoritmo a lo largo de las iteraciones
                                            logTabu.dibujarGrafica()
            case _:
                error('El algoritmo',algoritmo,'no ha sido programado, no se han obtenido resultados\n')

finPrograma()
# generaLogs('prueba',134,'datos01')

# Cuando tenemos dos o más tuplas con la misma distancia, deberiamos asignar todas las posibilidades a la permutación.
# Por ejemplo, si tenemos [(2, 19), (5, 19), (6,20)...], ahora la permutación pondrá primero el 2, luego el 5, etc. 
# Pero puede que si pusiéramos primero el 5 y luego el 2, de un coste menor. RESUMEN, cuando hay igualdad, probar distinas 
# combinaciones, actualizando la mejor puntuacion hasta ahora y quedandonos con la mejor.

# Tenemos que usar una semilla UNICA para cada experimento.
# Lo que variamos del greedy es coger los x (parametro externo en el archivo config, ALEAT) mejores valores y sacar uno al azar.
# Es lo mismo solo que hacer un pop(x), del numero que salga en vez de 0 y asi.

# Hacer la suma teniendo en cuenta que sea simetrica, hacemos que el primer for vaya de 0 a tam y el segundo for vaya de i a tam.

# INFORME:
    # Descripción del problema (1-2 páginas)
    # Análisis del algoritmo
    # Explicación de cómo se ha implementado (NO METER CAPTURAS DE PANTALLA, pero sí hay que poner código)
    # Incluir gráficas para comparar algoritmos, así como para comparar un solo algoritmo con el mejor resultado que nos dan

# Dont look bits
# Vector inicializado a 0. Se para la búsqueda cuando todo el vector está a 1
# Si la unidad 1 se compara con todas y ninguna mejora la situación, es porque la 1 es la mejor, así que le ponemos un 1 (ver código platea,)