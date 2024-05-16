import sys
import igraph as ig
from src.lib.read_graph import read_graph

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
        print(f"Arista {e.index} entre {e.source} y {e.target}: {e.attributes()}")

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
