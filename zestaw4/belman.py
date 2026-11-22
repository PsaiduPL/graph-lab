from graph.digraph import WeightedDiGraph
from graph.shortest_paths import bellman_ford, shortest_path


def main():
    graph = WeightedDiGraph.random_strong_graph(8, 0.25, -5, 10)

    graph.print_pretty()
    vertices = list(graph.adjacency_list)
    d, path = bellman_ford(graph, vertices[0])
    print([x + 1 for x in shortest_path(path, vertices[0], vertices[-1])])
    print(d[vertices[-1]])
    graph.visualize(min_distance=2)
    

if __name__ == "__main__":
    main()
