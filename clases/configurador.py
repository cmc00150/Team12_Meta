import os
from modulos.func_auxiliares import error

def limpiar_terminal(): # Limpia la terminal en cada ejecución
    os.system('cls' if os.name == 'nt' else 'clear')

class Configurador:
    def __init__(self, ruta):
        with open(ruta,'r') as archivo:
            texto=archivo.read().splitlines() # Abro el archivo y obtengo sus líneas

            if len(texto) < 2:
                error('El fichero de configuración debe recibir al menos dos argumentos:',
                    '\n[!] OBLIGATORIO [!] \tDATA = {ejemplo.txt} (Datos para trabajar)',
                    '\n[!] OBLIGATORIO [!] \tALG = {greedy}  (Algoritmos con los que ejecutar)',
                    '\n\t\t\tSEED = {0} (Semillas para generar aleatoriedad)',
                    '\n\t\t\tArgumentos extra (opcional)')
                exit(1)

            self.__data: list[str]  = [] # Inicializo valores para comprobar errores después
            self.alg: str         = ""
            self.__seed: list[str]  = []
            self.cruce: str = ""
            self.poblacion: int = -1
            self.elite: int = -1
            self.kBest: int = -1
            self.kWorst: int = -1
            self.__extra: list[str] = []

            for linea in texto: # Recorro las líneas del archivo de configuración
                contenido=linea.split() # Guardo una lista con el contenido de la línea
                if len(contenido) < 3: # Si no hay al menos 3 carácteres (nombre, '=', valor) nos lo saltamos
                    continue

                campo=contenido.pop(0) # Miro en qué campo tengo que guardar los datos
                contenido.pop(0) # Elimino '='
                match campo: # Guardo los datos según el campo al que pertenezcan
                    case 'DATA':
                        self.__data=contenido
                        if not self.__data:
                            error("La lista de ficheros de datos no puede estar vacía")
                            exit(1)
                    case 'ALG':
                        self.__alg=contenido.pop(0)
                        if not self.__alg:
                            error("La lista de algoritmos no puede estar vacía")
                            exit(1)
                    case 'SEED':
                        self.__seed=contenido if contenido else []
                        if not self.__seed:
                            error("La lista de semillas no puede estar vacía")
                            exit(1)
                    case 'CRUCE':
                        self.cruce=contenido.pop(0) if contenido else None
                        if self.cruce is None:
                            error("El tipo de cruce no puede estar vacío")
                            exit(1)
                    case 'M':
                        try:
                            self.poblacion = int(contenido[0])
                        except Exception:
                            error("El tamaño de la población no es un número")
                            exit(1)
                    case 'E':
                        try:
                            self.elite = int(contenido[0])
                        except Exception:
                            error("El valor de élite no es un número")
                            exit(1)
                    case 'kBest':
                        try:
                            self.kBest = int(contenido[0])
                        except Exception:
                            error("El k mejor no es un número")
                            exit(1)
                    case 'kWorst':
                        try:
                            self.kWorst = int(contenido[0])
                        except Exception:
                            error("El k peor no es un número")
                            exit(1)
                    case _:
                        # Guardamos el resto como argumentos extra (como lista de contenido)
                        if contenido:
                            self.__extra.append([campo] + contenido)

            # Compruebo que hay datos y algoritmo para trabajar
            if not self.__data :
                error('La lista de ficheros de datos NO puede estar vacía')
                exit(1)

    @property
    def data(self) -> list[str]:
        return self.__data.copy()

    @property
    def seed(self) -> list[str]:
        return self.__seed.copy()

    @property
    def extra(self) -> list[list[str]]:
        return [e.copy() for e in self.__extra]

    def mostrarInfo(self):
        print(' CONFIGURACIÓN APLICADA: '.center(100, 'X'))
        print(f'  Archivos de datos: {self.data}')
        print(f'  Algoritmos a usar: {self.alg}')
        print(f'  Semillas: {self.seed}')
        print(f'  Cruce: {self.cruce}')
        print(f'  Población: {self.poblacion}  Elite: {self.elite}')
        print(f'  kBest: {self.kBest}  kWorst: {self.kWorst}')
        print(f'  Argumentos extra: {self.extra}')
        print('X' * 100)