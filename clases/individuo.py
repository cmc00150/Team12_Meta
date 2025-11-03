class Individuo:
    def __init__(self, permutacion, costo, generacion):
        self.__permutacion = permutacion
        self.__costo = costo
        self.__generacion = generacion
        self.__evaluado = False

    @property
    def getIndividuo(self):
        return (self.__permutacion, self.__costo)
    
    @property
    def getGeneracion(self):
        return (self.__generacion)
    
    @property
    def getEvaluado(self):
        return (self.__evaluado)