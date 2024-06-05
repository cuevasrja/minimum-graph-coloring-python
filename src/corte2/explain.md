# Corte 2 - Minimum Graph Coloring

**Realizado Por:**
- Joao Pinto. (17-10490)
- Jhonaiker Blanco. (18-10784)
- Juan Cuevas. (19-10056)

En este corte se implementaron soluciones para el problema de coloración mínima de grafos. En particular, se implementaron los siguientes algoritmos:

- Búsqueda Local Iterativa
- Búsqueda Tabú
- Recocido Simulado
- Algoritmo Genético
- GRASP

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
| Grafo 1 | DSJC250.5.col   | 250             | 15668           | **DSJC**        | Desconocido      |
| Grafo 2 | DSJC250.9.col   | 250             | 27897           | **DSJC**        | Desconocido      |
| Grafo 3 | le450_15b.col   | 450             | 8169            | **LEI**         | 15               |
| Grafo 4 | le450_15c.col   | 450             | 16680           | **LEI**         | 15               |
| Grafo 5 | le450_25c.col   | 450             | 17343           | **LEI**         | 25               |
| Grafo 6 | queen5_5.col    | 25              | 320             | **SGB queen**   | 5                |
| Grafo 7 | fpsol2.i.1.col  | 496             | 11654           | **REG**         | 65               |
| Grafo 8 | fpsol2.i.2.col  | 451             | 8691            | **REG**         | 30               |
| Grafo 9 | zeroin.i.3.col  | 206             | 3540            | **REG**         | 30               |
| Grafo 10| mulsol.i.1.col  | 197             | 3925            | **REG**         | 49               |


## Soluciones implementadas

### Algoritmo de Búsqueda Local Iterativa

Este algoritmo se basa en la idea de que se puede mejorar una solución inicial iterativamente, cambiando los colores de los nodos de manera local. En cada iteración, se selecciona un nodo aleatorio y se le asigna un color aleatorio. Si la solución resultante es mejor que la anterior, se actualiza la solución actual. Este proceso se repite hasta que no se puedan mejorar más las soluciones.

Para la implementación de este algoritmo, se utilizó una función de evaluación que mide la calidad de una solución en términos de la cantidad de vértices en cada partición. En particular, se utilizó la siguiente función de evaluación:

$$f(\text{coloring}) = \sum_{i=1}^{n} C_i^{2}$$

Donde $C_i$ es el conjunto de nodos de color $i$ y $n$ es el número de colores utilizados. Nótese que son particiones de los nodos, por lo que la función de evaluación es el cuadrado de la cantidad de nodos de cada color.

#### Pseudocódigo

```python
def iterative_local_search(graph):
    # Primera iteración de la busqueda local
    local_search(graph)
    # Calcular porcentajes de iteraciones
    amount_of_colors, current_colors_in_graph = graph.colors_used()
    iterations_percentage = calculate_rounded_percentages(amount_of_colors)
    # Guardar la mejor solución
    best_solution = graph.coloring_as_dict()
    best_number_of_colors = amount_of_colors

    NON_IMPROVEMENT_LIMIT = 5
    non_improvement_count = 0

    # Por cada ronda de perturbación
    for clear_pct in iterations_percentage:
        # Calcular cuantos colores se deben eliminar
        expeted_to_clear = int(clear_pct * amount_of_colors / 100)
        colors_to_clear = get_random_values(current_colors_in_graph, expeted_to_clear)
        # Perturbar la solución eliminando colores
        graph.uncolor(colors_to_clear)
        # Rellenar los colores eliminados con D-Satur y búsqueda local
        graph.local_search()
        amount_of_colors, current_colors_in_graph = graph.colors_used()
        # Actualizar la mejor solución
        if amount_of_colors < best_number_of_colors:
            best_solution = graph.coloring_as_dict()
            best_number_of_colors = amount_of_colors
            non_improvement_count = 0
        else:
            non_improvement_count += 1
        if non_improvement_count >= NON_IMPROVEMENT_LIMIT:
            break
    graph.apply_coloring_dict(best_solution)
```

### Algoritmo de Búsqueda Tabú

Similar al algoritmo de búsqueda local iterativa, el algoritmo de búsqueda tabú se basa en la idea de que se puede mejorar una solución iterativamente, cambiando los colores de los nodos de manera local. Sin embargo, en este caso, se mantiene una lista de soluciones tabú, que son soluciones que no se pueden visitar nuevamente en un número determinado de iteraciones. Esto permite explorar el espacio de soluciones de manera más amplia y evitar caer en óptimos locales.

Para la implementación de este algoritmo, se utilizó una lista de soluciones tabú, que se actualiza cada vez que se encuentra una solución mejor que la anterior. Además, se utilizó una función de evaluación que mide la calidad de una solución en términos de la cantidad de conflictos entre los nodos.

$$\text{fitness}(\text{coloring}) = \sum_{v \in N} \text{conflicts}(v)$$

Donde $\text{conflicts}(v)$ es el número de conflictos del nodo $v$, es decir, el número de nodos adyacentes al nodo $v$ que tienen el mismo color.

#### Pseudocódigo

```python
def tabu_search(graph):
    # Inicializar la lista tabú
    tabu_list: List[Dict[int, str]] = []

    # Inicializar la mejor solución encontrada
    self.d_satur()
    best_solution: Dict[int, str] = self.coloring_as_dict()
    best_fitness: int = get_fitness(self, best_solution)

    # Realizar la búsqueda tabú
    for iter_count in range(max_iter):
        # Seleccionar el vecino con mejor fitness
        best_local_solution, best_local_fitness = get_best_neighbor(self, best_solution)

        # Actualizar la mejor solución global
        if best_local_fitness < best_fitness:
            best_solution = best_local_solution
            best_fitness = best_local_fitness

        # Actualizar la lista tabú
        tabu_list.append(best_local_solution)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

    # Colorear el grafo con la mejor solución encontrada
    self.apply_coloring_dict(best_solution)
```

### Algoritmo de Recocido Simulado

El algoritmo de recocido simulado es una técnica de optimización que se inspira en el proceso de recocido de los metales. En este algoritmo, se mantiene una temperatura que controla la probabilidad de aceptar movimientos peores. En cada iteración, se genera un movimiento aleatorio, y se calcula la probabilidad de aceptar el movimiento. Si la probabilidad es mayor que un número aleatorio, se acepta el movimiento. Este proceso se repite durante un número determinado de iteraciones, y la temperatura se reduce gradualmente. De esta manera, el algoritmo puede escapar de óptimos locales y explorar el espacio de soluciones de manera más amplia.

Como función de evaluación se utilizó la siguiente función:

$$f(\text{coloring}) = \sum_{i=1}^{n} C_i^{2}$$

Donde $C_i$ es el conjunto de nodos de color $i$ y $n$ es el número de colores utilizados. Nótese que son particiones de los nodos, por lo que la función de evaluación es el cuadrado de la cantidad de nodos de cada color.

#### Pseudocódigo

```python
def simulated_annealing(graph):
    mode = 'MAX'

    temperature: float = 16.0 # Temperatura inicial
    cooling_rate: float = 0.1  # efectivamente sera (1 - cooling_rate) = 0.9
    freezing_temperature: float = 0.02  # Cerca de 50 iteraciones
    freezing_counter: int = 0 # Contador de congelamiento
    # La solución inicial es D-Satur
    graph.d_satur()
    # Constantes del algoritmo
    FREEZE_LIM = 3 # Numero de veces que la temperatura debe ser menor a freezing_temperature
    TRIALS_LIM = 100  # Numero de exploraciones por valor de temperatura
    # Mejor solución encontrada
    best_coloring: Dict[int, str] = graph.coloring_as_dict()
    best_eval: int = f(best_coloring)

    current_coloring: Dict[int, str] = best_coloring
    # Criterio de congelamiento
    while freezing_counter < FREEZE_LIM:
        trials = 0
        best_changed = False
        # Criterio de parada
        while trials < TRIALS_LIM:
            # Obtenemos la vecindad de Kempe
            neighbours = graph.kempe_neighbourhood()
            # Random shuffle a la vecindad
            random.shuffle(neighbours)
            for neighbour in neighbours:
                # Calcular la probabilidad de aceptar el movimiento
                prob = movement_probability(current_coloring, neighbour, temperature, mode)
                # Si el movimiento es aceptado
                if random.random() < prob:
                    current_coloring = neighbour
                    graph.apply_coloring_dict(current_coloring)
                    # Actualizar la mejor solución
                    if (mode == 'MAX' and f(current_coloring) > best_eval) or (mode == 'MIN' and f(current_coloring) < best_eval):
                        best_coloring = current_coloring
                        best_eval = f(best_coloring)
                        best_changed = True
                trials += 1
                if trials >= TRIALS_LIM:
                    break
        # Actualizar la temperatura
        temperature *= 1 - cooling_rate
        # Actualizar el contador de congelamiento
        if temperature < freezing_temperature and not best_changed:
            freezing_counter += 1
    # Aplicar la mejor solución encontrada
    graph.apply_coloring_dict(best_coloring)
```

### Algoritmo Genético

Un algoritmo genético es una técnica de optimización inspirada en la evolución biológica. En este algoritmo, se mantiene una población de soluciones, que se cruzan y mutan para generar nuevas soluciones. Estas nuevas soluciones compiten entre sí, y las mejores soluciones se seleccionan para la siguiente generación. Este proceso se repite durante un número determinado de generaciones. Particularmente, en el problema de coloración de grafos, se pueden utilizar operadores de cruce y mutación específicos para generar nuevas soluciones. Además, se pueden utilizar operadores de selección para seleccionar las mejores soluciones de la población.

En este caso, se utilizó la siguiente función de evaluación la suma de los conflictos de cada nodo:

$$f(\text{coloring}) = \sum_{v \in N} \text{conflicts}(v)$$

Donde $N$ es el conjunto de nodos del grafo y $\text{conflicts}(v)$ es el número de conflictos del nodo $v$, es decir, el número de nodos adyacentes al nodo $v$ que tienen el mismo color.

#### Pseudocódigo

```python
def genetic_algorithm(graph):
    mode = 'MIN'
    def find_best_solution(population):
        return min(population, key=f) if mode == 'MIN' else max(population, key=f)

    # Generar población inicial
    population: List[Dict[int, str]] = create_population(graph, population_size)
    # Evaluar la población inicial
    best_solution: Dict[int, str] = find_best_solution(population)
    best_score: int = f(best_solution)
    # Evolución de la población
    for i in range(generations):
        # Seleccionar K  parejas de padres
        K = population_size // 2
        parents: List[List[Dict[int, str]]] = get_parents(population, K, f, mode)
        # Cruzar las parejas de padres para obtener K hijos
        children: List[Dict[int, str]] = [crossover(graph, p) for p in parents]
        # Mutar a los K hijos
        children = [mutate(graph, c, mutation_rate) for c in children]
        # Agregar a la población a los K hijos
        population.extend(children)
        # Seleccionar K + 1 individuos de la población según que tan malo es su desempeño
        killed = random.choices(population, k=K + 1, weights=[
            f(c) if mode == 'MIN' else 1 / f(c) for c in population
        ])
        population = [p for p in population if p not in killed]
        # Actualizar la mejor solución
        generation_best = find_best_solution(population)
        generation_best_score = f(generation_best)
        if (mode == 'MIN' and generation_best_score < best_score) or (mode == 'MAX' and generation_best_score > best_score):
            best_solution = generation_best
            best_score = generation_best_score
        # Agregar a la mejor solución a la población (intensificación)
        population.append(best_solution)
    # Aplicar mejor solución
    graph.apply_coloring_dict(best_solution)
```

### Algoritmo GRASP

El algoritmo GRASP (Greedy Randomized Adaptive Search Procedure) es una técnica de búsqueda local que combina la exploración de soluciones con la explotación de soluciones. En cada iteración, se construye una solución de manera aleatoria, y se mejora iterativamente mediante una búsqueda local. Además, se mantiene una lista de soluciones tabú, que son soluciones que no se pueden visitar nuevamente en un número determinado de iteraciones. Este proceso se repite durante un número determinado de iteraciones, y se selecciona la mejor solución encontrada. Adicionalmente, se utiliza un valor alpha para controlar la cantidad de aleatoriedad en la construcción de las soluciones.

#### Pseudocódigo

```python
def grasp(G: Graph, max_iter: int = 100, alpha: float = 0.5) -> None:
    n: int = len(G.vs)
    colors: List[int] = []
    best_number_of_colors: int = n
    best_colors: List[int] = []
    for _ in range(max_iter):
        # Fase de construcción
        colors, color_count = select_random_permutation(G, n, alpha)

        # Fase de búsqueda local
        for node in random.sample(range(n), n):
            for color in range(color_count):
                if color != colors[node] and all(colors[neighbor] != color for neighbor in G.neighbors(node)):
                    old_color: int = colors[node]
                    colors[node] = color
                    if old_color not in colors:
                        color_count -= 1
                    break
    if color_count < best_number_of_colors:
        best_number_of_colors = color_count
        best_colors = colors

    for i, color in enumerate(best_colors):
        G.vs[i]["color"] = color
```

## Experimentos y Resultados

Por motivos de practicidad, se le asignó a cada algoritmo un tiempo máximo de 5 minutos para terminar su ejecución.

Las pruebas fueron realizadas en un equipo con las siguientes características: 

- **Procesador**: Ryzen 7 7735H 
- **Memoria RAM**: 32GB 
- **SO**: Windows 11 con WSL


## Comparación con Corte Anterior

Con la implementación de los nuevos algoritmos pudimos mejorar nuestra solución previa en algunos de los casos. Sin embargo, por lo general, estas mejoras no fueron muy significativas y, en general, requirieron una mayor cantidad de recursos computacionales. El motivo principal por el cual las mejoras no fueron tan destacadas es porque el algoritmo de DSatur que usamos para obtener el caso base en la mayoria de las casos, ya nos daba una solucion bastante buena

Particularmente, el algoritmo GRASP (Greedy Randomized Adaptive Search Procedure) mostró una mejora en un caso específico, logrando una solución mejor en comparación con la anterior. No obstante, en términos generales, GRASP ofreció soluciones bastante peores. Esto es comprensible dado que GrASP no utiliza DSatur como base, lo que limita su capacidad para encontrar soluciones óptimas de manera consistente.

Los mejores resultados se observaron con los algoritmos Iterative Local Search (ILS) y Tabu Search. Estos algoritmos lograron mejoras bastante buenas en algunos casos. ILS, con su enfoque en mejorar soluciones a través de iteraciones locales, y Tabu Search, con su capacidad para evitar ciclos y explorar nuevas áreas del espacio de soluciones, demostraron ser efectivos en la obtención de mejores soluciones en comparación con los métodos anteriores.

## Conclusiones

<!-- TODO -->

