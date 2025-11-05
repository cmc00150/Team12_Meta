from clases.individuo import Individuo
import random

class Poblacion:
    def __init__(self, tam: int, elites: int, t_cruce: str):
        self.__individuos = [Individuo() for _ in tam]
        self.__elites = [0] * elites
        self.__cruce = t_cruce

    def _construir_hijo(self, mantener: list[int], asignar: list[int], referencia: list[int]) -> list[int]:
        hijo = []
        for e in referencia:
            if e in mantener:
                hijo.append(e)
            else:
                hijo.append(asignar.pop(0))
        return hijo

    def cruce(self, padre1: list[int], padre2: list[int]) -> tuple[list[int], list[int]]:
        tam = len(padre1)

        hijos = (None, None)
        if self.__cruce == "MOC":
            pivote = random.randint(1, tam-1) - 1 # Va desde el primero al penúltimo, lo convertimos en índice
            hijos[0] = self._construir_hijo(mantener=padre1[:pivote], asignar=padre1[pivote+1:], referencia=padre2)
            hijos[1] = self._construir_hijo(mantener=padre2[:pivote], asignar=padre2[pivote+1:], referencia=padre1)

        elif self.__cruce == "OX2":
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
