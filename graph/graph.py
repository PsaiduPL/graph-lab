import random
from enum import Enum

from zestaw1.graf import (
    lista_sasiedztwa_do_macierzy_sasiedztwa,
    load_lista_sasiedztwa,
    load_macierz_incydencji,
    load_macierz_sasiedztwa,
    macierz_incydencji_do_macierzy_sasiedztwa,
    macierz_sasiedztwa_do_listy_sasiedztwa,
    macierz_sasiedztwa_do_macierzy_incydencji,
)
from zestaw1.wizualizacja import rysuj_graf


class Representation(Enum):
    ADJACENCY_MATRIX = "adjacency_matrix"
    ADJACENCY_LIST = "adjacency_list"
    INCIDENCE_MATRIX = "incidence_matrix"

class Graph:
    def __init__(self, adjacency_matrix: list[list[int]]) -> None:
        self.adjacency_matrix = adjacency_matrix

    # --- build from a representation ---

    @classmethod
    def from_adjacency_matrix(cls, adjacency_matrix: list[list[int]]) -> "Graph":
        return cls(adjacency_matrix)

    @classmethod
    def from_adjacency_list(cls, adjacency_list: dict[int, list[int]]) -> "Graph":
        return cls(lista_sasiedztwa_do_macierzy_sasiedztwa(adjacency_list))

    @classmethod
    def from_incidence_matrix(cls, incidence_matrix: list[list[int]]) -> "Graph":
        return cls(macierz_incydencji_do_macierzy_sasiedztwa(incidence_matrix))

    @classmethod
    def from_degree_sequence(cls, degree_sequence: list[int]) -> "Graph":
        from zestaw2.graph_sequence import build_graph_from_degree_sequence

        adjacency_list = build_graph_from_degree_sequence(
            sorted(degree_sequence, reverse=True)
        )
        return cls.from_adjacency_list(adjacency_list)

    @classmethod
    def from_degree_sequence_file(cls, file_name: str) -> "Graph":
        from zestaw2.graph_sequence import build_graph_from_degree_sequence
        from zestaw2.load_sequence import load_degree_sequence_sorted_desc

        adjacency_list = build_graph_from_degree_sequence(
            sorted(load_degree_sequence_sorted_desc(file_name), reverse=True)
        )
        return cls.from_adjacency_list(adjacency_list)

    # --- build from a file ---

    @classmethod
    def from_adjacency_matrix_file(cls, filename: str) -> "Graph":
        return cls.from_adjacency_matrix(load_macierz_sasiedztwa(filename))

    @classmethod
    def from_adjacency_list_file(cls, filename: str) -> "Graph":
        return cls.from_adjacency_list(load_lista_sasiedztwa(filename))

    @classmethod
    def from_incidence_matrix_file(cls, filename: str) -> "Graph":
        return cls.from_incidence_matrix(load_macierz_incydencji(filename))

    # --- convert to a representation ---

    def to_adjacency_matrix(self) -> list[list[int]]:
        return [row[:] for row in self.adjacency_matrix]

    def to_adjacency_list(self) -> dict[int, list[int]]:
        return macierz_sasiedztwa_do_listy_sasiedztwa(self.adjacency_matrix)

    def to_incidence_matrix(self) -> list[list[int]]:
        return macierz_sasiedztwa_do_macierzy_incydencji(self.adjacency_matrix)

    def degree_sequence(self) -> list[int]:
        return sorted((sum(row) for row in self.adjacency_matrix), reverse=True)

    @classmethod
    def from_representation(cls, data, representation: Representation) -> "Graph":
        match representation:
            case Representation.ADJACENCY_MATRIX:
                return cls.from_adjacency_matrix(data)
            case Representation.ADJACENCY_LIST:
                return cls.from_adjacency_list(data)
            case Representation.INCIDENCE_MATRIX:
                return cls.from_incidence_matrix(data)
        raise ValueError(f"Unknown representation: {representation}")

    @classmethod
    def from_file(cls, filename: str, representation: Representation) -> "Graph":
        match representation:
            case Representation.ADJACENCY_MATRIX:
                return cls.from_adjacency_matrix_file(filename)
            case Representation.ADJACENCY_LIST:
                return cls.from_adjacency_list_file(filename)
            case Representation.INCIDENCE_MATRIX:
                return cls.from_incidence_matrix_file(filename)
        raise ValueError(f"Unknown representation: {representation}")

    def to(self, representation: Representation):
        match representation:
            case Representation.ADJACENCY_MATRIX:
                return self.to_adjacency_matrix()
            case Representation.ADJACENCY_LIST:
                return self.to_adjacency_list()
            case Representation.INCIDENCE_MATRIX:
                return self.to_incidence_matrix()
        raise ValueError(f"Unknown representation: {representation}")

    # Zestaw 2 zad 2
    @classmethod
    def random_graph(cls, n: int, p: float) -> "Graph":
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < p:
                    G[i][j] = G[j][i] = 1
        return Graph.from_adjacency_matrix(G)
        
    def randomize(self, random_count: int) -> "Graph":
        matrix = self.to_adjacency_matrix()
        n = len(matrix)
        edges = [(i, j) for i in range(n) for j in range(i + 1, n) if matrix[i][j] == 1]
        if len(edges) < 2:
            return Graph(matrix)

        done = 0
        attempts = 0
        max_attempts = 100 * random_count + 1000  # some graphs (e.g. complete) allow no swap
        while done < random_count and attempts < max_attempts:
            attempts += 1
            e1, e2 = random.sample(range(len(edges)), 2)
            a, b = edges[e1]
            c, d = edges[e2]
            if random.random() < 0.5:
                c, d = d, c

            if len({a, b, c, d}) < 4:
                continue                                    # would create a loop
            if matrix[a][d] == 1 or matrix[b][c] == 1:
                continue                                    # would create a multiple edge

            matrix[a][b] = matrix[b][a] = 0
            matrix[c][d] = matrix[d][c] = 0
            matrix[a][d] = matrix[d][a] = 1
            matrix[b][c] = matrix[c][b] = 1
            edges[e1] = (a, d)
            edges[e2] = (b, c)
            done += 1

        return Graph(matrix)

    def visualize(self,filename : str | None = None):
        rysuj_graf(self.adjacency_matrix, filename)

    @classmethod
    def k_regular(cls,n,k) -> "Graph":
        return Graph.from_adjacency_list(k_regular_graph(n,k))

def k_regular_graph(n, k, max_tries=1000) -> dict[int,list[int]]:
    assert 0 <= k < n and (n * k) % 2 == 0
    for _ in range(max_tries):
        adj = {i: set() for i in range(n)}
        stuck = False
        for vertex in range(n):
            while len(adj[vertex]) < k:
                candidates = [u for u in range(n)
                              if u != vertex
                              and len(adj[u]) < k
                              and u not in adj[vertex]]
                if not candidates:
                    stuck = True
                    break
                u = random.choice(candidates)
                adj[vertex].add(u)
                adj[u].add(vertex)
            if stuck:
                break
        if not stuck:
            return {i: sorted(s) for i, s in adj.items()}
    raise RuntimeError("couldn't build a k-regular graph")
