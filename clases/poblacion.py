from clases.individuo import Individuo
from modulos.func_auxiliares import (costo, aleatorio, greedy_aleatorizado)
from clases.extractor import Extractor
from copy import deepcopy
from sortedcontainers import SortedKeyList
import random

class Poblacion:
    def __init__(self, tamPoblacion: int, prcAleatorio: int, k: int, data: Extractor):
        self._tamPoblacion = tamPoblacion
        self._individuos: list[Individuo] = []

        # -- INICIALIZACIÓN --
        # GENERACIÓN Y EVALUACIÓN DE LA POBLACIÓN
        for _ in range(tamPoblacion):
            if random.randint(0, 100) < prcAleatorio: # Si al sacar un valor entre [0,1) cae dentro del porcentaje de aleatorios usamos aleatorio
                perm = aleatorio(data.dimension)
            else: # Sino usamos greedy
                perm = greedy_aleatorizado(data.flujos, data.distancias, data.dimension, k)

            self._individuos.append(Individuo(perm, costo(perm, data.flujos, data.distancias)))

    def __getitem__(self, index: int) -> Individuo:
        return self._individuos[index]

    def __setitem__(self, index: int, value: Individuo):
        self._individuos[index] = value

    def __len__(self):
        return self._tamPoblacion
    
    def __iter__(self):
        return iter(self._individuos)

    def seleccion(self):
        raise NotImplementedError("Método seleccion no implementado en la clase Población")

    def reemplazo(self):
        raise NotImplementedError("Método reemplazo no implementado en la clase Población")
    
    def getMejor(self) -> Individuo:
        raise NotImplementedError("Método getMejor no implementado en la clase Población")

    @property
    def getIndividuos(self) -> list[Individuo]:
        return self._individuos
    
    @property
    def getTamPoblacion(self) -> int:
        return self._tamPoblacion

class PoblacionGEN(Poblacion):
    def __init__(self, numElites, tamPoblacion, prcAleatorio, k, data):
        super().__init__(tamPoblacion, prcAleatorio, k, data)
        self.__elites: SortedKeyList = []
        # Lista ordenada de élites: tupla de (copia, indice). Se ordena por el costo de la copia
        self.__numElites = numElites
        self.guardarElites()

    def guardarElites(self):
        elites = []
        ordenados = sorted(range(self._tamPoblacion), key=lambda idx: self._individuos[idx].getCosto) # Ordenamos según el costo (menor a mayor)
        for n in range(self.__numElites): # Nos quedamos con los n primeros
            idx = ordenados.pop(n)                
            elites.append((deepcopy(self._individuos[idx]), idx))

        self.__elites = SortedKeyList(elites, key=lambda ind_tuple: ind_tuple[0].getCosto)

    def seleccion(self, kBest):
        # ACTUALIAZAMOS LOS ELITES DE LA NUEVA GENERACIÓN
        self.guardarElites()

        # KBEST TORNEO
        ganadores = []
        for _ in range(self._tamPoblacion):
            torneo = random.choices(self._individuos, k=kBest) # Cogemos aleatoriamente a los kBest
            ganadores.append(min(torneo, key=lambda i: i.getCosto)) # Gana el que menor coste tenga
        
        return ganadores

    def reemplazo(self, kworst: int, nueva_poblacion: list[Individuo]):
        self._individuos = nueva_poblacion
        # REVISIÓN ÉLITES
        for i in range(len(self.__elites)):
            copia, idx = self.__elites[i]
            if copia is not self._individuos[idx]: # Entonces es porque hemos perdido a ese élite
                # Cogemos aleatoriamente a varios ind. para escoger el peor de ellos
                torneo = random.sample(range(self._tamPoblacion), k=kworst) # Cogemos aleatoriamente índices
                idx_perdedor = max(torneo, key=lambda idx: self._individuos[idx].getCosto) # Gana el indice del individuo con el peor costo

                self.__elites.pop(i) # Lo borramos porque las tuplas son inmutables
                self.__elites.add((copia, idx_perdedor))  # Ponemos la referencia a este nuevo individuo.

                self._individuos[idx_perdedor] = copia # Actualizamos el valor en la población
    
    @property
    def getElites(self) -> list[tuple[Individuo, int]]:
        return self.__elites

class PoblacionEST(Poblacion):
    def __init__(self, tamPoblacion, prcAleatorio, k, data):
        super().__init__(tamPoblacion, prcAleatorio, k, data)

    def seleccion(self, kBest, numPadres) -> tuple[int, int]:
        # KBEST TORNEO
        ganadores = []

        for _ in range(numPadres):
            # SIN REEMPLAZO para diversificar
            torneo = random.sample(range(self._tamPoblacion), k=kBest) # Cogemos aleatoriamente a los kBest
            ganadores.append(min(torneo, key=lambda i: i.getCosto)) # Gana el que menor coste tenga
        
        return ganadores
    
    def reemplazo(self, kworst:int , individuos: tuple):
        for i in range(len(individuos)):
            torneo = random.sample(range(self._tamPoblacion), k=kworst)
            idx_perdedor = min(torneo, key=lambda idx: self._individuos[idx].getCosto)

            self._individuos[idx_perdedor] = individuos[i]
        
    def getMejor(self) -> Individuo:
        return self._individuos.sort(key=lambda i: i.getCosto)[0] # Devuelve el mejor encontrado