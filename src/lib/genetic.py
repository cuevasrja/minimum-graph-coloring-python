from typing import List
import igraph as ig
import random
from typing import Dict, Callable, List
from src.lib.eval_functions import eval_sum_of_squared_color_sizes, eval_scaled_number_of_conflics


def genetic_algorithm(self: ig.Graph,
                      population_size: int = 100,
                      generations: int = 10,
                      mutation_rate: float = 0.5):
    eval_sol: Callable[[Dict[int, str]],
                       int] = eval_scaled_number_of_conflics(self)
    mode = 'MIN'

    def find_best_solution(population):
        return min(
            population, key=eval_sol) if mode == 'MIN' else max(population, key=eval_sol)

    # Generar población inicial
    population: List[Dict[int, str]] = create_population(self, population_size)

    # Evaluar la población inicial
    best_solution: Dict[int, str] = find_best_solution(population)
    best_score: int = eval_sol(best_solution)

    # Evolución de la población
    for i in range(generations):
        # Seleccionar K  parejas de padres
        K = population_size // 2
        parents: List[List[Dict[int, str]]] = get_parents(
            population, K, eval_sol, mode)

        # Cruzar las parejas de padres para obtener K hijos
        children: List[Dict[int, str]] = [
            crossover(self, p) for p in parents]

        # Mutar a los K hijos
        children = [mutate(self, c, mutation_rate) for c in children]

        # Agregar a la población a los K hijos
        population.extend(children)

        # Seleccionar K + 1 individuos de la población según que tan malo es su desempeño
        killed = random.choices(population, k=K + 1, weights=[
            eval_sol(c) if mode == 'MIN' else 1 / eval_sol(c)
            for c in population
        ])
        population = [p for p in population if p not in killed]

        # Actualizar la mejor solución
        generation_best = find_best_solution(population)
        generation_best_score = eval_sol(generation_best)

        if (mode == 'MIN' and generation_best_score < best_score) or (mode == 'MAX' and generation_best_score > best_score):
            best_solution = generation_best
            best_score = generation_best_score

        # Agregar a la mejor solución a la población (intensificación)
        population.append(best_solution)

    # Aplicar mejor solución
    self.apply_coloring_dict(best_solution)


def get_parents(population: List[Dict[int, str]],
                K: int,
                eval_sol: Callable[[Dict[int, str]], int],
                mode: str) -> List[Dict[int, str]]:
    """
    Obtiene K parejas de padres de la población.

    El primer padre de cada pareja se escoge con probabilidad proporcional a su desempeño.
    El segundo padre de cada pareja se escoge aleatoriamente.

    Se evita que un padre sea seleccionado dos veces en la misma pareja.
    """

    best_sample = random.choices(
        population, k=K, weights=[
            eval_sol(c) if mode == 'MIN' else 1 / eval_sol(c)
            for c in population
        ]
    )

    parents = []

    for i in range(K):
        parent1 = best_sample[i]
        parent2 = random.choice([p for p in population if p != parent1])

        parents.append([parent1, parent2])

    return parents


def crossover(self: ig.Graph, parents: List[Dict[int, str]]) -> Dict[int, str]:
    crossover_point: int = random.randint(0, len(self.vs))
    child: Dict[int, str] = {}

    for i in range(crossover_point):
        child[i] = parents[0][i]

    for i in range(crossover_point, len(self.vs)):
        child[i] = parents[1][i]

    return child


def mutate(self: ig.Graph, child: Dict[int, str], mutation_rate: float) -> Dict[int, str]:
    for i in range(len(self.vs)):
        if random.random() < mutation_rate:
            child[i] = random.choice(
                list(set(child.values()) - set({child[i]})))

    return child


def create_population(self: ig.Graph, population_size: int) -> List[Dict[int, str]]:
    population: List[Dict[int, str]] = []

    # Random color graph 90% of the initial population
    for _ in range(90 * population_size // 100):
        self.random_color_graph()
        population.append(self.coloring_as_dict())
        self.reset_colors()

    # D-Satur rest of the initial population
    for _ in range(population_size - len(population)):
        self.d_satur()
        population.append(self.coloring_as_dict())
        self.reset_colors()

    return population
