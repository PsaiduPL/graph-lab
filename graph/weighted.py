"""
Grafy ważone (nieskierowane) — zestaw 3.

Reprezentacja: macierz wag `weights` (n x n, indeksy 0-based).
  weights[i][j] == 0  -> brak krawędzi
  weights[i][j] == w  -> krawędź i–j o wadze w (w >= 1)
Na zewnątrz (wypisywanie, pliki) wierzchołki są numerowane od 1.
"""

import math
import random

from graph.graph import Graph
from zestaw2.graph_component import largest_connected_component

INF = math.inf


class WeightedGraph:
    def __init__(self, weights: list[list[int]]) -> None:
        n = len(weights)
        for i in range(n):
            if weights[i][i] != 0:
                raise ValueError(f"pętla w wierzchołku {i + 1}")
            for j in range(n):
                if weights[i][j] != weights[j][i]:
                    raise ValueError(f"macierz wag nie jest symetryczna ({i + 1}, {j + 1})")
        self.weights = weights

    # tworzenie

    @classmethod
    def from_graph(cls, graph: Graph, w_min: int = 1, w_max: int = 10) -> "WeightedGraph":
        """Przypisuje każdej krawędzi grafu losową wagę z [w_min, w_max]."""
        adjacency = graph.to_adjacency_matrix()
        n = len(adjacency)
        weights = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if adjacency[i][j]:
                    weights[i][j] = weights[j][i] = random.randint(w_min, w_max)
        return cls(weights)

    @classmethod
    def from_edge_list_file(cls, filename: str) -> "WeightedGraph":
        """Plik: w każdej linii `u v waga` (wierzchołki od 1), '#' = komentarz."""
        edges = []
        with open(filename, encoding="utf-8") as f:
            for line in f:
                line = line.split("#", 1)[0].strip()
                if line:
                    u, v, w = (int(x) for x in line.split())
                    edges.append((u, v, w))
        n = max(max(u, v) for u, v, _ in edges)
        weights = [[0] * n for _ in range(n)]
        for u, v, w in edges:
            weights[u - 1][v - 1] = weights[v - 1][u - 1] = w
        return cls(weights)

    @classmethod
    def random_connected(
        cls, n: int, p: float, w_min: int = 1, w_max: int = 10, max_tries: int = 10_000
    ) -> "WeightedGraph":
        """
        Zad. 1
        """
        for _ in range(max_tries):
            graph = Graph.random_graph(n, p)
            if is_connected(graph):
                return cls.from_graph(graph, w_min, w_max)
        raise RuntimeError(f"nie udało się wylosować spójnego grafu (n={n}, p={p}) — zwiększ p")

    # ---------- podstawowe operacje ----------

    @property
    def n(self) -> int:
        return len(self.weights)

    def neighbours(self, u: int) -> list[int]:
        return [v for v in range(self.n) if self.weights[u][v]]

    def edges(self) -> list[tuple[int, int, int]]:
        return [
            (i, j, self.weights[i][j])
            for i in range(self.n)
            for j in range(i + 1, self.n)
            if self.weights[i][j]
        ]

    # zad. 2: Dijkstra

    def dijkstra(self, s: int) -> tuple[list[float], list[int | None]]:
        w = self.weights
        # init(G, s)
        ds: list[float] = [INF] * self.n
        ps: list[int | None] = [None] * self.n
        ds[s] = 0

        def relax(u: int, v: int) -> None:
            if ds[v] > ds[u] + w[u][v]:
                ds[v] = ds[u] + w[u][v]
                ps[v] = u

        S: set[int] = set()
        while len(S) < self.n:
            u = min((v for v in range(self.n) if v not in S), key=lambda v: ds[v])
            if ds[u] == INF:
                break
            S.add(u)
            for v in self.neighbours(u):
                if v not in S:
                    relax(u, v)
        return ds, ps

    @staticmethod
    def path_to(ps: list[int | None], s: int, v: int) -> list[int]:
        path = [v]
        while path[-1] != s:
            prev = ps[path[-1]]
            if prev is None:
                return []  # v nieosiągalny
            path.append(prev)
        return path[::-1]

    # ---------- zad. 3: macierz odległości ----------

    def distance_matrix(self) -> list[list[float]]:
        """Wiersz w = wynik Dijkstry startującego z w."""
        return [self.dijkstra(s)[0] for s in range(self.n)]

    # ---------- zad. 4: centrum / centrum minimax ----------

    def center(self) -> tuple[int, float]:
        D = self.distance_matrix()
        sums = [sum(row) for row in D]
        best = min(range(self.n), key=lambda v: sums[v])
        return best, sums[best]

    def minimax_center(self) -> tuple[int, float]:
        D = self.distance_matrix()
        ecc = [max(row) for row in D]
        best = min(range(self.n), key=lambda v: ecc[v])
        return best, ecc[best]

    # ---------- zad. 5: minimalne drzewo rozpinające ----------

    def mst_kruskal(self) -> list[tuple[int, int, int]]:
        parent = list(range(self.n))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # skracanie ścieżki
                x = parent[x]
            return x

        tree: list[tuple[int, int, int]] = []
        for u, v, w in sorted(self.edges(), key=lambda e: e[2]):
            ru, rv = find(u), find(v)
            if ru != rv:
                parent[ru] = rv
                tree.append((u, v, w))
                if len(tree) == self.n - 1:
                    break
        if len(tree) != self.n - 1:
            raise ValueError("graf niespójny — brak drzewa rozpinającego")
        return tree

    # rysowanie

    def draw(
        self,
        filename: str | None = None,
        highlight: list[tuple[int, int, int]] | None = None,
        title: str | None = None,
        show: bool = True,
        seed: int = 1,
    ) -> None:
        """Rysuje graf z wagami; krawędzie z `highlight` (np. MST) na niebiesko."""
        import matplotlib.pyplot as plt
        import networkx as nx

        g = nx.Graph()
        g.add_nodes_from(range(1, self.n + 1))
        for u, v, w in self.edges():
            g.add_edge(u + 1, v + 1, weight=w)
        pos = nx.spring_layout(g, seed=seed)

        hl = {frozenset((u + 1, v + 1)) for u, v, _ in (highlight or [])}
        is_hl = [frozenset(e) in hl for e in g.edges()]

        fig, ax = plt.subplots(figsize=(9, 7))
        nx.draw_networkx_edges(
            g, pos, ax=ax,
            edge_color=["#1f3fbf" if h else ("#cccccc" if hl else "#555555") for h in is_hl],
            width=[3.0 if h else 1.0 for h in is_hl],
        )
        nx.draw_networkx_nodes(g, pos, ax=ax, node_color="#d9d9ff", edgecolors="#1f3fbf", node_size=500)
        nx.draw_networkx_labels(g, pos, ax=ax)
        nx.draw_networkx_edge_labels(
            g, pos, ax=ax, edge_labels=nx.get_edge_attributes(g, "weight"), font_size=9
        )
        if title:
            ax.set_title(title)
        ax.axis("off")
        fig.tight_layout()
        if filename:
            fig.savefig(filename)  # zapis PRZED show(), inaczej plik byłby pusty
        if show:
            plt.show()
        plt.close(fig)


def is_connected(graph: Graph) -> bool:
    _, components = largest_connected_component(graph)
    return len(components) <= 1
