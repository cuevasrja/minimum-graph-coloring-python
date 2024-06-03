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


def eval_scaled_number_of_conflics(self: ig.Graph) -> int:
    """
    Recibe un grafo y retorna una función de evaluación que cuenta la 
    cantidad de conflictos en una coloración y lo multiplica por la cantidad de colores.

    Penaliza las coloraciones con muchos conflictos y muchos colores.
    """
    def eval_coloring(coloring: dict[int, str]) -> int:
        """
        Evalúa una coloración de un grafo contando la cantidad de conflictos que tiene.
        """
        # Inicializar el contador de conflictos
        conflicts: int = 0

        # Iterar sobre los lados del grafo
        for edge in self.es:
            # Obtener los nodos extremos del lado
            node1: int = edge.source
            node2: int = edge.target

            # Obtener los colores de los nodos
            color1: str = coloring[node1]
            color2: str = coloring[node2]

            # Si los colores son iguales, hay un conflicto
            if color1 == color2:
                conflicts += 1

        return (1 + conflicts) * len(set(coloring.values()))

    return eval_coloring
