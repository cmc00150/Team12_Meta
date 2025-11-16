from pathlib import Path
from clases.poblacion import (Individuo, Poblacion)

class Log:
    def __init__(self, algoritmo, datos, semilla, k, prc_aleat, tampoblacion, kbest, prc_cruce, tipoCruce, 
                 prc_mutacion, kworst, maxEvaluaciones, maxSegundos, numelites=-1):
        
        self.__algoritmo = algoritmo
        self.__datos = Path(datos)
        self.__lineas = []
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

        self.__lineas.append(f' LOGS ALGORITMO {self.__algoritmo.upper()}' .center(100, '-'))
        self.__lineas.append(f' ARCHIVO DE DATOS: {self.__datos}'.center(100,' '))

        self.__lineas.append(f' SEMILLA: {self.__semilla}'.center(100,' '))
        self.__lineas.append(f' K: {self.__k}'.center(100, ' '))
        self.__lineas.append(f' % INDIVIDUOS ALEATORIOS: {self.__prc_aleat}'.center(100, ' '))
        self.__lineas.append(f' TAMAÑO POBLACIÓN: {self.__tampoblacion}'.center(100, ' '))

        if(numelites > 0):
            self.__lineas.append(f' NÚMERO DE ÉLITES: {self.__numelites}'.center(100, ' '))

        self.__lineas.append(f' K MEJORES: {self.__kbest}'.center(100, ' '))
        self.__lineas.append(f' % CRUCE: {self.__prc_cruce}'.center(100, ' '))
        self.__lineas.append(f' TIPO DE CRUCE: {self.__tipoCruce}'.center(100, ' '))
        self.__lineas.append(f' % MUTACIÓN: {self.__prc_mutacion}'.center(100, ' '))
        self.__lineas.append(f' K PEORES: {self.__kworst}'.center(100, ' '))
        self.__lineas.append(f' MÁXIMO DE EVALUACIONES: {self.__maxEvaluaciones}'.center(100, ' '))
        self.__lineas.append(f' MÁXIMO DE SEGUNDOS: {self.__maxSegundos}'.center(100, ' '))
        
        self.__lineas.append(f'-'.center(100,'-'))

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
            arch.write('\n'.join(self.__lineas)) # Unimos todas las lineas con un salto de linea

    def registrarGeneracion(self, nuevaGeneracion: Poblacion, numGeneracion):
        indvs = nuevaGeneracion.getIndividuos
        elts = nuevaGeneracion.getElites if hasattr(nuevaGeneracion, 'getElites') else []

        self.__lineas.append(f'\t'+f' GENERACION {numGeneracion} '.center(40,'g'))

        for i in range (0,nuevaGeneracion.getTamPoblacion):
            self.__lineas.append(f'{indvs[i]}')

        if(len(elts) == 0): # Algoritmo estacionario. No tiene élites
            return
            
        self.__lineas.append(f'\t'+f' ÉLITES DE LA GENERACIÓN {numGeneracion} '.center(40,'e'))  

        for i in range (0,len(elts)):
            self.__lineas.append(f'{elts[i][0]}')

        self.__lineas.append(f'\t'+'e'.center(40,'e'))

    def registrarSolucion(self, nuevaSolucion: tuple[Individuo, float], numEvaluaciones=-1):
        """
        Añade una solución FINAL al contenido del fichero: la permutación, costo de evaluación, generación y tiempo de ejecución
        """
        tiempo = f"{nuevaSolucion[1]:.4f}" # Ajusto el tiempo para que se muestre en s aproximando al 4to  

        self.__lineas.append('\n')
        self.__lineas.append(f'-'.center(100,'-'))
        self.__lineas.append(f'Asignación: {[elem+1 for elem in nuevaSolucion[0].getPermutacion]}')
        self.__lineas.append(f'Costo: {nuevaSolucion[0].getCosto}')
        self.__lineas.append(f'Generacion: {nuevaSolucion[0].getGeneracion}')
        self.__lineas.append(f'Tiempo de ejecución: {tiempo}s')
        
        if numEvaluaciones > -1:
            self.__lineas.append(f' FIN POR LÍMITE DE EVALUACIONES: {numEvaluaciones} '.center(100,' '))

        else:
            self.__lineas.append(f' FIN POR LÍMITE DE TIEMPO: {tiempo} '.center(100,' '))

        self.__lineas.append(f'-'.center(100,'-'))

    def registrarCruce (self, p1: Individuo, p2: Individuo, hijos: tuple[Individuo, Individuo]):
        self.__lineas.append(f'\t\tCruce:')
        self.__lineas.append(f'\t\t  Padre1: {p1.getPermutacion}')
        self.__lineas.append(f'\t\t  Padre2: {p2.getPermutacion}')

        for i in range(2):
            self.__lineas.append(f'\t\t\tHijo {i+1}: {hijos[i].getPermutacion}')
            self.__lineas.append(f'\t\t\t\t\tCosto: {hijos[i].getCosto}')
            self.__lineas.append(f'\t\t\t\t\tGeneracion: {hijos[i].getGeneracion}')

    def registrarMutacion(self, posi, posj, nuevoInd: Individuo):
        self.__lineas.append(f'\t\tMutacion: cambian las posiciones [{posi} - {posj}]')
        self.__lineas.append(f'\t\t\tNueva permutacion: {[elem+1 for elem in nuevoInd.getPermutacion]}')
        self.__lineas.append(f'\t\t\tCosto: {nuevoInd.getCosto}')
        self.__lineas.append(f'\t\t\tGeneracion: {nuevoInd.getGeneracion}')
        pass

    def registrarReemplazo(self):
        self.__lineas.append(f'\t\tReemplazo de población finalizado\n')