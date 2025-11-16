def analizar_costes(nombre_archivo):
    """
    Analiza el archivo de logs del algoritmo evolutivo y encuentra el menor coste.
    """
    menor_costo = float('inf')
    linea_menor_costo = None
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
                        linea_menor_costo = i
                        
                        # Buscar la permutación en la línea anterior
                        if i > 1 and 'Permutacion:' in lineas[i-2]:
                            permutacion_menor = lineas[i-2].split('Permutacion:')[1].strip()
                            if 'Generacion:' in lineas[i-3]: # Buscar la generación
                                generacion_menor = lineas[i-3].split('Generacion:')[1].strip()
                            
                except (ValueError, IndexError):
                    continue
        
        # Extraer la información final del archivo (buscar desde el final)
        for i in range(len(lineas)-1, -1, -1):
            linea = lineas[i]
            
            # Buscar "AsignaciÃ³n:" (puede tener diferentes encodings)
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
        
        # Mostrar resultados
        print("\n" + "="*70)
        print("ANÁLISIS DEL ARCHIVO DE LOGS DEL ALGORITMO EVOLUTIVO")
        print("="*70)
        print("MEJOR SOLUCIÓN ENCONTRADA")
        print(f"{'─'*70}")
        print(f"  Permutación: {permutacion_menor if permutacion_menor else 'No encontrada'}")
        print(f"  Coste:       {menor_costo}")
        print(f"  Generación:  {generacion_menor if generacion_menor else 'No encontrada'}")
        print(f"  Línea:       {linea_menor_costo}")
        
        print(f"\n{'─'*70}")
        print("SOLUCIÓN FINAL REPORTADA")
        print(f"{'─'*70}")
        print(f"  Permutación: {permutacion_final if permutacion_final else 'No encontrada'}")
        print(f"  Coste:       {costo_final if costo_final else 'No encontrado'}")
        print(f"  Generación:  {generacion_final if generacion_final else 'No encontrada'}")
        
        print(f"\n{'─'*70}")
        print("VERIFICACIÓN")
        print(f"{'─'*70}")
        if costo_final:
            if costo_final == menor_costo:
                print("  ✅ CORRECTO: El coste final coincide con el mejor encontrado.")
            else:
                print(f"  ❌ INCORRECTO: El coste final ({costo_final}) NO coincide")
                print(f"     con el mejor encontrado ({menor_costo}).")
                print(f"     Diferencia: {abs(costo_final - menor_costo)}")
        else:
            print("  ❌ No se pudo extraer el coste final del archivo.")
        
        print("="*70 + "\n")
        
        return {
            'mejor_costo': menor_costo,
            'linea': linea_menor_costo,
            'costo_final': costo_final,
            'coinciden': costo_final == menor_costo if costo_final else None
        }
        
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{nombre_archivo}'")
        return None
    except Exception as e:
        print(f"❌ Error al procesar el archivo: {e}")
        return None


# Ejecutar el análisis
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("❌ Error: Debe proporcionar el nombre del archivo como parámetro.")
        print("\nUso: python script.py <nombre_archivo>")
        print("Ejemplo: python script.py evolutivo_generacional_ford01.txt")
        sys.exit(1)
    
    archivo = sys.argv[1]
    resultado = analizar_costes(archivo)