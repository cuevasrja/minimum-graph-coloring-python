import igraph as ig

def read_graph(file_path: str) -> ig.Graph:
    with open(file_path, "r") as f:
        lines = f.readlines()
    lines: list[str] = [line.strip() for line in lines]
    format: str = ''
    nodes: int = 0
    edges: int = 0
    for line in lines:
        if line.startswith("c"):
            lines.remove(line) 
        elif line.startswith("p"):
            format, nodes, edges = line.split(' ')[1:]
            nodes, edges = int(nodes), int(edges)
            break
    g = ig.Graph(directed=False)

    for i in range(nodes):
        g.add_vertex(name=str(i+1), color="#")

    if format == "edge":
        for line in lines:
            if line.startswith("e"):
                _, v1, v2 = line.split(' ')
                g.add_edge(v1, v2)
    else:
        print("\033[91mError: The graph format is not supported.\033[0m")

    return g
    