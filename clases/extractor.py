from itertools import islice

class extractor:
    def __init__(self, archivo):
        self.flujos: list[list[int]] = []
        self.distancias: list[list[int]] = []
        self.dimension: int = 0

        try: 
            with open(archivo, mode="r") as fichero:
                numeros = list(map(int, fichero.read().split())) # 1. Sacamos y separamos todos los caracteres en un vector. 2. Map recorre cada elemento del vector y aplica la funcin int (int("2")). 3. Lo comvertimos a lista otra vez
                
                self.dimension = numeros.pop(0) # Cogemos la dimensión
                if self.dimension <= 0: 
                    raise Exception("La dimensión debe ser mayor que 0")
                if (len(numeros)) != pow(self.dimension, 2) * 2: # Comprobamos que todos los caracteres que hay es lo mismo que hacer dos matrices de dimensionXdimension
                    raise Exception("No se han encontrado dos matrices de " + self.dimension + "x" + self.dimension)
                iterador = iter(numeros)
                for matriz in (self.flujos, self.distancias):
                    for _ in range(self.dimension): # Vamos de la fila 0 hasta la dimensión
                        row = list(islice(iterador, self.dimension)) # islice() coge desde el valor que apunta el iterador hasta self.dimension, en la proxima iteración el iterador continuará por donde estaba
                        matriz.append(row)

        except (ValueError, TypeError) as e:
            print("[!] Error - Se ha introducido alguna letra en vez de número.", e)
            exit(1)
        except OSError: 
            print("[!] Error - El archivo no se puede leer.")
            exit(1)
        except Exception as e:
            print("[!] Error -",e)
            exit(1)  