import random
from modulos.func_auxiliares import (costo, aleatorio, greedy_aleatorizado, dos_opt, fact)

class Individuo:
    def __init__(self, permutacion=[], costo=None, generacion=1):
        self.__permutacion: list[int] = permutacion
        self.__costo = costo
        self.__generacion = generacion

    @staticmethod
    def cruce(padre1: "Individuo", padre2: "Individuo", cruce: str, flujos: list[list[int]], distancias: list[list[int]]) -> tuple["Individuo", "Individuo"]:
        tam = len(padre1.getPermutacion)
        p1 = padre1.getPermutacion
        p2 = padre2.getPermutacion

        if cruce == 'MOC':
            pivote = random.randint(1,tam-2) # El pivote se escoge entre el segundo y el penúltimo
            # Asignación
            asignarhijo1 = p1[pivote+1:] # Resto de valores del padre a reasignar en el hijo
            asignarhijo2 = p2[pivote+1:]
        else: # Consideramos que en el resto de casos usamos el OX2
            asignarhijo1 = []
            asignarhijo2 = []
            # Asignación
            for i in range(tam):
                # 50% de cogerlo y 50% de que no
                if random.random() < 0.5: # Si escogemos esta posición es que la asignamos
                    asignarhijo1.append(p1[i]) # Valores a reasignar del padre 1
                    asignarhijo2.append(p2[i]) # Lo mismo para el padre 2

        cont1 = cont2 = 0
        h1 = []
        h2 = []
        for i in range(tam):
            if p2[i] not in asignarhijo1: # Si no está en asignar, lo mantenemos
                h1.append(p2[i])
            else: # Si no, lo asignamos según el orden del padre
                h1.append(asignarhijo1[cont1])
                cont1+=1

            if p1[i] not in asignarhijo2:
                h2.append(p1[i])
            else:
                h2.append(asignarhijo2[cont2])
                cont2+=1

        nuevaGen = -1
        if (padre1.getGeneracion >= padre2.getGeneracion): # La generación de los hijos será la siguiente a la mayor de los padres
            nuevaGen = padre1.getGeneracion + 1
        else:
            nuevaGen = padre2.getGeneracion + 1

        hijo1 = Individuo(h1,costo(h1,flujos,distancias),nuevaGen)
        hijo2 = Individuo(h2,costo(h2,flujos,distancias),nuevaGen)

        return (hijo1,hijo2)

    def mutar(self, flujos, distancias):
        # 1. Copiamos la permutación
        perm = self.__permutacion
        # 2. Selecciono los genes a mutar
        posiciones = random.sample(range(len(perm)), k=2) # Cojo dos posiciones de esta permutación
        # 3. Calculo el costo (parcialmente)
        variacion = fact(posiciones[0], posiciones[1], perm, flujos, distancias)
        # 4. Le hago la mutación
        dos_opt(self.__permutacion, posiciones[0], posiciones[1]) # Los intercambio
        # 5. Actualizo el costo
        self.__costo += variacion

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
        return f'\tPermutacion: {[elem+1 for elem in self.__permutacion]}\n\tCosto: {self.__costo}\n\tGeneracion: {self.__generacion}\n'