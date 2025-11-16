def analizar_costes(nombre_archivo):
    """
    Analiza el archivo de logs del algoritmo evolutivo y encuentra el menor coste.
    Retorna un diccionario con los resultados.
    """
    menor_costo = float('inf')
    permutacion_menor = None
    generacion_menor = None
    
    permutacion_final = None
    costo_final = None
    generacion_final = None
    
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
            
        # Buscar todos los costes en el archivo
        for i, linea in enumerate(lineas, 1):
            if 'Costo:' in linea:
                try:
                    # Extraer el coste de la línea
                    costo = int(linea.split('Costo:')[1].strip())
                    
                    if costo < menor_costo:
                        menor_costo = costo
                        
                        # Buscar la permutación en la línea anterior
                        if i > 1 and 'Permutacion:' in lineas[i-2]:
                            permutacion_menor = lineas[i-2].split('Permutacion:')[1].strip()
                        
                        # Buscar la generación en la línea siguiente
                        if i < len(lineas) and 'Generacion' in lineas[i]:
                            generacion_menor = lineas[i].split('Generacion:')[1].strip().split()[0]
                except (ValueError, IndexError):
                    continue
        
        # Extraer la información final del archivo (buscar desde el final)
        for i in range(len(lineas)-1, -1, -1):
            linea = lineas[i]
            
            # Buscar "Asignación:" (puede tener diferentes encodings)
            if 'Asignaci' in linea or 'AsignaciÃ³n' in linea:
                try:
                    permutacion_final = linea.split(':')[1].strip()
                    
                    # El coste está en la siguiente línea
                    if i+1 < len(lineas) and 'Costo:' in lineas[i+1]:
                        costo_final = int(lineas[i+1].split('Costo:')[1].strip())
                    
                    # La generación puede estar en la misma línea del coste o cercana
                    # Buscar en las siguientes líneas cercanas
                    for j in range(i+1, min(i+5, len(lineas))):
                        if 'Generacion' in lineas[j] or 'generaci' in lineas[j].lower():
                            try:
                                generacion_final = lineas[j].split(':')[1].strip().split()[0]
                                break
                            except:
                                continue
                    
                    break
                except (ValueError, IndexError):
                    continue
        
        return {
            'exito': True,
            'mejor_costo': menor_costo,
            'mejor_permutacion': permutacion_menor,
            'mejor_generacion': generacion_menor,
            'final_costo': costo_final,
            'final_permutacion': permutacion_final,
            'final_generacion': generacion_final,
            'coinciden': costo_final == menor_costo if costo_final else None
        }
        
    except FileNotFoundError:
        return {
            'exito': False,
            'error': f"No se encontró el archivo '{nombre_archivo}'"
        }
    except Exception as e:
        return {
            'exito': False,
            'error': f"Error al procesar el archivo: {e}"
        }


def mostrar_resultado(nombre_archivo, resultado):
    """
    Muestra los resultados del análisis de un archivo de forma formateada.
    """
    print(f"\n{'='*70}")
    print(f"ARCHIVO: {nombre_archivo}")
    
    if not resultado['exito']:
        print(f"  ❌ ERROR: {resultado['error']}")
        return
    
    print("\nMEJOR SOLUCIÓN ENCONTRADA")
    print(f"{'─'*70}")
    print(f"  Permutación: {resultado['mejor_permutacion'] if resultado['mejor_permutacion'] else 'No encontrada'}")
    print(f"  Coste:       {resultado['mejor_costo']}")
    print(f"  Generación:  {resultado['mejor_generacion'] if resultado['mejor_generacion'] else 'No encontrada'}")
    
    print(f"\n{'─'*70}")
    print("SOLUCIÓN FINAL REPORTADA")
    print(f"{'─'*70}")
    print(f"  Permutación: {resultado['final_permutacion'] if resultado['final_permutacion'] else 'No encontrada'}")
    print(f"  Coste:       {resultado['final_costo'] if resultado['final_costo'] else 'No encontrado'}")
    print(f"  Generación:  {resultado['final_generacion'] if resultado['final_generacion'] else 'No encontrada'}")
    
    print(f"\n{'─'*70}")
    print("VERIFICACIÓN")
    print(f"{'─'*70}")
    if resultado['final_costo']:
        if resultado['coinciden']:
            print("  ✅ CORRECTO: El coste final coincide con el mejor encontrado.")
        else:
            print(f"  ❌ INCORRECTO: El coste final ({resultado['final_costo']}) NO coincide")
            print(f"     con el mejor encontrado ({resultado['mejor_costo']}).")
            print(f"     Diferencia: {abs(resultado['final_costo'] - resultado['mejor_costo'])}")
    else:
        print("  ❌ No se pudo extraer el coste final del archivo.")


def leer_archivo_listado(archivo_listado):
    """
    Lee el archivo de listado y extrae los nombres de archivos.
    Formato esperado: 
    - ficheros: fichero1 fichero2 fichero3...
    - ficheros: logs\* (para todos los archivos .txt en la carpeta logs)
    """
    import os
    from pathlib import Path
    
    try:
        with open(archivo_listado, 'r', encoding='utf-8') as f:
            contenido = f.read().strip()
        
        # Buscar la línea que empieza con "ficheros:"
        if contenido.startswith('ficheros:'):
            # Extraer los nombres de archivo después de "ficheros:"
            especificacion = contenido.split('ficheros:')[1].strip()
            
            # Verificar si es un patrón con *
            if '*' in especificacion:
                # Extraer la carpeta del patrón (ej: "logs\*" -> "logs")
                carpeta = especificacion.replace('*', '').replace('\\', '').replace('/', '').strip()
                
                # Construir la ruta absoluta a la carpeta logs
                script_dir = Path(__file__).parent
                logs_dir = script_dir / carpeta
                
                if not logs_dir.exists():
                    print(f"❌ Error: No se encontró la carpeta '{carpeta}'")
                    return []
                
                # Obtener todos los archivos .txt en la carpeta
                archivos = []
                for archivo in logs_dir.glob('*.txt'):
                    # Usar ruta relativa desde el directorio del script
                    ruta_relativa = str(archivo.relative_to(script_dir))
                    archivos.append(ruta_relativa)
                
                if not archivos:
                    print(f"⚠️  Advertencia: No se encontraron archivos .txt en '{carpeta}'")
                    return []
                
                # Ordenar los archivos alfabéticamente
                archivos.sort()
                return archivos
            else:
                # Comportamiento original: lista de archivos específicos
                archivos = especificacion.split()
                return archivos
        else:
            print(f"❌ Error: El archivo '{archivo_listado}' no tiene el formato esperado.")
            print("   Formato esperado: ficheros: fichero1 fichero2 fichero3...")
            print("   O bien: ficheros: logs\\*")
            return []
            
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{archivo_listado}'")
        return []
    except Exception as e:
        print(f"❌ Error al leer el archivo de listado: {e}")
        return []


def generar_resumen(resultados):
    """
    Genera un resumen comparativo de todos los archivos analizados.
    """
    print(f"\n\n{'='*100}")
    print("RESUMEN COMPARATIVO")
    print(f"{'='*100}\n")
    
    print(f"{'Archivo':<70} {'Mejor Coste':<15} {'Verificación'}")
    print(f"{'-'*70} {'-'*15} {'-'*15}")
    
    for archivo, resultado in resultados.items():
        if resultado['exito']:
            verificacion = "✅ OK" if resultado['coinciden'] else "❌ ERROR"
            print(f"{archivo:<70} {resultado['mejor_costo']:<15} {verificacion}")
        else:
            print(f"{archivo:<70} {'ERROR':<15} {'N/A'}")
    
    print(f"\n{'='*100}\n")


# Ejecutar el análisis
if __name__ == "__main__":
    import sys
    
    # Usar config_comprobador.txt por defecto si no se especifica otro archivo
    if len(sys.argv) < 2:
        archivo_listado = "config_comprobador.txt"
        print(f"ℹ️  Usando archivo de configuración por defecto: {archivo_listado}")
    else:
        archivo_listado = sys.argv[1]
    
    print("="*70)
    print("ANÁLISIS DE LOGS OBTENIDOS")
    print("="*70)
    
    # Leer el archivo de listado
    archivos = leer_archivo_listado(archivo_listado)
    
    if not archivos:
        print("\n❌ No se encontraron archivos para analizar.")
        sys.exit(1)
    
    print(f"Archivos a analizar: {len(archivos)}")
    for i, arch in enumerate(archivos, 1):
        print(f"  {i}. {arch}")
    
    # Analizar cada archivo
    resultados = {}
    for archivo in archivos:
        resultado = analizar_costes(archivo)
        resultados[archivo] = resultado
        mostrar_resultado(archivo, resultado)
    
    # Mostrar resumen comparativo
    generar_resumen(resultados)