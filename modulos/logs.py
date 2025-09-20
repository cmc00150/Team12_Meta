from modulos.heuristicas import costo

def error(mensaje:str):
      print('[!] Error -',mensaje)

def mostrarResultados(config, dataset, algoritmo, result):
    print(f" RESULTADOS ALGORITMO {algoritmo.upper()} ".center(50, '-'), '\n')
    for r, archivo, instancia in zip(result, config.data, dataset):
            tiempo = f"{r[1]*1000:.4f}" # Ajusto el tiempo para que se muestre en ms aproximando al 4to        
            print("  Archivo:", archivo,
            "\n  Asignacion:", [elem+1 for elem in r[0]], 
            "\n  Costo:", costo(r[0],instancia.flujos, instancia.distancias),
            "\n  Tiempo de ejecucion:",tiempo,"ms\n")
