from clases.individuo import Individuo
from modulos.func_auxiliares import (costo, aleatorio, greedy_aleatorizado)
from clases.extractor import Extractor
from copy import deepcopy
from sortedcontainers import SortedKeyList
import random

class Poblacion:
    def __init__(self, numElites: int, tamPoblacion: int, prcAleatorio: int, k: int, data: Extractor):
        self.__tamPoblacion = tamPoblacion
        self.__individuos: list[Individuo] = []
        self.__elites: SortedKeyList = SortedKeyList(key=lambda ind_tuple: ind_tuple[0].getCosto)
        # Lista ordenada de élites: tupla de (copia, indice). Se ordena por el costo de la copia
        self.__numElites = numElites

        # -- INICIALIZACIÓN --
        # GENERACIÓN Y EVALUACIÓN DE LA POBLACIÓN
        for _ in range(tamPoblacion):
            if random.randint(0, 100) < prcAleatorio: # Si al sacar un valor entre [0,1) cae dentro del porcentaje de aleatorios usamos aleatorio
                perm = aleatorio(data.dimension)
            else: # Sino usamos greedy
                perm = greedy_aleatorizado(data.flujos, data.distancias, data.dimension, k)

            self.__individuos.append(Individuo(perm, costo(perm, data.flujos, data.distancias)))

        # -- INICIALIZAMOS LOS ÉLITES --
        ordenados = sorted(range(self.__tamPoblacion), key=lambda idx: self.__individuos[idx].getCosto) # Ordenamos según el costo (menor a mayor)
        for n in range(self.__numElites): # Nos quedamos con los n primeros
            idx = ordenados.pop(n)
            self.__elites.add((deepcopy(self.__individuos[idx]), idx))

    def __getitem__(self, index: int) -> Individuo:
        return self.__individuos[index]

    def __setitem__(self, index: int, value: Individuo):
        self.__individuos[index] = value

    def __len__(self):
        return self.__tamPoblacion

    def seleccion(self, kBest: int):
        # ACTUALIAZAMOS LOS ELITES DE LA NUEVA GENERACIÓN
        ordenados = sorted(range(self.__tamPoblacion), key=lambda idx: self.__individuos[idx].getCosto) # Ordenamos según el costo (menor a mayor)
        for n in range(self.__numElites): # Nos quedamos con los n primeros
            idx = ordenados.pop(n)                
            if self.__individuos[idx].getCosto < self.__elites[-1][0].getCosto: # Si el actual es mejor que el peor élite lo sustituimos
                self.__elites.pop()
                self.__elites.add((deepcopy(self.__individuos[idx]), idx))

        # KBEST TORNEO
        ganadores = []
        for _ in range(self.__tamPoblacion):
            torneo = random.sample(self.__individuos, k=kBest) # Cogemos aleatoriamente a los kBest
            ganadores.append(min(torneo, key=lambda i: i.getCosto)) # Gana el que menor coste tenga
        
        return ganadores

    def reemplazo(self, kworst: int, nueva_poblacion: list[Individuo]):
        self.__individuos = nueva_poblacion

        # REVISIÓN ÉLITES
        for i in range(len(self.__elites)):
            copia, idx = self.__elites[i]
            if copia is not self.__individuos[idx]: # Entonces es porque hemos perdido a ese élite
                # Cogemos aleatoriamente a varios ind. para escoger el peor de ellos
                torneo = random.sample(range(self.__tamPoblacion), k=kworst) # Cogemos aleatoriamente índices
                idx_perdedor = max(torneo, key=lambda idx: self.__individuos[idx].getCosto) # Gana el indice del individuo con el peor costo

                self.__elites.pop(i) # Lo borramos porque las tuplas son inmutables
                self.__elites.add((copia, idx_perdedor))  # Ponemos la referencia a este nuevo individuo.

                self.__individuos[idx_perdedor] = copia # Actualizamos el valor en la población


    def getMejor(self) -> Individuo:
        return self.__elites[0][0] # Devuelve la referencia mejor de los élites
    
    @property
    def getIndividuos(self) -> list[Individuo]:
        return self.__individuos
    
    @property
    def getElites(self):
        return self.__elites
    
    @property
    def getTamPoblacion(self) -> int:
        return self.__tamPoblacion