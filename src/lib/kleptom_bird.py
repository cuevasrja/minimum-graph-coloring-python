from typing import List
import igraph as ig
import random
import math
from typing import Dict, Callable, List, Tuple
from src.lib.eval_functions import eval_scaled_number_of_conflics
from src.lib.genetic import mutate
from collections import Counter


import igraph as ig
import random


def create_population_with_initial_colors(self: ig.Graph, population_size: int, min_initial_colors_amount: float, max_initial_colors_amount: float) -> List[Dict[int, str]]:
    population: List[Dict[int, str]] = []
    
    def random_initial_color_amount():
        random_value = random.uniform(min_initial_colors_amount, max_initial_colors_amount)
        number_of_nodes = self.vcount()
        initial_colors_amount = math.ceil(random_value * number_of_nodes)
        return initial_colors_amount

    # Random color graph 90% of the initial population
    for _ in range(90 * population_size // 100):
        initial_colors_to_use = random_initial_color_amount()
        self.color_graph_with_multiple_colors_random_order(initial_colors_to_use)
        self.random_color_graph()
        population.append(self.coloring_as_dict())
        self.reset_colors()

    # D-Satur rest of the initial population
    for _ in range(population_size - len(population)):
        initial_colors_to_use = random_initial_color_amount()
        self.color_graph_with_multiple_colors_random_order(initial_colors_to_use)        
        self.d_satur()
        population.append(self.coloring_as_dict())
        self.reset_colors()

    return population


def most_common_color(parents: List[Dict[int, str]]) -> Tuple[str, int]:
    """
    Devuelve el color más común entre los tres padres y el índice del padre que lo tiene más veces.
    """
    color_parent_count = []

    for i, parent in enumerate(parents):
        color_counts = Counter(parent.values())
        most_common_color, count = color_counts.most_common(1)[0]
        color_parent_count.append((most_common_color, count, i))

    most_common_color, _, most_common_parent_index = max(color_parent_count, key=lambda x: x[1])

    return most_common_color, most_common_parent_index

def triple_partition_crossover(self: ig.Graph, parents: List[Dict[int, str]]) -> Dict[int, str]:
    """
    Cruza a tres padres utilizando el metodo de cruze voraz de particiones.

    Adicionalmente, mantiene un blacklist que asegura que no se use un padre m veces seguidas.
    
    Se usa una funcion para verificar cual es el padre que posea la clase color mas alta y esta siempre se hereda en el hijo

    Esto representa una implementación sencilla de AMPaX para n = 3.
    """
    M = 2

    blacklist = {
        1: 0,  # Padre 1
        2: 0,  # Padre 2
        3: 0  # Padre 3
    }
    parent_1, parent_2, parent_3 = parents

    parent_1_graph = self.copy()
    parent_1_graph.apply_coloring_dict(parent_1)
    parent_2_graph = self.copy()
    parent_2_graph.apply_coloring_dict(parent_2)
    parent_3_graph = self.copy()
    parent_3_graph.apply_coloring_dict(parent_3)

    result_graph = self.copy()
    for v in result_graph.vs:
        v['color'] = ''

    # Calcular el color más común entre los tres padres
    common_color, common_parent_index = most_common_color(parents)

    # Asignar el color más común a todos los vértices del hijo que están en el padre con el color más común
    common_parent = parents[common_parent_index]
    for vertex, color in common_parent.items():
        if color == common_color:
            result_graph.vs[vertex]['color'] = common_color

    def compute_color_classes(graph: ig.Graph, parent_index: int) -> Dict[str, List[int]]:
        color_classes = {}

        for v in graph.vs:
            color = v['color']
            if color not in color_classes:
                color_classes[color] = []
            color_classes[color].append(v.index)

        return [(parent_index, color, nodes) for color, nodes in color_classes.items()]

    # Calcular el arreglo de clase de colores para cada padre
    parent_1_color_classes = compute_color_classes(parent_1_graph, 1)
    parent_2_color_classes = compute_color_classes(parent_2_graph, 2)
    parent_3_color_classes = compute_color_classes(parent_3_graph, 3)

    all_color_classes = (parent_1_color_classes +
                         parent_2_color_classes + parent_3_color_classes)

    while True:
        # Decrementar la cantidad de veces que se ha seleccionado un padre
        for p in blacklist:
            blacklist[p] = max(0, blacklist[p] - 1)

        # Obtener la clase de color con más nodos
        options = [
            (p, c, vs)
            for p, c, vs in all_color_classes
            if blacklist[p] < M and c != common_color
        ]
        if len(options) == 0:  # Si no hay opciones,
            # Si no hay elementos porque estan en el blacklist, se resetea el blacklist
            if any(blacklist[p] != 0 for p in blacklist):
                for p in blacklist:
                    blacklist[p] = 0
                # Y se intenta de nuevo
                continue

            # Si no hay elementos porque ya se han seleccionado todos los colores, se termina
            break

        selected_class = max(
            [
                (p, c, vs)
                for p, c, vs in all_color_classes
                if blacklist[p] < M and c != common_color
            ],
            key=lambda x: len(x[2])
        )
        selected_parent, selected_color, selected_nodes = selected_class

        # Eliminar la clases del mismo color que el seleccionado
        # Eliminar los nodos que ya han sido seleccionados
        all_color_classes = [
            (p, c, [v for v in vs if v not in selected_nodes])
            for p, c, vs in all_color_classes
            if c != selected_color
        ]
        all_color_classes = [
            (p, c, vs)
            for p, c, vs in all_color_classes
            if len(vs) > 0
        ]

        # Incrementar la cantidad de veces que se ha seleccionado el padre
        blacklist[selected_parent] += M

        # Asignar el color a los nodos
        for v in selected_nodes:
            result_graph.vs[v]['color'] = selected_color

    # En este punto, tenemos un grafo parcialmente coloreado
    # El resto de nodos se colorean con D-Satur
    result_graph.refresh_saturations()
    result_graph.d_satur()

    return result_graph.coloring_as_dict()

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

def enhance_sol(graph: ig.Graph, sol: Dict[int, str], i: int, K: int, last_gen: bool):
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
    # Esto solo se aplica si en el caso del algoritmo memetico, en busqueda dispersa no se aplica
    if last_gen:
        graph.local_search_without_d_satur(strict=True, max_strict_iters=3)

    # Retornar la solución mejorada
    return graph.coloring_as_dict()


def kleptom_bird(self: ig.Graph,
                      nests_amount: int = 100,
                      generations: int = 3,
                      mutation_rate: float = 0.5,
                      min_initial_colors_amount: float = 0.01,
                      max_initial_colors_amount: float = 0.05):
    eval_sol: Callable[[Dict[int, str]],
                       int] = eval_scaled_number_of_conflics(self)
    mode = 'MIN'

    def find_best_solution(nest_population):
        return min(
            nest_population, key=eval_sol) if mode == 'MIN' else max(nest_population, key=eval_sol)

    # Generar población inicial de nidos
    nest_population: List[Dict[int, str]] = create_population_with_initial_colors(self, nests_amount, min_initial_colors_amount, max_initial_colors_amount)

    # Evaluar los nidos iniciales
    best_nest: Dict[int, str] = find_best_solution(nest_population)
    best_score: int = eval_sol(best_nest)

    # Evolución de la población de nidos
    for _ in range(generations):
        # print(f"Generación {i + 1}/{generations}",
        #       f"Mejor solución: {best_score}")

        # Seleccionar K tripletas de padres
        K = nests_amount // 6
        parents: List[List[Dict[int, str]]] = get_parent_triplets(
            nest_population, K, eval_sol, mode)

        # Cruzar las tripletas de padres para obtener K hijos
        children: List[Dict[int, str]] = [
            triple_partition_crossover(self, p) for p in parents]

        # Mutar a los K hijos
        children = [mutate(self, c, mutation_rate) for c in children]

        # Mejorar a los hijos
        children = [enhance_sol(self, c, i, K, i == generations - 1) for i, c in enumerate(children)]

        # Agregar a la población a los K hijos
        nest_population.extend(children)

        # Seleccionar K // 2 individuos de la población según que tan malo es su desempeño
        killed = random.choices(nest_population, k=K // 2, weights=[
            eval_sol(c) if mode == 'MIN' else 1 / eval_sol(c)
            for c in nest_population
        ])
        nest_population = [n for n in nest_population if n not in killed]

        # Actualizar la mejor solución
        generation_best = find_best_solution(nest_population)
        generation_best_score = eval_sol(generation_best)

        if (mode == 'MIN' and generation_best_score < best_score) or (mode == 'MAX' and generation_best_score > best_score):
            best_nest = generation_best
            best_score = generation_best_score

        # Agregar a la mejor solución a la población (intensificación)
        nest_population.append(best_nest)

    # Aplicar mejor solución
    self.apply_coloring_dict(best_nest)
