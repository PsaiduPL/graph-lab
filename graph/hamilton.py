from graph.graph import Graph


def hamilton_cycle(graph: Graph) -> list[int]:
    """
    Szukanie cyklu Hamiltona przez DFS z nawrotami (backtracking).
    Zwraca kolejne wierzchołki cyklu (pierwszy == ostatni) albo [] gdy
    graf nie jest hamiltonowski.

    Struktury:
      - path: aktualnie budowana ścieżka prosta (jednocześnie stos DFS-a),
      - visited: wierzchołki leżące na path (szybkie sprawdzanie),
      - next_neighbour[i]: indeks kolejnego sąsiada path[i], którego jeszcze
        nie próbowaliśmy — dzięki temu po cofnięciu nie zaczynamy od nowa.

    W każdym kroku patrzymy na ostatni wierzchołek ścieżki:
      1. ścieżka zawiera wszystkie wierzchołki i ostatni sąsiaduje ze
         startem -> mamy cykl,
      2. ma niesprawdzonego sąsiada spoza ścieżki -> dokładamy go,
      3. w przeciwnym razie ślepy zaułek -> zdejmujemy wierzchołek ze
         ścieżki i *odznaczamy go w visited*, żeby mógł być użyty w innej
         kolejności.

    Start jest dowolny, bo cykl Hamiltona przechodzi przez każdy wierzchołek.
    Złożoność pesymistyczna O(n!) — problem jest NP-zupełny.
    """
    adjacency_list = graph.to_adjacency_list()
    vertex_count = len(adjacency_list)
    if vertex_count < 3:
        return []

    start = next(iter(adjacency_list))
    path = [start]
    visited = {start}
    next_neighbour = [0]

    while path:
        vertex = path[-1]
        neighbours = adjacency_list[vertex]

        if len(path) == vertex_count and start in neighbours:
            return path + [start]

        # szukamy kolejnego niesprawdzonego sąsiada spoza ścieżki
        index = next_neighbour[-1]
        while index < len(neighbours) and neighbours[index] in visited:
            index += 1

        if index < len(neighbours):
            next_neighbour[-1] = index + 1
            path.append(neighbours[index])
            visited.add(neighbours[index])
            next_neighbour.append(0)
        else:
            # ślepy zaułek: cofamy się o jeden wierzchołek
            visited.remove(path.pop())
            next_neighbour.pop()

    return []
