import sys
import igraph as ig
from src.lib.read_graph import read_graph


def main():
    # Leemos los argumentos de la línea de comandos
    file_path: str = sys.argv[1]
    g: ig.Graph = read_graph(file_path)
    # print(g)
    # Muestro la cantidad de lados
    print("\033[103;1mCantidad de lados:\033[0m \033[93m", len(g.es), "\033[0m")
    # Muestro la cantidad de nodos
    print("\033[103;1mCantidad de nodos:\033[0m \033[93m", len(g.vs), "\033[0m")

    # Invocando D-Satur
    print("\n\033[100;1mInvocando D-Satur...\033[0m")

    g.reset_colors()
    g.d_satur()

    g.group_nodes_by_color()
    is_valid: str = "\033[92;1mTrue" if g.is_valid_coloring() else "\033[91mFalse"
    print(f"Coloración válida: {is_valid}\033[0m")

    # Invocando Backtracking
    print("\n\033[100;1mInvocando Backtracking...\033[0m")

    g.reset_colors()
    m = g.backtracking()
    if m == -1:
        print("\033[91;1mError:\033[0m Backtracking no pudo colorear el grafo")
        exit()

    g.group_nodes_by_color()
    is_valid: str = "\033[92;1mTrue" if g.is_valid_coloring() else "\033[91mFalse"
    print(f"Coloración válida: {is_valid}\033[0m")

    # Invocando Local Search
    print("\n\033[100;1mInvocando Local Search...\033[0m")

    g.reset_colors()
    g.local_search()

    g.group_nodes_by_color()
    is_valid: str = "\033[92;1mTrue" if g.is_valid_coloring() else "\033[91mFalse"
    print(f"Coloración válida: {is_valid}\033[0m")


if __name__ == "__main__":
    main()
