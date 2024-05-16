import igraph as ig


def backtracking(self: ig.Graph):
    """
    Colorea el grafo utilizando el metodo de backtracking (fuerza bruta).
    """

    for m in range(1, len(self.vs) + 1):
        self.reset_colors()

        if backtrack(self, 0, m):
            return m

    return -1


def backtrack(self: ig.Graph, node_index, m):
    """
    Retorna true si es posible colorear el grafo con m colores, de lo contrario retorna false.
    """

    if self.is_colored():
        return True

    for c in range(m):
        color = f'{c}'

        if self.is_safe_to_color(node_index, color):
            self.vs[node_index]['color'] = color

            if backtrack(self, node_index + 1, m):
                return True

            self.vs[node_index]['color'] = ''

    return False
