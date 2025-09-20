from modulos.heuristicas import costo

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
  * i: Parámetro opcional, [Default: -1]. Indica el número de iteración en la que se ha obtenido el resultado. Se utiliza en algoritmos que tengan que ejecutarse más de una vez
  * k: Parámetro opcional, [Default: -1]. Establece el rango para aplicar la aleatoriedad dentro del greedy_aleatorio
"""
def mostrarResultados(config, dataset, algoritmo, result, semilla=-1, i=-1, k=-1):
    print(f" RESULTADOS ALGORITMO {algoritmo.upper()} ".center(50, '-'))
    if i>=0:
          print(f" ITERACION NUMERO {i+1} ".center(50, '-'), '\n')

    for r, archivo, instancia in zip(result, config.data, dataset):
            tiempo = f"{r[1]*1000:.4f}" # Ajusto el tiempo para que se muestre en ms aproximando al 4to        
            print("  Archivo:", archivo)

            if semilla > 0:
                  print("  Semilla:",semilla)
            
            if k > 0:
                  print("  k:",k)
                  
            print("  Asignacion:", [elem+1 for elem in r[0]], 
                  "\n  Costo:", costo(r[0],instancia.flujos, instancia.distancias),
                  "\n  Tiempo de ejecucion:",tiempo,"ms\n")