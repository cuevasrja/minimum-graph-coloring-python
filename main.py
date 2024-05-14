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

if __name__ == "__main__":
    main()