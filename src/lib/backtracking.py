from typing import List
import igraph as ig

best_number_of_colors: int = 0
best_colors: List[str] = []


def backtracking(self: ig.Graph) -> int:
    """
    Colorea el grafo utilizando el metodo de backtracking (fuerza bruta).
    """

    global best_number_of_colors, best_colors

    self.reset_colors()

    best_number_of_colors = len(self.vs)
    backtrack(self, 0)

    if len(best_colors) > 0:
        for i, v in enumerate(self.vs):
            v['color'] = best_colors[i]

        return len(best_colors)

    return -1


def backtrack(self: ig.Graph, node_index, color_counts: dict = {}):
    """
    Explora sistemáticamente todas las posibles coloraciones válidas del grafo.
    """
    global best_number_of_colors, best_colors

    if self.is_colored():
        if self.is_valid_coloring() and self.number_of_colors() < best_number_of_colors:
            best_number_of_colors = len(color_counts)
            best_colors = [v['color'] for v in self.vs]

        return

    for c in range(len(self.vs)):
        color: str = f'{c}'

        # Si ya se encontró una coloración con menos colores, se puede podar
        if c > best_number_of_colors - 1:
            return

        # Si la coloración no es válida, se puede podar
        if self.is_safe_to_color(node_index, color):
            # Asignar el color al nodo
            self.vs[node_index]['color'] = color

            # Incrementar el contador de colores
            if color in color_counts:
                color_counts[color] += 1
            else:
                color_counts[color] = 1

            # Si aun es posible encontrar una coloración con menos colores, continuar con la búsqueda
            if len(color_counts) < best_number_of_colors:
                backtrack(self, node_index + 1, color_counts)

            # Decrementar el contador de colores
            if color_counts[color] == 1:
                del color_counts[color]
            else:
                color_counts[color] -= 1

            # Backtrack
            self.vs[node_index]['color'] = ''
