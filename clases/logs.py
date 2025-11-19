from pathlib import Path
from clases.poblacion import (Individuo, Poblacion)
from enum import Enum
from pydantic import FilePath

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
    def __init__(self, data: FilePath, alg: Enum, seed, k, prcAleatorio, tampoblacion, kBest, prcCruce, cruce: Enum, prcMutacion, kWorst, maxEvaluaciones, maxSegundos): 
        self._data = data
        self._alg = alg.value
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
        self._lineas = []
        
        # Estadísticas
        self._total_cruces = 0
        self._total_mutaciones = 0
        self._mejor_costo_previo = float('inf')

        # Encabezado compacto
        self._lineas.append('='*90)
        self._lineas.append(f' {self._alg.upper()} '.center(90, '='))
        self._lineas.append('='*90)
        self._lineas.append(f'Datos: {self._data.stem} | Seed: {seed} | Cruce: {self._cruce} | Población: {tampoblacion}')
        self._lineas.append(f'k_greedy: {k} | Aleatorios: {prcAleatorio}% | k_torneo: {kBest} | Cruce: {prcCruce}% | Mutación: {prcMutacion}%')
        self._lineas.append(f'Max eval: {maxEvaluaciones} | Max seg: {maxSegundos}')
        self._lineas.append('='*90)
        self._lineas.append('')

    def registrarPoblacionInicial(self, poblacion: Poblacion):
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

    def registrarSolucion(self, solucion: tuple[Individuo, float], evaluaciones: int):
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

class LogGeneracional(Log):
    def __init__(self, data, alg, seed, k, prcAleatorio, tampoblacion, numElites, kBest, prcCruce, cruce, prcMutacion, kWorst, maxEvaluaciones, maxSegundos):
        super().__init__(data, alg, seed, k, prcAleatorio, tampoblacion, kBest, prcCruce, cruce, prcMutacion, kWorst, maxEvaluaciones, maxSegundos)
        self._numElites = numElites
        self._poblacion_previa = {}  # {idx: costo} para comparar
        
        # Acumuladores del ciclo actual
        self._poblacion_seleccionada = []
        self._parejas_cruce = []
        self._indices_mutados = set()
        
        if self._numElites > 0:
            self._lineas[4] += f' | Élites: {numElites}'
    
    def iniciarCiclo(self, poblacion_seleccionada: list[Individuo]):
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
            
            # Formato con alineación generosa
            self._lineas.append(f'{marca_mut}{marca_cruce}  [{i:3d}]  {perm_str:30s}  |  {ind.getCosto:>6.0f}  |  Gen: {ind.getGeneracion:>2d}')
        
        # Resumen
        self._lineas.append(f'   → {len(self._parejas_cruce)} cruces | {len(self._indices_mutados)} mutaciones')
    
    def registrarGeneracion(self, poblacion: Poblacion, numGeneracion: int, evaluaciones: int):
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
        costos = [ind.getCosto for ind in indvs]
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

    def registrarReemplazo(self, poblacion_nueva: list[Individuo]):
        """Registra el reemplazo comparando con población previa"""
        self._lineas.append('')
        self._lineas.append(f'{SimbolosLog.REEMPLAZO} REEMPLAZO:')
        
        mejoras = empeoramientos = sin_cambios = 0
        
        for i, ind in enumerate(poblacion_nueva):
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
        nombreArchivo = f"{self._alg}_{nombreDatos}_{self._seed}_{self._cruce}"
        
        if self._numElites > 0:
            nombreArchivo += f"_E{self._numElites}"
        
        nombreArchivo += f"_kBest{self._kBest}.txt"
        ruta = carpetaActual.parent / 'logs' / nombreArchivo

        with open(ruta, 'w', encoding='utf-8') as arch:
            arch.write('\n'.join(self._lineas))

class LogEstacionario(Log):
    def __init__(self, data, alg, seed, k, prcAleatorio, tampoblacion, kBest, prcCruce, cruce, prcMutacion, kWorst, maxEvaluaciones, maxSegundos):
        super().__init__(data, alg, seed, k, prcAleatorio, tampoblacion, kBest, prcCruce, cruce, prcMutacion, kWorst, maxEvaluaciones, maxSegundos)
        self._ciclo_actual = 0
        self._padres_actuales = []
        self._hijos_actuales = []
        self._mutaciones_actuales = []

    def iniciarCiclo(self, padres: list[Individuo]):
        """Inicia un nuevo ciclo guardando los padres seleccionados"""
        self._ciclo_actual += 1
        self._padres_actuales = padres
        self._hijos_actuales = []
        self._mutaciones_actuales = []
        
        # Registrar ciclo y padres en 2 líneas
        self._lineas.append('')
        self._lineas.append(f'{"─"*90}')
        self._lineas.append(f'CICLO {self._ciclo_actual}')
        
        # Padres en una sola línea
        padres_str = ' | '.join([
            f'P{i+1}:{p.getCosto:.0f}' 
            for i, p in enumerate(padres)
        ])
        self._lineas.append(f'{SimbolosLog.SELECCION} Padres: {padres_str}')

    def registrarCruce(self, h1: Individuo, h2: Individuo):
        """Registra el cruce y guarda los hijos"""
        self._hijos_actuales.extend([h1, h2])
        self._mutaciones_actuales.extend([False, False])  # Aún no mutados
        self._total_cruces += 1

    def registrarMutacion(self, idx_hijo: int):
        """
        Registra que un hijo mutó
        idx_hijo: índice del hijo en la lista de hijos
        """
        if idx_hijo < len(self._mutaciones_actuales):
            self._mutaciones_actuales[idx_hijo] = True
            self._total_mutaciones += 1

    def finalizarCruceMutacion(self):
        """Registra los hijos después de cruce y mutación en 2 líneas"""
        if not self._hijos_actuales:
            return
        
        # Hijos en una línea
        hijos_str = ' | '.join([
            f'{"🧬" if self._mutaciones_actuales[i] else ""}H{i+1}:{h.getCosto:.0f}' 
            for i, h in enumerate(self._hijos_actuales)
        ])
        self._lineas.append(f'{SimbolosLog.CRUCE} Hijos: {hijos_str}')

    def registrarReemplazo(self, padres: list[Individuo]):
        """
        Registra el reemplazo en 1-2 líneas máximo
        padres: Los padres originales del ciclo
        """
        if not self._hijos_actuales:
            return
        
        # Reemplazos compactos
        reemplazos = []
        mejoras = empeoramientos = 0
        
        for i, hijo in enumerate(self._hijos_actuales):
            if i < len(padres):
                padre = padres[i]
                diff = hijo.getCosto - padre.getCosto
                
                if diff < 0:
                    simbolo = SimbolosLog.MEJORA
                    mejoras += 1
                elif diff > 0:
                    simbolo = SimbolosLog.EMPEORA
                    empeoramientos += 1
                else:
                    simbolo = '='
                
                reemplazos.append(f'P{i+1}→H{i+1}({diff:+.0f}{simbolo})')
        
        # Todo en una línea
        reemplazos_str = ' | '.join(reemplazos)
        self._lineas.append(f'{SimbolosLog.REEMPLAZO} {reemplazos_str}')
        
        # Resumen (opcional, solo si hay cambios)
        if mejoras > 0 or empeoramientos > 0:
            self._lineas.append(f'   → {SimbolosLog.MEJORA}{mejoras} | {SimbolosLog.EMPEORA}{empeoramientos}')

    def generaLogs(self):
        carpetaActual = Path(__file__).parent
        nombreDatos = self._data.stem.split('\\')[-1]
        nombreArchivo = f"{self._alg}_{nombreDatos}_{self._seed}_{self._cruce}_kBest{self._kBest}.txt"
        ruta = carpetaActual.parent / 'logs' / nombreArchivo

        with open(ruta, 'w', encoding='utf-8') as arch:
            arch.write('\n'.join(self._lineas))