from typing import List, Set, Dict
import random
import igraph as ig

def conflicted_vertexs(g: ig.Graph, coloring: Dict[int, str]) -> List[int]:
    conflicted: Set[int] = set()
    for e in g.es:
        source_color: str = coloring[e.source]
        target_color: str = coloring[e.target]
        if source_color == target_color:
            conflicted.add(e.source)
            conflicted.add(e.target)
    return list(conflicted)

def random_color_graph(g: ig.Graph) -> None:
    n: int = len(g.vs)
    colors: List[int] = []
    for node in range(n):
        colors.append(random.randint(0, n-1))
    for i, color in enumerate(colors):
        g.vs[i]['color'] = color

def tabu_search(self: ig.Graph, tabu_size: int = 10, max_iter: int = 100, reps: int = 50) -> None:
    random_color_graph(self)
    prev_sol: Dict[int, str] = self.coloring_as_dict()
    self.reset_colors()

    colors: List[int] = list(set(prev_sol.values()))

    best_sol: Dict[int, str] = prev_sol.copy()
    best_sol_conflicts: int = len(conflicted_vertexs(self, best_sol))
    tabu_list: List[Dict[int, str]] = [prev_sol]
    
    # Aspiration level A(z), represented by a mapping: f(s) -> best f(s') seen so far
    aspiration_level = dict()

    for _ in range(max_iter):
        move_candidates: List[int] = conflicted_vertexs(self, best_sol)

        if len(move_candidates) == 0:
            break

        new_solution: Dict[int, str] = {}
        for r in range(reps):
            # choose a random vertex to move
            v: int = random.choice(move_candidates)

            # choose a random color to move to
            new_color: int = random.choice(colors)
            while new_color == best_sol[v]:
                new_color = random.choice(colors)
            
            # move the vertex to the new color
            new_solution: Dict[int, str] = best_sol.copy()
            new_solution[v] = new_color

            # check if the new solution is in the tabu list
            if new_solution in tabu_list:
                continue

            # check if the new solution is better than the best solution
            new_conflicts: int = len(conflicted_vertexs(self, new_solution))
            if new_conflicts < best_sol_conflicts:
                if new_conflicts <= aspiration_level.setdefault(best_sol_conflicts, best_sol_conflicts - 1):
                    # Set A(z) to the best f(s') seen so far
                    aspiration_level[best_sol_conflicts] = new_conflicts - 1
                    best_sol = new_solution
                    if (v, new_color) in tabu_list:
                        tabu_list.remove((v, new_color))
                        break
                else:
                    if (v, new_color) in tabu_list:
                        tabu_list.remove((v, new_color))

        # add the new solution to the tabu list
        tabu_list.append(v, best_sol[v])
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

        best_sol_conflicts = len(conflicted_vertexs(self, best_sol))
        best_sol = new_solution.copy()

    if best_sol_conflicts != 0:
        print('No solution found')
    else:
        self.apply_coloring_dict(best_sol) 
