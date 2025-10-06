# ToDo
## Práctica 1
- [x] Sacar matrices
- [x] Greedy
- [x] Leer configuracion
- [x] Ejecutar con los ford01.dat... y apuntar resultados
## Práctica 2
> Ahora el greedy no cogera el mejor sino que elegira entre los x mejores (segun el parametro en config, ALEAT) aleatoriamente.

> [!IMPORTANT]
> - Por cada experimento debe haber una **única** semilla
> - Solo es copiar el greedy modificando el `pop(x)` para que coja uno de los x valores en vez de el primero siempre
> - **COMPROBAR LOS MINIMOS GLOBALES Y LOCALES CON LOS ARCHIVOS SLC Y NO EL EXCEL QUE TIENE ERRORES**

- [X] Modificar greedy
- [X] Comprobar que funcione
- [ ] Apuntar los resultados en el excel

# Práctica 3
> [!IMPORTANT]
> **LA SEMANA QUE VIENE VA A PREGUNTAR**

> - CheckMove comprueba si el cambio mejora.
>   ApplyMove lo que hace es aplicar el cambio.
>   No paso a la siguiente iteración hasta que haya intercambiado dos operaciones.
>   Hasta que iteraciones o DLB = 1 (porque todas las posiciones que están en 1 se suponen que están bien posicionadas).
>
> Si el resultado de la factorización sale igual que la función de evaluación completa es que esta bien. Es por dos porque es simétrica
>
> ```
> Repetir
> 	Repetir
> 		Generar Vecino
> 	Hasta entorno completo
> 
> 	Interaciones ++ // Que no siempre lo ahcemos
> 	Hasta iteraciones o DLB = 1
>
> Devuelve Mejor_solucion
> ```
>
> - La función de factorización se ha convertido de cuadrática a linear. Lo que hace es comprobar como influye el cambio de dos unidades con respecto al resto de unidades, mirando como ha variado el valor (diferencia de distancias). Entiendo que se han ahorrado la segunda iteración sumando lo que les sale en el resultado alterior más la nueva combinación posible.
> - Logs:
>   ```
>   PARÁMETROS (Alg, parámetros de ejecución del alg (iteraciones, semilla...)
>   Solución inicial y su coste
>   ----
>   Por cada cambio un registro en el log:
>   - Qué posiciones se han intercambiado.
>   - Solución nueva generada y su coste.
>   - Solución global encontrada hasta ahora y su coste.
>   --
>   Final
>   - Solucion final, su coste y el tiempo de ejecución.
>   ```

> [!IMPORTANT]
> Los limites de iteracion estan mal, si se ha intercambiado una posicion, i debe empezar en 'v' en vez de en 1. Donde 'v' es la posicion donde se quedo + 1 (la siguiente), porque si no se genera un bucle infinito.

- [X] Crear el DLB (dos loop bit)
- [X] Crear la función de factorización
- [X] Probarla con el greedy
- [X] Hacer logs
- [ ] Hacer pruebas y apuntar (supongo)

# Práctica 4
> Memoria a corto plazo: una lista con un contador para indicar por que posición va (hacer modulo len(lista))
> Memoria a largo plazo: una matriz de nxn (n es el número de unidades)
> ### Orden
> 1. Empeoramiento
> 2. Corto plazo
> 3. Largo plazo
> 4. Oscilacion

# Documento
- ✳️ Le gusta que despues de la tabla
- ✳️ Desviacion tipica, media, tiempo.
- ⚠️ **No hacemos una tabla por cada semilla**, baja un monton la nota.
- ⚠️ **NO GRAFICAS DE LA DESVIACION TIPICA**
- ❌ No cortar las graficas
- ✅ Informe corto 15 paginas
- Tabla final con todos los problemas, por cada uno hacemos la desviacion tipica y el tiempo

# ℹ️ Comandos
## Iniciar repositorio 
_(si no se ha iniciado previamente)_
```
cd directorio_base_del_proyecto
git init
```
## Descargar ⬇️
```
git clone https://github.com/cmc00150/Team12_Meta.git
```
## Subir actualizaciones ⬆️
```
git add ..
git commit -m "mensaje cualquiera"
git push origin main
```
## Ramas 🌳 
> Crear una nueva rama y cambiar a ella
> ```
> git switch -c nombre_rama
> ```

> Moverse entre ramas
> ```
> git switch nombre_rama
>```

> Conectar rama
>  _(Nos movemos al main y conectamos la otra rama desde ahi)_ >
> ```
> git switch main
> git merge nombre_rama
>```

> Sincronizarse con el contenido de GitHub
> ```
> git pull
> ```

> Ver en que commit estás
> _(esto devolverá un sha256 corto que podemos comparar con el id del commit)_
> ```
> git rev-parse --short HEAD
> ```
