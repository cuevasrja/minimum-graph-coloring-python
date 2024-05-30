import random
from typing import List, Dict, Set, Callable
import igraph as ig
from src.lib.local_search import eval_sum_of_squared_color_sizes

def max_degree(G: ig.Graph, V: Set[int], k) -> List[int]:
    """
    Retorna los k nodos con mayor grado en el grafo.
    """

    V_list: List[ig.Vertex] = list(v for v in G.vs if v['index'] in V)
    V_list.sort(key=lambda x: x.degree(), reverse=True)
    return [v['index'] for v in V_list[:k]]

def grasp(self: ig.Graph, max_iter: int = 2, c_iter: int = 5, c_size: int = 7) -> None:
    """
    Colorea el grafo utilizando el algoritmo GRASP.
    """
    # Diccionario de colores
    colors: List[Set[int]] = []

    for iter in range(max_iter):
        print(f"Iteración {iter + 1}")
        i: int = 0
        V: Set[int] = set(v['index'] for v in self.vs)
        while len(V) > 0:
            ecount: float = float('inf')
            for j in range(c_iter):
                print(f"Iteración {iter + 1}.{j + 1}")
                V_aux: Set[int] = V.copy()
                C: Set[int] = set()
                U: Set[int] = set()
                while len(V_aux) > 0:
                    print(f"Iteración {iter + 1}.{j + 1} - {len(V_aux)} nodos restantes")
                    print('V_aux', V_aux)
                    if len(U) == 0:
                        CL: List[int] = max_degree(self, V_aux, c_size)
                    else:
                        CL: List[int] = max_degree(self, U, c_size)
                    print("CL", CL)
                    # Seleccionar un nodo aleatorio de CL
                    v: ig.Vertex = CL[random.randint(0, len(CL) - 1)]
                    C = C.union(set([v]))
                    print('v', v)
                    neighbors: Set[int] = set(x['index'] for x in self.vs[v].neighbors())
                    print('neighbors', neighbors)
                    U = U.union(neighbors)
                    V_aux = V_aux.difference(neighbors.difference(set([v])))
                # Buscar los lados de V - C
                V_C: Set[int] = V.difference(C)
                print("V_C", V_C)
                print(self.es[0])
                E: Set[ig.Edge] = set(self.es.select(_source_in=V_C, _target_in=V_C))
                print(f"Iteración {iter + 1}.{j + 1} - {len(E)} lados")
                if len(E) < ecount:
                    ecount = len(E)
                    colors.append(C.copy())
                    print("colors", colors[i])
                    print(len(colors[i]))
            V = V.difference(colors[i])
            i += 1
    for i in range(len(colors)):
        for v in colors[i]:
            self.vs[v]['color'] = i
    
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
    