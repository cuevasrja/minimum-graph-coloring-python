# Corte 2 - Minimum Graph Coloring

**Realizado Por:**
- Joao Pinto. (17-10490)
- Jhonaiker Blanco. (18-10784)
- Juan Cuevas. (19-10056)

En este corte se implementaron soluciones para el problema de coloración mínima de grafos. En particular, se implementaron los siguientes algoritmos:

- Algoritmo Memético
- Algoritmo Memético con Búsqueda Dispersa
- Algoritmo de Optimización por Enjambre de Partículas (PSO)

Para la implementación de estos algoritmos se utilizó el lenguaje de programación Python, y se utilizó la librería iGraph para la representación de grafos y algunas operaciones sobre estos.

## Benchmark para el problema de coloración de grafos

Un benchmark es un conjunto de instancias de un problema que se utilizan para comparar diferentes algoritmos y evaluar su rendimiento. 

Para el problema de coloración de grafos, en la literatura es comun utilizar un conjunto de instancias seleccionadas por el DIMACS (Center for Discrete Mathematics and Theoretical Computer Science) para evaluar los algoritmos de coloración de grafos. El conjunto de instancias DIMACS contiene grafos con diferentes tamaños y densidades, que a su vez provienen de diferentes aplicaciones, esto permite evaluar el rendimiento de los algoritmos en diferentes escenarios.

Este benchmark se diseñó para [el segundo desafío de coloración de grafos de DIMACS](http://dimacs.rutgers.edu/archive/Challenges/#:~:text=NP-,Hard,-Problems%3A%20Maximum%20Clique). Para este corte, se utilizaron algunas instancias de este benchmark para evaluar los algoritmos implementados. 

En concreto se seleccionaron instancias DIMACS asociadas a las siguientes fuentes:

- **DSJC**: Generados por David Johnson, grafos utilizados en su articulo con Aragon, McGeoch y Schevon, _"Optimization by Simulated Annealing: An Experimental Evaluation; Part II, Graph Coloring and Number Partitioning"_, Operations Research 39, 378-406, 1991. Son grafos $(n, p)$ aleatorios estándar con densidad de aristas $p$.
- **REG**: Generados por Gary Lewandowski, son grafos asociados al problema de _"Register Allocation"_, los grafos provienen de programas reales.
- **LEI**: Generados por Craig Morgenstern. Son grafos de Leighton con tamaño de coloración garantizado. Una referencia es F.T. Leighton, Journal of Research of the National Bureau of Standards, 84: 489--505 (1979).
- **SGB queen**: Grafos asociados al [problema de las n-reinas](https://en.wikipedia.org/wiki/Eight_queens_puzzle) para tableros de ajedrez de tamaño $n \times n$.

Los grafos seleccionados se encuentran en la carpeta [data](../../data/) y se describen a continuación:

### Tabla de instancias

| Grafo   | Archivo         | Número de nodos | Número de lados | Fuente          | Número cromático |
|---------|-----------------|-----------------|-----------------|-----------------|------------------|
| Grafo 1 | DSJC250.5.col   | 250             | 15668           | **DSJC**        | 31               |
| Grafo 2 | DSJC250.9.col   | 250             | 27897           | **DSJC**        | 75               |
| Grafo 3 | le450_15b.col   | 450             | 8169            | **LEI**         | 15               |
| Grafo 4 | le450_15c.col   | 450             | 16680           | **LEI**         | 15               |
| Grafo 5 | le450_25c.col   | 450             | 17343           | **LEI**         | 25               |
| Grafo 6 | queen5_5.col    | 25              | 320             | **SGB queen**   | 5                |
| Grafo 7 | fpsol2.i.1.col  | 496             | 11654           | **REG**         | 65               |
| Grafo 8 | fpsol2.i.2.col  | 451             | 8691            | **REG**         | 30               |
| Grafo 9 | zeroin.i.3.col  | 206             | 3540            | **REG**         | 30               |
| Grafo 10| mulsol.i.1.col  | 197             | 3925            | **REG**         | 49               |


**Para este corte se decidió remover algunos grafos en donde DSatur no daba una solución óptima, para poder evaluar significativamente el rendimiento de los nuevos algoritmos implementados.**

## Soluciones implementadas

### Algoritmo Memético

El algoritmo memético es una técnica de optimización que combina la búsqueda local con la evolución de una población de soluciones. En este algoritmo, se mantiene una población de soluciones, y en cada iteración se seleccionan las mejores soluciones para aplicarles operadores de búsqueda local y evolución. Además, se pueden aplicar operadores de diversificación para explorar el espacio de soluciones.

En el algoritmo memético implementado, se utilizó una población de soluciones, y en cada iteración se seleccionan las mejores soluciones para aplicarles una búsqueda local basada en la heurística DSatur. Además, se aplicó un operador de diversificación basado en la mutación de soluciones.

### Algoritmo Memético con Búsqueda Dispersa

El algoritmo memético con búsqueda dispersa es una variante del algoritmo memético que utiliza una población de soluciones dispersas en el espacio de soluciones. En este algoritmo, se mantiene una población de soluciones, y en cada iteración se seleccionan las mejores soluciones para aplicarles operadores de búsqueda local y evolución. Además, se pueden aplicar operadores de diversificación para explorar el espacio de soluciones.

En el algoritmo memético con búsqueda dispersa implementado, se utilizó una población de soluciones dispersas, y en cada iteración se seleccionan las mejores soluciones para aplicarles una búsqueda local basada en la heurística DSatur. Además, se aplicó un operador de diversificación basado en la mutación de soluciones.

### Algoritmo de Optimización por Enjambre de Partículas (PSO)

El algoritmo de optimización por enjambre de partículas (PSO) es una técnica de optimización que se inspira en el comportamiento social de los enjambres de aves o peces. En este algoritmo, se mantiene una población de soluciones (partículas) que se mueven en el espacio de soluciones siguiendo la mejor solución encontrada por el enjambre y la mejor solución encontrada por cada partícula.

En el algoritmo PSO implementado, se utilizó una población de partículas que se mueven en el espacio de soluciones, y en cada iteración se actualizan las velocidades y posiciones de las partículas siguiendo la mejor solución encontrada por el enjambre y la mejor solución encontrada por cada partícula. Además, se aplicó un operador de diversificación basado en la mutación de soluciones.

## Experimentos y Resultados

## Comparación con Corte Anterior

## Conclusiones