from pathlib import Path
import matplotlib.pyplot as plt

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
        maxIteraciones: Número máximo de iteraciones permitidas para un algoritmo [o] (Se inicializa a -1)
        tenencia: Tenencia para utilizar en algoritmo busqueda_tabu [o] (Se inicializa a -1)
        oscilacion: Oscilacion para utilizar en algoritmo busqueda_tabu [o] (Se inicializa a -1)
        estancamiento: Estancamiento para utilizar en algoritmo busqueda_tabu [o] (Se inicializa a -1)

    NOTA: Los parámetros clasificados con [x] serán incluidos para generar el nombre del archivo
          Los parámetros clasificados con [o] son opcionales y podrán omitirse en caso necesario
    """
    def __init__(self, algoritmo, datos, semilla=-1, k=-1, maxIteraciones=-1, tenencia=-1, oscilacion=-1, estancamiento=-1):
        self.__algoritmo=algoritmo
        self.__datos=Path(datos)
        self.__texto=''
        self.__semilla=int(semilla)
        self.__k=int(k)
        self.__maxIteraciones=int(maxIteraciones)
        self.__tenencia=int(tenencia)
        self.__oscilacion=float(oscilacion)
        self.__estancamiento=float(estancamiento)


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

        if self.__maxIteraciones > 0:
            self.__texto+=f' maxIteraciones: {maxIteraciones}'.center(100,' ')
            self.__texto+='\n'

        if self.__tenencia > 0:
            self.__texto+=f' Tenencia: {tenencia}'.center(100,' ')
            self.__texto+='\n'

        if self.__oscilacion > 0:
            self.__texto+=f' Oscilacion: {oscilacion}'.center(100,' ')
            self.__texto+='\n'

        if self.__estancamiento > 0:
            self.__texto+=f' Estancamiento: {estancamiento}'.center(100,' ')
            self.__texto+='\n'
        
        self.__texto+=f'-'.center(100,'-')
        self.__texto+='\n'

    """
    Función que permite obtener un gráfico del avance del costo de la permutación en función de las iteraciones que han pasado
    Es útil para algoritmos como busqueda_local_dlb o busqueda_tabu
    """
    def dibujarGrafica(self):
        # Construir ruta del archivo de log
        carpetaActual = Path(__file__).parent
        nombreDatos = self.__datos.stem.lower()
        nombreArchivo = self.__algoritmo + '_' + nombreDatos
        if self.__semilla > 0:
            nombreArchivo += '_' + str(self.__semilla)
        nombreArchivo += '.txt'
        ruta = carpetaActual.parent / 'logs' / nombreArchivo

        # Costes óptimos por archivo
        costes_optimos = {
            "ford01": 3542,
            "ford02": 26876,
            "ford03": 13292,
            "ford04": 150528
        }
        coste_optimo = costes_optimos.get(nombreDatos, None)

        # Límites máximos del eje Y por archivo
        limites_y = {
            "ford01": 4000*1.5,
            "ford02": 40000*1.5,
            "ford03": 14000*1.5,
            "ford04": 200000*1.5
        }
        limite_superior_y = limites_y.get(nombreDatos, None)

        # Extraer datos
        iteraciones = []
        costes = []

        with open(ruta, "r", encoding="utf-8") as f:
            lineas = f.readlines()

        i = 0
        while i < len(lineas):
            linea = lineas[i].strip()
            if linea.startswith("Iteración"):
                partes = linea.split()
                num_iter = int(partes[1].replace(":", ""))-1
                while i + 1 < len(lineas):
                    i += 1
                    siguiente = lineas[i].strip()
                    if siguiente.startswith("Costo:"):
                        coste = float(siguiente.split(":")[1].strip())
                        iteraciones.append(num_iter)
                        costes.append(coste)
                        break
            i += 1

        if not iteraciones or not costes:
            print("No se encontraron datos para graficar.")
            return

        # Crear gráfico
        plt.figure(figsize=(12, 12))
        plt.plot(iteraciones, costes, color='darkgreen', linewidth=1.5, label='Costo por iteración')

        # Añadir línea roja con coste óptimo
        if coste_optimo:
            plt.axhline(coste_optimo, color='red', linestyle='--', linewidth=1.2, label=f'Coste óptimo: {coste_optimo}')

        # Configurar eje Y desde 0 hasta el límite definido
        if limite_superior_y:
            plt.ylim(0, limite_superior_y)
        else:
            # Si no hay límite definido, usar margen proporcional
            max_coste = max(costes)
            margen_superior = (max_coste - min(costes)) * 0.5
            plt.ylim(0, max_coste + margen_superior)

        # Etiquetas y leyenda
        plt.title("Evolución del coste por iteración", fontsize=14)
        plt.xlabel("Iteración")
        plt.ylabel("Costo")
        plt.grid(True)
        plt.legend()
        plt.xlim(left=0)
        plt.xlim(min(iteraciones), max(iteraciones))
        plt.tight_layout()

        # Guardar como PNG con nombre dinámico
        nombreGrafico = f"grafico_{self.__algoritmo}_{nombreDatos}"
        if self.__semilla > 0:
            nombreGrafico += f"_{self.__semilla}"
        nombreGrafico += ".png"

        rutaGrafico = carpetaActual.parent / 'logs/graficos' / nombreGrafico
        plt.savefig(rutaGrafico, format='png')
        plt.close()

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
        nombreArchivo+='.txt'

        ruta=carpetaActual.parent/'logs'/nombreArchivo

        with open(ruta,'w',encoding='utf-8') as arch:
            arch.write(self.__texto)
    """
    Añade una solución FINAL al contenido del fichero, incluyendo la permutación, costo de evaluación y tiempo de ejecución
    """
    def registrarSolucion(self, nuevaSolucion: tuple[list[int], float], costo):
        tiempo = f"{nuevaSolucion[1]:.4f}" # Ajusto el tiempo para que se muestre en s aproximando al 4to  
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

    """
    Registra cuándo se reinicializa en la búsqueda tabú, indicando si se ha hecho para intensificar o diversificar
    Se utiliza para registrar detalles en el algoritmo busqueda_tabu
    """
    def registrarReinicializacionIntensificar(self, permutacion, costo, iteracion, intensificar):
        self.__texto+='\t'
        if(intensificar):
            self.__texto+=f' Iteración {iteracion}: REINICIALIZACIÓN PARA APLICAR INTENSIFICACIÓN '.center(100,'I')
        else:
            self.__texto+=f' Iteración {iteracion}: REINICIALIZACIÓN PARA APLICAR DIVERSIFICACIÓN '.center(100,'D')
        self.__texto+='\n'
        self.__texto+=f'\tAsignación inicial: {[elem+1 for elem in permutacion]}\n'      
        self.__texto+=f'\tCosto: {costo}\n'
        if(intensificar):
            self.__texto+='\t'
            self.__texto+=f'I'.center(100,'I')
        else:
            self.__texto+='\t'
            self.__texto+=f'D'.center(100,'D')
        self.__texto+='\n\n'
    
    def registraCambioBTabu(self, posi, posj, nuevasol, nuevoCoste, mejorCoste, iteracion):
        self.__texto+=f'\tIteración {iteracion}: cambia el par ({nuevasol[posi]+1},{nuevasol[posj]+1})\n'
        self.__texto+=f'\tAsignación: {[elem+1 for elem in nuevasol]}\n'      
        self.__texto+=f'\tCosto: {nuevoCoste}\n'
        self.__texto+=f'\tMejor costo global: {mejorCoste}\n\n'