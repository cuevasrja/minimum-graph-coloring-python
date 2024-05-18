from typing import List
import igraph as ig
import numpy as np


def kempe_neighbourhood(self: ig.Graph) -> int:
    """
    ## Kempe neighbourhood.
    Kempe neighbourhood of the graph.
    ### Parameters:
    - self: ig.Graph
        Graph to be colored.
    ### Returns:
    - int
        Kempe neighbourhood of the graph.
    """
    colors: List[int] = []
    colors = [v["color"]
              for v in self.vs if v["color"] and v["color"] not in colors]

    if len(colors) == 1:
        return 0

    C: List[List[ig.Vertex]] = [[] for _ in range(len(colors))]

    for v in self.vs:
        C[int(v["color"])].append(v)

    kempe: int = 0
    for c in C:
        kempe += -(len(c) ** 2)

    return kempe


def local_search(self: ig.Graph):
    """
    ## GCP with local search.
    Solve the graph coloring problem using local search.
    ### Parameters:
    - self: ig.Graph
        Graph to be colored.
    """
    # Initialize the saturation of each vertex with D-Satur
    self.d_satur()

    # TODO: Implement local search
