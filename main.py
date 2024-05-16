import sys
import igraph as ig
from src.lib.read_graph import read_graph
from src.lib.methods_for_graph import vertex_with_max_saturation, adjacent_colors, change_color_and_increase_saturation, group_nodes_by_color, is_colored, is_safe_to_color, reset_colors, is_valid_coloring, number_of_colors
from src.lib.d_satur import d_satur
from src.lib.backtracking import backtracking


ig.Graph.number_of_colors = number_of_colors
ig.Graph.is_valid_coloring = is_valid_coloring
ig.Graph.reset_colors = reset_colors
ig.Graph.is_colored = is_colored
ig.Graph.is_safe_to_color = is_safe_to_color
ig.Graph.vertex_with_max_saturation = vertex_with_max_saturation
ig.Graph.adjacent_colors = adjacent_colors
ig.Graph.change_color_and_increase_saturation = change_color_and_increase_saturation
ig.Graph.d_satur = d_satur
ig.Graph.backtracking = backtracking
ig.Graph.group_nodes_by_color = group_nodes_by_color


def main():
    # Leemos los argumentos de la línea de comandos
    file_path: str = sys.argv[1]
    g: ig.Graph = read_graph(file_path)
    # print(g)
    # Muestro la cantidad de lados
    print("Cantidad de lados: ", len(g.es))
    # Muestro la cantidad de nodos
    print("Cantidad de nodos: ", len(g.vs))

    for v in g.vs:
        print(v)

    for e in g.es:
        print(f"Arista {e.index} entre {e.source} y {
              e.target}: {e.attributes()}")

    # Invocando D-Satur
    print("\nInvocando D-Satur")

    g.reset_colors()
    g.d_satur()

    g.group_nodes_by_color()
    print(f"Coloración válida: {g.is_valid_coloring()}")

    # Invocando Backtracking
    # print("\nInvocando Backtracking")

    # g.reset_colors()
    # m = g.backtracking()
    # if m == -1:
    #     print("Error: Backtracking no pudo colorear el grafo")
    #     exit()

    # g.group_nodes_by_color()
    # print(f"Coloración válida: {g.is_valid_coloring()}")


if __name__ == "__main__":
    main()
