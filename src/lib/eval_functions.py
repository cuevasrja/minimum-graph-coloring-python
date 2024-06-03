from typing import List, Set
import igraph as ig

def eval_sum_of_squared_color_sizes(coloring: dict[int, str]) -> int:
    """
    Evalúa una coloración de un grafo sumando el cuadrado de la 
    cantidad de nodos que tienen cada color.

    Si se maximiza esta función, implica que se minimiza la cantidad de colores.
    """
    # Obtener los colores utilizados en la coloración (a partir de coloring)
    colors: Set[str] = {color for color in coloring.values()}

    # Inicializar la suma de cuadrados de tamaños de colores
    sum_of_squared_color_sizes: int = 0

    # Iterar sobre los colores
    for color in colors:
        # Hallar los nodos que tienen el color actual
        nodes: List[int] = [node for node, c in coloring.items() if c == color]

        # Calcular el cuadrado de la cantidad de nodos
        squared_size: int = len(nodes) ** 2

        # Sumar el cuadrado al total
        sum_of_squared_color_sizes += squared_size

    return sum_of_squared_color_sizes

def eval_sum_of_conflicts(graph: ig.Graph, coloring: dict[int, str]) -> int:
    """
    Evalúa una coloración de un grafo sumando la cantidad de conflictos
    entre nodos adyacentes que tienen el mismo color.
    """
    # Inicializar la cantidad de conflictos
    conflicts: int = 0

    # Iterar sobre los arcos del grafo
    for edge in graph.es:
        # Obtener los nodos que conecta el arco
        node1: int = edge.source
        node2: int = edge.target

        # Verificar si los nodos tienen el mismo color
        if coloring[node1] == coloring[node2]:
            # Si tienen el mismo color, incrementar la cantidad de conflictos
            conflicts += 1

    return conflicts