# ToDo
## Práctica 1
- [x] Sacar matrices
- [x] Greedy
- [ ] Leer configuracion
- [ ] Ejecutar con los ford01.dat... y apuntar resultados
## Práctica 2
> Ahora el greedy no cogera el mejor sino que elegira entre los x mejores (segun el parametro en config, ALEAT) aleatoriamente.

- [ ] Modificar greedy
- [ ] Ejecutar y apuntar

> [!IMPORTANT]
> - Por cada experimento debe haber una **única** semilla
> - Solo es copiar el greedy modificando el `pop(x)` para que coja uno de los x valores en vez de el primero siempre

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