from itertools import it

from clases.individuo import Individuo
import random

class Poblacion:
    def __init__(self, tam: int, elites: int, t_cruce: str):
        self.__individuos = [Individuo() for _ in tam]
        self.__elites = [0] * elites
        self.__cruce = t_cruce

    def _construir_hijo_MOC(self, guia: list[int], modificado: list[int], pivote: int) -> list[int]:
        mantener = guia[:pivote] # Cojo la primera mitad
        it_asign = it(modificado[pivote:]) # Creamos un iterador de la segunda mitad
        hijo = []
        for e in modificado:
            if e in mantener:
                hijo.append(e)
            else:
                hijo.append(next(it_asign))
        return hijo
    
    def _construir_hijo_OX2(self, padre1: list[int], padre2: list[int]) -> list[int]:
        pass

    def cruce(self, padre1: list[int], padre2: list[int]) -> tuple[list[int], list[int]]:
        tam = len(padre1)
        pivote = random.randint(1, tam-1) - 1 # Va desde el primero al penúltimo, lo convertimos en índice

        hijos = (None, None)
        if self.__cruce == "MOC":
            hijos[0] = self._construir_hijo_MOC(padre1, padre2, pivote)
            hijos[1] = self._construir_hijo_MOC(padre2, padre1, pivote)
        elif self.__cruce == "OX2":
            hijos[0] = self._construir_hijo_OX2(padre1, padre2)
            hijos[1] = self._construir_hijo_OX2(padre2, padre1)
        return hijos
