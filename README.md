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

# Práctica 5
>   Si en la poblacion descendiente ha desaparecido el mejor padre anterior, quito uno de los hijos y meto al padre
> Tener esquema de generación de población, cruce, mutaciones etc
Nos da igual que se repita un individuo.
Lo relleno del 1 al 20 unas listas y asi hago el cruce.
```
PARA i=1 ht tamaño Pt
    Crear individuo
    Inicialización aleatoria
        generacion? Ver donde se estanca
        evaluado?
        elite? Ver si es elite mediante una propiedad en el individuo.
FIN PARA
```
Para ver el estancamiento es mejor ver los costes porque puede ser que dos padres iguales den un hijo igual, lo que da un mismo coste.
PARA i=1 ht  tamaño PT
    SI evaluado == falso

PARA i=1 ht tamaño Pt
    ind = Torneo binario
    indluir 

CRUCE
PARA i=1 tamaño Pt/2
    SI prob(cruce) <= 0.7
    ENTONCES
    Cruzar(P(i*2)t, P(i*2+1)t)
FIN PARA

MUTACION
Lanzar una probabilidad y si da que sí, cambio dos valores aleatorios.

Elite - calcular elite con respecto de qt, se calcula antes de empezar a generar los descendientes. Calculo cual es el elite del padre. 
Antes de coger Pt compruebo que Qt tenga un elite.

OX2
1. Lanzo un aleatorio por cada uno de sus genes (50%).
2. Eliminamos del padre2 los valores que se han marcado.
3. Rellenamos los huecos con los valores del padre1.
4. Podemos hacerlo otra vez pero con los padres invertidos o podemos hacer una funcion que de directamente dos

MOC
1. Marco un punto de corte
2. Intercambiamos los primeros del padre1 con los valores al padre2
3. Intercambiamos los últimos del padre2 con los valores al padre1

# Documento
- ✳️ Le gusta que despues de la tabla
- ✳️ Desviacion tipica, media, tiempo.
- ⚠️ **No hacemos una tabla por cada semilla**, baja un monton la nota.
- ⚠️ **NO GRAFICAS DE LA DESVIACION TIPICA**
- ❌ No cortar las graficas
- ✅ Informe corto 15 paginas
- Tabla final con todos los problemas, por cada uno hacemos la desviacion tipica y el tiempo