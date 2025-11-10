from clases.individuo import Individuo
from modulos.func_auxiliares import (fact, dos_opt, aleatorio, greedy_aleatorizado)
from clases.extractor import Extractor
from clases.configurador import Configurador
from copy import deepcopy
from sortedcontainers import SortedKeyList
import random

# TODO Control de repetidos

class Poblacion:
    def __init__(self, config: Configurador, data: Extractor):
        self.__tamPoblacion = config.tampoblacion
        self.__individuos: list[Individuo] = []
        self.__elites: SortedKeyList = SortedKeyList(lambda ind_tuple: ind_tuple[0].getCosto())
        # Lista ordenada de élites: tupla de (copia, referencia). Se ordena por el costo de la copia

        # -- INICIALIZACIÓN --
        # GENERACIÓN Y EVALUACIÓN DE LA POBLACIÓN
        for _ in range(config.tampoblacion):
            if random.random() < config.prcAleatorio: # Si al sacar un valor entre [0,1) cae dentro del porcentaje de aleatorios usamos aleatorio
                self.__individuos.append(aleatorio(
                    data.flujos, 
                    data.distancias, 
                    data.dimension
                    ))
            else: # Sino usamos greedy
                self.__individuos.append(greedy_aleatorizado(
                    data.flujos, 
                    data.distancias, 
                    data.dimension,
                    config.k,
                    ))

        # ÉLITES        
        ordenados = sorted(self.__individuos, key=lambda i: i.getCosto) # Ordenamos según el costo
        for n in config.numElites:
            ind = ordenados.pop(n) # Saco los n primeros
            self.__elites.add((deepcopy(ind), ind)) # Guardamos una copia exacta y la referencia al individuo

    def __getitem__(self, index: int) -> Individuo:
        return self.__individuos[index]

    def __setitem__(self, index: int, value: Individuo):
        self.__individuos[index] = value

    def __len__(self):
        return self.__tamPoblacion

    def seleccion(self, kBest: int):
        """
        **POST: Modifica la población actual**

        Consta de 3 fases:
        1. Revisa que los élites no se hayan perdido
        2. Genera una población intermedia de ganadores
        3. Sustituye a la población actual por esta población de ganadores
        """
        # REVISIÓN ÉLITES
        for i, e in enumerate(self.__elites):
            if e[0] != e[1]: # Si la copia es distinta de la referencia entonces es porque hemos perdido a ese élite
                # Obtenemos el índice de el individuo con mayor coste (el peor)
                peor = max(range(self.__tamPoblacion), key=lambda idx: self.__individuos[idx].getCosto())
                self.__elites[i][1] = self.__individuos[peor] # Ponemos la referencia a este nuevo individuo.
                self.__individuos[peor] = self.__elites[i][0] # Lo sustituimos por la copia del élite

        # TORNEO
        ganadores = []
        for _ in range(self.__tamPoblacion):
            torneo = random.choices(self.__individuos, k=kBest) # Cogemos aleatoriamente a los kBest
            ganadores.append(min(torneo, key=lambda i: i.getCosto())) # Gana el que menor coste tenga
        
        # -- REEMPLAZO --
        # SEGUN GENERACIONAL
        self.__individuos = ganadores # Reemplazamos al inicio
        # Si estos padres se cruzan y son sustituidos por los hijos dejamos a los hijos en la siguiente gen.
        # Si mutan, el resultado pasa a la siguiente gen.
        # Y si no le toca ni uno ni otro pasan a la siguiente gen igualmente.
        # Asi que ya los pasamos todos a la siguient gen y cruzamos y mutamos los que sean.

    def considerarElite(self, idx: int):
        # Objetivo: sustituir este ind por el peor de los élites, si lo mejora.
        peor = self.__elites[-1] # Sacamos el último
        indv = self.__individuos[idx]
        if indv.getCosto() < peor:
            self.__elites.pop() # Lo quitamos
            self.__elites.add((deepcopy(indv), indv)) # Añadimos el nuevo élite

    def getMejor(self) -> Individuo:
        return self.__elites[0][1] # Devuelve la referencia mejor de los élites

    """ VERSIÓN 2
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
        posElite=-1 # Estudio si el nuevo individuo puede ser un élitecorre el vector a la in
        for j in range (0,len(self.__elites)): # Se reversa, empezando por los élites con mayor costo
            if(self.__elites[j].getCosto==-1 or nuevoIndividuo.getCosto < self.__elites[j].getCosto): # Si no había un élite en esa posición o su valor era inferior al nuevo individuo
                posElite=j
            else:
                break

        if (posElite != -1): # Si se ha encontrado una posición válida
            self.__elites[posElite]=nuevoIndividuo # Actualizamos el élite"""