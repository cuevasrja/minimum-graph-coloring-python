from typing import List
import igraph as ig
import numpy as np

def random_permutation(self: ig.Graph) -> List[ig.Vertex]:
    """
    ## Random permutation.
    Random permutation of the nodes of the graph.
    ### Parameters:
    - self: ig.Graph
        Graph to be colored.
    ### Returns:
    - List[]
        Permutation of the nodes of the graph.
    """
    V: List[ig.Vertex] = self.vs
    # Shuffle the nodes
    return [V[i] for i in np.random.permutation(len(V))]

def greedy(self: ig.Graph, p: List[int]):
    """
    ## Greedy algorithm.
    Greedy algorithm for graph coloring.
    ### Parameters:
    - self: ig.Graph
        Graph to be colored.
    - p: List[int]
        Permutation of the nodes of the graph.
    """
    n = len(self.vs)
    C: List[List[ig.Vertex]] = [[] for _ in range(n)]
    C[0].append(p[0])
    for i in range(1, n):
        v: ig.Vertex = p[i]
        h: int = min([j for j in range(n) if all([v not in C[j], all([v not in self.neighbors(u) for u in C[j]])])])
        C[h].append(v)
    j: int = 0
    while C[j]:
        for v in C[j]:
            v["color"] = j
        j += 1
    C = C[:j]

def reduce_colors(self: ig.Graph):
    """
    ## Reduce the number of colors used in the graph.
    Reduce the number of k colors used in the graph to k - 1 colors.
    ### Parameters:
    - self: ig.Graph
        Graph to be colored.
    """
    # Get the colors used in the graph
    colors: List[int] = []
    colors = [v["color"] for v in self.vs if v["color"] and v["color"] not in colors]
    if len(colors) == 1:
        return
    # Erase a random color
    color = np.random.choice(colors)
    for v in self.vs:
        if v["color"] == color:
            v["color"] = np.random.choice([c for c in range(len(colors)) if c != color])

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
    colors = [v["color"] for v in self.vs if v["color"] and v["color"] not in colors]
    if len(colors) == 1:
        return 0
    C: List[List[ig.Vertex]] = [[] for _ in range(len(colors))]
    for v in self.vs:
        C[v["color"]].append(v)
    kempe: int = 0
    for c in C:
        kempe += -(len(c)**2)
    return kempe

def local_search(self: ig.Graph):
    """
    ## Local search.
    Local search algorithm for graph coloring.
    ### Parameters:
    - self: ig.Graph
        Graph to be colored.
    """
    pass

def GCP_local_search(self: ig.Graph):
    """
    ## GCP with local search.
    Solve the graph coloring problem using local search.
    ### Parameters:
    - self: ig.Graph
        Graph to be colored.
    """
    rand_p: List[int] = self.random_permutation()
    self.greedy(rand_p)

    while self.is_valid_coloring():
        self.reduce_colors()
        if not self.is_valid_coloring():
            self.local_search()

