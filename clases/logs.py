from pathlib import Path
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from clases.poblacion import (Individuo, Poblacion)

class SimbolosLog(str, Enum):
    MEJORA = '📈'
    EMPEORA = '📉'
    SIN_CAMBIOS = '➡️'
    CRUCE = '🔀'
    MUTACION = '🧬'
    SELECCION = '✓'
    REEMPLAZO = '♻️'
    SOLUCION = '🎉'
    ESTADISTICAS = '📊'
    CONFIGURACION = '📁'
    ELITE = '⭐'
    
    def __str__(self) -> str:
        """Devuelve el valor directamente para los prints."""
        return self.value

    def __format__(self, spec: str) -> str:
        """Permite usar f"{SimbolosLog.MEJORA:^3s}"."""
        return format(self.value, spec)

class Log():
    def __init__(self, data, seed, k, prcAleatorio, tampoblacion, numElites, kBest, prcCruce, cruce, prcMutacion, kWorst, maxEvaluaciones, maxSegundos, profundidadBT, evaluacionesBT, tenencia):
        self._data = data
        self._seed = seed
        self._k = k
        self._prcAleatorio = prcAleatorio
        self._tampoblacion = tampoblacion
        self._kBest = kBest
        self._prcCruce = prcCruce
        self._cruce = cruce.value
        self._prcMutacion = prcMutacion
        self._kWorst = kWorst
        self._maxEvaluaciones = maxEvaluaciones
        self._maxSegundos = maxSegundos
        self._numElites = numElites
        self._poblacion_previa = {}  # {idx: costo} para comparar
        self._evaluacionesTabu = evaluacionesBT
        # Acumuladores del ciclo actual
        self._poblacion_seleccionada = []
        self._parejas_cruce = []
        self._indices_mutados = set()
        # Parámetros BTABU
        self._profundidadTabu = profundidadBT
        self._tenencia = tenencia
        
        self._lineas = []
        
        # Estadísticas
        self._total_cruces = 0
        self._total_mutaciones = 0
        self._mejor_costo_previo = float('inf')

        # Encabezado compacto
        self._lineas.append('='*90)
        self._lineas.append(f' ALGORITMO MEMETICO GENERACIONAL '.center(90, '='))
        self._lineas.append('='*90)
        self._lineas.append(f'Datos: {self._data.stem} | Seed: {seed} | Cruce: {self._cruce} | Población: {tampoblacion}')
        self._lineas.append(f'k_greedy: {k} | Aleatorios: {prcAleatorio}% | k_torneo: {kBest} | Cruce: {prcCruce}% | Mutación: {prcMutacion}%')
        if self._numElites > 0:
            self._lineas.append(f'Élites: {numElites} | k_worst: {kWorst} | Max eval: {maxEvaluaciones} | Max seg: {maxSegundos}')
        else:
            self._lineas.append(f'k_worst: {kWorst} | Max eval: {maxEvaluaciones} | Max seg: {maxSegundos}')
        self._lineas.append(f'Evaluaciones BT: {evaluacionesBT} Profundidad BT: {profundidadBT} | Tenencia: {tenencia}')
        self._lineas.append('='*90)
        self._lineas.append('')

    def registrarPoblacionInicial(self, poblacion: 'Poblacion'):
        """Registra la población inicial"""
        indvs = poblacion.getIndividuos
        
        self._lineas.append('='*90)
        self._lineas.append('='+f' POBLACIÓN INICIAL '.center(88, ' ')+'=')
        self._lineas.append('='*90)
        
        for i, ind in enumerate(indvs):
            perm_str = str([x+1 for x in ind.getPermutacion][:6])[:-1] + '...]'
            self._lineas.append(f'   [{i:3d}]  {perm_str:30s}  |  Costo: {ind.getCosto:>6.0f}  |  Gen: {ind.getGeneracion:>2d}')
        
        costos = [ind.getCosto for ind in indvs]
        mejor = min(costos)
        peor = max(costos)
        promedio = sum(costos) / len(costos)
        
        self._lineas.append('')
        self._lineas.append(f'   → Mejor: {mejor:.0f} | Promedio: {promedio:.0f} | Peor: {peor:.0f}')
        self._lineas.append('='*90)

    def registrarSolucion(self, solucion: tuple['Individuo', float], evaluaciones: int):
        """Registra la solución final"""
        individuo, tiempo = solucion
        
        self._lineas.append('')
        self._lineas.append('='*90)
        self._lineas.append('='+f' SOLUCIÓN FINAL '.center(88, ' ')+'=')
        self._lineas.append('='*90)
        self._lineas.append(f'Permutación: {[x+1 for x in individuo.getPermutacion]}')
        self._lineas.append(f'Costo: {individuo.getCosto} | Gen: {individuo.getGeneracion} | Tiempo: {tiempo:.4f}s')
        
        if evaluaciones:
            self._lineas.append(f'Evaluaciones: {evaluaciones} | Cruces: {self._total_cruces} | Mutaciones: {self._total_mutaciones}')
            self._lineas.append(f'FIN POR LÍMITE DE EVALUACIONES ({evaluaciones})')
        else:
            self._lineas.append(f'Cruces: {self._total_cruces} | Mutaciones: {self._total_mutaciones}')
            self._lineas.append(f'FIN POR LÍMITE DE TIEMPO ({tiempo:.4f}s)')
        
        self._lineas.append('='*90)

    def iniciarCiclo(self, poblacion_seleccionada: list['Individuo']):
        """Inicia un nuevo ciclo guardando la población seleccionada"""
        self._poblacion_seleccionada = poblacion_seleccionada
        self._parejas_cruce = []
        self._indices_mutados = set()
        
        # Guardar costos previos para comparación en reemplazo
        self._poblacion_previa = {i: ind.getCosto for i, ind in enumerate(poblacion_seleccionada)}
    
    def registrarCruce(self, idx1: int, idx2: int):
        """Registra que los índices idx1 e idx2 se cruzaron"""
        self._parejas_cruce.append((idx1, idx2))
        self._total_cruces += 1
    
    def registrarMutacion(self, idx: int):
        """Registra que el índice idx mutó"""
        self._indices_mutados.add(idx)
        self._total_mutaciones += 1
    
    def finalizarSeleccion(self):
        """Genera el log de selección con toda la info acumulada"""
        self._lineas.append('')
        self._lineas.append(f'{SimbolosLog.SELECCION} SELECCIÓN ({len(self._poblacion_seleccionada)} individuos):')
        
        # Crear mapeo de índices a número de cruce
        idx_to_cruce = {}
        for num_cruce, (i1, i2) in enumerate(self._parejas_cruce, 1):
            idx_to_cruce[i1] = num_cruce
            idx_to_cruce[i2] = num_cruce
        
        # Determinar el número máximo de cruces para formateo
        max_cruce = max(idx_to_cruce.values()) if idx_to_cruce else 0
        cruce_width = len(str(max_cruce))
        
        for i, ind in enumerate(self._poblacion_seleccionada):
            # Marca de mutación (con espacios de sobra)
            marca_mut = f'{SimbolosLog.MUTACION} ' if i in self._indices_mutados else '   '
            
            # Marca de cruce con pareja visual: ╟─1─╢ para parejas
            if i in idx_to_cruce:
                num_cruce = idx_to_cruce[i]
                # Determinar si es el primero o segundo de la pareja
                pareja = self._parejas_cruce[num_cruce - 1]
                if i == pareja[0]:
                    marca_cruce = f'╔═'
                else:
                    marca_cruce = f'╚═'
            else:
                marca_cruce = ' ' * (cruce_width)
            
            perm_str = str([x+1 for x in ind.getPermutacion][:6])[:-1] + '...]'
            
            ind_costo = 'None' if not ind.getCosto else f'{ind.getCosto:>6.0f}'
            # Formato con alineación generosa
            self._lineas.append(f'{marca_mut}{marca_cruce}  [{i:3d}]  {perm_str:30s}  |  {ind_costo}  |  Gen: {ind.getGeneracion:>2d}')
        
        # Resumen
        self._lineas.append(f'   → {len(self._parejas_cruce)} cruces | {len(self._indices_mutados)} mutaciones')
    
    def registrarGeneracion(self, poblacion: 'Poblacion', numGeneracion: int, evaluaciones: int):
        """Registra estadísticas de la generación"""
        indvs = poblacion.getIndividuos
        elites = poblacion.getElites if hasattr(poblacion, 'getElites') else []

        # Separador de generación
        self._lineas.append('')
        self._lineas.append('█'*100)
        self._lineas.append('█'+f'GENERACIÓN {numGeneracion} - Evaluaciones: {evaluaciones}'.center(98,' ') + '█')
        self._lineas.append('█'*100)
        self._lineas.append('')
        
        # Estadísticas de la generación
        costos = [ind.getCosto if ind.getCosto is not None else float('inf') for ind in indvs]
        mejor = min(costos)
        peor = max(costos)
        promedio = sum(costos) / len(costos)
        
        self._lineas.append('')
        self._lineas.append(f'{"="*90}')
        self._lineas.append(f'GEN {numGeneracion} | Eval: {evaluaciones} | Mejor: {mejor:.0f} | Prom: {promedio:.0f} | Peor: {peor:.0f}')
        
        # Mostrar élites compactas
        if elites:
            elite_str = ' | '.join([f'E{i+1}[{idx+1}]:{e.getCosto:.0f}' for i, (e, idx) in enumerate(elites)])
            self._lineas.append(f'{SimbolosLog.ELITE} Élites: {elite_str}')
        
        self._lineas.append(f'{"="*90}')

    def registrarReemplazo(self, poblacion_nueva: list['Individuo']):
        """Registra el reemplazo comparando con población previa"""
        self._lineas.append('')
        self._lineas.append(f'{SimbolosLog.REEMPLAZO} REEMPLAZO:')
        
        mejoras = empeoramientos = sin_cambios = 0
        
        for i, ind in enumerate(poblacion_nueva):
            if ind.getCosto is None:
                self._lineas.append(f'   [{i:3d}]  ERROR: INDIVIDUO SIN EVALUAR')
                continue

            costo_nuevo = ind.getCosto
            costo_prev = self._poblacion_previa.get(i, costo_nuevo)
            diff = costo_nuevo - costo_prev
            
            if diff < 0:
                simbolo = SimbolosLog.MEJORA
                mejoras += 1
            elif diff > 0:
                simbolo = SimbolosLog.EMPEORA
                empeoramientos += 1
            else:
                simbolo = '='
                sin_cambios += 1
            
            diff_str = f'{diff:+.0f}' if diff != 0 else '(=)'
            perm_str = str([x+1 for x in ind.getPermutacion][:6])[:-1] + '...]'
            
            # Formato con alineación generosa
            self._lineas.append(f'   [{i:3d}]  {perm_str:30s}  |  {costo_nuevo:>6.0f}  |  Gen: {ind.getGeneracion:>2d}  |  {diff_str:>8s}  {simbolo}')
        
        self._lineas.append(f'   → {SimbolosLog.MEJORA} {mejoras} mejoras | {SimbolosLog.EMPEORA} {empeoramientos} empeoramientos | = {sin_cambios} sin cambio')

    def generaLogs(self):
        carpetaActual = Path(__file__).parent
        nombreDatos = self._data.stem.split('\\')[-1]
        nombreArchivo = f"MEMGEN_{nombreDatos}_S{self._seed}_{self._cruce}_E{self._evaluacionesTabu}_P{self._profundidadTabu}.txt"

        ruta = carpetaActual.parent / 'logs' / nombreArchivo

        with open(ruta, 'w', encoding='utf-8') as arch:
            arch.write('\n'.join(self._lineas))

    def registraCambioBTabu(self, posi, posj, nuevasol, nuevoCoste, mejorCoste, iteracion):
        self._lineas.append(f'\tIteración {iteracion}: cambia el par ({nuevasol[posi]+1},{nuevasol[posj]+1})\n')
        self._lineas.append(f'\tAsignación: {[elem+1 for elem in nuevasol]}\n'      )
        self._lineas.append(f'\tCosto: {nuevoCoste}\n')
        self._lineas.append(f'\tMejor costo global: {mejorCoste}\n\n')