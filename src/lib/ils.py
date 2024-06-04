from typing import Set, List
import igraph as ig
import math
import random


def calculate_perturbation_amounts(n_colors: int) -> List[int]:
    """
    Calcula la cantidad de colores a eliminar en cada perturbación para la implementación de ILS.
    """
    values = []

    for percent in range(5, 65, 5):
        values.append(math.ceil(n_colors * percent / 100))

    min_value = min(values)

    return [n for n in range(1, 4) if n < min_value] + values


def get_random_values(array, n):
    # Verificar que n no sea mas grande que el tamaño del array
    n = min(n, len(array))

    # Obtener n valores random del array
    random_values = random.sample(array, n)
    return random_values


def ils(self: ig.Graph):
    # Primera iteración de la busqueda local
    self.d_satur()
    self.local_search()

    amount_of_colors = self.number_of_colors()
    current_colors_in_graph = self.colors_used()
    best_solution = self.coloring_as_dict()
    best_number_of_colors = amount_of_colors

    # Calcular la cantidad de colores a eliminar en cada perturbación
    perturbation_amounts = calculate_perturbation_amounts(amount_of_colors)

    NON_IMPROVEMENT_LIMIT = 6
    non_improvement_count = 0
    random.seed(42)

    # Por cada ronda de perturbación
    for expected_to_clear in perturbation_amounts:
        # Obtener los colores que se deben eliminar
        colors_to_clear = get_random_values(
            current_colors_in_graph, expected_to_clear)

        # Perturbar la solución eliminando colores
        for color in colors_to_clear:
            self.uncolor(color)

        # Rellenar los colores eliminados con D-Satur
        self.d_satur()

        # Mejorar la solución con búsqueda local
        self.local_search()

        amount_of_colors = self.number_of_colors()
        current_colors_in_graph = self.colors_used()

        # Actualizar la mejor solución
        if amount_of_colors < best_number_of_colors:
            best_solution = self.coloring_as_dict()
            best_number_of_colors = amount_of_colors
            non_improvement_count = 0
        else:
            non_improvement_count += 1

        if non_improvement_count >= NON_IMPROVEMENT_LIMIT:
            break

    self.apply_coloring_dict(best_solution)
