import igraph as ig
from src.lib.methods_for_graph import vertex_with_max_saturation, adjacent_colors, change_color_and_increase_saturation, group_nodes_by_color, is_colored, is_safe_to_color, reset_colors, is_valid_coloring, number_of_colors, coloring_as_dict, apply_coloring_dict,count_and_sort_colors, uncolor, get_amount_of_colors, random_color_graph, colors_used, save_vertex_state, load_vertex_state, count_colors
from src.lib.d_satur import d_satur
from src.lib.ils import ils
from src.lib.backtracking import backtracking
from src.lib.local_search import local_search, kempe_neighbourhood, kempe_sorted, local_search_without_d_satur
from src.lib.grasp import grasp
from src.lib.genetic import genetic_algorithm
from src.lib.annealing import simulated_annealing

ig.Graph.count_colors = count_colors
ig.Graph.local_search_without_d_satur = local_search_without_d_satur
ig.Graph.save_vertex_state = save_vertex_state
ig.Graph.load_vertex_state = load_vertex_state
ig.Graph.colors_used = colors_used
ig.Graph.random_color_graph = random_color_graph
ig.Graph.ils = ils
ig.Graph.get_amount_of_colors = get_amount_of_colors
ig.Graph.uncolor = uncolor
ig.Graph.count_and_sort_colors = count_and_sort_colors
ig.Graph.number_of_colors = number_of_colors
ig.Graph.is_valid_coloring = is_valid_coloring
ig.Graph.reset_colors = reset_colors
ig.Graph.is_colored = is_colored
ig.Graph.is_safe_to_color = is_safe_to_color
ig.Graph.vertex_with_max_saturation = vertex_with_max_saturation
ig.Graph.adjacent_colors = adjacent_colors
ig.Graph.change_color_and_increase_saturation = change_color_and_increase_saturation
ig.Graph.d_satur = d_satur
ig.Graph.backtracking = backtracking
ig.Graph.group_nodes_by_color = group_nodes_by_color
ig.Graph.kempe_neighbourhood = kempe_neighbourhood
ig.Graph.local_search = local_search
ig.Graph.coloring_as_dict = coloring_as_dict
ig.Graph.kempe_sorted = kempe_sorted
ig.Graph.apply_coloring_dict = apply_coloring_dict
ig.Graph.grasp = grasp
ig.Graph.genetic_algorithm = genetic_algorithm
ig.Graph.simulated_annealing = simulated_annealing


def read_graph(file_path: str) -> ig.Graph:
    """
    Lee un archivo de texto que contiene la descripción de un grafo (en formato DIMACS)
    y retorna un objeto de tipo igraph.Graph.
    """

    with open(file_path, "r") as f:
        lines = f.readlines()

    i: int = 0
    lines: list[str] = [line.strip() for line in lines]
    format: str = ''
    nodes: int = 0
    edges: int = 0

    for line in lines:
        if line.startswith("c"):
            i += 1
            continue
        elif line.startswith("p"):
            format, nodes, edges = line.split(' ')[1:]
            nodes, edges = int(nodes), int(edges)
            i += 1
            break

    g: ig.Graph = ig.Graph(directed=False)

    g.colors = [str(x) for x in range(nodes)]

    for i in range(nodes):
        g.add_vertex(name=str(i + 1), color=-1, saturation=0, index=i)

    if format == "edge":
        for j in range(0, len(lines)):
            if lines[j].startswith("e"):
                _, v1, v2 = lines[j].split(' ')
                v1, v2 = int(v1), int(v2)
                g.add_edge(v1 - 1, v2 - 1)
    else:
        print("\033[91mError: The graph format is not supported.\033[0m")
        print("\033[91mSupported formats\033[0m: edge")
        print("\033[91mActual format\033[0m: ", format)

    return g
