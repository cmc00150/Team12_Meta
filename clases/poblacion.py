from clases.individuo import Individuo
from modulos.func_auxiliares import (fact, dos_opt, aleatorio, greedy_aleatorizado)
from clases.extractor import Extractor
from clases.configurador import Configurador
from copy import deepcopy
import random

class Poblacion:
    def __init__(self, config: Configurador, data: Extractor):
        self.__tamPoblacion = config.tampoblacion
        self.__individuos: list[Individuo] = []
        self.__elites: list[tuple[Individuo, Individuo]] = []
        self.__extra_data: Extractor = data

        # -- INICIALIZACIÓN --
        # GENERACION Y EVALUACIÓN DE LA POBLACION
        for _ in range(config.tampoblacion):
            if random.random() < config.prcAleatorio: # Si al sacar un valor entre [0,1) cae dentro del porcentaje de aleatorios usamos aleatorio
                self.__individuos.append(aleatorio(
                    self.__extra_data.flujos, 
                    self.__extra_data.distancias, 
                    self.__extra_data.dimension
                    ))
            else: # Sino usamos greedy
                self.__individuos.append(greedy_aleatorizado(
                    self.__extra_data.flujos, 
                    self.__extra_data.distancias, 
                    self.__extra_data.dimension,
                    config.k,
                    ))

        # ELITES        
        ordenados = sorted(self.__individuos, key=lambda i: i.getCosto) # Ordenamos según el costo
        for n in config.numElites:
            ind = ordenados.pop(n) # Saco los n primeros
            self.__elites.append((deepcopy(ind), ind)) # Guardamos una copia exacta y la referencia al individuo

    def seleccion(self, kBest: int):
        # TORNEO
        ganadores = []
        for _ in range(len(self.__individuos)):
            torneo = random.choices(self.__individuos, k=kBest) # Cogemos aleatoriamente a los kBest
            ganadores.append(min(torneo, key=lambda i: i.getCosto)) # Gana el que menor coste tenga
        
        # -- REEMPLAZO --
        self.__individuos = ganadores # Reemplazamos al inicio
        # Si estos padres se cruzan y son sustituidos por los hijos dejamos a los hijos en la siguiente gen.
        # Si mutan, el resultado pasa a la siguiente gen.
        # Y si no le toca ni uno ni otro pasan a la siguiente gen igualmente.
        # Asi que ya los pasamos todos a la siguient gen y cruzamos y mutamos los que sean.

    def cruce_mutacion(self, p_cruce: float, t_cruce: str, p_mutacion: float):
        # -- CRUCE --
        n = len(self.__individuos)
        for i in range(0, n - (n%2), 2): # Vamos cogiendo de dos en dos
            if random.random() < p_cruce: # Cae dentro de la probabilidad de cruce, los cruzamos
                padre1 = self.__individuos[i]
                padre2 = self.__individuos[i+1]

                hijo1 = padre1.cruce(padre2, t_cruce, self.__extra_data.flujos, self.__extra_data.distancias)
                hijo2 = padre2.cruce(padre1, t_cruce, self.__extra_data.flujos, self.__extra_data.distancias)

                self.__individuos[i] = hijo1
                self.__individuos[i+1] = hijo2
        
        # -- MUTACION --
        for i in range(n):
            if random.random() < p_mutacion: # Si cae dentro lo mutamos, sino no hacemos nada
                perm = self.__individuos[i].getPermutacion()
                posiciones = random.choices(range(len(perm)), k=2) # Cojo dos posiciones de esta permutación
                nuevaPerm = dos_opt(perm, posiciones[0], posiciones[1]) # Los intercambio
                costo = fact(posiciones[0], posiciones[1], perm, self.__extra_data.flujos, self.__extra_data.distancias)

                self.__individuos[i] = Individuo(nuevaPerm, costo, self.__individuos[i].getGeneracion()+1)

    @property
    def getTamPoblacion(self):
        return (self.__tamPoblacion)
    
    @property
    def getIndividuos(self):
        return (self.__individuos)
    
    @property
    def getElites(self):
        return (self.__elites)
    



    ######## VERSIÓN 2
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