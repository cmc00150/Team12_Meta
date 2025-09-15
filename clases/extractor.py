class extractor:
    def __init__(self, archivo):
        self.flujos: list = []
        self.distancias: list = []
        self.dimension: int = 0

        try: 
            with open(archivo, mode="r") as fichero:
                lines = fichero.readlines()
                try:
                    self.dimension = int(lines.pop(0)) # Cogemos la dimensión
                    if self.dimension < 0: 
                        raise Exception()
                except:
                    print("Error en la dimensión del archivo")
                    exit(1)
                lines.pop(0) # Quitamos el espacio en blanco

                seccion = 1 # Para saber en que matriz nos encontramos, 1.Flujos 2.Distancias
                rows = 0
                for line in lines:
                    if line == "\n": # Cambiamos de seccion
                        seccion += 1
                        rows=0
                        continue # Saltamos a la siguiente linea

                    cols = 0
                    try:
                        row = [int(n) for n in line.split()]
                        cols = len(row)
                    except Exception as e:
                        print("Las matrices solo deben contener números [", e, "]")
                        exit(1)

                    if cols != self.dimension: 
                        print("No se ha cumplido la dimensión establecida, ", cols, " columnas y una dimensión de ", self.dimension)
                        exit(1)

                    if seccion == 1:
                        self.flujos.append(row)
                    elif seccion == 2:
                        self.distancias.append(row)
                    rows += 1
                if rows != self.dimension:
                    print("No se ha cumplido la dimensión establecida, ", rows, " filas y una dimensión de ", self.dimension)
                    exit(1)
                        
            if seccion != 2:
                print("Debe haber dos matrices")
                exit(1)

        except Exception as e:
            print("Error con el archivo pasado", e)
            exit(1)  