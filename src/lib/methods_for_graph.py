from typing import List, Dict, Set
import igraph as ig
from src.lib.external_functions import filter_elements_of_array, delete_random_value_from_list
import random

def random_color_graph(self: ig.Graph) -> None:
    nodes_indexes = list(range(self.vcount()))
    
    while len(nodes_indexes) > 0:
        node_to_color = delete_random_value_from_list(nodes_indexes)
        adjacent_colors_to_current_node = self.adjacent_colors(node_to_color)
        list_of_possible_colors_for_node = filter_elements_of_array(self.colors, adjacent_colors_to_current_node)
        random_color = random.choice(list_of_possible_colors_for_node)
        self.change_color_and_increase_saturation(node_to_color, random_color)

def uncolor(self: ig.Graph, color: str) -> None:
    """
    Cambia el color de todos los nodos con el color especificado a una cadena vacía "",
    y reduce en 1 el valor de saturación de cada nodo conectado por una arista a uno de esos nodos.
    
    :param g: El grafo en el que se cambiarán los colores.
    :param color: El color que se va a cambiar a "" (como string).
    """
    vertices_to_uncolor = [v.index for v in self.vs if v["color"] == color]

    for v_index in vertices_to_uncolor:
        self.vs[v_index]["color"] = ""
        neighbors = self.neighbors(v_index)
        for neighbor_index in neighbors:
            if self.vs[neighbor_index]["saturation"] > 0:
                self.vs[neighbor_index]["saturation"] -= 1

def number_of_colors_used(self: ig.Graph) -> int:
    """
    Retorna el número de colores utilizados en el grafo.
    """
    unique_colors = set(v["color"] for v in self.vs)
    return len(unique_colors)

def count_and_sort_colors(g: ig.Graph) -> list:
    """
    Cuenta la cantidad de colores usados en el grafo y retorna una lista de colores
    ordenada de menos común a más común.
    """
    color_count = {}
    for v in g.vs:
        color = v["color"]
        if color not in color_count:
            color_count[color] = 0
        color_count[color] += 1

    sorted_colors = sorted(color_count.items(), key=lambda item: item[1])

    return sorted_colors

def apply_coloring_dict(self: ig.Graph, coloring: dict) -> None:
    """
    Aplica una coloración al grafo a partir de un diccionario.
    """
    for v in self.vs:
        v['color'] = coloring.get(v.index, '')


def coloring_as_dict(self: ig.Graph) -> Dict[int, str]:
    """
    Retorna la coloración del grafo como un diccionario.
    """
    return {v.index: v['color'] for v in self.vs if v['color']}


def number_of_colors(self: ig.Graph) -> int:
    """
    Retorna el número de colores utilizados en la coloración del grafo.
    """

    # Crear un conjunto con los colores de los nodos
    colors: List[str] = {v['color'] for v in self.vs if v['color']}

    # Retornar la cantidad de colores
    return len(colors)


def is_valid_coloring(self: ig.Graph) -> bool:
    """
    Verifica si la coloración del grafo es válida.
    """

    # Verificar si hay algún nodo sin color asignado
    if not self.is_colored():
        return False

    # Verificar si hay algún par de nodos adyacentes con el mismo color
    for e in self.es:
        source_color: str = self.vs[e.source]['color']
        target_color: str = self.vs[e.target]['color']
        if source_color == target_color:
            return False

    return True


def reset_colors(self: ig.Graph) -> None:
    """
    Resetea los colores de todos los nodos del grafo.
    """

    for v in self.vs:
        v['color'] = ''


def is_colored(self: ig.Graph) -> bool:
    """
    Verifica si todos los nodos del grafo tienen un color asignado.
    """

    # Verificar si hay algún nodo sin color asignado
    return all(v['color'] != '' for v in self.vs)


def is_safe_to_color(self: ig.Graph, node_index, color) -> bool:
    """
    Verifica si es seguro colorear el nodo con el color especificado.
    """

    # Obtener los índices de los nodos adyacentes
    adjacent_indices = self.neighbors(node_index, mode="ALL")

    # Verificar si alguno de los nodos adyacentes tiene el mismo color
    for neighbor in adjacent_indices:
        if self.vs[neighbor]['color'] == color:
            return False

    return True


def vertex_with_max_saturation(self: ig.Graph) -> int:
    """
    Retorna el índice del vértice con la saturación máxima entre los vértices 
    que tienen el atributo 'color' como una cadena vacía.
    """

    # Filtrar los vértices que tienen el atributo 'color' como una cadena vacía
    filtered_vertices: List[ig.Vertex] = [
        v for v in self.vs if v['color'] == '']
    if not filtered_vertices:
        return -1  # Retorna None si no hay vértices con color como cadena vacía
    # Encontrar el vértice con la saturación máxima entre los filtrados
    max_saturation_vertex: ig.Vertex = max(
        filtered_vertices, key=lambda v: v['saturation'])
    # Obtener el índice del nodo con máxima saturación en la lista original
    return max_saturation_vertex["index"]


def adjacent_colors(self: ig.Graph, node_index: int) -> Set[str]:
    """
    Retorna los colores de los nodos adyacentes al nodo especificado.
    """

    adjacent_indices: List[int] = self.neighbors(node_index, mode="ALL")
    colors: Set[str] = {self.vs[neighbor]['color']
                        for neighbor in adjacent_indices if self.vs[neighbor]['color']}
    return colors


def change_color_and_increase_saturation(self: ig.Graph, node_index: int, new_color: str) -> None:
    """
    Cambia el color del nodo especificado y aumenta en 1 la saturación de los nodos adyacentes.
    """

    # Cambiar el color del nodo especificado
    self.vs[node_index]['color'] = new_color

    # Obtener los nodos adyacentes
    adjacent_indices: List[int] = self.neighbors(node_index, mode="ALL")

    # Aumentar en 1 la saturación de los nodos adyacentes
    for neighbor in adjacent_indices:
        self.vs[neighbor]['saturation'] += 1


def group_nodes_by_color(self: ig.Graph) -> None:
    """
    Agrupa los nodos del grafo por color, muestra los nodos en cada grupo
    e imprime el número total de colores utilizados.
    """

    # Crear un diccionario para almacenar los nodos agrupados por color
    nodes_by_color: Dict[str, List[int]] = {}

    # Iterar sobre todos los nodos
    for v in self.vs:
        color: str = v['color']
        if color in nodes_by_color:
            nodes_by_color[color].append(v.index)
        else:
            nodes_by_color[color] = [v.index]

    # Imprimir los nodos agrupados por color
    # for color, nodes in nodes_by_color.items():
    #     print(f"\033[94mColor {color}\033[0m: {', '.join(map(str, nodes))}")

    # Imprimir el número total de colores
    total_colors: int = len(nodes_by_color)
    print(f"Número total de colores: \033[94;1m{total_colors}\033[0m")

def get_amount_of_colors(self: ig.Graph) -> int:
    """
    Agrupa los nodos del grafo por color y muestra el numero de colores utilizados
    """
    # Crear un diccionario para almacenar los nodos agrupados por color
    nodes_by_color: Dict[str, List[int]] = {}

    # Iterar sobre todos los nodos
    for v in self.vs:
        color: str = v['color']
        if color in nodes_by_color:
            nodes_by_color[color].append(v.index)
        else:
            nodes_by_color[color] = [v.index]

    total_colors: int = len(nodes_by_color)
    return total_colors