# Corte 1 - Minimum Graph Coloring

**Realizado Por:**
- Joao Pinto. (17-10490)
- Jhonaiker Blanco. (18-10784)
- Juan Cuevas. (19-10056)

En este corte se implementaron soluciones para el problema de coloración mínima de grafos. Se implementaron 3 algoritmos diferentes para resolver este problema, los cuales son:
- Algoritmo de Búsqueda Local con vecindad de Kempe.
- Algoritmo de D Satur.
- Algoritmo de Búsqueda Exacta (Backtracking).

Para la implementación de estos algoritmos se utilizó el lenguaje de programación Python, y se utilizó la librería iGraph para la representación de grafos y algunas operaciones sobre estos.

## Algoritmos usados

### D Satur

El algoritmo de D Satur se basa en la técnica de coloreo de nodos por saturación. La saturación de un nodo es la cantidad de colores diferentes que tiene en sus vecinos. El algoritmo selecciona el nodo con mayor saturación y le asigna el color que minimice la cantidad de conflictos. 

### Búsqueda Exacta (Backtracking)

El algoritmo de Búsqueda Exacta se basa en la técnica de backtracking, donde se prueban todas las posibles combinaciones de colores para los nodos del grafo. Para este algoritmo, se implementó una variante que premite podar el árbol de búsqueda, seleccionando los nodos de forma determinística. La poda se realiza cuando se llega a un nodo que no tiene solución, es decir, cuando se llega a un nodo que no se puede colorear con los colores disponibles, o cuando se llega a una solución que no es mejor que la mejor solución encontrada hasta el momento.

### Búsqueda Local con vecindad de Kempe

El algoritmo de Búsqueda Local con vecindad de Kempe se basa en la técnica de búsqueda local, donde se intercambian los colores de dos nodos vecinos. La vecindad de Kempe se define como el conjunto de nodos que comparten un color con el nodo seleccionado. Para empezar la búsqueda local, se toma un grafo con una coloración válida usando el algoritmo de D Satur. Luego, se seleccionan dos nodos de forma determinística y se intercambian sus colores. Si la solución resultante es mejor que la solución actual, se actualiza la solución actual con la nueva solución. Este proceso se repite hasta que no se puedan encontrar soluciones mejores.


## Pruebas

Los grafos utilizados en las pruebas se encuentran en la carpeta data, en cada archivo además de la información de los vertices y las aristas también está la
procedencia de cada uno

### Tabla de grafos

| Grafo   | Archivo         | Número de nodos | Número de lados |
|---------|-----------------|-----------------|-----------------|
| Grafo 1 | DSJC250.5.col   | 250             | 15668           |
| Grafo 2 | DSJC250.9.col   | 250             | 27897           |
| Grafo 3 | fpsol2.i.1.col  | 496             | 11654           |
| Grafo 4 | fpsol2.i.2.col  | 451             | 8691            |
| Grafo 5 | fpsol2.i.3.col  | 425             | 8688            |
| Grafo 6 | inithx.i.1.col  | 864             | 18707           |
| Grafo 7 | inithx.i.2.col  | 645             | 13979           |
| Grafo 8 | inithx.i.3.col  | 621             | 13969           |
| Grafo 9 | le450_15b.col   | 450             | 8169            |
| Grafo 10| le450_15c.col   | 450             | 16680           |
| Grafo 11| le450_25c.col   | 450             | 17343           |
| Grafo 12| mulsol.i.1.col  | 197             | 3925            |
| Grafo 13| myciel3.col     | 11              | 20              |
| Grafo 14| queen5_5.col    | 25              | 320             |
| Grafo 15| zeroin.i.3.col  | 206             | 3540            |

## Resultados

Por temas de practicidad, le dimos a cada algoritmo un tiempo máximo de 5 minutos para correr. El algoritmo de busqueda local utiliza el resultado de DSatur como punto de partida

### Tabla de grafos

| Grafo    | Tiempo con Dsatur | Colores | Tiempo con busqueda local | Colores        | Tiempo con Backtracking | Colores con bactracking |
|----------|-------------------|---------|---------------------------|----------------|-------------------------|-------------------------|
| Grafo 1  | 0.12098 segundos  |  42     |   32.37499 segundos       |  41            |    Más de 5 minutos     |      No calculados      |
| Grafo 2  | 0.07322 segundos  |  97     |   57.06781 segundos       |  92            |    Más de 5 minutos     |      No calculados      |
| Grafo 3  | 0.10175 segundos  |  65     |   251.55769 segundos      |  65            |    Más de 5 minutos     |      No calculados      |
| Grafo 4  | 0.08047 segundos  |  30     |   31.34456 segundos       |  30            |    Más de 5 minutos     |      No calculados      |
| Grafo 5  | 0.07440 segundos  |  30     |   31.49850 segundos       |  30            |    Más de 5 minutos     |      No calculados      |
| Grafo 6  | 0.26938 segundos  |  54     |   Más de 5 minutos        |  No calculados |    Más de 5 minutos     |      No calculados      |
| Grafo 7  | 0.15670 segundos  |  31     |   76.5435 segundos        |  31            |    Más de 5 minutos     |      No calculados      |
| Grafo 8  | 0.15550 segundos  |  31     |   93.1823 segundos        |  31            |    Más de 5 minutos     |      No calculados      |
| Grafo 9  | 0.08113 segundos  |  18     |   5.40957 segundos        |  18            |    Más de 5 minutos     |      No calculados      |
| Grafo 10 | 0.09588 segundos  |  26     |   13.0586 segundos        |  25            |    Más de 5 minutos     |      No calculados      |
| Grafo 11 | 0.09588 segundos  |  31     |   26.3236 segundos        |  29            |    Más de 5 minutos     |      No calculados      |
| Grafo 12 | 0.02099 segundos  |  49     |   17.8212 segundos        |  49            |    Más de 5 minutos     |      No calculados      |
| Grafo 13 | 0.00099 segundos  |  4      |   0.00300 segundos        |  4             |    0.02290 segundos     |      4                  |
| Grafo 14 | 0.00099 segundos  |  8      |   0.00700 segundos        |  7             |    0.01354 segundos     |      5                  |
| Grafo 15 | 0.02092 segundos  |  30     |   4.46516 segundos        |  30            |    Más de 5 minutos     |      No calculados      |


## Conclusiones

En general, el algoritmo DSatur demostró ser capaz de dar soluciones muy buenas en un tiempo muy corto. 

La busqueda local es bastante útil para optimizar estas soluciones, no siempre mejora la solución obtenida con DSatur, pero, en algunos casos puede mejorar la solución previa y su tiempo de ejecució, a pesar de ser más grande que el tiempo de la busqueda inicial, sigue siendo practico. 

El backtracking obtiene soluciones perfectas pero por lo general no es aplicable en grafos grandes, los tiempos de ejecución son demasiado altos, solo hace sentido aplicarlo en grafos pequeños