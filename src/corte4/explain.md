# Corte 3 - Minimum Graph Coloring

**Realizado Por:**

- Joao Pinto. (17-10490)
- Jhonaiker Blanco. (18-10784)
- Juan Cuevas. (19-10056)

En este corte se implementaron soluciones para el problema de coloración mínima de grafos. En particular, se implementó una metaheurística propia llamada "Heurística del Ave Cleptómana".

Para la implementación de este algoritmo se utilizó el lenguaje de programación Python, y se utilizó la librería iGraph para la representación de grafos y algunas operaciones sobre estos.

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


**Para este corte se decidió remover algunos grafos en donde DSatur daba una solución óptima, para poder evaluar significativamente el rendimiento de los nuevos algoritmos implementados.**

## Solución Implementada

### Algoritmo del ave cleptomana

El algoritmo del ave cleptomana es una técnica de optimización computacional creada por nosotros que combina los algoritmos meméticos con los métodos de apareamiento de algunas especies de ave

Ese algoritmo se diferencia de un algoritmo memético convencional en que usa un método que se encarga de colorear la mayor cantidad de de nodos posibles dentro del grafo con n colores posibles (esto debido a que las aves por lo general empiezan un nido usando las ramas más grandes como base) y luego usamos DSatur para coloreas los otros nodos con el fin de tapar las "agujeros" que quedaron en el grafo

Otra característica especial de este algoritmo es que la clase color más grande que posea cualquiera de los padres siempre se heredará

En nuestra implementación, se utilizó la siguiente función de evaluación la suma de los conflictos de cada nodo:

$$f(\text{coloring}) = \left(\left(\sum_{v \in N} \text{conflicts}(v, \text{coloring})\right) + 1\right) \cdot \text{ncolors}(\text{coloring})$$

Donde $N$ es el conjunto de nodos del grafo, $\text{conflicts}(v, \text{coloring})$ es el número de conflictos del nodo $v$ en la coloración, es decir, el número de nodos adyacentes al nodo $v$ que tienen el mismo color, y $\text{ncolors}(\text{coloring})$ es el número de colores utilizados en la coloración.

Esta función de evaluación penaliza las soluciones con conflictos y favorece las soluciones con menos colores. 

#### Operador de combinación de padres

En este proyecto se utilizó una versión modificada del operador de cruce voraz de particiones con lista tabú tal como se vio en clases para el caso de `n = 3`. 

Tomaremos la clase color más grande que posea cualquiera de los padres, a partir de ahí procedemos de manera convencional

Este operador obtiene la clase de color con mayor cardinalidad, colorea esa clase en la solución hija, elimina los nodos de la clase de color de los padres, elimina el color de las clase de color de los padres y repite el proceso hasta que la solución hija este completa.

Para no tomar el mismo padre en la siguiente iteración, se utiliza una lista tabú que almacena los padres que ya han sido seleccionados, esta lista garantiza que no se seleccione el padre seleccionado por tres iteraciones.

#### Metodo de mejora

Nuestro método de mejora asegura que todos los hijos sean soluciones válidas, ademas de esto, mejora su aptitud ejecutando busqueda local.

Para asegurar que todos los hijos sean validos, descolorea todos los nodos que tengan conflictos y aplica D-Satur para colorear los nodos descoloreados.

Por limitaciones de tiempo de ejecución, la mejora de búsqueda local solo se aplica en la última iteración del algoritmo.

#### Pseudocódigo

```python

def kleptomaniac_bird(graph: Graph):
    # Hiperparámetros del algoritmo memetico
    population_size: int = 100
    generations: int = 3
    mutation_rate: float = 0.5
    min_initial_colors_amount: float = 0.01,
    max_initial_colors_amount: float = 0.05
    

    def find_best_solution(population):
        return min(
            population, key=eval_sol) if mode == 'MIN' else max(population, key=eval_sol)

    # Generar población inicial
    population: List[Dict[int, str]] = create_population(graph, population_size, min_initial_colors_amount, max_initial_colors_amount)
    # Evaluar la población inicial

    best_solution: Dict[int, str] = find_best_solution(population)
    best_score: int = eval_sol(best_solution)

    # Evolución de la población
    for i in range(generations):
        # Seleccionar K  tripletas de padres
        K = population_size // 6
        parents: List[List[Dict[int, str]]] = get_parent_triplets(
            population, K, eval_sol, mode)

        # Cruzar las tripletas de padres para obtener K hijos
        children: List[Dict[int, str]] = [triple_partition_crossover(self, p) for p in parents]

        # Mutar a los K hijos
        children = [mutate(graph, c, mutation_rate) for c in children]

        # Mejorar a los hijos, se usa metodo del nido en todas las generaciones menos en la ultima, ahi tambien se usa busqueda local
        children = [enhance_sol(self, c, i, K, i == generations - 1) for i, c in enumerate(children)]

        # Agregar a la población a los K hijos
        population.extend(children)

        # Seleccionar K // 2 individuos de la población según que tan malo es su desempeño
        killed = random.choices(population, k=K // 2, weights=[
            eval_sol(c) if mode == 'MIN' else 1 / eval_sol(c)
            for c in population
        ])

        # Eliminar los K // 2 seleccionados
        population = [p for p in population if p not in killed]

        # Actualizar la mejor solución
        generation_best = find_best_solution(population)
        generation_best_score = eval_sol(generation_best)
        if generation_best_score < best_score:
            best_solution = generation_best
            best_score = generation_best_score
        # Agregar a la mejor solución a la población (intensificación)
        population.append(best_solution)
        
    # Aplicar mejor solución
    graph.apply_coloring_dict(best_solution)
```



## Experimentos y Resultados

Por motivos de practicidad, se le asignó a cada algoritmo un tiempo máximo de 20 minutos para terminar su ejecución.

Las pruebas fueron realizadas en un equipo con las siguientes características: 

- **Procesador**: Ryzen 7 7735H 
- **Memoria RAM**: 32GB 
- **SO**: Windows 11 con WSL

## Comparación con Corte Anterior



## Conclusiones

