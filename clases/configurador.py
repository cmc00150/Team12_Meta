import os

def limpiar_terminal(): # Limpia la terminal en cada ejecución
    os.system('cls' if os.name == 'nt' else 'clear')

class Configurador:
    def __init__(self, ruta):
        with open(ruta,'r') as archivo:
            texto=archivo.read().splitlines() # Abro el archivo y obtengo sus líneas

            if len(texto) < 2:
                print('El fichero de configuración debe recibir al menos dos argumentos:',
                    '\n[!] OBLIGATORIO [!] \tDATA = {ejemplo.txt} (Datos para trabajar)',
                    '\n[!] OBLIGATORIO [!] \tALG = {greedy}  (Algoritmos con los que ejecutar)',
                    '\n\t\t\tSEED = {0} (Semillas para generar aleatoriedad)',
                    '\n\t\t\tArgumentos extra (opcional)')
                exit(1)

            self.__data=[0] # Inicializo valores para comprobar errores después
            self.__alg=[0]
            self.__seed=[0]
            self.__extra=[]

            for linea in texto: # Recorro las líneas del archivo de configuración
                contenido=linea.split() # Guardo una lista con el contenido de la línea
                campo=contenido.pop(0) # Miro en qué campo tengo que guardar los datos
                contenido.pop(0) # Elimino '='
                if len(contenido) < 1:
                    continue
                match campo: # Guardo los datos según el campo al que pertenezcan
                    case 'DATA':
                        self.__data=contenido
                    case 'ALG':
                        self.__alg=contenido
                    case 'SEED':
                        self.__seed=contenido
                    case _: # Caso por defecto (argumentos extra)
                        self.__extra.append(contenido)

            # Compruebo que hay datos y algoritmo para trabajar
            if self.__data[0]==0:
                print('[!] Error - La lista de ficheros de datos NO puede estar vacía')
                exit(1)
            if self.__alg[0]==0:
                print('[!] Error - Debe indicar al menos un algoritmo para usar')
                exit(1)

    def mostrarInfo(self): # Función para verificar que se han añadido los datos correctamente
        print('Archivos de datos: ',self.__data,
              '\nAlgoritmos a usar: ',self.__alg,
              '\nSemillas: ',self.__seed,
              '\nArgumentos extra: ',self.__extra)