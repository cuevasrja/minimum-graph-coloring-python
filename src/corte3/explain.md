# Corte 3 - Minimum Graph Coloring

**Realizado Por:**
- Joao Pinto. (17-10490)
- Jhonaiker Blanco. (18-10784)
- Juan Cuevas. (19-10056)

En este corte se implementaron soluciones para el problema de coloración mínima de grafos. En particular, se implementaron los siguientes algoritmos:

- Algoritmo Memético
- Búsqueda Dispersa
- Algoritmo de la Colonia de Hormigas

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

Un Algoritmo Memético es una técnica de optimización computacional que combina la búsqueda heurística local con la búsqueda evolutiva basada en poblaciones, inspirada en los procesos de evolución biológica.

Los algoritmos meméticos funcionan de manera similar a los algoritmos genéticos, pero incorporan un paso adicional de búsqueda local para refinar las soluciones individuales. Esto les permite superar algunas de las limitaciones de los algoritmos genéticos, como la convergencia prematura a soluciones subóptimas y la dificultad para encontrar soluciones de alta calidad en espacios de búsqueda complejos.

### Búsqueda Dispersa

La Búsqueda Dispersa es una técnica de optimización metaheurística basada en la búsqueda iterativa de mejores soluciones dentro de un conjunto de soluciones factibles. A diferencia de los algoritmos de búsqueda local, que se enfocan en mejorar una solución individual, la búsqueda dispersa explora el espacio de búsqueda de manera más amplia mediante la combinación y diversificación de soluciones existentes.



### Algoritmo de la Colonia de Hormigas

El Algoritmo de la Colonia de Hormigas es una técnica de optimización metaheurística inspirada en el comportamiento de las hormigas en su búsqueda de alimento. Las hormigas, a través de la comunicación mediante feromonas, logran encontrar caminos eficientes entre su nido y las fuentes de alimento. El ACO simula este comportamiento para resolver problemas complejos, especialmente aquellos que pueden representarse como un grafo, como la búsqueda de rutas óptimas o la asignación eficiente de recursos.


## Experimentos y Resultados

Por motivos de practicidad, se le asignó a cada algoritmo un tiempo máximo de 20 minutos para terminar su ejecución.

Las pruebas fueron realizadas en un equipo con las siguientes características: 

- **Procesador**: Ryzen 7 7735H 
- **Memoria RAM**: 32GB 
- **SO**: Windows 11 con WSL

|Nombre del grafo |	Numero de nodos | Numero de aristas |	Numero cromatico |	Tiempo Memético |	Resultado Memético |	Tiempo Busqueda Dispersa |	Resultado Busqueda Dispersa |	Tiempo Ant Colony |	Resultado Ant Colony |
|-----------------|------------------|-------------------|------------------|----------------|-------------------|----------------------|-------------------------|--------------|------------------|
DSJC250.5.col |	250 | 15668 | 31 | 121,253 |  40   | 195,901        | 40 | 623,218          | 40 |
DSJC250.9.col | 250 | 27897 | 75 | 189,173 |  91   | 427,642        | 91 | 878,744          | 89 |
le450_15b.col | 450 | 8169  | 15 |	130,936|	18 | Mas de 20 min  | ?  | Mas de 20 min    | ?  |
le450_15c.col | 450 | 16680 | 15 |	74,953 |	26 | Mas de 20 min  | ?  | Mas de 20 min    | ?  |
le450_25c.col | 450 | 17343 | 25 |	114,26 |	31 | Mas de 20 min	| ?  | Mas de 20 min    | ?  |
queen5_5.col  | 25  | 320   | 5	 |  1,308  |	7  | 7,719	        | 7	 | 1,158            | 5  |
fpsol2.i.1.col| 496 | 11654 | 65 |	374,592|	65 | Mas de 20 min  | ?  | Mas de 20 min    | ?  |
zeroin.i.3.col| 206 | 3540	| 30 |	32,085 |	30 | 473,614	    | 30 | 486,546          | 51 |
mulsol.i.1.col| 197	| 3925	| 49 |	31,332 |	49 | 512,685	    | 49 | 318,995          | 61 |
fpsol2.i.2.col| 425 | 8688	| 30 |	128,567|	30 | Mas de 20 min	| ?  | Mas de 20 min    | ?  |

## Comparación con Corte Anterior

Con la implementación de los nuevos algoritmos pudimos mejorar nuestra solución previa en algunos de los casos. Sin embargo, por lo general, estas mejoras no fueron muy significativas y, en la mayoria de los casos, requirieron una mayor cantidad de recursos computacionales. El motivo principal por el cual las mejoras no fueron tan destacadas es porque algoritmos como Busqueda Tabu y DSatur que usamos para obtener el caso base en la mayoria de las casos, ya nos daban soluciones bastante buenas.

Particularmente, el algoritmo de la colonia de hormigas fue el que más se destacó en comparación con los algoritmos anteriores, ya que en algunos casos logró obtener soluciones más cercanas al número cromático real del grafo. Sin embargo, este algoritmo también fue el que requirió más tiempo de ejecución en la mayoría de los casos. Además, en algunos casos, como en los grafos de la fuente LEI, el algoritmo de la colonia de hormigas no logró encontrar una solución en el tiempo asignado.

En el caso de la búsqueda dispersa y el algoritmo memético, estos algoritmos lograron mejorar las soluciones obtenidas por DSatur en algunos casos, pero en general, no lograron superar significativamente el rendimiento de DSatur en términos de tiempo de ejecución y calidad de la solución. Especialmente en Búsqueda Dispersa, donde en la mayoria de los casos no logró encontrar una solución en el tiempo asignado. Mientras que el algoritmo memético logró encontrar soluciones en la mayoria de los casos, pero no logró mejorar significativamente las soluciones obtenidas por DSatur.

## Conclusiones

- Los algoritmos implementados en este corte, en general, lograron mejorar las soluciones obtenidas por DSatur en algunos casos, pero en la mayoría de los casos, no lograron superar significativamente el rendimiento de DSatur en términos de tiempo de ejecución y calidad de la solución.
- El algoritmo de la colonia de hormigas fue el que más se destacó en comparación con los algoritmos anteriores, ya que en algunos casos logró obtener soluciones más cercanas al número cromático real del grafo. Sin embargo, este algoritmo también fue el que requirió más tiempo de ejecución en la mayoría de los casos, y el que tuvo más dificultades para encontrar soluciones en algunos casos. Por lo mismo, si bien es un algoritmo que puede encontrar soluciones de alta calida, es muy variable en cuanto a su rendimiento.
- La búsqueda dispersa y el algoritmo memético lograron encontrar soluciones en la mayoría de los casos, pero no lograron mejorar significativamente las soluciones obtenidas por DSatur. En el caso de la búsqueda dispersa, en la mayoria de los casos no logró encontrar una solución en el tiempo asignado.
- Comparando el algoritmo memético con el algoritmo genético implementado en el corte anterior, podemos observar que el algoritmo memético es una buena derivación del algoritmo genético, ya que logra mejorar o igualar las soluciones obtenidas por el algoritmo genético en la mayoría de casos, pero en general, no logra superar significativamente el rendimiento del algoritmo genético en términos de tiempo de ejecución y calidad de la solución.