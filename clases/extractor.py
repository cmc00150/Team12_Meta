from itertools import islice
from modulos.prints import error
import copy

class Extractor:
    def __init__(self, archivo):
        self.__flujos: list[list[int]] = []
        self.__distancias: list[list[int]] = []
        self.__dimension: int = 0

        try: 
            with open(archivo, mode="r") as fichero:
                numeros = list(map(int, fichero.read().split())) # 1. Sacamos y separamos todos los caracteres en un vector. 2. Map recorre cada elemento del vector y aplica la funcin int (int("2")). 3. Lo comvertimos a lista otra vez
                
                self.__dimension = numeros.pop(0) # Cogemos la dimensión
                if self.__dimension <= 0: 
                    raise Exception("La dimensión debe ser mayor que 0")
                if (len(numeros)) != pow(self.__dimension, 2) * 2: # Comprobamos que todos los caracteres que hay es lo mismo que hacer dos matrices de dimensionXdimension
                    raise Exception("No se han encontrado dos matrices de " + self.__dimension + "x" + self.__dimension)
                iterador = iter(numeros)
                for matriz in (self.__flujos, self.__distancias):
                    for _ in range(self.__dimension): # Vamos de la fila 0 hasta la dimensión
                        row = list(islice(iterador, self.__dimension)) # islice() coge desde el valor que apunta el iterador hasta self.__dimension, en la proxima iteración el iterador continuará por donde estaba
                        matriz.append(row)

        except (ValueError, TypeError) as e:
            error('Se ha introducido alguna letra en vez de número.')
            print(e)
            exit(1)
        except OSError: 
            error('Algún archivo no se puede leer o no existe.')
            exit(1)
        except Exception as e:
            error(e)
            exit(1)  

    @property
    def flujos(self):
        return copy.deepcopy(self.__flujos)
    @property
    def distancias(self):
        return copy.deepcopy(self.__distancias)
    @property
    def dimension(self):
        return self.__dimension