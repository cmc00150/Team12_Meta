import random
from modulos.func_auxiliares import costo

class Individuo:
    def __init__(self, permutacion=[], costo=-1, generacion=-1, evaluado=False):
        self.__permutacion = permutacion
        self.__costo = costo
        self.__generacion = generacion
        self.__evaluado = evaluado
        
    @staticmethod
    def cruce(padre1: "Individuo", padre2: "Individuo", cruce: str, flujos: list[list[int]], distancias: list[list[int]]) -> tuple["Individuo", "Individuo"]:
        tam = len(padre1.getPermutacion)
        perm_hijos = ([],[]) # Permutación que acabará siendo parte de los individuos hijos
        p1 = padre1.getPermutacion
        p2 = padre2.getPermutacion

        if cruce == 'MOC':
            pivote = random.randint(1,tam-2) # El pivote se escoge entre el selgundo y el penúltimo

            mantenerhijo1 = p1[:pivote] # Se mantienen fijos los valores del padre 1 dentro del padre 2
            asignarhijo1 = p1[pivote:] # El resto de valores se asignan por orden
            mantenerhijo2 = p2[:pivote] # Igual pero a la inversa
            asignarhijo2 = p2[pivote:]

            for i in range (0,tam):
                if p2[i] in mantenerhijo1:
                    perm_hijos[0].append(p2[i])
                else:
                    perm_hijos[0].append(asignarhijo1.pop(0))

                if p1[i] in mantenerhijo2:
                    perm_hijos[1].append(p1[i])
                else:
                    perm_hijos[1].append(asignarhijo2.pop())

        elif cruce == 'OX2': # Cruce modificado para que dé dos hijos (en lugar de solo uno) a partir de dos padres
            eliminarpadre2 = []
            mantenerpadre1 = []
            eliminarpadre1 = []
            mantenerpadre2 = []

            for i in range (0, tam):
                if (random.randint(0,100) < 50):
                    eliminarpadre2.append(p1[i])
                    mantenerpadre1.append(p1[i])
                if (random.randint(0,100) < 50):
                    eliminarpadre1.append(p2[i])
                    mantenerpadre2.append(p2[i])
            
            perm_hijos[0]=p2
            for i in range (0,tam):
                if (p1[i] in eliminarpadre2):
                    perm_hijos[0][i]=mantenerpadre1.pop()
                if (p2[i] in eliminarpadre1):
                    perm_hijos[1][i]=mantenerpadre2.pop()
        
        nuevaGen = -1
        if (padre1.getGeneracion >= padre2.getGeneracion): # La generación de los hijos será la siguiente a la mayor de los padres
            nuevaGen = padre1.getGeneracion + 1
        else:
            nuevaGen = padre2.getGeneracion + 1

        hijo1 = Individuo(perm_hijos[0],costo(perm_hijos[0],flujos,distancias),nuevaGen, True)
        hijo2 = Individuo(perm_hijos[1],costo(perm_hijos[1],flujos,distancias),nuevaGen, True)

        return (hijo1,hijo2)

    @property
    def getPermutacion(self) -> list[int]:
        return (self.__permutacion)
    
    @property
    def getCosto(self):
        return (self.__costo)
    
    
    @property
    def getGeneracion(self):
        return (self.__generacion)
    
    @property
    def getEvaluado(self):
        return (self.__evaluado)
    
    @property
    def setEvaluado(self, evaluado):
        self.__evaluado=evaluado

    @property
    def setIndividuo(self, permutacion, costo, generacion):
        self.__permutacion=permutacion
        self.__costo=costo
        self.__generacion=generacion

    def __str__(self): # Sobrecarga del operador print para hacer pruebas
        return f'\tPermutacion: {self.__permutacion}\n\tCosto: {self.__costo}\n\tGeneracion: {self.__generacion}\n'
