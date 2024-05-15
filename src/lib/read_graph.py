import igraph as ig

def read_graph(file_path: str) -> ig.Graph:
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
    g = ig.Graph(directed=False)

    for i in range(nodes):
        g.add_vertex(name=str(i+1), color="#")

    if format == "edge":
        for j in range(i, len(lines)):
            if lines[j].startswith("e"):
                _, v1, v2 = lines[j].split(' ')
                g.add_edge(v1, v2)
    else:
        print("\033[91mError: The graph format is not supported.\033[0m")
        print("\033[91mSupported formats\033[0m: edge")
        print("\033[91mActual format\033[0m: ", format)

    return g
    