from clases.individuo import Individuo

class Poblacion:
    def __init__(self, tam):
        self.__individuos = [Individuo([],-1) for _ in tam]
