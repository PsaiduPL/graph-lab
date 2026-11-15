from graph.graph import Graph
from graph.hamilton import hamilton_cycle


def main():
    graph = Graph.k_regular(7, 4)

    print("Lista sąsiedztwa:")
    for vertex, neighbours in graph.to_adjacency_list().items():
        print(f"{vertex}: {neighbours}")

    cycle = hamilton_cycle(graph)
    if cycle:
        print("Cykl Hamiltona:")
        print(" - ".join(str(vertex) for vertex in cycle))
    else:
        print("Graf nie jest hamiltonowski")

    graph.visualize()


if __name__ == "__main__":
    main()
