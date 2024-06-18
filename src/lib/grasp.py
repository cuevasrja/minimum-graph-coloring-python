from typing import List, Set
import igraph as ig
import random


def RCL_select(G: ig.Graph, alpha: float) -> int:
    """
    Construye la lista de candidatos restringida (RCL) y selecciona un nodo aleatorio de ella.

    La funcion de costo asociada es el grado de saturación de los nodos.

    Retorna el índice del nodo seleccionado.
    """
    # Obtener los índices de los nodos no coloreados
    uncolored_nodes = [v.index for v in G.vs if v['color'] == '']

    # Si no hay nodos no coloreados, retornar -1
    if len(uncolored_nodes) == 0:
        return -1

    # Obtener el grado de saturación de los nodos no coloreados
    saturations = [v['saturation'] for v in G.vs if v['color'] == '']

    # Calcular el umbral de la RCL
    max_saturation = max(saturations)
    min_saturation = min(saturations)
    threshold = min_saturation + alpha * (max_saturation - min_saturation)

    # Construir la RCL, modo maximización
    RCL = [uncolored_nodes[i] for i in range(len(uncolored_nodes))
           if saturations[i] >= threshold]

    # Seleccionar un nodo aleatorio de la RCL
    return random.choice(RCL)


def grasp_build(self: ig.Graph, alpha: float = 0.5) -> None:
    """
    Implementa la fase de construcción del algoritmo GRASP para colorear grafos.
    """
    # Inicializar los atributos de los nodos
    for v in self.vs:
        v['color'] = ''
        v['saturation'] = 0

    # Mientras haya nodos sin colorear
    while True:
        # Seleccionar un nodo aleatorio de la RCL
        node_index = RCL_select(self, alpha)

        # Si no hay nodos no coloreados, terminar
        if node_index == -1:
            break

        # Obtener los colores de los nodos adyacentes
        adjacent_colors = self.adjacent_colors(node_index)

        # Seleccionar el color más pequeño que no esté en los nodos adyacentes
        color = min(
            set(range(len(self.vs))) -
            set([int(c) for c in adjacent_colors])
        )

        # Cambiar el color del nodo y aumentar la saturación de los nodos adyacentes
        self.change_color_and_increase_saturation(node_index, f'{color}')


def grasp(self: ig.Graph) -> None:
    """
    Implementa el algoritmo GRASP para colorear grafos.
    """
    N_iter = 30  # Número de iteraciones
    alpha = 0.8  # Parámetro alpha

    # La solucion inicial es una coloración aleatoria
    self.random_color_graph()

    # Inicializar la mejor solución
    best_solution = self.coloring_as_dict()
    best_n_colors = self.number_of_colors()

    # Iterar N_iter veces
    for _ in range(N_iter):
        # Construir una solución
        grasp_build(self, alpha)

        # Mejorar la solución con local search
        self.local_search_without_d_satur(strict=True)

        # Si la solución es mejor que la mejor solución encontrada
        if self.number_of_colors() < best_n_colors:
            # Actualizar la mejor solución
            best_solution = self.coloring_as_dict()
            best_n_colors = self.number_of_colors()

    # Aplicar la mejor solución encontrada
    self.apply_coloring_dict(best_solution)
