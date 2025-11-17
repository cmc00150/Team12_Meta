from pathlib import Path
from clases.poblacion import (Individuo, Poblacion)
from enum import Enum
from pydantic import FilePath

class Log():
    def __init__(self, data: FilePath, alg: Enum, seed, k, prcAleatorio, tampoblacion, kBest, prcCruce, cruce, prcMutacion, kWorst, maxEvaluaciones, maxSegundos): 
        self._data = data
        self._alg = alg
        self._seed = seed
        self._k = k
        self._prcAleatorio = prcAleatorio
        self._tampoblacion = tampoblacion
        self._kBest = kBest
        self._prcCruce = prcCruce
        self._cruce = cruce
        self._prcMutacion = prcMutacion
        self._kWorst = kWorst
        self._maxEvaluaciones = maxEvaluaciones
        self._maxSegundos = maxSegundos
        self._lineas = []
        
        # Estadísticas
        self._total_cruces = 0
        self._total_mutaciones = 0
        self._mejor_costo_previo = float('inf')

        # Encabezado
        self._lineas.append('='*100)
        self._lineas.append(f' LOGS ALGORITMO {self._alg.upper()} '.center(100, '='))
        self._lineas.append('='*100)
        self._lineas.append('')
        
        # Configuración
        self._lineas.append('📁 CONFIGURACIÓN:')
        self._lineas.append(f'   Archivo de datos: {self._data}')
        self._lineas.append(f'   Semilla: {self._seed}')
        self._lineas.append(f'   K (greedy): {self._k}')
        self._lineas.append(f'   % Individuos aleatorios: {self._prcAleatorio}%')
        self._lineas.append(f'   Tamaño población: {self._tampoblacion}')
        self._lineas.append(f'   K mejores (torneo): {self._kBest}')
        self._lineas.append(f'   % Cruce: {self._prcCruce}%')
        self._lineas.append(f'   Tipo de cruce: {self._cruce}')
        self._lineas.append(f'   % Mutación: {self._prcMutacion}%')
        self._lineas.append(f'   K peores (reemplazo): {self._kWorst}')
        self._lineas.append(f'   Máximo evaluaciones: {self._maxEvaluaciones}')
        self._lineas.append(f'   Máximo segundos: {self._maxSegundos}')
        self._lineas.append('')
        self._lineas.append('='*100)
        self._lineas.append('')

    def registrarSeleccion(self, numSeleccionados: int):
        """Registra la fase de selección"""
        self._lineas.append(f'   ✓ Selección completada: {numSeleccionados} individuos seleccionados por torneo (k={self._kBest})')
        self._lineas.append('')

    def registrarCruce(self, padre1: Individuo, padre2: Individuo, hijos: tuple[Individuo, Individuo]):
        """Registra un cruce específico en GENERACIONAL"""
        self._total_cruces += 1
        
        self._lineas.append(f'   🔀 CRUCE ({self._cruce}):')
        self._lineas.append(f'      Padre 1: Perm={[x+1 for x in padre1.getPermutacion][:8]}... | Costo={padre1.getCosto:>8.2f} | Gen={padre1.getGeneracion}')
        self._lineas.append(f'      Padre 2: Perm={[x+1 for x in padre2.getPermutacion][:8]}... | Costo={padre2.getCosto:>8.2f} | Gen={padre2.getGeneracion}')
        
        promedio_padres = (padre1.getCosto + padre2.getCosto) / 2
        
        for i, hijo in enumerate(hijos, 1):
            mejora = promedio_padres - hijo.getCosto
            simbolo = '✓' if mejora > 0 else '✗'
            self._lineas.append(f'      {simbolo} Hijo {i}:  Perm={[x+1 for x in hijo.getPermutacion][:8]}... | Costo={hijo.getCosto:>8.2f} | Gen={hijo.getGeneracion} | Δ={mejora:+.2f}')
        
        self._lineas.append('')

    def registrarMutacion(self, individuo: Individuo, posiciones: tuple[int, int], costo_anterior: float):
        """Registra mutación en ESTACIONARIO"""
        self._total_mutaciones += 1
        
        cambio = individuo.getCosto - costo_anterior
        simbolo = '✓' if cambio < 0 else '✗'
        
        self._lineas.append(f'   {simbolo} 🧬 Mutación [{posiciones[0]+1}↔{posiciones[1]+1}]: {costo_anterior:>8.2f} → {individuo.getCosto:>8.2f} (Δ={cambio:+.2f})')

    def registrarSolucion(self, solucion: tuple[Individuo, float], numEvaluaciones: int = -1):
        """Registra la solución final"""
        individuo, tiempo = solucion
        
        self._lineas.append('')
        self._lineas.append('='*100)
        self._lineas.append('  🎉 SOLUCIÓN FINAL  '.center(100, '='))
        self._lineas.append('='*100)
        self._lineas.append('')
        
        self._lineas.append('📈 RESULTADO:')
        self._lineas.append(f'   Permutación: {[x+1 for x in individuo.getPermutacion]}')
        self._lineas.append(f'   Costo: {individuo.getCosto}')
        self._lineas.append(f'   Generación: {individuo.getGeneracion}')
        self._lineas.append(f'   Tiempo de ejecución: {tiempo:.4f}s')
        
        if numEvaluaciones > 0:
            self._lineas.append(f'   Total evaluaciones: {numEvaluaciones}')
        
        self._lineas.append('')
        self._lineas.append('📊 ESTADÍSTICAS:')
        self._lineas.append(f'   Total de cruces realizados: {self._total_cruces}')
        self._lineas.append(f'   Total de mutaciones realizadas: {self._total_mutaciones}')
        self._lineas.append('')
        
        if numEvaluaciones > 0:
            self._lineas.append(f'🏁 FIN POR LÍMITE DE EVALUACIONES: {numEvaluaciones}'.center(100))
        else:
            self._lineas.append(f'🏁 FIN POR LÍMITE DE TIEMPO: {tiempo:.4f}s'.center(100))
        
        self._lineas.append('')
        self._lineas.append('='*100)

class LogGeneracional(Log):
    def __init__(self, data, alg, seed, k, prcAleatorio, tampoblacion, numElites, kBest, prcCruce, cruce, prcMutacion, kWorst, maxEvaluaciones, maxSegundos):
        super().__init__(data, alg, seed, k, prcAleatorio, tampoblacion, kBest, prcCruce, cruce, prcMutacion, kWorst, maxEvaluaciones, maxSegundos)
        self._numElites = numElites
        if self._numElites > 0:
            self._lineas.insert(5, f'   Número de élites: {self._numElites}') # Lo insertamos en medio de los parámetros iniciales
    
    def registrarGeneracion(self, poblacion: Poblacion, numGeneracion: int, evaluaciones: int):
        """
        Registra una generación completa del algoritmo GENERACIONAL
        Incluye: población completa, élites, estadísticas
        """
        indvs = poblacion.getIndividuos
        elites = poblacion.getElites if hasattr(poblacion, 'getElites') else []
        
        # Separador de generación
        self._lineas.append('')
        self._lineas.append('█'*100)
        self._lineas.append(f'█  GENERACIÓN {numGeneracion} - Evaluaciones: {evaluaciones}  █'.ljust(99) + '█')
        self._lineas.append('█'*100)
        self._lineas.append('')
        
        # Estadísticas de la generación
        costos = [ind.getCosto for ind in indvs]
        mejor_costo = min(costos)
        peor_costo = max(costos)
        promedio_costo = sum(costos) / len(costos)
        
        self._lineas.append('📊 ESTADÍSTICAS DE LA GENERACIÓN:')
        self._lineas.append(f'   Mejor costo:     {mejor_costo:>10.2f}')
        self._lineas.append(f'   Peor costo:      {peor_costo:>10.2f}')
        self._lineas.append(f'   Promedio:        {promedio_costo:>10.2f}')
        self._lineas.append(f'   Rango:           {peor_costo - mejor_costo:>10.2f}')
        
        if self._mejor_costo_previo != float('inf'):
            mejora = self._mejor_costo_previo - mejor_costo
            if mejora > 0:
                self._lineas.append(f'   🎯 Mejora:        {mejora:>+10.2f} (¡MEJOR!)')
            elif mejora < 0:
                self._lineas.append(f'   ⚠️  Empeora:       {mejora:>+10.2f}')
            else:
                self._lineas.append(f'   ➡️  Sin cambios')
        
        self._mejor_costo_previo = mejor_costo
        self._lineas.append('')
        
        # Élites de la generación
        if elites:
            self._lineas.append('⭐'*50)
            self._lineas.append(f'   ÉLITES DE LA GENERACIÓN {numGeneracion}'.center(100))
            self._lineas.append('⭐'*50)
            for i, (elite, idx) in enumerate(elites):
                self._lineas.append(f'   🏆 Élite {i+1} (posición {idx}):')
                self._lineas.append(f'      Permutación: {[x+1 for x in elite.getPermutacion]}')
                self._lineas.append(f'      Costo: {elite.getCosto}')
                self._lineas.append(f'      Generación: {elite.getGeneracion}')
            self._lineas.append('')
        
        # Población completa (resumen)
        self._lineas.append('📋 POBLACIÓN COMPLETA:')
        for i, ind in enumerate(indvs):
            marca = '🏆' if any(ind.getCosto == e[0].getCosto for e in elites) else '  '
            self._lineas.append(f'   {marca} [{i+1:2d}] Costo: {ind.getCosto:>8.2f} | Gen: {ind.getGeneracion:>3d} | Perm: {[x+1 for x in ind.getPermutacion]}')
        
        self._lineas.append('')

    def iniciarCiclo(self, numGeneracion: int):
        """Marca el inicio de un ciclo de reproducción en GENERACIONAL"""
        self._lineas.append('')
        self._lineas.append('┌' + '─'*98 + '┐')
        self._lineas.append(f'│  🔄 CICLO DE REPRODUCCIÓN - Generación {numGeneracion}'.ljust(99) + '│')
        self._lineas.append('└' + '─'*98 + '┘')
        self._lineas.append('')

    def registrarReemplazo(self):
        """Registra el reemplazo de población en GENERACIONAL"""
        self._lineas.append('')
        self._lineas.append(f'   ♻️  REEMPLAZO: Nueva población establecida')
        self._lineas.append('')

    def generaLogs(self):
        carpetaActual = Path(__file__).parent
        
        nombreDatos = self._data.stem.split('\\')[-1]
        nombreArchivo = f"{self._alg.value}_{nombreDatos}_{self._seed}_{self._cruce}"
        
        if self._numElites > 0:
            nombreArchivo += f"_E{self._numElites}"
        
        nombreArchivo += f"_kB{self._kBest}.txt"
        ruta = carpetaActual.parent / 'logs' / nombreArchivo

        with open(ruta, 'w', encoding='utf-8') as arch:
            arch.write('\n'.join(self._lineas))

class LogEstacionario(Log):
    def __init__(self, data, alg, seed, k, prcAleatorio, tampoblacion, kBest, prcCruce, cruce, prcMutacion, kWorst, maxEvaluaciones, maxSegundos):
        super().__init__(data, alg, seed, k, prcAleatorio, tampoblacion, kBest, prcCruce, cruce, prcMutacion, kWorst, maxEvaluaciones, maxSegundos)

    def registrarSeleccion(self, padres: list[Individuo]):
        """Registra la selección de padres en ESTACIONARIO"""
        self._lineas.append(f'   ✓ Selección de {len(padres)} padres por torneo (k={self._kBest}):')
        for i, padre in enumerate(padres, 1):
            self._lineas.append(f'      Padre {i}: Costo={padre.getCosto:>8.2f} | Gen={padre.getGeneracion}')
        self._lineas.append('')

    def registrarCruce(self, padre1: Individuo, padre2: Individuo, hijos: tuple[Individuo, Individuo]):
        """Registra cruce en ESTACIONARIO"""
        self._total_cruces += 1
        
        self._lineas.append(f'   🔀 CRUCE ({self._cruce}):')
        self._lineas.append(f'      P1: Costo={padre1.getCosto:>8.2f} | P2: Costo={padre2.getCosto:>8.2f}')
        self._lineas.append(f'      H1: Costo={hijos[0].getCosto:>8.2f} | H2: Costo={hijos[1].getCosto:>8.2f}')
        self._lineas.append('')

    def registrarReemplazo(self, hijos: list[Individuo]):
        """Registra reemplazo en ESTACIONARIO"""
        self._lineas.append(f'   ♻️  Reemplazo individuos insertados en población (torneo k={self._kWorst})')
        for i, hijo in enumerate(hijos, 1):
            self._lineas.append(f'      Hijo {i}: Costo={hijo.getCosto:>8.2f} insertado')
        self._lineas.append('')

    def generaLogs(self):
        carpetaActual = Path(__file__).parent
        
        nombreDatos = self._data.stem.split('\\')[-1]
        nombreArchivo = f"{self._alg.value}_{nombreDatos}_{self._seed}_{self._cruce}"
        
        nombreArchivo += f"_kB{self._kBest}.txt"
        ruta = carpetaActual.parent / 'logs' / nombreArchivo

        with open(ruta, 'w', encoding='utf-8') as arch:
            arch.write('\n'.join(self._lineas))