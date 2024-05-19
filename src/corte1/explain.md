# Corte 1 - Minimum Graph Coloring

**Realizado Por:**
- Joao Pinto. (17-10490)
- Jhonaiker Blanco. (18-10784)
- Juan Cuevas. (19-10056)

En este corte se implementaron soluciones para el problema de coloración mínima de grafos. En particular, se implementaron los siguientes algoritmos:

- Busqueda Local con vecindad de Kempe
- Heurística especializada: D-Satur
- Solución Exacta: Backtracking

Para la implementación de estos algoritmos se utilizó el lenguaje de programación Python, y se utilizó la librería iGraph para la representación de grafos y algunas operaciones sobre estos.

## El problema de coloración de grafos

El problema de coloración de grafos es un problema clásico en teoría de grafos y consiste en asignar colores a los vértices de un grafo de tal manera que no haya dos vértices adyacentes (es decir, conectados directamente por una arista) que tengan el mismo color. 

El objetivo es minimizar el número de colores utilizados, es decir, encontrar la coloración con el menor número de colores posible. El número mínimo de colores necesarios para colorear un grafo se conoce como el número cromático del grafo.

## Benchmark para el problema de coloración de grafos

Un benchmark es un conjunto de instancias de un problema que se utilizan para comparar diferentes algoritmos y evaluar su rendimiento. 

Para el problema de coloración de grafos, en la literatura es comun utilizar un conjunto de instancias seleccionadas por el DIMACS (Center for Discrete Mathematics and Theoretical Computer Science) para evaluar los algoritmos de coloración de grafos. El conjunto de instancias DIMACS contiene grafos con diferentes tamaños y densidades, que a su vez provienen de diferentes aplicaciones, esto permite evaluar el rendimiento de los algoritmos en diferentes escenarios.

Este benchmark se diseñó para [el segundo desafío de coloración de grafos de DIMACS](http://dimacs.rutgers.edu/archive/Challenges/#:~:text=NP-,Hard,-Problems%3A%20Maximum%20Clique). Para este corte, se utilizaron algunas instancias de este benchmark para evaluar los algoritmos implementados. 

En concreto se seleccionaron instancias DIMACS asociadas a las siguientes fuentes:

- **DSJC**: Generados por David Johnson, grafos utilizados en su articulo con Aragon, McGeoch y Schevon, _"Optimization by Simulated Annealing: An Experimental Evaluation; Part II, Graph Coloring and Number Partitioning"_, Operations Research 39, 378-406, 1991. Son grafos $(n, p)$ aleatorios estándar con densidad de aristas $p$.
- **REG**: Generados por Gary Lewandowski, son grafos asociados al problema de _"Register Allocation"_, los grafos provienen de programas reales.
- **LEI**: Generados por Craig Morgenstern. Son grafos de Leighton con tamaño de coloración garantizado. Una referencia es F.T. Leighton, Journal of Research of the National Bureau of Standards, 84: 489--505 (1979).
- **MYC**: Grafos basados en la [transformarción de Mycielski](https://en.wikipedia.org/wiki/Mycielskian).
- **SGB queen**: Grafos asociados al [problema de las n-reinas](https://en.wikipedia.org/wiki/Eight_queens_puzzle) para tableros de ajedrez de tamaño $n \times n$.

Los grafos seleccionados se encuentran en la carpeta [data](../../data/) y se describen a continuación:

### Tabla de grafos

| Grafo   | Archivo         | Número de nodos | Número de lados | Fuente          | Número cromático |
|---------|-----------------|-----------------|-----------------|-----------------|------------------|
| Grafo 1 | DSJC250.5.col   | 250             | 15668           | **DSJC**        | Desconocido      |
| Grafo 2 | DSJC250.9.col   | 250             | 27897           | **DSJC**        | Desconocido      |
| Grafo 3 | fpsol2.i.1.col  | 496             | 11654           | **REG**         | 65               |
| Grafo 4 | fpsol2.i.2.col  | 451             | 8691            | **REG**         | 30               |
| Grafo 5 | fpsol2.i.3.col  | 425             | 8688            | **REG**         | 30               |
| Grafo 6 | inithx.i.1.col  | 864             | 18707           | **REG**         | 54               |
| Grafo 7 | inithx.i.2.col  | 645             | 13979           | **REG**         | 31               |
| Grafo 8 | inithx.i.3.col  | 621             | 13969           | **REG**         | 31               |
| Grafo 9 | le450_15b.col   | 450             | 8169            | **LEI**         | 15               |
| Grafo 10| le450_15c.col   | 450             | 16680           | **LEI**         | 15               |
| Grafo 11| le450_25c.col   | 450             | 17343           | **LEI**         | 25               |
| Grafo 12| mulsol.i.1.col  | 197             | 3925            | **REG**         | 49               |
| Grafo 13| myciel3.col     | 11              | 20              | **MYC**         | 4                |
| Grafo 14| queen5_5.col    | 25              | 320             | **SGB queen**   | 5                |
| Grafo 15| zeroin.i.3.col  | 206             | 3540            | **REG**         | 30               |

## Soluciones implementadas

### Heurística especializada: D-Satur

Este algoritmo es una heurística especializada para el problema de coloración de grafos, y su componente principal es el coloreado de nodos según su grado de saturación. El grado de saturación de un nodo es la cantidad de colores diferentes que tiene en sus vecinos. El algoritmo selecciona el nodo con mayor grado de saturación y le asigna el color que minimice la cantidad de conflictos.

#### Pseudocódigo

```python
def dsatur(G: Grafo):
    while True:
        max_saturacion: Vertex = vertice_con_mayor_saturacion(G)

        if (max_saturacion == -1):
            break

        colores_adyacentes: Set[str] = colores_de_adyacentes(G, max_saturacion)

        color_to_paint: str = primer_elemento_no_perteneciente(G.colors, colores_adyacentes)

        cambiar_color_y_aumentar_saturacion(G, max_saturacion, color_to_paint)
```

### Solución Exacta: Backtracking

La solución exacta implementada se basa en el algoritmo de backtracking, donde se prueban todas las posibles combinaciones de colores para los nodos del grafo. Para este algoritmo, se implementó una variante que permite podar el árbol de búsqueda, podando aquellas coloraciones parciales que no sean válidas ó que produzcan soluciones con mayor numero de colores que la mejor solucion hasta el momento.

#### Pseudocódigo

```python
mejor_cantidad_colores: int = 0
mejores_colores: List[str] = []

def backtracking(G: Grafo) -> int:
    global mejor_cantidad_colores, mejores_colores

    G.reset_colors()

    mejor_cantidad_colores = len(G.vs)

    # Buscamos la mejor solución para este grafo
    backtrack(G, 0)

    # Aplicamos la mejor solución encontrada
    if len(mejores_colores) > 0:
        for i, v in enumerate(G.vs):
            v['color'] = mejores_colores[i]

        return len(mejores_colores)

    return -1

def backtrack(G: Grafo, node_index: int):
    global mejor_cantidad_colores, mejores_colores

    if G.is_colored():
        if G.is_valid_coloring() and G.number_of_colors() < mejor_cantidad_colores:
            mejor_cantidad_colores = G.number_of_colors()
            mejores_colores = [v['color'] for v in self.vs]

        return

    for c in range(len(self.vs)):
        color: str = f'{c}'

        # Si ya se encontró una coloración con menos colores, se puede podar
        if c > mejor_cantidad_colores - 1:
            return

        # Si la coloración no es válida, se puede podar
        if self.is_safe_to_color(node_index, color):
            # Asignar el color al nodo
            self.vs[node_index]['color'] = color

            # Si aun es posible encontrar una coloración con menos colores, continuar con la búsqueda
            if G.number_of_colors() < mejor_cantidad_colores:
                backtrack(G, node_index + 1)

            # Backtrack
            self.vs[node_index]['color'] = ''
```

### Búsqueda Local con vecindad de Kempe

El algoritmo de búsqueda local explora el espacio de soluciones a partir de una solución inicial, moviéndose a soluciones vecinas que mejoren la solución actual. 

Para esta implementación, se utilizó la vecindad de Kempe, la cual consiste en intercambiar los colores de las componentes conexas de los subgrafos inducidos por los nodos que tienen dos colores fijos, para todos los pares de colores diferentes presentes en la solución.

El pseudocódigo para hallar la vecindad de Kempe para una coloración $C$ del grafo $G = (N, E)$ es el siguiente:

- Inicializar $V$ como el conjunto vacío.
- Para cada par de colores $i$ y $j$ diferentes en $C$:
    - Hallar $G_{ij}$, el subgrafo inducido por los nodos que tienen los colores $i$ y $j$.
    - Hallar $H_{ij}$, las componentes conexas de $G_{ij}$.
    - Para cada componente conexa $h$ en $H_{ij}$:
        - Construir $C'$ a partir de $C$ intercambiando los colores de los nodos en $h$, es decir:
          - Para cada nodo $n$ en $h$:
            - Si $C(n) = i$, entonces $C'(n) = j$.
            - Si $C(n) = j$, entonces $C'(n) = i$.
            - Si $C(n) \neq i$ y $C(n) \neq j$, entonces $C'(n) = C(n)$.
        - $V = V \cup \{C'\}$
- Retornar $V$.

Se puede demostrar que esta vecinidad solo contiene soluciones válidas. 

Para la implementación de búsqueda local, es necesario definir una función de evaluación que permita comparar dos soluciones. En este caso, se utilizó la función de evaluación $f(C) = \sum |N_i|^2$ para $0 \leq i \leq k, donde $N_i$ es el conjunto de nodos que tienen el color $i$ en la coloración $C$. Cuando de maximiza esta función, se minimiza la cantidad de colores utilizados.

Como solución inicial, se utilizó la salida del algoritmo de D-Satur.

A continuación se presenta el pseudocódigo de la búsqueda local:

#### Pseudocódigo

```python
def busqueda_local(G: Grafo):
    # Nuestra solución inicial será la salida de D-Satur
    d_satur(G)

    # Obtenemos la vecindad de Kempe ordenada por evaluación f
    _, mejor, mejor_eval = G.kempe_ordenado()

    # Mientras la evaluación de la mejor solución vecina sea mejor que la actual
    while mejor is not None and mejor_eval > f(G.coloracion()):
        # Aplicamos el mejor vecino
        G.aplicar_coloracion(mejor)

        # Obtenemos la vecindad de Kempe ordenada por evaluación
        _, mejor, mejor_eval = G.kempe_ordenado()
```

## Resultados

Por temas de practicidad, se le asignó a cada algoritmo un tiempo máximo de 5 minutos para terminar su ejecución.

Las pruebas fueron realizadas en un equipo con las siguientes caracteristicas:

- **Procesador**: Ryzen 7 7735H
- **Memoria ram**: 32GB
- **SO**: Windows 11 

Acontinuación se presentan los resultados obtenidos para cada grafo:

| Grafo    |Número cromático| Tiempo con Dsatur | Colores con Dsatur | Tiempo con busqueda local | Colores con busqueda local       | Tiempo con Backtracking | Colores con bactracking |
|----------|----------------|-------------------|---------|---------------------------|----------------|-------------------------|-------------------------|
| Grafo 1  | Desconocido    | 0.12098 segundos  |  42     |   32.37499 segundos       |  41            |    Más de 5 minutos     |      No calculados      |
| Grafo 2  | Desconocido    | 0.07322 segundos  |  97     |   57.06781 segundos       |  92            |    Más de 5 minutos     |      No calculados      |
| Grafo 3  | 65             | 0.10175 segundos  |  65     |   251.55769 segundos      |  65            |    Más de 5 minutos     |      No calculados      |
| Grafo 4  | 30             | 0.08047 segundos  |  30     |   31.34456 segundos       |  30            |    Más de 5 minutos     |      No calculados      |
| Grafo 5  | 30             | 0.07440 segundos  |  30     |   31.49850 segundos       |  30            |    Más de 5 minutos     |      No calculados      |
| Grafo 6  | 54             | 0.26938 segundos  |  54     |   Más de 5 minutos        |  No calculados |    Más de 5 minutos     |      No calculados      |
| Grafo 7  | 31             | 0.15670 segundos  |  31     |   76.5435 segundos        |  31            |    Más de 5 minutos     |      No calculados      |
| Grafo 8  | 31             | 0.15550 segundos  |  31     |   93.1823 segundos        |  31            |    Más de 5 minutos     |      No calculados      |
| Grafo 9  | 15             | 0.08113 segundos  |  18     |   5.40957 segundos        |  18            |    Más de 5 minutos     |      No calculados      |
| Grafo 10 | 15             | 0.09588 segundos  |  26     |   13.0586 segundos        |  25            |    Más de 5 minutos     |      No calculados      |
| Grafo 11 | 25             | 0.09588 segundos  |  31     |   26.3236 segundos        |  29            |    Más de 5 minutos     |      No calculados      |
| Grafo 12 | 49             | 0.02099 segundos  |  49     |   17.8212 segundos        |  49            |    Más de 5 minutos     |      No calculados      |
| Grafo 13 | 4              | 0.00099 segundos  |  4      |   0.00300 segundos        |  4             |    0.02290 segundos     |      4                  |
| Grafo 14 | 5              | 0.00099 segundos  |  8      |   0.00700 segundos        |  7             |    0.01354 segundos     |      5                  |
| Grafo 15 | 30             | 0.02092 segundos  |  30     |   4.46516 segundos        |  30            |    Más de 5 minutos     |      No calculados      |


## Conclusiones

En general, el algoritmo DSatur demostró ser capaz de dar soluciones muy buenas e incluso óptimas en algunos casos, todo esto en un tiempo de ejecución muy bajo. Sin embargo, en algunos casos, la solución obtenida no es la óptima, pero sigue siendo bastante buena.

La busqueda local es bastante útil para mejorar soluciones, no siempre se mejora la solución obtenida con DSatur, pero en algunos casos se logra una mejora significativa. A pesar de tener un tiempo de ejecución mayor que DSatur, es mucho menor que el de backtracking y en la mayoría de los casos sigue siendo aceptable.

El backtracking obtiene soluciones óptimas pero por lo general no es utilizable en grafos grandes, los tiempos de ejecución son demasiado altos, por lo que solo hace sentido utilizarlo en grafos pequeños.