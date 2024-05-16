import sys
import igraph as ig
from src.lib.read_graph import read_graph
from src.lib.methods_for_graph import vertex_with_max_saturation, adjacent_colors, change_color_and_increase_saturation, group_nodes_by_color
from src.lib.d_satur import d_satur


ig.Graph.vertex_with_max_saturation = vertex_with_max_saturation
ig.Graph.adjacent_colors = adjacent_colors
ig.Graph.change_color_and_increase_saturation = change_color_and_increase_saturation
ig.Graph.d_satur = d_satur
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

    g.d_satur()

    for v in g.vs:
        print(v)

    for e in g.es:
        print(f"Arista {e.index} entre {e.source} y {
              e.target}: {e.attributes()}")

    g.group_nodes_by_color()


if __name__ == "__main__":
    main()
