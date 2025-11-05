import random
from modulos.func_auxiliares import (costo, dos_opt)

class Individuo:
    def __init__(self, permutacion=[], costo=-1, generacion=-1):
        self.__permutacion = permutacion
        self.__costo = costo
        self.__generacion = generacion
        self.__evaluado = False

    def _construir_hijo(self, mantener: list[int], asignar: list[int], referencia: "Individuo", flujos, distancias) -> "Individuo":
        hijo = []
        for e in referencia.getPermutacion():
            if e in mantener:
                hijo.append(e)
            else:
                hijo.append(asignar.pop(0))
        
        return Individuo(hijo, costo(hijo, flujos, distancias), referencia.getGeneracion+1)

    def cruce(self, pareja: "Individuo", cruce: str, flujos: list[list[int]], distancias: list[list[int]]) -> "Individuo":
        tam = len(pareja.getPermutacion())

        if cruce == "MOC":
            pivote = random.randint(1, tam-1) - 1 # Va desde el primero al penúltimo, lo convertimos en índice
            return self._construir_hijo(flujos, distancias, mantener=self.__permutacion[:pivote], asignar=self.__permutacion[pivote+1:], referencia=pareja)

        elif cruce == "OX2":
            asignar = []
            mantener = []
            for e in self.__permutacion:
                if random.randint(1, 100) <= 50:
                    mantener.append(e)
                else:
                    asignar.append(e)
            return self._construir_hijo(mantener, asignar, pareja, flujos, distancias)

    @property
    def getPermutacion(self):
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
