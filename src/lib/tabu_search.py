from typing import List, Set, Dict
import igraph as ig

def get_adjacent_colors(graph: ig.Graph, node_index: int, solution: Dict[int, str]) -> Set[str]:
    """
    Obtiene los colores de los nodos adyacentes a un nodo.
    """
    adjacent_indices: List[int] = graph.neighbors(node_index, mode="ALL")
    colors: Set[str] = {solution[neighbor] for neighbor in adjacent_indices if neighbor in solution}
    return colors

def get_neighbors(graph: ig.Graph, solution: Dict[int, str]) -> List[Dict[int, str]]:
    """
    Obtiene los vecinos de una solución de coloración.
    """
    neighbors: List[Dict[int, str]] = []

    # Iterar sobre todos los nodos
    for node_index in range(len(graph.vs)):
        # Obtener los colores de los nodos adyacentes
        adjacent_colors: Set[str] = get_adjacent_colors(graph, node_index, solution)

        # Iterar sobre todos los colores
        for color in adjacent_colors:
            # Crear un vecino intercambiando el color del nodo actual por un color adyacente
            neighbor: Dict[int, str] = solution.copy()
            neighbor[node_index] = color
            neighbors.append(neighbor)

    return neighbors

def get_fitness(graph: ig.Graph, solution: Dict[int, str]) -> int:
    """
    Calcula el fitness de una solución de coloración.
    """
    fitness: int = 0

    # Iterar sobre todos los nodos
    for node_index in range(len(graph.vs)):
        # Obtener los colores de los nodos adyacentes
        adjacent_colors: Set[str] = get_adjacent_colors(graph, node_index, solution)

        # Incrementar el fitness si el color del nodo actual es igual a un color adyacente
        if solution[node_index] in adjacent_colors:
            fitness += 1

    return fitness


def tabu_search(self: ig.Graph, tabu_size: int = 5, max_iter: int = 5) -> None:
    """
    Realiza una búsqueda tabú para colorear el grafo.
    """
    # Inicializar la lista tabú
    tabu_list: List[Dict[int, str]] = []

    # Inicializar la mejor solución encontrada
    self.d_satur()
    best_solution: Dict[int, str] = self.coloring_as_dict()
    best_fitness: int = get_fitness(self, best_solution)

    # Inicializar la mejor solución local
    best_local_solution: Dict[int, str] = best_solution
    best_local_fitness: int = best_fitness

    # Inicializar el contador de iteraciones
    iter_count: int = 0

    # Realizar la búsqueda tabú
    while iter_count < max_iter:
        # Incrementar el contador de iteraciones
        iter_count += 1

        # Inicializar la mejor solución local de la iteración
        best_local_solution = best_solution
        best_local_fitness = best_fitness

        # Obtener los vecinos de la mejor solución local
        neighbors: List[Dict[int, str]] = get_neighbors(self, best_local_solution)

        # Seleccionar el vecino con mejor fitness
        for neighbor in neighbors:
            # Si el vecino no está en la lista tabú
            if neighbor not in tabu_list:
                # Calcular el fitness del vecino
                neighbor_fitness: int = get_fitness(self, neighbor)

                # Actualizar la mejor solución local
                if neighbor_fitness < best_local_fitness:
                    best_local_solution = neighbor
                    best_local_fitness = neighbor_fitness

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