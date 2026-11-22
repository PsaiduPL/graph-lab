import random

from graph.digraph import Edge, WeightedDiGraph


def without_negative_cycle(
    graph: WeightedDiGraph, w_min: int, w_max: int, max_tries: int = 1000
) -> WeightedDiGraph:
    for _ in range(max_tries):
        try:
            graph.distance_matrix()
            return graph
        except ValueError:
            graph = WeightedDiGraph(
                graph.adjacency_list,
                [
                    Edge(e.from_, e.to, random.randint(w_min, w_max))
                    for e in graph.weights
                ],
            )
    raise ValueError("No weights without a negative cycle found")


def main():
    w_min, w_max = -5, 10
    graph = WeightedDiGraph.random_strong_graph(7, 0.25, w_min, w_max)
    graph = without_negative_cycle(graph, w_min, w_max)

    graph.print_pretty()
    graph.print_distance_matrix()
    graph.visualize(min_distance=2)


if __name__ == "__main__":
    main()
