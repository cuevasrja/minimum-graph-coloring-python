from typing import Set
import igraph as ig
from src.lib.external_functions import first_element_not_in_set


def d_satur(self: ig.Graph):
    """
    Colorea el grafo utilizando el algoritmo heuristico D-Satur.
    """

    while True:
        node_with_max_saturation: int = self.vertex_with_max_saturation()

        if (node_with_max_saturation == -1):
            break

        adjacent_colors_of_current_node: Set[str] = self.adjacent_colors(
            node_with_max_saturation)

        color_to_paint: str|None = first_element_not_in_set(
            self.colors, adjacent_colors_of_current_node)

        self.change_color_and_increase_saturation(
            node_with_max_saturation, color_to_paint)
