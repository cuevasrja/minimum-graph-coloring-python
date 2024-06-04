from typing import Set, List
import igraph as ig
import math
import random


def calculate_rounded_percentages(number: int) -> List[int]:
    """
    Calcula los porcentajes de un número en incrementos de 0.05 desde 0.05 hasta 0.50 y redondea hacia arriba.
    """
    percentages = []

    # Iterar sobre los valores de porcentaje en incrementos de 0.05 desde 0.05 hasta 0.65
    for percent in range(5, 65, 5):
        # Calcular el porcentaje correspondiente y redondear hacia arriba
        percentage_value = math.ceil(number * percent / 100)
        percentages.append(percentage_value)

    return percentages


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
    iterations_percentage = calculate_rounded_percentages(amount_of_colors)
    best_solution = self.coloring_as_dict()
    best_number_of_colors = amount_of_colors

    NON_IMPROVEMENT_LIMIT = 5
    non_improvement_count = 0

    # Por cada ronda de perturbación
    for clear_pct in iterations_percentage:
        # Calcular cuantos colores se deben eliminar
        expeted_to_clear = int(clear_pct * amount_of_colors / 100)
        colors_to_clear = get_random_values(
            current_colors_in_graph, expeted_to_clear)

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
