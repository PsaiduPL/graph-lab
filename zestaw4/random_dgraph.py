from graph.digraph import DiGraph


def main():
    graph = DiGraph.random_graph(7, 0.3)
    graph.print_pretty()
    graph.print_adjacency_matrix()
    graph.visualize()


if __name__ == "__main__":
    main()
