import random

from graph.graph import Graph
from zestaw2.graph_component import largest_connected_component
from zestaw2.graph_sequence import is_valid_graph_from_degree_sequence


def is_connected(graph: Graph) -> bool:
    _, components = largest_connected_component(graph)
    return len(components) <= 1


def is_euler_graph(graph: Graph) -> bool:
    if any(degree % 2 == 1 for degree in graph.degree_sequence()):
        return False
    return is_connected(graph)


def random_euler_graph(n: int, randomize_count: int = 20, max_tries: int = 1000) -> Graph:
    if n < 3:
        raise ValueError("graf eulerowski z krawędziami wymaga co najmniej 3 wierzchołków")
    even_degrees = range(2, n, 2)
    for _ in range(max_tries):
        degree_sequence = sorted(random.choices(even_degrees, k=n), reverse=True)
        if not is_valid_graph_from_degree_sequence(degree_sequence[:]):
            continue
        graph = Graph.from_degree_sequence(degree_sequence).randomize(randomize_count)
        if is_euler_graph(graph):
            return graph
    raise RuntimeError("couldn't build a random Euler graph")


def euler_cycle(graph: Graph) -> list[int]:
    """
    Algorytm Hierholzera. Zwraca kolejne wierzchołki cyklu
    """
    if not is_euler_graph(graph):
        raise ValueError("graph is not Eulerian")
    adjacency_list = graph.to_adjacency_list()
    start = next((v for v, neighbours in adjacency_list.items() if neighbours), None)
    if start is None:
        return []

    stack = [start]  # aktualnie budowana ścieżka
    cycle = []
    while stack:
        vertex = stack[-1]
        if adjacency_list[vertex]:
            # idziemy dalej dowolną nieużytą krawędzią i usuwamy ją z grafu
            neighbour = adjacency_list[vertex].pop()
            adjacency_list[neighbour].remove(vertex)
            stack.append(neighbour)
        else:
            # ślepy zaułek: wierzchołek nie ma już krawędzi, trafia do wyniku
            cycle.append(stack.pop())
    return cycle[::-1]
