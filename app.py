import webview
import sys
from clases.configurador import * 
from clases.extractor import *
from modulos.heuristicas import greedy

class Api:
    def __init__(self):
        self.__config = None
        self.__data = None
        self.__estado = "seleccionando"  # Estados: seleccionando, mostrando, resultado
        self.__window = None

    def set_window(self, window):
        self.__window = window

    def seleccionar_archivo(self, config_file):
        """Estado 1 -> Estado 2: Procesar archivo seleccionado"""
        try:
            print("archivo seleccionado", config_file)
            self.__config = Configurador(config_file)
            self.__data = Extractor(self.__config.data[0])

            return {
                "status": "success",
                "message": f"Archivo {config_file} procesado correctamente"
            }
        except Exception as e:
            return {
                "status": "error", 
                "message": f"Error al procesar archivo: {str(e)}"
            }

    def mostrar_configuracion(self):
        try:
          return {
              "status": "success",
              "algoritmo": self.__config.alg[0],
              "matrices": [self.__data.flujos, self.__data.distancias]
          }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error al extraer los datos del archivo {self.__config.data[0]}"
            }

    def ejecutar_algoritmo(self):
        """Estado 2 -> Estado 3: Ejecutar algoritmo y mostrar resultados"""
        try:
            if not self.__config or not self.__data:
                raise Exception("No hay datos cargados")
            
            resultado = greedy(self.__data.flujos, self.__data.distancias, self.__data.dimension)
            
            return {
                "status": "success",
                "resultado": f"Permutación: {resultado[0]}, costo: {resultado[1]}"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error al ejecutar algoritmo: {str(e)}"
            }
        
    def siguiente_estado(self):
      if self.__estado == "seleccionando":
          self.__estado = "configuracion"
          self.__window.load_html("menu/estados/comprobacion.html")
      elif self.__estado == "configuracion":
          self.__estado = "resultados"
          self.__window.load_html("menu/estados/resultados.html")
      else:
          return {
              "status": "error",
              "message" : "Estado no reconocido"
          }
    
    def salir():
        window.destroy()

if __name__ == '__main__':
    api = Api()
    window = webview.create_window('Meta App', './menu/estados/elegir_archivo.html', js_api=api)
    webview.start(api.set_window, window)
    sys.exit(0)