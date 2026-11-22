from graph.digraph import DiGraph


def dfs(digraph: DiGraph) -> list[list[int]]:
    adj = digraph.adjacency_list
    visited: set[int] = set()
    components: list[list[int]] = []

    for start in adj:
        if start in visited:
            continue
        visited.add(start)
        stack = [start]
        component = []
        while stack:
            v = stack.pop()
            component.append(v + 1)
            for u in adj.get(v, []):
                if u not in visited:
                    visited.add(u)
                    stack.append(u)
        components.append(component)

    return components


def dfs_visit(
    digraph: DiGraph, v: int, d: dict[int, int], f: dict[int, int], t: int
) -> int:
    t = t + 1
    d[v] = t
    for u in digraph.adjacency_list[v]:
        if d[u] == -1:
            t = dfs_visit(digraph, u, d, f, t)
    t = t + 1
    f[v] = t
    return t


def components_r(nr: int, v: int, graph: DiGraph, comp: dict[int, int]):
    for u in graph.adjacency_list[v]:
        if comp[u] == -1:
            comp[u] = nr
            components_r(nr, u, graph, comp)


def kosaraju(digraph: DiGraph):
    adj = digraph.adjacency_list
    d: dict[int, int] = {}
    f: dict[int, int] = {}
    for i in adj:
        d[i] = -1
        f[i] = -1
    t = 0
    for v in digraph.adjacency_list:
        if d[v] == -1:
            t = dfs_visit(digraph, v, d, f, t)
    t_graph = digraph.transpose()
    nr = 0
    comp: dict[int, int] = {}
    for v in t_graph.adjacency_list:
        comp[v] = -1

    order = sorted([(i, f[i]) for i in f], key=lambda x: x[1], reverse=True)
    for v, _ in order:
        if comp[v] == -1:
            nr += 1
            comp[v] = nr
            components_r(nr, v, t_graph, comp)
    components : dict[int,list[int]] = {c : [] for c in sorted(comp.values())}
    for (v,c) in comp.items():
        components[c].append(v + 1) 
    return components

def main():
    graph = DiGraph.random_graph(10, 0.15)
    comp = kosaraju(graph)
    for (k,v) in comp.items():
        print(f"{k} -- {v}")
    
    
    graph.visualize()


if __name__ == "__main__":
    main()
