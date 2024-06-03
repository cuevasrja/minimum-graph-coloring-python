from typing import List, Dict, Set, Tuple, Callable
import igraph as ig
import random
import math

from src.lib.eval_functions import eval_sum_of_squared_color_sizes


def movement_probability(from_coloring: Dict[int, str],
                         to_coloring: Dict[int, str],
                         temperature: float, mode='MIN') -> float:
    """
    Calcula la probabilidad de aceptar un movimiento en el algoritmo de simulated annealing.

    Args:
    - from_coloring (`Dict[int, str]`): La coloración actual.
    - to_coloring (`Dict[int, str]`): La coloración siguiente.
    - temperature (`float`): La temperatura actual.
    - mode (`str`): El modo de optimización ('MAX' o 'MIN').
    """
    # Evaluar las funciones objetivo de los estados actual y siguiente
    current_eval: int = eval_sum_of_squared_color_sizes(from_coloring)
    next_eval: int = eval_sum_of_squared_color_sizes(to_coloring)

    # Calcular la diferencia de evaluaciones
    delta_eval: int = next_eval - current_eval
    if mode != 'MAX':
        delta_eval = -delta_eval

    # Calcular la probabilidad de aceptar el movimiento
    return 1.0 if delta_eval <= 0 else math.exp(-delta_eval / temperature)


def simulated_annealing(self: ig.Graph):
    """
    Realiza la optimización de la coloración del grafo utilizando el algoritmo de 
    simulated annealing con vecindad de Kempe.
    """
    eval_sol: Callable[[Dict[int, str]], int] = eval_sum_of_squared_color_sizes

    temperature: float = 8.0
    cooling_rate: float = 0.1  # efectivamente sera (1 - cooling_rate) = 0.9
    freezing_temperature: float = 0.02  # Cerca de 50 iteraciones

    freezing_counter: int = 0

    # La solución inicial es D-Satur
    self.d_satur()

    # Constantes del algoritmo
    FREEZE_LIM = 3
    TRIALS_LIM = 100  # Numero de exploraciones por valor de temperatura

    # Mejor solución encontrada
    best_coloring: Dict[int, str] = self.coloring_as_dict()
    best_eval: int = eval_sol(best_coloring)

    current_coloring: Dict[int, str] = best_coloring

    # Criterio de congelamiento
    while freezing_counter < FREEZE_LIM:
        trials = 0
        best_changed = False

        # Criterio de parada
        while trials < TRIALS_LIM:
            # Obtenemos la vecindad de Kempe
            neighbours = self.kempe_neighbourhood()

            # Random shuffle a la vecindad
            random.shuffle(neighbours)

            for neighbour in neighbours:
                # Calcular la probabilidad de aceptar el movimiento
                prob = movement_probability(
                    current_coloring, neighbour, temperature, 'MAX')

                # Si el movimiento es aceptado
                if random.random() < prob:
                    current_coloring = neighbour
                    self.apply_coloring_dict(current_coloring)

                    # Actualizar la mejor solución
                    if eval_sol(current_coloring) < best_eval:
                        best_coloring = current_coloring
                        best_eval = eval_sol(best_coloring)
                        best_changed = True

                trials += 1
                if trials >= TRIALS_LIM:
                    break

        # Actualizar la temperatura
        temperature *= 1 - cooling_rate

        # Actualizar el contador de congelamiento
        if temperature < freezing_temperature and not best_changed:
            freezing_counter += 1

    # Aplicar la mejor solución encontrada
    self.apply_coloring_dict(best_coloring)
