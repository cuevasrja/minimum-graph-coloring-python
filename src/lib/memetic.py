from typing import List
import igraph as ig
import random
from typing import Dict, Callable, List
from src.lib.eval_functions import eval_scaled_number_of_conflics, eval_sum_of_squared_color_sizes
from src.lib.genetic import mutate, create_population


def triple_common_crossover(self: ig.Graph, parents: List[Dict[int, str]]) -> Dict[int, str]:
    """
    Cruza a tres padres para obtener un hijo.
    """
    # Seleccionar los padres
    parent1, parent2, parent3 = parents

    # Crear hijo
    child: Dict[int, str] = {}

    # Iterar sobre los vértices
    for vertex in self.vs:
        vertex_index = vertex.index

        # Seleccionar el color que más se repite en los padres
        color1 = parent1[vertex_index]
        color2 = parent2[vertex_index]
        color3 = parent3[vertex_index]

        # Si los colores son iguales, se selecciona ese color
        if color1 == color2 == color3:
            child[vertex_index] = color1
        # Si existe un color común entre dos padres, se selecciona ese color
        elif color1 == color2:
            child[vertex_index] = color1
        elif color1 == color3:
            child[vertex_index] = color1
        elif color2 == color3:
            child[vertex_index] = color2
        else:
            # Si no hay colores comunes, se selecciona un color aleatorio
            child[vertex_index] = random.choice([color1, color2, color3])

    return child


def triple_point_crossover(self: ig.Graph, parents: List[Dict[int, str]]) -> Dict[int, str]:
    """
    Cruza a tres padres para obtener un hijo.

    Se seleccionan tres puntos de corte aleatorios y se asigna un padre a cada segmento.
    """
    # Seleccionar los padres
    parent1, parent2, parent3 = parents

    # Crear hijo
    child: Dict[int, str] = {}

    # Seleccionar dos puntos de corte
    cut_points = random.sample(range(self.vcount()), 2)
    cut_points.sort()
    p1, p2 = cut_points

    # Iterar sobre los vértices
    for vertex in self.vs:
        vertex_index = vertex.index

        color1 = parent1[vertex_index]
        color2 = parent2[vertex_index]
        color3 = parent3[vertex_index]

        if vertex_index < p1:
            child[vertex_index] = color1
        elif vertex_index < p2:
            child[vertex_index] = color2
        else:
            child[vertex_index] = color3

    return child


def get_parent_triplets(population: List[Dict[int, str]],
                        K: int,
                        eval_sol: Callable[[Dict[int, str]], int],
                        mode: str) -> List[List[Dict[int, str]]]:
    """
    Selecciona K tripletes de padres de la población.

    El primer padre de cada tripleta se escoge con probabilidad proporcional a su desempeño.
    El segundo y tercer padre de cada tripleta se escogen aleatoriamente.
    """
    best_sample = random.choices(
        population, k=K, weights=[
            eval_sol(c) if mode == 'MAX' else 1 / eval_sol(c)
            for c in population
        ]
    )

    parent_triplets = []

    for i in range(0, K):
        parent1 = best_sample[i]
        parent2 = random.choice([p for p in population if p != parent1])
        parent3 = random.choice(
            [p for p in population if p != parent1 and p != parent2])

        parent_triplets.append([parent1, parent2, parent3])

    return parent_triplets


def enhance_sol(graph: ig.Graph, sol: Dict[int, str], i: int, K: int):
    """
    Mejora una solución de coloración aplicando D-Satur y búsqueda local limitada.

    Si la solución no es válida, se descolorean los nodos con conflictos y se aplica D-Satur.
    Luego, se aplica búsqueda local estricta para mejorar la solución.

    Para reducir tiempo de ejecución, se limita la cantidad de iteraciones de búsqueda local.
    """
    # print(f"Mejorando solución {i + 1}/{K}...")

    # Inicializar los atributos de los nodos
    for v in graph.vs:
        v['color'] = ''
        v['saturation'] = 0

    # Aplicar la solución
    graph.apply_coloring_dict(sol)

    # Chequear si la solución es válida
    is_valid = graph.is_valid_coloring()

    # Si la solución no es válida
    if not is_valid:
        # Descolorear los nodos que tengan conflict
        for v in graph.vs:
            for neighbor in graph.neighbors(v.index):
                if v['color'] == graph.vs[neighbor]['color']:
                    v['color'] = ''
                    break

        # Refrescar los valores de saturación
        graph.refresh_saturations()

        # Aplicar d-satur para colorear lo que falta
        graph.d_satur()

        if not graph.is_valid_coloring():
            raise Exception("D-Satur no logró colorear el grafo correctamente")

    # En este punto, tenemos una solución válida, aplicamos una busqueda local estricta
    # Con el objetivo de mejorar la solución
    graph.local_search_without_d_satur(strict=True, max_strict_iters=2)

    # Retornar la solución mejorada
    return graph.coloring_as_dict()


def memetic_algorithm(self: ig.Graph,
                      population_size: int = 100,
                      generations: int = 3,
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
        # print(f"Generación {i + 1}/{generations}",
        #       f"Mejor solución: {best_score}")

        # Seleccionar K tripletas de padres
        K = population_size // 6
        parents: List[List[Dict[int, str]]] = get_parent_triplets(
            population, K, eval_sol, mode)

        # Cruzar las tripletas de padres para obtener K hijos
        children: List[Dict[int, str]] = [
            triple_point_crossover(self, p) for p in parents]

        # Mutar a los K hijos
        children = [mutate(self, c, mutation_rate) for c in children]

        # Mejorar a los hijos
        children = [enhance_sol(self, c, i, K) for i, c in enumerate(children)]

        # Agregar a la población a los K hijos
        population.extend(children)

        # Seleccionar K // 2 individuos de la población según que tan malo es su desempeño
        killed = random.choices(population, k=K // 2, weights=[
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
        # population.append(best_solution)

    # Aplicar mejor solución
    self.apply_coloring_dict(best_solution)
