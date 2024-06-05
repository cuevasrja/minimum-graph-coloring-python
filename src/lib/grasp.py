from typing import List, Set
import igraph as ig
import random

def select_random_permutation(g: ig.Graph, colors: List[int], n: int, alpha: float) -> int:
    color_count: int = 0
    # Seleccionar un nodo aleatorio y asignarle un color
    for node in random.sample(range(n), n):
        available_colors: Set[int] = set(range(color_count)) - {colors[neighbor] for neighbor in g.neighbors(node)}
        if not available_colors:
            available_colors = {color_count}
            color_count += 1
        available_colors = list(available_colors)
        cutoff = int(alpha * len(available_colors))
        colors[node] = random.choice(available_colors[:cutoff+1])
    return color_count

def grasp(self: ig.Graph, max_iter: int = 100, alpha: float = 0.5) -> None:
    n: int = len(self.vs)
    colors: List[int] = []
    best_number_of_colors: int = n
    best_colors: List[int] = []
    for _ in range(max_iter):
        # Fase de construcción
        colors = [-1] * n
        color_count: int = select_random_permutation(self, colors, n, alpha)

        # Fase de búsqueda local
        for node in random.sample(range(n), n):
            for color in range(color_count):
                if color != colors[node] and all(colors[neighbor] != color for neighbor in self.neighbors(node)):
                    old_color: int = colors[node]
                    colors[node] = color
                    if old_color not in colors:
                        color_count -= 1
                    break
    if color_count < best_number_of_colors:
        best_number_of_colors = color_count
        best_colors = colors

    for i, color in enumerate(best_colors):
        self.vs[i]["color"] = color