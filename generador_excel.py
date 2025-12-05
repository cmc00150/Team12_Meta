import os
import re
from pathlib import Path
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
import statistics

def leer_costo_optimo(archivo_datos, carpeta_datos='Datos'):
    """Lee el costo óptimo de un archivo .sln"""
    try:
        ruta = Path(carpeta_datos) / archivo_datos
        with open(ruta, 'r') as f:
            primera_linea = f.readline().strip()
            partes = primera_linea.split()
            if len(partes) >= 2:
                return int(partes[1])
    except Exception as e:
        print(f"Error leyendo {archivo_datos}: {e}")
    return None

def extraer_info_log(archivo_log):
    """Extrae información relevante del archivo de log"""
    try:
        with open(archivo_log, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Buscar la sección "SOLUCIÓN FINAL" y extraer costo y tiempo de ahí
        # Esto asegura que tomamos los valores finales correctos
        match_solucion = re.search(r'SOLUCIÓN FINAL.*?Costo:\s*(\d+)\s*\|\s*Gen:\s*\d+\s*\|\s*Tiempo:\s*([\d.]+)s', contenido, re.DOTALL)
        
        if match_solucion:
            costo = int(match_solucion.group(1))
            tiempo = float(match_solucion.group(2))
        else:
            # Fallback: buscar cualquier ocurrencia (por compatibilidad)
            match_costo = re.search(r'Costo:\s*(\d+)', contenido)
            costo = int(match_costo.group(1)) if match_costo else None
            
            match_tiempo = re.search(r'Tiempo:\s*([\d.]+)s', contenido)
            tiempo = float(match_tiempo.group(1)) if match_tiempo else None
        
        # Extraer semilla (si existe en el nombre del archivo).
        # Soporta formatos como "_12255133" o "_S12255133" y variantes con '-' en lugar de '_'.
        nombre_archivo = os.path.basename(str(archivo_log))
        match_semilla = re.search(r'[_-]S?(\d{6,})(?:_|\.txt|$)', nombre_archivo, re.IGNORECASE)
        semilla = match_semilla.group(1) if match_semilla else None
        
        return {
            'costo': costo,
            'tiempo': tiempo,
            'semilla': semilla
        }
    except Exception as e:
        print(f"Error procesando {archivo_log}: {e}")
        return None

def agrupar_archivos_logs(carpeta_logs='Logs'):
    """Agrupa los archivos de log por tipo de algoritmo y archivo de datos"""
    grupos = {}
    for archivo in Path(carpeta_logs).glob('*.txt'):
        nombre = archivo.stem

        # Separar por '_' o '-'
        partes = re.split(r'[_-]', nombre)

        # Buscar la parte que parece un nombre de instancia (ej. 'ford01' o 'ford01.sln')
        data_idx = None
        for i, p in enumerate(partes):
            if re.match(r'^[A-Za-z]+\d+(?:\.sln)?$', p, re.IGNORECASE):
                data_idx = i
                break

        # Si no hemos encontrado, buscar heurísticamente 'ford' dentro de una parte
        if data_idx is None:
            for i, p in enumerate(partes):
                if 'ford' in p.lower():
                    data_idx = i
                    break

        # Fallback a la posición 2 si sigue sin detectarse
        if data_idx is None and len(partes) >= 3:
            data_idx = 2

        if data_idx is None:
            continue

        archivo_datos = partes[data_idx]
        # Normalizar: quitar extensión si la tiene
        if archivo_datos.lower().endswith('.sln'):
            archivo_datos = archivo_datos[:-4]

        # Determinar tipo y variante (si la variante no coincide con el archivo_datos)
        tipo = partes[0] if len(partes) > 0 else ''
        variante = ''
        if len(partes) > 1 and partes[1] != archivo_datos:
            variante = partes[1]

        # Separar semilla e info_extra a partir de lo que viene después del archivo_datos
        semilla = None
        info_extra_parts = []
        for token in partes[data_idx+1:]:
            token_digits = re.sub(r'^[Ss]', '', token)
            if token_digits.isdigit() and len(token_digits) >= 6 and semilla is None:
                semilla = token_digits
                continue
            info_extra_parts.append(token)

        info_extra = '_'.join(info_extra_parts) if info_extra_parts else ''

        # Construir clave de grupo (sin semilla)
        if variante:
            clave = f"{tipo}_{variante}_{info_extra}" if info_extra else f"{tipo}_{variante}"
        else:
            clave = f"{tipo}_{info_extra}" if info_extra else tipo

        if clave not in grupos:
            grupos[clave] = {}

        if archivo_datos not in grupos[clave]:
            grupos[clave][archivo_datos] = []

        grupos[clave][archivo_datos].append(str(archivo))
    
    return grupos

def crear_hoja_resumen(ws, nombre_configuracion, grupo_datos, carpeta_datos='Datos'):
    """Compatibilidad: ya no se crea una hoja por grupo.
    Esta función mantiene la firma antigua llamando a la función
    `crear_tabla_en_hoja` con `start_col=1` en una hoja ya existente.
    """
    crear_tabla_en_hoja(ws, 1, nombre_configuracion, grupo_datos, carpeta_datos, start_row=1)


def crear_tabla_en_hoja(ws, start_col, nombre_configuracion, grupo_datos, carpeta_datos='Datos', start_row=1):
    """Dibuja la tabla de resumen en la hoja `ws` empezando en la columna `start_col` y fila `start_row`.
    Devuelve (num_columnas_ocupadas, num_filas_ocupadas).
    """
    archivos_datos = sorted(grupo_datos.keys())
    num_columnas = len(archivos_datos) * 2 + 2  # 2 por archivo + etiqueta + semilla

    ultima_col_titulo = max(8, num_columnas)
    end_col = start_col + ultima_col_titulo - 1
    # Escribir el valor en la celda superior izquierda antes de fusionar
    cell_config = ws.cell(row=start_row, column=start_col)
    cell_config.value = nombre_configuracion.upper().replace('_', ' ')
    cell_config.font = Font(bold=True, size=14, color="FFFFFF")
    cell_config.alignment = Alignment(horizontal='center', vertical='center')
    cell_config.fill = PatternFill(start_color="3F9E5E", end_color="3F9E5E", fill_type="solid")
    ws.merge_cells(start_row=start_row, start_column=start_col, end_row=start_row, end_column=end_col)

    fila_actual = start_row + 1

    # Fila 2: Nombres de archivos
    col = start_col
    ws.cell(row=fila_actual, column=col).value = ''
    col += 1

    for arch in archivos_datos:
        nombre_upper = arch.upper().replace('.SLN', '')
        ws.merge_cells(start_row=fila_actual, start_column=col, end_row=fila_actual, end_column=col+1)
        cell = ws.cell(row=fila_actual, column=col)
        cell.value = nombre_upper
        cell.font = Font(bold=True, size=12)
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.fill = PatternFill(start_color="70C78D", end_color="70C78D", fill_type="solid")
        col += 2

    ws.cell(row=fila_actual, column=col).value = ''
    fila_actual += 1

    # Fila 3: Tamaño
    col = start_col
    ws.cell(row=fila_actual, column=col).value = 'GREEDY AL'
    ws.cell(row=fila_actual, column=col).font = Font(bold=True)
    col += 1

    for arch_datos in archivos_datos:
        arch_sln = f"{arch_datos}.sln" if not arch_datos.endswith('.sln') else arch_datos
        try:
            ruta = Path(carpeta_datos) / arch_sln
            with open(ruta, 'r') as f:
                primera_linea = f.readline().strip()
                tamaño = int(primera_linea.split()[0])
        except:
            tamaño = '?'

        ws.cell(row=fila_actual, column=col).value = 'Tamaño'
        ws.cell(row=fila_actual, column=col+1).value = tamaño
        col += 2

    ws.cell(row=fila_actual, column=col).value = ''
    fila_actual += 1

    # Fila 4: Minimo global
    col = start_col
    ws.cell(row=fila_actual, column=col).value = ''
    col += 1

    for arch_datos in archivos_datos:
        arch_sln = f"{arch_datos}.sln" if not arch_datos.endswith('.sln') else arch_datos
        costo_optimo = leer_costo_optimo(arch_sln, carpeta_datos)

        ws.cell(row=fila_actual, column=col).value = 'Minimo global'
        ws.cell(row=fila_actual, column=col+1).value = costo_optimo if costo_optimo else '?'
        col += 2

    ws.cell(row=fila_actual, column=col).value = ''
    fila_actual += 1
    fila_actual += 1  # fila vacía

    # Encabezados
    col = start_col
    ws.cell(row=fila_actual, column=col).value = ''
    col += 1

    for _ in archivos_datos:
        cell_sol = ws.cell(row=fila_actual, column=col)
        cell_sol.value = 'Sol'
        cell_sol.font = Font(bold=True, italic=True)
        cell_sol.fill = PatternFill(start_color="A8D5BA", end_color="A8D5BA", fill_type="solid")

        cell_time = ws.cell(row=fila_actual, column=col+1)
        cell_time.value = 'Time'
        cell_time.font = Font(bold=True, italic=True)
        cell_time.fill = PatternFill(start_color="A8D5BA", end_color="A8D5BA", fill_type="solid")
        col += 2

    ws.cell(row=fila_actual, column=col).value = 'Semilla'
    ws.cell(row=fila_actual, column=col).font = Font(bold=True)
    ws.cell(row=fila_actual, column=col).fill = PatternFill(start_color="A8D5BA", end_color="A8D5BA", fill_type="solid")

    fila_encabezado = fila_actual
    fila_actual += 1

    # Recopilar datos y ordenar por semilla
    datos_por_archivo = {}
    for arch_datos in archivos_datos:
        datos_por_archivo[arch_datos] = []
        for log_file in grupo_datos[arch_datos]:
            info = extraer_info_log(log_file)
            if info:
                datos_por_archivo[arch_datos].append(info)
        datos_por_archivo[arch_datos].sort(key=lambda x: x['semilla'] or '')

    max_ejecuciones = max((len(datos) for datos in datos_por_archivo.values()), default=0)

    # Filas de ejecuciones
    for i in range(max_ejecuciones):
        col = start_col
        ws.cell(row=fila_actual, column=col).value = f'Ejecución {i+1}'
        ws.cell(row=fila_actual, column=col).font = Font(bold=True)
        col += 1

        semilla_fila = None
        for arch_datos in archivos_datos:
            datos = datos_por_archivo[arch_datos]
            if i < len(datos):
                ws.cell(row=fila_actual, column=col).value = datos[i]['costo']
                ws.cell(row=fila_actual, column=col+1).value = datos[i]['tiempo']
                if semilla_fila is None:
                    semilla_fila = datos[i]['semilla']
            col += 2

        ws.cell(row=fila_actual, column=col).value = semilla_fila if semilla_fila else ''
        fila_actual += 1

    ultima_fila = fila_actual - 1

    # Desviación típica
    col = start_col
    ws.cell(row=fila_actual, column=col).value = 'Desv. típica'
    ws.cell(row=fila_actual, column=col).font = Font(bold=True, italic=True)
    ws.cell(row=fila_actual, column=col).fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    col += 1

    for idx_archivo, arch_datos in enumerate(archivos_datos):
        datos = datos_por_archivo[arch_datos]
        if datos:
            arch_sln = f"{arch_datos}.sln" if not arch_datos.endswith('.sln') else arch_datos
            costo_optimo = leer_costo_optimo(arch_sln, carpeta_datos)
            if costo_optimo:
                errores_relativos = [(d['costo'] - costo_optimo) / costo_optimo for d in datos if d['costo']]
                if len(errores_relativos) > 1:
                    desv_tipica = statistics.stdev(errores_relativos)
                    ws.cell(row=fila_actual, column=col).value = desv_tipica
                    ws.cell(row=fila_actual, column=col).number_format = '0.00%'
                else:
                    ws.cell(row=fila_actual, column=col).value = ''
            else:
                ws.cell(row=fila_actual, column=col).value = ''
        else:
            ws.cell(row=fila_actual, column=col).value = ''

        ws.cell(row=fila_actual, column=col).fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
        ws.cell(row=fila_actual, column=col+1).value = ''
        col += 2

    fila_desv = fila_actual
    fila_actual += 1

    # Desviación de error
    col = start_col
    ws.cell(row=fila_actual, column=col).value = 'Desviación de error'
    ws.cell(row=fila_actual, column=col).font = Font(bold=True, italic=True)
    ws.cell(row=fila_actual, column=col).fill = PatternFill(start_color="A8D5BA", end_color="A8D5BA", fill_type="solid")
    col += 1

    for idx_archivo, arch_datos in enumerate(archivos_datos):
        datos = datos_por_archivo[arch_datos]
        if datos:
            arch_sln = f"{arch_datos}.sln" if not arch_datos.endswith('.sln') else arch_datos
            costo_optimo = leer_costo_optimo(arch_sln, carpeta_datos)
            if costo_optimo:
                errores_relativos = [(d['costo'] - costo_optimo) / costo_optimo for d in datos if d['costo']]
                if errores_relativos:
                    promedio_error = statistics.mean(errores_relativos)
                    ws.cell(row=fila_actual, column=col).value = promedio_error
                    ws.cell(row=fila_actual, column=col).number_format = '0.00%'
                else:
                    ws.cell(row=fila_actual, column=col).value = ''
            else:
                ws.cell(row=fila_actual, column=col).value = ''
        else:
            ws.cell(row=fila_actual, column=col).value = ''

        ws.cell(row=fila_actual, column=col).fill = PatternFill(start_color="A8D5BA", end_color="A8D5BA", fill_type="solid")
        ws.cell(row=fila_actual, column=col+1).value = ''
        col += 2

    ws.cell(row=fila_actual, column=col).value = ''

    # Ajustar anchos de columna del bloque
    ws.column_dimensions[get_column_letter(start_col)].width = 18
    for i in range(start_col+1, start_col + len(archivos_datos) * 2 + 2):
        ws.column_dimensions[get_column_letter(i)].width = 12
    ws.column_dimensions[get_column_letter(start_col + len(archivos_datos) * 2 + 1)].width = 15

    # Aplicar bordes al bloque
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
    for row in ws.iter_rows(min_row=start_row+1, max_row=fila_actual, min_col=start_col, max_col=start_col + len(archivos_datos)*2 + 1):
        for cell in row:
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='center', vertical='center')

    num_filas_usadas = fila_actual - start_row
    return ultima_col_titulo, num_filas_usadas

def generar_excel(carpeta_logs='logs', carpeta_datos='Datos', archivo_salida='resumen.xlsx'):
    """Genera el archivo Excel con todas las tablas resumen"""
    
    # Agrupar archivos
    grupos = agrupar_archivos_logs(carpeta_logs)
    
    if not grupos:
        print("No se encontraron archivos de log para procesar.")
        return
    
    # Crear workbook con una sola hoja 'Resumen'
    wb = Workbook()
    # Usar la hoja creada por defecto y nombrarla 'Resumen'
    ws = wb.active
    ws.title = 'Resumen'

    # Agrupar las configuraciones por parámetro E extraído del nombre del log
    e_groups: dict[str, list[tuple[str, dict]]] = {}
    for nombre_grupo, datos_grupo in grupos.items():
        # Tomar el primer fichero de los archivos de datos disponibles para detectar 'E'
        primer_log = None
        for lst in datos_grupo.values():
            if lst:
                primer_log = lst[0]
                break

        e_val = 'NOE'
        if primer_log:
            m = re.search(r'[Ee](\d+)', os.path.basename(primer_log))
            if m:
                e_val = m.group(1)

        e_groups.setdefault(e_val, []).append((nombre_grupo, datos_grupo))

    # Ordenar claves E numéricas primero
    def e_sort_key(k):
        try:
            return (0, int(k))
        except:
            return (1, k)

    current_col = 1
    gap_between_blocks = 3
    gap_between_tables = 2
    # Recorrer por orden de E
    for e_key in sorted(e_groups.keys(), key=e_sort_key):
        grupos_e = e_groups[e_key]
        # Apilar tablas verticalmente dentro del mismo bloque de columnas para este E
        current_row = 1
        max_used_cols = 0
        for nombre_grupo, datos_grupo in grupos_e:
            used_cols, used_rows = crear_tabla_en_hoja(ws, current_col, nombre_grupo, datos_grupo, carpeta_datos, start_row=current_row)
            current_row += used_rows + gap_between_tables
            if used_cols > max_used_cols:
                max_used_cols = used_cols

        # Avanzar a la siguiente zona de columnas después de apilar todas las tablas de este E
        current_col += max_used_cols + gap_between_blocks
    
    # Guardar archivo
    try:
        wb.save(archivo_salida)
        print(f"✓ Excel generado exitosamente: {archivo_salida}")
        print(f"✓ Se generaron {len(grupos)} tablas agrupadas en la hoja 'Resumen'")
    except Exception as e:
        print(f"✗ Error al guardar el archivo: {e}")

# Ejecutar
if __name__ == "__main__":
    generar_excel(
        carpeta_logs='logs',
        carpeta_datos='datos',
        archivo_salida='resumen_experimentos.xlsx'
    )