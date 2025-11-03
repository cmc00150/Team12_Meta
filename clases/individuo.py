class Individuo:
    def __init__(self, permutacion=[], costo=-1, generacion=-1):
        self.__permutacion = permutacion
        self.__costo = costo
        self.__generacion = generacion
        self.__evaluado = False

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