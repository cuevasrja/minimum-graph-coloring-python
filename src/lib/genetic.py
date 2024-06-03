from typing import List
import igraph as ig
import random

def genetic_algorithm(self: ig.Graph, population_size: int = 100, generations: int = 100, mutation_rate: float = 0.01):
    # Generar población inicial
    population: List[int] = [random_coloring(self) for _ in range(population_size)]
    
    for _ in range(generations):
        # Evaluar aptitud
        fitness: List[int] = [color_count(coloring) for coloring in population]
        
        # Seleccionar padres
        parents: List[int] = random.choices(population, weights=fitness, k=2)
        
        # Cruzar padres para crear hijo
        child: List[int] = crossover(parents[0], parents[1])
        
        # Mutar hijo
        if random.random() < mutation_rate:
            mutate(child)
        
        # Añadir hijo a la población
        population.append(child)
        
        # Eliminar individuo menos apto
        least_fit_index: int = fitness.index(min(fitness))
        population.pop(least_fit_index)
    
    # Devolver individuo más apto
    best_coloring = min(population, key=color_count)
    for i, color in enumerate(best_coloring):
        self.vs[i]["color"] = color

def random_coloring(graph: ig.Graph) -> List[int]:
    # Asignar a cada nodo un color aleatorio
    return [random.randint(0, len(graph.vs) - 1) for _ in graph.vs]

def color_count(coloring: List[int]) -> int:
    # Contar el número de colores utilizados
    return len(set(coloring))

def crossover(parent1: int, parent2: int) -> List[int]:
    # Crear un nuevo individuo combinando los colores de los padres
    return [parent1[i] if random.random() < 0.5 else parent2[i] for i in range(len(parent1))]

def mutate(coloring: List[int]) -> None:
    # Cambiar el color de un nodo aleatorio
    coloring[random.randint(0, len(coloring) - 1)] = random.randint(0, len(coloring) - 1)
    