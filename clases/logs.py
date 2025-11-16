from pathlib import Path
from clases.poblacion import (Individuo, Poblacion)

class Log:
    def __init__(self, algoritmo, datos, semilla, k, prc_aleat, tampoblacion, kbest, prc_cruce, tipoCruce, 
                 prc_mutacion, kworst, maxEvaluaciones, maxSegundos, numelites=-1):
        
        self.__algoritmo = algoritmo
        self.__datos = Path(datos)
        self.__texto = ''
        self.__semilla = int(semilla)
        self.__k = k
        self.__prc_aleat = prc_aleat
        self.__tampoblacion = tampoblacion
        self.__numelites = numelites
        self.__kbest = kbest
        self.__prc_cruce = prc_cruce
        self.__tipoCruce = tipoCruce
        self.__prc_mutacion = prc_mutacion
        self.__kworst = kworst
        self.__maxEvaluaciones = maxEvaluaciones
        self.__maxSegundos = maxSegundos

        self.__texto+=f' LOGS ALGORITMO {self.__algoritmo.upper()}' .center(100, '-')
        self.__texto+='\n'
        self.__texto+=f' ARCHIVO DE DATOS: {self.__datos}'.center(100,' ')
        self.__texto+='\n'    

        self.__texto+=f' SEMILLA: {self.__semilla}'.center(100,' ')
        self.__texto+='\n'
        self.__texto+=f' K: {self.__k}'.center(100, ' ')
        self.__texto+='\n'
        self.__texto+=f' % INDIVIDUOS ALEATORIOS: {self.__prc_aleat}'.center(100, ' ')
        self.__texto+='\n'
        self.__texto+=f' TAMAÑO POBLACIÓN: {self.__tampoblacion}'.center(100, ' ')
        self.__texto+='\n'

        if(numelites > 0):
            self.__texto+=f' NÚMERO DE ÉLITES: {self.__numelites}'.center(100, ' ')
            self.__texto+='\n'

        self.__texto+=f' K MEJORES: {self.__kbest}'.center(100, ' ')
        self.__texto+='\n'
        self.__texto+=f' % CRUCE: {self.__prc_cruce}'.center(100, ' ')
        self.__texto+='\n'
        self.__texto+=f' TIPO DE CRUCE: {self.__tipoCruce}'.center(100, ' ')
        self.__texto+='\n'
        self.__texto+=f' % MUTACIÓN: {self.__prc_mutacion}'.center(100, ' ')
        self.__texto+='\n'
        self.__texto+=f' K PEORES: {self.__kworst}'.center(100, ' ')
        self.__texto+='\n'
        self.__texto+=f' MÁXIMO DE EVALUACIONES: {self.__maxEvaluaciones}'.center(100, ' ')
        self.__texto+='\n'
        self.__texto+=f' MÁXIMO DE SEGUNDOS: {self.__maxSegundos}'.center(100, ' ')
        self.__texto+='\n'
        
        self.__texto+=f'-'.center(100,'-')
        self.__texto+='\n'

    def generaLogs(self):
        carpetaActual=Path(__file__).parent # Obtengo la carpeta actual para salir luego a la carpeta padre y acceder a la carpeta logs
        
        nombreDatos=self.__datos.stem
        nombreArchivo=self.__algoritmo+'_'+nombreDatos+'_'+str(self.__semilla)+'_'+self.__tipoCruce
        if(self.__numelites > 0):
            nombreArchivo+='_E'+str(self.__numelites)

        nombreArchivo+='_kB'+str(self.__kbest)
        nombreArchivo+='.txt'

        ruta=carpetaActual.parent/'logs'/nombreArchivo

        with open(ruta,'w',encoding='utf-8') as arch:
            arch.write(self.__texto)

    def registrarGeneracion(self, nuevaGeneracion: Poblacion, numGeneracion):
        indvs = nuevaGeneracion.getIndividuos
        elts = nuevaGeneracion.getElites if hasattr(nuevaGeneracion, 'getElites') else []

        self.__texto+=f'\t'+f' GENERACION {numGeneracion} '.center(40,'g')
        self.__texto+='\n'

        for i in range (0,nuevaGeneracion.getTamPoblacion):
            self.__texto+=f'{indvs[i]}'

        if(len(elts) == 0): # Algoritmo estacionario. No tiene élites
            self.__texto+='\n\n\n'
            return
        
        self.__texto+='\n'        
        self.__texto+=f'\t'+f' ÉLITES DE LA GENERACIÓN {numGeneracion} '.center(40,'e')
        self.__texto+='\n'        

        for i in range (0,len(elts)):
            self.__texto+=f'{elts[i][0]}'

        self.__texto+=f'\t'+'e'.center(40,'e')
        self.__texto+='\n\n\n'        

    def registrarSolucion(self, nuevaSolucion: tuple[Individuo, float]):
        """
        Añade una solución FINAL al contenido del fichero: la permutación, costo de evaluación, generación y tiempo de ejecución
        """
        tiempo = f"{nuevaSolucion[1]:.4f}" # Ajusto el tiempo para que se muestre en s aproximando al 4to  
        ind = nuevaSolucion[0]
        self.__texto+=f' Asignación: {[elem+1 for elem in ind.getPermutacion]}'      
        self.__texto+=f'\n Costo: {ind.getCosto}'
        self.__texto+=f'\n Generacion: {ind.getGeneracion}'
        self.__texto+=f'\n Tiempo de ejecución: {tiempo}s'