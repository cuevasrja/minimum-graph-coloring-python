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


**Para este corte se decidió remover algunos grafos en donde DSatur daba una solución óptima, para poder evaluar significativamente el rendimiento de los nuevos algoritmos implementados.**

## Soluciones implementadas

### Algoritmo Memético

Un Algoritmo Memético es una técnica de optimización computacional que combina la búsqueda heurística local con la búsqueda evolutiva basada en poblaciones, inspirada en los procesos de evolución biológica.

Los algoritmos meméticos funcionan de manera similar a los algoritmos genéticos, pero incorporan un paso adicional de mejora para refinar las soluciones individuales, asi como tambien extienden la nocion de cruce para permitir combinacion entre mas de dos padres. Esto les permite superar algunas de las limitaciones de los algoritmos genéticos, como la convergencia prematura a soluciones subóptimas y la dificultad para encontrar soluciones de alta calidad en espacios de búsqueda complejos.

En nuestra implementación, se utilizó la siguiente función de evaluación la suma de los conflictos de cada nodo:

$$f(\text{coloring}) = \left(\left(\sum_{v \in N} \text{conflicts}(v, \text{coloring})\right) + 1\right) \cdot \text{ncolors}(\text{coloring})$$

Donde $N$ es el conjunto de nodos del grafo, $\text{conflicts}(v, \text{coloring})$ es el número de conflictos del nodo $v$ en la coloración, es decir, el número de nodos adyacentes al nodo $v$ que tienen el mismo color, y $\text{ncolors}(\text{coloring})$ es el número de colores utilizados en la coloración.

Esta función de evaluación penaliza las soluciones con conflictos y favorece las soluciones con menos colores. 

#### Operador de combinación de padres

En este proyecto se utilizo el operador de cruce voraz de particiones con lista tabú tal como se vio en clases para el caso de `n = 3`. 

Este operador obtiene la clase de color con mayor cardinalidad, colorea esa clase en la solucion hija, elimina los nodos de la clase de color de los padres, elimina el color de las clase de color de los padres y repite el proceso hasta que la solucion hija este completa.

Para no tomar el mismo padre en la siguiente iteracion, se utiliza una lista tabú que almacena los padres que ya han sido seleccionados, esta lista garantiza que no se seleccione el padre seleccionado por tres iteraciones.

#### Metodo de mejora

Nuestro metodo de mejora asegura que todos los hijos sean soluciones validas, ademas de esto, mejora su aptitud ejecutando busqueda local.

Para asegurar que todos los hijos sean validos, descolorea todos los nodos que tengan conflictos y aplica D-Satur para colorear los nodos descoloreados.

Por limitaciones de tiempo de ejecucion, la mejora de busqueda local solo se aplica en la ultima iteracion del algoritmo.

#### Pseudocódigo

```python
def memetic_algorithm(graph: Graph):
    # Hiperparámetros del algoritmo memetico
    population_size: int = 100
    generations: int = 3
    mutation_rate: float = 0.5

    def find_best_solution(population):
        return min(
            population, key=eval_sol) if mode == 'MIN' else max(population, key=eval_sol)
    # Generar población inicial
    population: List[Dict[int, str]] = create_population(graph, population_size)
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

        # Mejorar a los hijos, se usa solo DSatur en todas las generaciones menos en la ultima, ahi tambien se usa busqueda local
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


### Búsqueda Dispersa

La Búsqueda Dispersa es una técnica de optimización metaheurística basada en la búsqueda iterativa de mejores soluciones dentro de un conjunto de soluciones factibles. A diferencia de los algoritmos de búsqueda local, que se enfocan en mejorar una solución individual, la búsqueda dispersa explora el espacio de búsqueda de manera más amplia mediante la combinación y diversificación de soluciones existentes.

En nuestra implementación, se utilizó la misma función de evaluación que en el algoritmo memético, la suma de los conflictos de cada nodo:

$$f(\text{coloring}) = \left(\left(\sum_{v \in N} \text{conflicts}(v, \text{coloring})\right) + 1\right) \cdot \text{ncolors}(\text{coloring})$$

#### Nocion de distancia

TODO

#### Indice de diversidad

TODO

#### Indice de evaluacion

TODO

#### Generación de soluciones pro-diversidad

TODO

#### Operador de re-enlazado de caminos

TODO

#### Pseudocódigo

```python
def disperse_search(G: grafo):
    # Generar población inicial
    population: List[Dict[int, str]] = create_population(self, population_size)

    # Evaluar la población inicial
    best_solution: Dict[int, str] = find_best_solution(population)
    best_score: int = eval_sol(best_solution)

    # Evolución de la población
    for i in range(generations):
        # Generar population_size // 2 soluciones diversas
        diverse_solutions = pro_diverse_gen(
            G, population, population_size // 2)

        # Agregar las soluciones diversas a la población
        population.extend(diverse_solutions)

        # Aplica re-enlazado de caminos a un porcentaje de las soluciones
        n_tracing = int(TRACING_PCT * len(population))
        tracing_pairs = select_tracing_pairs(population, n_tracing)

        # Aplicar reenlazado de caminos
        traced_solutions = []
        for [sol_a, sol_b] in tracing_pairs:
            traced_solutions.extend(trace_path(G, sol_a, sol_b))

        # Agregar las soluciones re-enlazadas a la población
        population.extend(traced_solutions)

        # Seleccionar K tripletas de padres
        K = population_size // 3
        parents = get_parent_triplets(population, K, lambda sol: eval_index(
            self, sol, population, ALPHA, BETA), 'MAX')

        # Cruzar las tripletas de padres para obtener K hijos
        children = [triple_point_crossover(self, p) for p in parents]

        # Mutar a los K hijos
        children = [mutate(self, c, mutation_rate) for c in children]

        # Mejorar a los hijos
        children = [enhance_sol(G, c, i, K) for i, c in enumerate(children)]

        # Agregar a la población a los K hijos
        population.extend(children)

        # Seleccionar len(population) - population_size individuos de la población según que tan malo es su eval_index
        killed = random.choices(population, k=len(population) - population_size, weights=[
            1 / eval_index(self, c, population, ALPHA, BETA) for c in population
        ])
        population = [p for p in population if p not in killed]

        # Actualizar la mejor solución
        generation_best = find_best_solution(population)
        generation_best_score = eval_sol(generation_best)

        best_solution, best_score = mejor_coloracion(generation_best, generation_best_score)

    # Aplicar mejor solución
    self.apply_coloring_dict(best_solution)
```

### Algoritmo de la Colonia de Hormigas

El Algoritmo de la Colonia de Hormigas es una técnica de optimización metaheurística inspirada en el comportamiento de las hormigas en su búsqueda de alimento. Las hormigas, a través de la comunicación mediante feromonas, logran encontrar caminos eficientes entre su nido y las fuentes de alimento. El ACO simula este comportamiento para resolver problemas complejos, especialmente aquellos que pueden representarse como un grafo, como la búsqueda de rutas óptimas o la asignación eficiente de recursos.

#### Ciclo de vida de una hormiga

En nuestra implementación, una hormiga se mueve entre los componentes de una solucion que mantiene. La hormiga cumple con su ciclo de vida cuando una solución completa ha sido construida. 

La hormiga comienza con una solucion vacia y en cada paso selecciona un par `(nodo, color)` segun la probabilidad de movimiento tal como se explico en clase.

En cada epoca, una vez que todas las hormigas han completado su ciclo de vida, se actualizan las feromonas y se reinician las hormigas.

#### Representación de feromonas

En este proyecto se mantienen dos formas de feromonas, una asociada a los componentes de la solucion y otra al orden en el que se construyen los componentes (transicion entre nodos).

Las feromonas asociadas a los componentes de la solucion se almacenan en una matriz de tamaño `n x n` donde `n` es el numero de nodos, cada celda `(i, j)` representa la feromona asociada al nodo `i` y al color `j`. Esto escencialmente representa la feromona asociada a colorear un nodo de un color especifico.

Las feromonas asociadas a las transiciones entre nodos se almacenan en una matriz de tamaño `n x n` donde `n` es el numero de nodos, cada celda `(i, j)` representa la feromona asociada a la transicion entre los nodos `i` y `j`. Esto esencialmente representa la feromona asociada a colorear un nodo despues de colorear otro nodo.

Las feromonas se actualiza en cada epoca, se evapora y se deposita feromona en las celdas correspondientes a los movimientos de las hormigas.

En concreto, se utiliza la siguiente regla de evaporación y deposito de feromonas:

$$\tau_1(i,j) = (1 - \rho) \cdot \tau_1(i,j) + \sum_{k=1}^{m} \frac{n}{\chi_k} \cdot \epsilon(k, i, j)$$

donde $\rho$ es el factor de evaporación, $\tau_1(i,j)$ es la feromona asociada a colorear el nodo $j$ inmediatamente despues de $i$, $n$ es el número de nodos, $m$ es el numero de hormigas, $\chi_k$ es el número de colores en la solución de la hormiga $k$, y $\epsilon(k, i, j)$ es una función que indica si la hormiga $k$ coloreó el nodo $j$ inmediatamente después del nodo $i$.

y de forma analoga:

$$\tau_2(i, color) = (1 - \rho) \cdot \tau_2(i,color) + \sum_{k=1}^{m} \frac{n}{\chi_k} \cdot \delta(k, i, color)$$

donde $\tau_2(i, color)$ es la feromona asociada a colorear el nodo $i$ de un color específico, y $\delta(k, i, color)$ es una función que indica si la hormiga $k$ coloreó el nodo $i$ con el color $color$.

#### Componente heurístico

El componente heurístico utilizado depende del nodo a colorear y del color seleccionado. En nuestra implementación, se utilizó la siguiente función heurística:

$$\eta(i, color) = \lambda(color) \sqrt{S_i^2 + D_i^2}$$

Donde:

$$
\lambda(color) =
\begin{cases}
    \frac{1}{n} & \text{si } \text{$color$ no está presente en la solucion} \\
    1 & \text{en otro caso}
\end{cases}
$$

$S_i$ es el grado de saturación de D-satur del nodo $i$ y $D_i$ es el grado del nodo $i$.

Esto significa que el componente heurístico favorece la selección de colores que no aunmenten el número de colores en la solución, y que favorece la selección de nodos que maximizen tanto el grado de saturación de D-satur como el grado del nodo.

En el algoritmo no se consideran aquellos colores que causen conflictos en la solución parcial.

#### Optimización multi-hilo

Para mejorar el rendimiento del algoritmo, se implementó una versión multi-hilo del algoritmo de la colonia de hormigas. En esta versión, las hormigas se dividen en `N_THREADS` grupos, y cada grupo se ejecuta en un hilo separado. Cada hilo se encarga de mover las hormigas en paralelo, y al final de cada iteración, se actualizan las feromonas en un hilo principal.

#### Pseudocódigo

```python
def ant_colony(G: grafo):
    # Parámetros del algoritmo de la colonia de hormigas
    N_ANTS = 8
    N_ITERATIONS = 3
    ALPHA = 1.5
    BETA = 5.0
    RHO = 0.1

    N_THREADS = 8


    pheromones_nodes = [ # [node][color]
        [1.0 / (len(G.vs) ** 2) for _ in range(len(self.vs))]
        for _ in range(len(self.vs))
    ]
    pheromones_pairs = [ # [node1][node2]
        [1.0 / (len(G.vs) ** 2) for _ in range(len(G.vs))]
        for _ in range(len(self.vs))
    ]
    ants_solutions = inicializar_hormigas(N_ANTS, G)

    # Agrupar las hormigas N_THREADS grupos
    ants_groups = agrupar_hormigas(N_ANTS, N_THREADS)

    best_solution, best_n_colors = None, float('inf')

    # Definir el target de los threads
    def thread_fn(ants_group: List[Ant], i: int, epoch: int):
        for _ in range(len(G.vs) - 1):
            for ant in ants_group:
                ant.move(pheromones_nodes, pheromones_pairs, ALPHA, BETA)

    for epoch in range(N_ITERATIONS):
        # Crear threads para mover las hormigas
        threads = []
        for i, ants_group in enumerate(ants_groups):
            crear_hilo_grupo(ants_group, i, epoch, thread_fn)
            threads.append(thread)
        for thread in threads:
            thread.esperar_hilo()

        # Actualizar las feromonas
        actualizar_feromonas(pheromones_nodes,  pheromones_pairs, 1 - RHO)
        for ant in ants_solutions:
            n_colors = ant.graph.number_of_colors()
            for prev_node, next_node, color in ant.movements:
                factor = len(ant.all_colors) / (n_colors)
                pheromones_nodes[next_node][int(color)] += factor
                pheromones_pairs[prev_node][next_node] += factor

        # Obtener la mejor solución
        for ant in ants_solutions:
            if not ant.graph.is_valid_coloring():
                continue
            if ant.graph.number_of_colors() < best_n_colors:
                best_solution = ant.graph.coloring_as_dict()
                best_n_colors = ant.graph.number_of_colors()
                
        reiniciar_hotmigas(ants_solutions)

    # Aplicar la mejor solución
    if best_solution:
        G.apply_coloring_dict(best_solution)
```



## Experimentos y Resultados

Por motivos de practicidad, se le asignó a cada algoritmo un tiempo máximo de 20 minutos para terminar su ejecución.

Las pruebas fueron realizadas en un equipo con las siguientes características: 

- **Procesador**: Ryzen 7 7735H 
- **Memoria RAM**: 32GB 
- **SO**: Windows 11 con WSL

|Nombre del grafo |	Numero de nodos | Numero de aristas |	Numero cromatico |  Tiempo Dsatur |	Resultado D_Satur |	Tiempo Memético |	Resultado Memético |	Tiempo Busqueda Dispersa |	Resultado Busqueda Dispersa |	Tiempo Ant Colony |	Resultado Ant Colony |
|-----------------|------------------|-------------------|------------------|----------------|-------------------|----------------------|-------------------------|--------------|------------------|------------------|------------------|
DSJC250.5.col |	250 | 15668 | 31 | 0,1034  |   42  | 121,253 |  40 | 195,901        | 40 | 623,218          | 40 |
DSJC250.9.col | 250 | 27897 | 75 | 0,237   |   97  | 189,173 |  91 | 427,642        | 91 | 878,744          | 89 |
le450_15b.col | 450 | 8169  | 15 | 0,2379  |   18  | 130,936 |	18 | Mas de 20 min  | ?  | Mas de 20 min    | ?  |
le450_15c.col | 450 | 16680 | 15 | 0,2136  |   26  | 74,953  |	26 | Mas de 20 min  | ?  | Mas de 20 min    | ?  |
le450_25c.col | 450 | 17343 | 25 | 0,213   |   31  | 114,26  |	31 | Mas de 20 min	| ?  | Mas de 20 min    | ?  |
queen5_5.col  | 25  | 320   | 5	 | 0,003   |   8   | 1,308   |	7  | 7,719	        | 7	 | 1,158            | 5  |
fpsol2.i.1.col| 496 | 11654 | 65 | 0,1567  |   65  | 374,592 |	65 | Mas de 20 min  | ?  | Mas de 20 min    | ?  |
zeroin.i.3.col| 206 | 3540	| 30 | 0,088   |   30  | 32,085  |	30 | 473,614	    | 30 | 486,546          | 51 |
mulsol.i.1.col| 197	| 3925	| 49 | 0,091   |   49  | 31,332  |	49 | 512,685	    | 49 | 318,995          | 61 |
fpsol2.i.2.col| 425 | 8688	| 30 | 0,2381  |   30  | 128,567 |	30 | Mas de 20 min	| ?  | Mas de 20 min    | ?  |

## Comparación con Corte Anterior

Con la implementación de los nuevos algoritmos pudimos mejorar nuestra solución previa en algunos de los casos. Sin embargo, por lo general, estas mejoras no fueron muy significativas y, en la mayoria de los casos, requirieron una mayor cantidad de recursos computacionales. El motivo principal por el cual las mejoras no fueron tan destacadas es porque algoritmos como Busqueda Tabu y DSatur ya nos daban soluciones bastante buenas.

Particularmente, el algoritmo de la colonia de hormigas fue el que más se destacó en comparación con los algoritmos anteriores, ya que en algunos casos logró obtener soluciones más cercanas al número cromático real del grafo. Sin embargo, este algoritmo también fue el que requirió más tiempo de ejecución en la mayoría de los casos. Además, en algunos casos, como en los grafos de la fuente LEI, el algoritmo de la colonia de hormigas no logró encontrar una solución en el tiempo asignado.

En el caso de la búsqueda dispersa y el algoritmo memético, estos algoritmos lograron mejorar las soluciones obtenidas por DSatur en algunos casos, pero en general, no lograron superar significativamente el rendimiento de DSatur en términos de tiempo de ejecución y calidad de la solución. Especialmente en Búsqueda Dispersa, donde en la mayoria de los casos no logró encontrar una solución en el tiempo asignado. Mientras que el algoritmo memético logró encontrar soluciones en la mayoria de los casos, pero no logró mejorar significativamente las soluciones obtenidas por DSatur.

## Conclusiones

- Los algoritmos implementados en este corte, en general, lograron mejorar las soluciones obtenidas por DSatur en algunos casos, pero en la mayoría de los casos, no lograron superar significativamente el rendimiento de DSatur en términos de tiempo de ejecución y calidad de la solución.
- El algoritmo de la colonia de hormigas fue el que más se destacó en comparación con los algoritmos anteriores, ya que en algunos casos logró obtener soluciones más cercanas al número cromático real del grafo. Sin embargo, este algoritmo también fue el que requirió más tiempo de ejecución en la mayoría de los casos, y el que tuvo más dificultades para encontrar soluciones en algunos casos. Por lo mismo, si bien es un algoritmo que puede encontrar soluciones de alta calida, es muy variable en cuanto a su rendimiento.
- La búsqueda dispersa y el algoritmo memético lograron encontrar soluciones en la mayoría de los casos, pero no lograron mejorar significativamente las soluciones obtenidas por DSatur. En el caso de la búsqueda dispersa, en la mayoria de los casos no logró encontrar una solución en el tiempo asignado.
- Comparando el algoritmo memético con el algoritmo genético implementado en el corte anterior, podemos observar que el algoritmo memético es una buena derivación del algoritmo genético para ciertas instancias concretas, ya que logra mejorar o igualar las soluciones obtenidas por el algoritmo genético, todo esto con un número mucho menor de generaciones, pero en general, no logra superar significativamente el rendimiento del algoritmo genético en términos de tiempo de ejecución y calidad de la solución.
