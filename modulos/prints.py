<<<<<<< HEAD
from .func_auxiliares import costo
=======
from modulos.func_auxiliares import costo
>>>>>>> 7d93e6507f2d84be65f1cf653b0fff0da2f14b78

def error(mensaje:str):
      print('[!] Error -',mensaje)

"""
      FUNCIÓN PRINCIPAL PARA MOSTRAR RESULTADOS POR PANTALLA
            Muestra los resultados obtenidos tras ejecutar un algoritmo, así como los detalles principales para tener claro qué se está presentando
Parámetros
  - config: Fichero de configuración. Se usa para conocer el nombre del archivo al que pertenecen los resultados
  - dataset: Fichero de datos. Se usa para poder calcular la función de evaluación una vez obtenido el resultado
  - algoritmo: Algoritmo utilizado para resolver el problema
  - result: Conjunto de resultados obtenidos tras aplicar el algoritmo a los diferentes ficheros de datos indicados en configuración
  * semilla: Parámetro opcional, [Default: -1]. Se utiliza para indicar qué semilla utilizamos en aquellos algoritmos que dependan de la aleatoriedad
  * k: Parámetro opcional, [Default: -1]. Establece el rango para aplicar la aleatoriedad dentro del greedy_aleatorio
"""
def mostrarResultados(config, dataset, algoritmo, result, semilla=-1, k=-1):
    print(f" RESULTADOS ALGORITMO {algoritmo.upper()} ".center(50, '-'))
    if semilla>0:
          print(f" SEMILLA {semilla} ".center(50, '-'), '\n')

    for r, archivo, instancia in zip(result, config.data, dataset):
      tiempo = f"{r[1]*1000:.4f}" # Ajusto el tiempo para que se muestre en ms aproximando al 4to        
      print("  Archivo:", archivo)
      
      if k > 0:
            print("  k:",k)
            
      print("  Asignacion:", [elem+1 for elem in r[0]], 
            "\n  Costo:", costo(r[0],instancia.flujos, instancia.distancias),
            "\n  Tiempo de ejecucion:",tiempo,"ms\n")

def finPrograma():
      print(' o'*50,
            '\n',
            f" FIN DEL PROGRAMA, CONSULTE LOS LOGS PARA OBTENER LOS RESULTADOS ".center(100, " "),
            '\n',
            ' o'*50)