from typing import List, Dict, Set, Tuple, Callable
import igraph as ig

from src.lib.eval_functions import eval_sum_of_squared_color_sizes


def kempe_neighbourhood(self: ig.Graph) -> List[Dict[int, str]]:
    """
    Retorna la vecindad de Kempe de una coloración.

    Esto lo hace obteniendo todos los posibles intercabios de kempe.
    """
    # Obtener la coloración actual
    coloring: Dict[int, str] = self.coloring_as_dict()

    # Inicializar la vecindad de Kempe
    kempe: List[Dict[int, str]] = []

    # Obtener los colores utilizados en la coloración
    colors: Set[str] = {v['color']
                        for v in self.vs if v['color'] and v['color'] != ''}

    # Construir conjunto de pares no-ordenados de colores
    pairs: List[Tuple[str, str]] = [(c1, c2)
                                    for c1 in colors for c2 in colors if c1 < c2]

    # Iterar sobre los pares de colores
    for c1, c2 in pairs:
        pair_set: Set[str] = {c1, c2}
        # Hallar los ids nodos que tienen los colores c1 y c2
        nodes: List[int] = [v.index for v in self.vs if v['color'] in pair_set]

        # Halla el subgrafo inducido por los nodos
        subgraph: ig.Graph = self.induced_subgraph(
            nodes, implementation="copy_and_delete")

        # Obtener las componentes conexas
        components = subgraph.connected_components()

        # Iterar sobre las componentes conexas
        for component in components:
            # Si la componente tiene un solo nodo, no se puede intercambiar
            if len(component) == 1:
                continue

            # Copiar la coloración actual
            new_coloring: Dict[int, str] = coloring.copy()

            # Por cada nodo en la componente
            for nc in component:
                # Hallar el indice en el grafo original
                node: int = nodes[nc]

                # Hallar el color actual del nodo
                current_color: str = coloring[node]

                # Intercambiar los colores
                new_color: str = c1 if current_color == c2 else c2

                # Actualizar la coloración con el nuevo color
                new_coloring[node] = new_color

            # Agregar la nueva coloración a la vecindad de Kempe
            kempe.append(new_coloring)

    return kempe


def kempe_sorted(self: ig.Graph) -> Tuple[List[Dict[int, str]], Dict[int, str], int | None]:
    """
    Retorna la vecindad de Kempe de una coloración ordenada por evaluación.

    Adicionalmente, retorna el primer vecino de la vecindad ordenada 
    y su evaluación.
    """

    neighbours: List[Dict[int, str]] = self.kempe_neighbourhood()
    evals: List[int] = [eval_sum_of_squared_color_sizes(v) for v in neighbours]

    # Ordenar los vecinos por evaluación de mayor a menor
    neighbours, evals = zip(
        *sorted(zip(neighbours, evals), key=lambda x: -x[1]))

    # Obtener el mejor vecino
    best: Dict[int, str] = neighbours[0] if len(neighbours) > 0 else None
    best_eval: int | None = evals[0] if len(evals) > 0 else None

    return neighbours, best, best_eval


def local_search(self: ig.Graph):
    """
    Coloración local del grafo utilizando busqueda local con la vecindad de Kempe.
    """
    # Al maximizar esta función, se minimiza la cantidad de colores
    eval_sol: Callable[[Dict[int, str]], int] = eval_sum_of_squared_color_sizes

    # Nuestra solución inicial será la salida de D-Satur
    self.d_satur()

    # Obtenemos la vecindad de Kempe ordenada por evaluación
    _, best, best_eval = self.kempe_sorted()

    # Mientras la evaluación de la mejor solución vecina sea mejor que la actual
    while best is not None and best_eval > eval_sol(self.coloring_as_dict()):
        # Aplicamos el mejor vecino
        self.apply_coloring_dict(best)

        # Obtenemos la vecindad de Kempe ordenada por evaluación
        _, best, best_eval = self.kempe_sorted()

def local_search_without_d_satur(self: ig.Graph):
    """
    Coloración local del grafo utilizando busqueda local con la vecindad de Kempe.
    """
    # Al maximizar esta función, se minimiza la cantidad de colores
    eval_sol: Callable[[Dict[int, str]], int] = eval_sum_of_squared_color_sizes

    # Obtenemos la vecindad de Kempe ordenada por evaluación
    _, best, best_eval = self.kempe_sorted()

    # Mientras la evaluación de la mejor solución vecina sea mejor que la actual
    while best is not None and best_eval > eval_sol(self.coloring_as_dict()):
        # Aplicamos el mejor vecino
        self.apply_coloring_dict(best)

        # Obtenemos la vecindad de Kempe ordenada por evaluación
        _, best, best_eval = self.kempe_sorted()
