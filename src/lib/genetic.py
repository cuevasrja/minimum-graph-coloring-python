from typing import List
import igraph as ig
import random
from typing import Dict, Callable, List
from src.lib.eval_functions import eval_sum_of_squared_color_sizes

def genetic_algorithm(self: ig.Graph, population_size: int = 100, generations: int = 100, mutation_rate: float = 0.01):
    # Generar población inicial
    population: List[Dict[int, str]] = create_population(self, population_size)
    
    # Evaluar la población inicial
    eval_sol: Callable[[Dict[int, str]], int] = eval_sum_of_squared_color_sizes
    best_solution: Dict[int, str] = min(population, key=eval_sol)
    best_score: int = eval_sol(best_solution)

    # Evolución de la población
    for _ in range(generations):
        # Seleccionar padres
        parents: List[Dict[int, str]] = get_parents(self, population)
        
        # Cruzar padres
        child: Dict[int, str] = crossover(self, parents)
        
        # Mutar hijo
        child = mutate(self, child, mutation_rate)
        
        # Evaluar hijo
        child_score: int = eval_sol(child)
        
        # Reemplazar peor solución
        worst_solution: Dict[int, str] = max(population, key=eval_sol)
        worst_score: int = eval_sol(worst_solution)
        if child_score < worst_score:
            population.remove(worst_solution)
            population.append(child)
        
        # Actualizar mejor solución
        if child_score < best_score:
            best_solution = child
            best_score = child_score

    # Aplicar mejor solución
    self.apply_coloring_dict(best_solution)

def get_parents(self: ig.Graph, population: List[Dict[int, str]]) -> List[Dict[int, str]]:
    eval_sol: Callable[[Dict[int, str]], int] = eval_sum_of_squared_color_sizes
    return random.choices(population, weights=[1/eval_sol(sol) for sol in population], k=2)

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
            child[i] = random.choice(list(set(child.values()) - set({child[i]})))
    return child

def create_population(self: ig.Graph, population_size: int) -> List[Dict[int, str]]:
    population: List[Dict[int, str]] = []
    for _ in range(population_size):
        self.random_color_graph()
        population.append(self.coloring_as_dict())
    return population