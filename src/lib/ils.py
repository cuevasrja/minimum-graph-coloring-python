from typing import Set
import igraph as ig
from src.lib.external_functions import first_element_not_in_set
import copy

def clonar_instancia(instancia):
    return copy.deepcopy(instancia)

def obtener_primeros_elementos(tuplas, n):
    """
    Obtiene los primeros elementos de las primeras n tuplas de una lista de tuplas.
    
    :param tuplas: Lista de tuplas.
    :param n: Número de tuplas de las que se quieren obtener los primeros elementos.
    :return: Lista con los primeros elementos de las primeras n tuplas.
    """
    return [t[0] for t in tuplas[:n]]


def ils(self: ig.Graph):
  
    """
    Colorea el grafo utilizando el algoritmo heuristico D-Satur.
    """    
    self.d_satur()
    # new_graph = clonar_instancia(self)
    
    colors_by_use = self.count_and_sort_colors()
    list_of_numbers_to_test = list(range(1, self.number_of_colors_used() // 2 + 1))
    amount_of_color = self.get_amount_of_colors()
        
    iteracion = 10

    for number_of_nodes_to_uncolor in list_of_numbers_to_test:
        colors_by_use = self.count_and_sort_colors()
        for i in range(0, number_of_nodes_to_uncolor):
            self.uncolor(colors_by_use[i])
            
        while True:
            node_with_max_saturation: int = self.vertex_with_max_saturation()

            if (node_with_max_saturation == -1):
                break

            adjacent_colors_of_current_node: Set[str] = self.adjacent_colors(node_with_max_saturation)

            color_to_paint: str|None = first_element_not_in_set(self.colors, adjacent_colors_of_current_node)

            self.change_color_and_increase_saturation(node_with_max_saturation, color_to_paint)
            
        self.local_search()
            
        print("New amount of colors ", self.get_amount_of_colors())