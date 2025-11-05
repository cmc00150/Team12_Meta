from clases.individuo import Individuo
from modulos.func_auxiliares import (fact, dos_opt, aleatorio, greedy_aleatorizado)
from clases.extractor import Extractor
from clases.configurador import Configurador
from copy import deepcopy
import random

class Poblacion:
    def __init__(self, config: Configurador, data: Extractor):
        self.__poblacion: list[Individuo] = []
        self.__elites: list[tuple[Individuo, Individuo]] = []
        self.__extra_data: Extractor = data

        # -- INICIALIZACIÓN --
        # GENERACION Y EVALUACIÓN DE LA POBLACION
        for _ in range(config.tampoblacion):
            if random.random() < config.prcAleatorio: # Si al sacar un valor entre [0,1) cae dentro del porcentaje de aleatorios usamos aleatorio
                self.__poblacion.append(aleatorio(
                    self.__extra_data.flujos, 
                    self.__extra_data.distancias, 
                    self.__distancias
                    ))
            else: # Sino usamos greedy
                self.__poblacion.append(greedy_aleatorizado(
                    self.__extra_data.flujos, 
                    self.__extra_data.distancias, 
                    self.__extra_data.candidatos,
                    config.k,
                    ))

        # ELITES        
        ordenados = sorted(self.__poblacion, key=lambda i: i.getCosto) # Ordenamos según el costo
        for n in config.numElites:
            ind = ordenados.pop(n) # Saco los n primeros
            self.__elites.append((deepcopy(ind), ind)) # Guardamos una copia exacta y la referencia al individuo

    def seleccion(self, kBest: int):
        # TORNEO
        ganadores = []
        for _ in range(len(self.__poblacion)):
            torneo = random.choices(self.__poblacion, k=kBest) # Cogemos aleatoriamente a 3
            ganadores.append(min(torneo, key=lambda i: i.getCosto)) # Gana el que menor coste tenga
        
        # -- REEMPLAZO --
        self.__poblacion = ganadores # Reemplazamos al inicio
        # Si estos padres se cruzan y son sustituidos por los hijos dejamos a los hijos en la siguiente gen.
        # Si mutan, el resultado pasa a la siguiente gen.
        # Y si no le toca ni uno ni otro pasan a la siguiente gen igualmente.
        # Asi que ya los pasamos todos a la siguient gen y cruzamos y mutamos los que sean.

    def cruce_mutacion(self, p_cruce: float, t_cruce: str, p_mutacion: float):
        # -- CRUCE --
        n = len(self.__poblacion)
        for i in range(0, n - (n%2), 2): # Vamos cogiendo de dos en dos
            if random.random() < p_cruce: # Cae dentro de la probabilidad de cruce, los cruzamos
                padre1 = self.__poblacion[i]
                padre2 = self.__poblacion[i+1]

                hijo1 = padre1.cruce(padre2, t_cruce, self.__extra_data.flujos, self.__extra_data.distancias)
                hijo2 = padre2.cruce(padre1, t_cruce, self.__extra_data.flujos, self.__extra_data.distancias)

                self.__poblacion[i] = hijo1
                self.__poblacion[i+1] = hijo2
        
        # -- MUTACION --
        for i in range(n):
            if random.random() < p_mutacion: # Si cae dentro lo mutamos, sino no hacemos nada
                perm = self.__poblacion[i].getPermutacion()
                posiciones = random.choices(range(len(perm)), k=2) # Cojo dos posiciones de esta permutación
                nuevaPerm = dos_opt(perm, posiciones[0], posiciones[1]) # Los intercambio
                costo = fact(posiciones[0], posiciones[1], perm, self.__extra_data.flujos, self.__extra_data.distancias)

                self.__poblacion[i] = Individuo(nuevaPerm, costo, self.__poblacion[i].getGeneracion()+1)

