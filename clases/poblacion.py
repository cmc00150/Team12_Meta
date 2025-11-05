from clases.individuo import Individuo
from modulos.func_auxiliares import (greedy_aleatorizado, aleatorio)
import random

class Poblacion:
    def __init__(self, tam: int, elites: int):
        self.__tamPoblacion = tam
        self.__individuos = [Individuo() for _ in range(tam)]
        self.__elites = [Individuo() for _ in range(elites)] # Vector de élites ordenado de mayor a menor costo

    # No defino la generación de la población en el constructor para no tener que pasar tantos argumentos y que quede más limpio el código
    def generarPoblacionInicial(self, k, prcAleat, flujos, distancias, dimension):        
        for i in range (0, self.__tamPoblacion):
            nuevoIndividuo=Individuo()
            if(random.randint(0,100) > prcAleat):
                nuevoIndividuo = greedy_aleatorizado(flujos,distancias,dimension,k)
                self.__individuos[i]=nuevoIndividuo
            else:
                nuevoIndividuo = aleatorio(flujos,distancias,dimension)
                self.__individuos[i]=nuevoIndividuo

            self.estudiarElite(nuevoIndividuo) # Para mejorar el rendimiento, los primeros élites se obtienen mientras se genera la población
    
    def estudiarElite(self, nuevoIndividuo: Individuo):
        posElite=-1 # Estudio si el nuevo individuo puede ser un élite
        for j in range (0,len(self.__elites)): # Se recorre el vector a la inversa, empezando por los élites con mayor costo
            if(self.__elites[j].getCosto==-1 or nuevoIndividuo.getCosto < self.__elites[j].getCosto): # Si no había un élite en esa posición o su valor era inferior al nuevo individuo
                posElite=j
            else:
                break

        if (posElite != -1): # Si se ha encontrado una posición válida
            self.__elites[posElite]=nuevoIndividuo # Actualizamos el élite

    def _construir_hijo(self, mantener: list[int], asignar: list[int], referencia: list[int]) -> list[int]:
        hijo = []
        for e in referencia:
            if e in mantener:
                hijo.append(e)
            else:
                hijo.append(asignar.pop(0))
        return hijo

    def cruce(self, padre1: list[int], padre2: list[int], tipoCruce: str) -> tuple[list[int], list[int]]:
        tam = len(padre1)

        hijos = (None, None)
        if tipoCruce == "MOC": # Todo el tipo de cruce es del algoritmo no de la población
            pivote = random.randint(1, tam-1) - 1 # Va desde el primero al penúltimo, lo convertimos en índice
            hijos[0] = self._construir_hijo(mantener=padre1[:pivote], asignar=padre1[pivote+1:], referencia=padre2)
            hijos[1] = self._construir_hijo(mantener=padre2[:pivote], asignar=padre2[pivote+1:], referencia=padre1)

        elif tipoCruce == "OX2":
            asignar = []
            mantener = []
            for i, p in enumerate(zip(padre1, padre2)):
                for e in p:
                    if random.randint(1, 100) <= 50:
                        mantener.append(e)
                    else:
                        asignar.append(e)
                hijos[i] = self._construir_hijo(mantener, asignar, p)

        return hijos

    def imprimeElites(self):
        print('LISTA DE ELITES:')
        for i in range (0, len(self.__elites)):
            print(self.__elites[i])

    @property
    def getTamPoblacion(self):
        return (self.__tamPoblacion)
    
    @property
    def getIndividuos(self):
        return (self.__individuos)
    
    @property
    def getElites(self):
        return (self.__elites)