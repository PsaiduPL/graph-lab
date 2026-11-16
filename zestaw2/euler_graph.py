import sys

from graph.euler import euler_cycle, random_euler_graph


def main():
    
    graph = random_euler_graph(6)

    print("Lista sąsiedztwa:")
    for vertex, neighbours in graph.to_adjacency_list().items():
        print(f"{vertex}: {neighbours}")
    print(f"Stopnie: {graph.degree_sequence()}")

    cycle = euler_cycle(graph)
    print("Cykl Eulera:")
    print(" - ".join(str(vertex) for vertex in cycle))

    graph.visualize()


if __name__ == "__main__":
    main()
