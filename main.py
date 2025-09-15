import sys 
from modulos.heuristicas import *
from clases.extractor import Extractor
from clases.configurador import Configurador

if len(sys.argv) < 2 or len(sys.argv) > 3: 
    print("Seleccione un archivo para abrir")
    exit(1)

config = Configurador(sys.argv[1])
dataset = [Extractor(archivo) for archivo in config.data]
result = [greedy(data.flujos, data.distancias, data.dimension) for data in dataset]

for r in result:
    print([elem+1 for elem in r[0] ], "Costo: ", r[1])

# Cuando tenemos dos o más tuplas con la misma distancia, deberiamos asignar todas las posibilidades a la permutación.
# Por ejemplo, si tenemos [(2, 19), (5, 19), (6,20)...], ahora la permutación pondrá primero el 2, luego el 5, etc. 
# Pero puede que si pusiéramos primero el 5 y luego el 2, de un coste menor. RESUMEN, cuando hay igualdad, probar distinas 
# combinaciones, actualizando la mejor puntuacion hasta ahora y quedandonos con la mejor.

# Tenemos que usar una semilla UNICA para cada experimento.
# Lo que variamos del greedy es coger los x (parametro externo en el archivo config, ALEAT) mejores valores y sacar uno al azar.
# Es lo mismo solo que hacer un pop(x), del numero que salga en vez de 0 y asi.

# Hacer la suma teniendo en cuenta que sea simetrica, hacemos que el primer for vaya de 0 a tam y el segundo for vaya de i a tam.