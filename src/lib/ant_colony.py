from typing import List, Set
import igraph as ig
import random


class Ant:
    def __init__(self, graph: ig.Graph):
        """
        Inicializa una hormiga en un grafo dado.
        """

        self.graph = graph
        self.all_colors = set(
            str(i) for i in range(len(self.graph.vs))
        )
        self.current_node = random.randint(0, len(graph.vs) - 1)
        self.movements = []

        # Colorear el nodo actual con el color '0'
        self.graph.vs[self.current_node]['color'] = '0'

        # Inicializar el tamaño de las clases de equivalencia de los colores
        self.color_classes_sizes = {
            color: 0 for color in self.all_colors
        }
        self.color_classes_sizes['0'] = 1

        # Inicializar dict de grado de vertices
        self.vertex_degree = {
            v.index: v.degree() for v in self.graph.vs
        }

    def move(
            self,
            pheromones_nodes: List[float],
            pheromones_pairs: List[List[float]],
            alpha: float, beta: float) -> None:
        """
        Realiza un movimiento de la hormiga.
        """

        # Obtener los nodos no coloreados
        uncolored_nodes = [
            v.index for v in self.graph.vs if v['color'] == ''
        ]

        # Si no hay nodos no coloreados, terminar
        if len(uncolored_nodes) == 0:
            return

        # Obtener las opciones de coloreo
        def adjacent_colors(v: int) -> Set[str]:
            return {
                self.graph.vs[neighbour]['color']
                for neighbour in self.graph.neighbors(v)
                if self.graph.vs[neighbour]['color'] != ''
            }

        coloring_options = [
            (v, color)
            for v in uncolored_nodes
            for color in self.all_colors - adjacent_colors(v)
        ]

        # Calcular la probabilidad de moverse a cada nodo
        norm_factor = sum(
            self.prob(v, color, pheromones_nodes,
                      pheromones_pairs, alpha, beta)
            for v, color in coloring_options
        )

        # Seleccionar una acción con base en las probabilidades
        selected_move = random.choices(
            population=coloring_options,
            weights=[
                self.prob(v, color, pheromones_nodes,
                          pheromones_pairs, alpha, beta) / norm_factor
                for v, color in coloring_options
            ],
            k=1
        )[0]

        # Moverse al nodo seleccionado
        previous_node = self.current_node
        self.current_node = selected_move[0]
        selected_color = selected_move[1]

        # Colorear el nodo seleccionado
        self.graph.change_color_and_increase_saturation(
            self.current_node, f'{selected_color}'
        )
        self.color_classes_sizes[selected_color] += 1

        # Guardar el movimiento
        self.movements.append(
            (previous_node, self.current_node, selected_color))

    def prob(self,
             v: int,
             color: str,
             pheromones_nodes: List[float],
             pheromones_pairs: List[List[float]],
             alpha: float, beta: float) -> float:
        """
        Calcula la probabilidad de moverse al nodo `v` y colorearlo con el color `color`.
        """
        pheromone_component = (
            (pheromones_nodes[v][int(color)] +
             pheromones_pairs[self.current_node][v])
        )

        heuristic_component = (
            (
                (
                    # Grado de saturación al cuadrado
                    self.graph.vs[v]['saturation'] ** 2 +

                    # Grado del nodo al cuadrado
                    self.vertex_degree[v] ** 2
                ) ** 0.5
            )
            *
            # Cuadrado del tamaño de la clase de equivalencia del color
            (self.color_classes_sizes[color] + 1) ** 2
        )

        return (
            (pheromone_component ** alpha) *
            (heuristic_component ** beta)
        ) + 1e-6

    def reset(self) -> None:
        """
        Reinicia la hormiga.
        """
        self.current_node = random.randint(0, len(self.graph.vs) - 1)
        self.movements = []

        # Restablecer los colores de los nodos
        for v in self.graph.vs:
            v['color'] = ''
            v['saturation'] = 0

        # Colorear el nodo actual con el color '0'
        self.graph.vs[self.current_node]['color'] = '0'

        # Restablecer el tamaño de las clases de equivalencia de los colores
        self.color_classes_sizes = {
            color: 0 for color in self.all_colors
        }
        self.color_classes_sizes['0'] = 1


def ant_colony(self: ig.Graph) -> None:
    """
    Implementa el algoritmo de colonia de hormigas para colorear grafos.
    """

    N_ANTS = 3
    N_ITERATIONS = 5
    ALPHA = 2.5
    BETA = 1.6
    RHO = 0.1

    # Reset graph
    for v in self.vs:
        v['color'] = ''
        v['saturation'] = 0

    pheromones_nodes = [
        # [node][color]
        [1.0 / (len(self.vs) ** 2) for _ in range(len(self.vs))]
        for _ in range(len(self.vs))
    ]
    pheromones_pairs = [
        # [node1][node2]
        [1.0 / (len(self.vs) ** 2) for _ in range(len(self.vs))]
        for _ in range(len(self.vs))
    ]

    ants_solutions = [
        Ant(self.copy()) for _ in range(N_ANTS)
    ]

    best_solution = None
    best_n_colors = float('inf')

    for iter in range(N_ITERATIONS):
        print(f"Iteration {iter + 1}", "Best number of colors:", best_n_colors)

        # Mover las hormigas hasta que todas hayan coloreado el grafo
        for n in range(len(self.vs) - 1):
            print(f"Moving ants, step {n + 1} / {len(self.vs) - 1}")
            for ant in ants_solutions:
                ant.move(
                    pheromones_nodes, pheromones_pairs, ALPHA, BETA
                )

        # Actualizar las feromonas
        for i in range(len(self.vs)):
            for j in range(len(self.vs)):
                pheromones_nodes[i][j] *= (1 - RHO)
                pheromones_pairs[i][j] *= (1 - RHO)

        for ant in ants_solutions:
            n_colors = ant.graph.number_of_colors()

            for prev_node, next_node, color in ant.movements:
                factor = len(ant.all_colors) / (n_colors)

                pheromones_nodes[next_node][int(color)] += factor
                pheromones_pairs[prev_node][next_node] += factor

        # Obtener la mejor solución
        for ant in ants_solutions:
            if not ant.graph.is_valid_coloring():
                print("WARNING: An ant found an invalid coloring")
                continue

            if ant.graph.number_of_colors() < best_n_colors:
                best_solution = ant.graph.coloring_as_dict()
                best_n_colors = ant.graph.number_of_colors()

        # Reiniciar las hormigas
        for ant in ants_solutions:
            ant.reset()

    # Aplicar la mejor solución
    if best_solution:
        self.apply_coloring_dict(best_solution)
    else:
        print("WARNING: No valid coloring found")
