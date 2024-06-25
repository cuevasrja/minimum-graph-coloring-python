from typing import List
import igraph as ig
import random
from typing import Dict, Callable, List
from src.lib.eval_functions import eval_scaled_number_of_conflics, eval_sum_of_squared_color_sizes
from src.lib.genetic import mutate, create_population
from src.lib.memetic import triple_point_crossover, triple_partition_crossover, get_parent_triplets, enhance_sol


def distance(sol_a: Dict[int, str], sol_b: Dict[int, str]) -> int:
    """
    Calcula la distancia entre dos soluciones.

    Para calcular la distancia, realiza un re-etiquetado voraz de los colores
    de la solución B para que coincidan con los colores de la solución A lo mejor posible de forma voraz.

    Finalmente, calcula la cantidad de colores diferentes entre el re-etiquetado y la solución A.
    """
    # Crear copia de la solución A donde se almacenará el re-etiquetado
    diff = sol_a.copy()

    # Crear diccionario de colores
    color_map: Dict[str, str] = {}

    # Crear un mapea desde los colores de la solución A a los colores de la solución B
    for vertex_index in sol_a.keys():
        # Obtener colores
        color_a = sol_a[vertex_index]
        color_b = sol_b[vertex_index]

        # Si el color de la solución A no está en el diccionario, se agrega
        if color_a not in color_map:
            color_map[color_a] = color_a

        # Si el color de B es diferente al color de A, se re-etiqueta
        if color_a != color_b:
            # Si ya existe un mapeo cuyo valor es el color B, no se puede re-etiquetar, es un conflicto
            if color_b in color_map.values():
                continue

            color_map[color_a] = color_b

    # Re-etiquetar los colores de la solución A, de acuerdo al mapeo
    for vertex_index in sol_a.keys():
        diff[vertex_index] = color_map[sol_a[vertex_index]]

    # Contar la cantidad de colores diferentes entre el re-etiquetado y la solución B (nodo a nodo)
    return sum(1 for vertex_index in sol_a.keys() if sol_b[vertex_index] != diff[vertex_index])


def diversity_index(self: ig.Graph,
                    sol: Dict[int, str], population: List[Dict[int, str]]) -> float:
    """
    Calcula la diversidad de una solución con respecto a una población.
    """
    # Calcular la distancia de la solución con respecto a cada miembro de la población
    distances = [distance(sol, other) for other in population]

    # Calcular la diversidad
    return sum(distances) / len(population)


def eval_index(self: ig.Graph,
               sol: Dict[int, str],
               population: List[Dict[int, str]],
               alpha: float, beta: float) -> float:
    """
    Permite evaluar una solución con respecto a una población.

    Este índice toma en cuenta tanto la aptitud de la solución como su diversidad.

    `alpha`: Peso de la aptitud
    `beta`: Peso de la diversidad
    """
    eval_sol = eval_scaled_number_of_conflics(self)
    mode = 'MIN'

    diversity = diversity_index(self, sol, population)
    aptitude = eval_sol(sol) if mode == 'MAX' else 1 / eval_sol(sol)

    return (aptitude ** alpha) * (diversity ** beta)


def pro_diverse_gen(self: ig.Graph, population: List[Dict[int, str]], K: int):
    """
    Genera K soluciones que maximizan la diversidad con respecto a la población.
    """
    graph = self.copy()
    all_colors = set(str(i) for i in range(len(graph.vs)))

    # Generar K soluciones
    generated = []
    for _ in range(K):
        # Restablecer los colores de los nodos
        for v in graph.vs:
            v['color'] = ''
            v['saturation'] = 0

        # Generar una solucion a partir de los elementos menos comunes de la población
        for v in graph.vs:
            v_index = v.index

            # Obtener los colores presentes en las soluciones de la población para el nodo actual (pemitiendo repetidos)
            colors = [sol[v_index] for sol in population]

            # Obtener el color con menos apariciones
            color = min(set(colors), key=lambda c: colors.count(c))

            # Colorear el nodo con el color menos común
            v['color'] = color

        # En este punto, se tiene una solucion potencialmente inválida, por lo tanto:

        # Descolorear los nodos que tengan conflict
        for v in graph.vs:
            for neighbor in graph.neighbors(v.index):
                if v['color'] == graph.vs[neighbor]['color']:
                    v['color'] = ''
                    break

        # Coloreamos los colores faltantes con un color aleatorio que no esté en los vecinos
        for v in graph.vs:
            if v['color'] == '':
                neigh_colors = {
                    graph.vs[neighbour]['color'] for neighbour in graph.neighbors(v.index)
                }

                color = random.choice(list(all_colors - neigh_colors))
                v['color'] = color

        # Agregar la solución a la lista de soluciones generadas
        if (not graph.is_valid_coloring()):
            raise Exception(
                "Coloracion invalida generada en pro_diverse_gen()")

        generated.append(graph.coloring_as_dict())

    return generated


def trace_path(self: ig.Graph, sol_a: Dict[int, str], sol_b: Dict[int, str]) -> Dict[int, str]:
    """
    Rastrea el camino entre dos soluciones.

    Para ello aplica de forma voraz la vecinidad 1-intercambio sobre A para llegar a B.

    Retorna la lista de soluciones intermedias que son coloraciones válidas.
    """
    graph = self.copy()
    graph.apply_coloring_dict(sol_a)
    valid_intermediate_solutions = []

    # Iterar sobre los nodos para intercambiar uno a uno los colores
    for i, v in enumerate(graph.vs):
        v_index = v.index

        # Si el color del nodo en A es diferente al color del nodo en B
        if graph.vs[v_index]['color'] != sol_b[v_index]:
            # Colorear el nodo con el color de B
            graph.vs[v_index]['color'] = sol_b[v_index]
        else:
            continue

        # En este punto, `graph` continene una solución intermedia

        # Si la coloración es válida, agregarla a la lista de soluciones intermedias
        # La solución N - 1 es la misma B, así que no se agrega
        if graph.is_valid_coloring() and i != len(graph.vs) - 1:
            valid_intermediate_solutions.append(graph.coloring_as_dict())

    return valid_intermediate_solutions


def select_tracing_pairs(population: List[Dict[int, str]], n: int) -> List[List[Dict[int, str]]]:
    """
    Selecciona n pares de soluciones de la población de forma aleatoria.

    Estos pares de soluciones serán utilizados para re-enlazar el camino entre ellas.
    """
    pairs = []

    for _ in range(n):
        first = random.choice(population)
        second = random.choice([p for p in population if p != first])

        pairs.append([first, second])

    return pairs


def disperse_search(self: ig.Graph,
                    population_size: int = 100,
                    generations: int = 3,
                    mutation_rate: float = 0.5
                    ):
    ALPHA = 1.0
    BETA = 2.0
    TRACING_PCT = 0.1  # Porcentaje de soluciones para aplicar re-enlazado de caminos

    eval_sol: Callable[[Dict[int, str]],
                       int] = eval_scaled_number_of_conflics(self)

    def find_best_solution(population):
        return min(population, key=eval_sol)

    # Generar población inicial
    population: List[Dict[int, str]] = create_population(self, population_size)

    # Evaluar la población inicial
    best_solution: Dict[int, str] = find_best_solution(population)
    best_score: int = eval_sol(best_solution)

    # Evolución de la población
    for i in range(generations):
        # print(f"Generación {i + 1}/{generations}",
        #       f"Mejor solución: {best_score}")

        # Generar population_size // 2 soluciones diversas
        diverse_solutions = pro_diverse_gen(
            self, population, population_size // 2)

        # Agregar las soluciones diversas a la población
        population.extend(diverse_solutions)

        # Aplica re-enlazado de caminos a un porcentaje de las soluciones
        n_tracing = int(TRACING_PCT * len(population))
        tracing_pairs = select_tracing_pairs(population, n_tracing)

        # Aplicar reenlazado de caminos
        traced_solutions = []
        for [sol_a, sol_b] in tracing_pairs:
            traced_solutions.extend(trace_path(self, sol_a, sol_b))

        # Agregar las soluciones re-enlazadas a la población
        population.extend(traced_solutions)

        # Seleccionar K tripletas de padres
        K = population_size // 3
        parents = get_parent_triplets(population, K, lambda sol: eval_index(
            self, sol, population, ALPHA, BETA), 'MAX')

        # Cruzar las tripletas de padres para obtener K hijos
        children = [triple_point_crossover(self, p) for p in parents]

        # Mutar a los K hijos
        children = [mutate(self, c, mutation_rate) for c in children]

        # Mejorar a los hijos
        children = [enhance_sol(self, c, i, K, False) for i, c in enumerate(children)]

        # Agregar a la población a los K hijos
        population.extend(children)

        # Seleccionar len(population) - population_size individuos de la población según que tan malo es su eval_index
        killed = random.choices(population, k=len(population) - population_size, weights=[
            1 / eval_index(self, c, population, ALPHA, BETA) for c in population
        ])
        population = [p for p in population if p not in killed]

        # Actualizar la mejor solución
        generation_best = find_best_solution(population)
        generation_best_score = eval_sol(generation_best)
        # all_population_scores = [eval_sol(sol) for sol in population]
        # print(f'Generación {
        #       i + 1}/{generations} - Solución gen xhi: {set(all_population_scores)}')

        if generation_best_score < best_score:  # La coloración es mejor si el score es menor
            best_solution = generation_best
            best_score = generation_best_score

    # Aplicar mejor solución
    self.apply_coloring_dict(best_solution)
