from pathlib import Path
"""
    CLASE PRINCIPAL PARA GUARDAR LOS LOGS DE CADA ALGORITMO EN ARCHIVOS DE TEXTO
    Guarda en un fichero de texto con formato 'nombreAlgoritmo_nombreFicheroDatos_semilla' los resultados obtenidos tras la ejecución de los diferentes algoritmos
    Al principio de los logs se incluirá el nombre del algoritmo, el archivo de datos utilizado, la semilla (opcional) y el parámetro k (opcional)
    En el cuerpo de los archivos se encontrarán las asignaciones, costo y tiempo de ejecución a lo largo de la ejecución de los algoritmos
"""

class Log:
    """
    Constructor parametrizado
        algoritmo: Nombre del algoritmo para generar el log [x]
        datos: Nombre del fichero de datos con el que se ejecutará [x]
        semilla: Semilla a utilizar en caso de emplear aleatoriedad [x][o] (Se inicializa a -1)
        k: Parámetro extra para utilizar en algoritmo greedy_aleatorizado [o] (Se inicializa a -1)

    NOTA: Los parámetros clasificados con [x] serán incluidos para generar el nombre del archivo
          Los parámetros clasificados con [o] son opcionales y podrán omitirse en caso necesario
    """
    def __init__(self, algoritmo, datos, semilla=-1, k=-1):
        self.__algoritmo=algoritmo
        self.__datos=Path(datos)
        self.__texto=''
        self.__semilla=int(semilla)
        self.__k=int(k)

        self.__texto+=f' LOGS ALGORITMO {self.__algoritmo.upper()}' .center(100, '-')
        self.__texto+='\n'
        self.__texto+=f' ARCHIVO DE DATOS: {self.__datos}'.center(100,' ')
        self.__texto+='\n'    

        if self.__semilla > 0:
            self.__texto+=f' SEMILLA: {self.__semilla}'.center(100,' ')
            self.__texto+='\n'

        if self.__k > 0:
            self.__texto+=f' K: {k}'.center(100,' ')
            self.__texto+='\n'
        
        self.__texto+=f'-'.center(100,'-')
        self.__texto+='\n'

    """
    Función para generar logs
        Genera un archivo de texto con el nombre algoritmo_nombreArchivoDatos_semilla, (donde semilla es un parámetro opcional) en la carpeta logs
        Permite llevar un registro de la evolución de los algoritmos
    """
    def generaLogs(self):
        carpetaActual=Path(__file__).parent # Obtengo la carpeta actual para salir luego a la carpeta padre y acceder a la carpeta logs
        
        nombreDatos=self.__datos.stem
        nombreArchivo=self.__algoritmo+'_'+nombreDatos
        if(self.__semilla > 0):
            nombreArchivo+='_'+str(self.__semilla)

        ruta=carpetaActual.parent/'logs'/nombreArchivo

        with open(ruta,'w',encoding='utf-8') as arch:
            arch.write(self.__texto)

    """
    Añade una solución FINAL al contenido del fichero, incluyendo la permutación, costo de evaluación y tiempo de ejecución
    """
    def registrarSolucion(self, nuevaSolucion: tuple[list[int], float], costo):
        tiempo = f"{nuevaSolucion[1]*1000:.4f}" # Ajusto el tiempo para que se muestre en s aproximando al 4to  
        self.__texto+=f' Asignación: {[elem+1 for elem in nuevaSolucion[0]]}'      
        self.__texto+=f'\n Costo: {costo}'
        self.__texto+=f'\n Tiempo de ejecución: {tiempo}s'

    """
    Añade una solución INICIAL al contenido del fichero, incluyendo la permutación y costo de evaluación
    """
    def registrarSolucionInicial(self, solInicial: list[int], costo):
        self.__texto+=f' Asignación Inicial: {[elem+1 for elem in solInicial]}'      
        self.__texto+=f'\n Costo Inicial: {costo}\n\n'

    """
    Añade una solución INTERMEDIA al contenido del fichero, incluyendo los elementos intercambiados (2-OPT), la nueva permutación, su costo de evaluación y la iteración en la que se ha producido el cambio
    Se utiliza para registrar los cambios en el algoritmo busqueda_local_dlb
    """
    def registraCambioBLocal(self, posi, posj, nuevasol, nuevoCoste, iteracion):
        self.__texto+=f'\tIteración {iteracion}: cambia el par ({nuevasol[posi]+1},{nuevasol[posj]+1})\n'
        self.__texto+=f'\tAsignación: {[elem+1 for elem in nuevasol]}\n'      
        self.__texto+=f'\tCosto: {nuevoCoste}\n\n'