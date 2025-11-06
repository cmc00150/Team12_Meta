import os
from modulos.func_auxiliares import error

def limpiar_terminal(): # Limpia la terminal en cada ejecución
    os.system('cls' if os.name == 'nt' else 'clear')

class Configurador:
    def __init__(self, ruta):
        with open(ruta,'r') as archivo:
            texto=archivo.read().splitlines() # Abro el archivo y obtengo sus líneas

            self.data: list[str]  = [] # Inicializo valores para comprobar errores después
            self.alg: list[str]  = []
            self.seed: list[int]  = []
            self.k: list[int]  = []
            self.prcAleatorio: list[int]  = []
            self.tampoblacion: list[int]  = []
            self.numElites: list[int]  = []
            self.kBest: list[int]  = []
            self.prcCruce: list[int]  = []
            self.cruce: list[str]  = []
            self.prcMutacion: list[int]  = []
            self.kWorst: list[int]  = []
            self.maxEvaluaciones: list[int]  = []
            self.maxSegundos: list[int]  = []
            self.extra: list[str] = []

            for linea in texto: # Recorro las líneas del archivo de configuración
                contenido=linea.split() # Guardo una lista con el contenido de la línea
                if len(contenido) < 3: # Si no hay al menos 3 carácteres (nombre, '=', valor) nos lo saltamos
                    continue

                campo=contenido.pop(0) # Miro en qué campo tengo que guardar los datos
                contenido.pop(0) # Elimino '='
                match campo: # Guardo los datos según el campo al que pertenezcan
                    case 'DATA':
                        self.data=contenido
                        if not self.data:
                            error("La lista de ficheros de datos no puede estar vacía")
                            exit(1)
                    case 'ALG':
                        self.alg=contenido
                        if not self.alg:
                            error("La lista de algoritmos no puede estar vacía")
                            exit(1)
                    case 'SEED':
                        self.seed=[int(x) for x in contenido]
                        if not self.seed:
                            error("La lista de semillas no puede estar vacía")
                            exit(1)
                    case 'K':
                        self.k=[int(x) for x in contenido]
                        if not self.k:
                            error("Debe introducir al menos un parametro k")
                            exit(1)
                    case 'PRC_ALEATORIO':
                        self.prcAleatorio=[int(x) for x in contenido]
                        if not self.prcAleatorio:
                            error("Debe introducir al menos un porcentaje de individuos generados completamente aleatorios")
                            exit(1)   
                    case 'TAMPOBLACION':
                        self.tampoblacion=[int(x) for x in contenido]
                        if not self.tampoblacion:
                            error("Debe introducir al menos un tamaño de población")
                            exit(1) 
                    case 'NUMELITES':
                        self.numElites=[int(x) for x in contenido]
                    case 'KBEST':
                        self.kBest=[int(x) for x in contenido]
                        if not self.kBest:
                            error("Debe introducir al menos un valor de KBEST")
                            exit(1)   
                    case 'PRC_CRUCE':
                        self.prcCruce=[int(x) for x in contenido]
                        if not self.prcCruce:
                            error("Debe introducir al menos un porcentaje de cruce")
                            exit(1)                                                               
                    case 'CRUCE':
                        self.cruce=contenido
                        if not self.cruce:
                            error("Debe introducir al menos un tipo de cruce")
                            exit(1)
                    case 'PRC_MUTACION':
                        self.prcMutacion=[int(x) for x in contenido]
                        if not self.prcMutacion:
                            error("Debe introducir al menos un porcentaje de mutación")
                            exit(1)
                    case 'KWORST':
                        self.kWorst=[int(x) for x in contenido]
                        if not self.kWorst:
                            error("Debe introducir al menos un valor de KWORST")
                            exit(1)
                    case 'MAX_EVALUACIONES':
                        self.maxEvaluaciones=[int(x) for x in contenido]
                        if not self.maxEvaluaciones:
                            error("Debe introducir al menos un máximo de evaluaciones a ejecutar")
                            exit(1)
                    case 'MAX_SEGUNDOS':
                        self.maxSegundos=[int(x) for x in contenido]
                        if not self.maxSegundos:
                            error("Debe introducir al menos un máximo de segundos a ejecutar")
                            exit(1)
                    case _:
                        # Guardamos el resto como argumentos extra (como lista de contenido)
                        if contenido:
                            self.extra.append([campo] + contenido)

            # Compruebo que hay datos y algoritmo para trabajar
            if not self.data :
                error('La lista de ficheros de datos NO puede estar vacía')
                exit(1)

    def mostrarInfo(self):
        print(' CONFIGURACIÓN APLICADA: '.center(100, 'X'))
        print(f'  Archivos de datos: {self.data}')
        print(f'  Algoritmos a usar: {self.alg}')
        print(f'  Semillas: {self.seed}')
        print(f'  K: {self.k}')
        print(f'  Porcentaje de generación de población inicial generados completamente aleatorios: {self.prcAleatorio}')
        print(f'  Tamaño de población: {self.tampoblacion}')
        if(self.numElites):
            print(f'  Número de élites a conservar: {self.numElites}')
        print(f'  kBest: {self.kBest}')
        print(f'  Porcentaje de cruce: {self.prcCruce}')
        print(f'  Cruce: {self.cruce}')
        print(f'  Porcentaje de mutación: {self.prcMutacion}')
        print(f'  kWorst: {self.kWorst}')
        print(f'  Max evaluaciones: {self.maxEvaluaciones}')
        print(f'  Max segundos: {self.maxSegundos}')
        print(f'  Argumentos extra: {self.extra}')
        print('X' * 100)