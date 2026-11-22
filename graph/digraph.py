import math
import random
from dataclasses import dataclass

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.patches import FancyArrowPatch


def _enforce_min_distance(pos: dict, min_distance: float, max_iter: int = 1000) -> dict:
    """Push vertices apart until every pair is at least `min_distance` apart."""
    nodes = list(pos)
    coords = np.array([pos[n] for n in nodes], dtype=float)
    rng = np.random.default_rng(42)
    for _ in range(max_iter):
        diff = coords[:, None, :] - coords[None, :, :]
        dist = np.linalg.norm(diff, axis=-1)
        np.fill_diagonal(dist, np.inf)
        close = dist < min_distance
        if not close.any():
            break
        for i, j in zip(*np.nonzero(np.triu(close, k=1))):
            d = dist[i, j]
            direction = diff[i, j] / d if d > 1e-9 else rng.normal(size=2)
            direction /= np.linalg.norm(direction)
            shift = (min_distance - d) / 2 * direction
            coords[i] += shift
            coords[j] -= shift
    return {n: coords[k] for k, n in enumerate(nodes)}


def _print_matrix(matrix: list[list[int | float]]) -> None:
    cells = [[str(x) for x in row] for row in matrix]
    width = max((len(c) for row in cells for c in row), default=0)
    for row in cells:
        print(" ".join(c.rjust(width) for c in row))


_SINGLE_RADS = (0.0, 0.12, -0.12, 0.25, -0.25, 0.4, -0.4)
_RECIPROCAL_RADS = (0.2, 0.3, 0.45)
_LABEL_POSITIONS = (0.5, 0.35, 0.65, 0.25, 0.75)
_NODE_AREA = 500


def _sample_curve(p1: np.ndarray, p2: np.ndarray, rad: float, count: int = 24):
    t = np.linspace(0, 1, count)[:, None]
    control = (p1 + p2) / 2 + rad * np.array([p2[1] - p1[1], p1[0] - p2[0]])
    return (1 - t) ** 2 * p1 + 2 * (1 - t) * t * control + t**2 * p2


def _choose_rads(
    pos: dict, edges: list[tuple[int, int]], clearance: float
) -> dict[tuple[int, int], float]:
    edge_set = set(edges)
    ordered = sorted(
        edges, key=lambda e: np.linalg.norm(pos[e[0]] - pos[e[1]]), reverse=True
    )
    rads: dict[tuple[int, int], float] = {}
    placed: list[np.ndarray] = []
    for u, v in ordered:
        candidates = _RECIPROCAL_RADS if (v, u) in edge_set else _SINGLE_RADS
        others = np.array([pos[w] for w in pos if w not in (u, v)]).reshape(-1, 2)
        occupied = np.vstack(placed) if placed else np.empty((0, 2))
        best_rad, best_score = candidates[0], math.inf
        for rad in candidates:
            points = _sample_curve(pos[u], pos[v], rad)
            score = 0.0
            if len(others):
                near = np.linalg.norm(points[:, None] - others[None], axis=-1)
                score += 100 * (near < clearance).sum()
            if len(occupied):
                near = np.linalg.norm(points[4:-4, None] - occupied[None], axis=-1)
                score += (near < clearance).sum()
            if score < best_score:
                best_rad, best_score = rad, score
        rads[(u, v)] = best_rad
        placed.append(_sample_curve(pos[u], pos[v], best_rad)[4:-4])
    return rads


def _draw_digraph(
    adjacency_list: dict[int, list[int]],
    labels: dict[tuple[int, int], int] | None,
    min_distance: float,
    seed: int,
) -> None:
    g = nx.DiGraph()
    g.add_nodes_from(adjacency_list)
    for u, neighbours in adjacency_list.items():
        for v in neighbours:
            g.add_edge(u, v)
    n = max(len(adjacency_list), 1)
    layout = nx.spring_layout(g, k=2 / math.sqrt(n), seed=seed, iterations=300)
    pos = {
        v: np.asarray(p, dtype=float)
        for v, p in _enforce_min_distance(layout, min_distance).items()
    }

    fig, ax = plt.subplots(figsize=(10, 8))
    coords = np.array(list(pos.values())).reshape(-1, 2)
    pad = 0.7 * min_distance
    ax.set_xlim(coords[:, 0].min() - pad, coords[:, 0].max() + pad)
    ax.set_ylim(coords[:, 1].min() - pad, coords[:, 1].max() + pad)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    fig.canvas.draw()

    radius_pt = math.sqrt(_NODE_AREA / math.pi)
    origin = ax.transData.transform((0, 0))
    unit = ax.transData.transform((1, 0)) - origin
    pixels_per_unit = float(np.linalg.norm(unit))
    clearance = 1.4 * radius_pt * fig.dpi / 72 / pixels_per_unit

    rads = _choose_rads(pos, list(g.edges), clearance)
    for (u, v), rad in rads.items():
        ax.add_patch(
            FancyArrowPatch(
                pos[u],
                pos[v],
                connectionstyle=f"arc3,rad={rad}",
                arrowstyle="-|>",
                mutation_scale=14,
                shrinkA=radius_pt + 1,
                shrinkB=radius_pt + 1,
                color="#555555",
                linewidth=1.0,
                zorder=1,
            )
        )

    ax.scatter(
        coords[:, 0],
        coords[:, 1],
        s=_NODE_AREA,
        c="#d9d9ff",
        edgecolors="#1f3fbf",
        zorder=3,
    )
    for v, p in pos.items():
        ax.text(p[0], p[1], str(v + 1), ha="center", va="center", zorder=4)

    if labels:
        curves = {e: _sample_curve(pos[e[0]], pos[e[1]], r, 101) for e, r in rads.items()}
        taken: list[np.ndarray] = []
        for edge, curve in curves.items():
            others = np.vstack([c for e, c in curves.items() if e != edge] or [np.empty((0, 2))])
            best_point, best_score = curve[50], math.inf
            for t in _LABEL_POSITIONS:
                point = curve[int(t * 100)]
                score = 0.0
                score += 100 * sum(np.linalg.norm(point - q) <= 2.5 * clearance for q in taken)
                score += 100 * sum(np.linalg.norm(point - c) <= 1.5 * clearance for c in coords)
                score += (np.linalg.norm(others - point, axis=-1) < 0.9 * clearance).sum()
                if score < best_score:
                    best_point, best_score = point, score
            taken.append(best_point)
            ax.text(
                best_point[0],
                best_point[1],
                str(labels[edge]),
                ha="center",
                va="center",
                fontsize=9,
                zorder=5,
                bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.0},
            )

    plt.show()


class DiGraph:
    def __init__(self, adjacency_list: dict[int, list[int]]) -> None:
        self.adjacency_list = adjacency_list

    @classmethod
    def from_adjacency_list(cls, adjacency_list: dict[int, list[int]]) -> "DiGraph":
        return DiGraph(adjacency_list)

    @classmethod
    def from_adjacency_matrix(cls, matrix: list[list[int]]) -> "DiGraph":
        n = len(matrix)
        if any(len(row) != n for row in matrix):
            raise ValueError("Adjacency matrix must be square")
        return DiGraph({i: [j for j in range(n) if matrix[i][j]] for i in range(n)})

    def to_adjacency_matrix(self) -> list[list[int]]:
        n = len(self.adjacency_list)
        matrix = [[0] * n for _ in range(n)]
        for u, neighbours in self.adjacency_list.items():
            for v in neighbours:
                matrix[u][v] = 1
        return matrix

    def print_adjacency_matrix(self) -> None:
        _print_matrix(self.to_adjacency_matrix())

    @classmethod
    def from_incidence_matrix(cls, matrix: list[list[int]]) -> "DiGraph":
        adjacency_list: dict[int, list[int]] = {i: [] for i in range(len(matrix))}
        for k in range(len(matrix[0]) if matrix else 0):
            column = [row[k] for row in matrix]
            if column.count(-1) != 1 or column.count(1) != 1:
                raise ValueError(f"Invalid incidence matrix column {k + 1}")
            adjacency_list[column.index(-1)].append(column.index(1))
        return DiGraph(adjacency_list)

    def to_incidence_matrix(self) -> list[list[int]]:
        edges = [(u, v) for u, vs in self.adjacency_list.items() for v in vs]
        matrix = [[0] * len(edges) for _ in self.adjacency_list]
        for k, (u, v) in enumerate(edges):
            matrix[u][k] = -1
            matrix[v][k] = 1
        return matrix

    def print_incidence_matrix(self) -> None:
        _print_matrix(self.to_incidence_matrix())

    def transpose(self) -> "DiGraph":
        adjacency_list: dict[int, list[int]] = {i: [] for i in self.adjacency_list}
        for u in adjacency_list:
            for v in self.adjacency_list[u]:
                adjacency_list[v].append(u)
        return DiGraph.from_adjacency_list(adjacency_list)

    @classmethod
    def random_graph(cls, n: int, p: float, seed: None | float = None) -> "DiGraph":
        G: dict[int, list[int]] = {i: [] for i in range(n)}
        if seed is not None:
            random.seed(seed)
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                if random.random() < p:
                    G[i].append(j)
        return DiGraph(G)

    def print_pretty(self) -> None:
        for v, edges in self.adjacency_list.items():
            print(f"{v + 1}:", end="")
            print("".join([f"|{edge + 1}|" for edge in edges]))

    def visualize(self, min_distance: float = 1.0, seed: int = 42) -> None:
        _draw_digraph(self.adjacency_list, None, min_distance, seed)


@dataclass
class Edge:
    from_: int
    to: int
    weight: int


class WeightedDiGraph(DiGraph):
    def __init__(
        self, adjacency_list: dict[int, list[int]], weights: list[Edge]
    ) -> None:
        super().__init__(adjacency_list)
        self.weights = weights

    def find_edge(self, from_: int, to: int) -> None | Edge:
        for i in self.weights:
            if i.from_ == from_ and i.to == to:
                return i
        return None

    @classmethod
    def from_weight_matrix(cls, matrix: list[list[int | float]]) -> "WeightedDiGraph":
        n = len(matrix)
        if any(len(row) != n for row in matrix):
            raise ValueError("Weight matrix must be square")
        adjacency_list: dict[int, list[int]] = {i: [] for i in range(n)}
        weights: list[Edge] = []
        for i in range(n):
            for j in range(n):
                if i != j and matrix[i][j] != math.inf:
                    adjacency_list[i].append(j)
                    weights.append(Edge(from_=i, to=j, weight=matrix[i][j]))
        return WeightedDiGraph(adjacency_list, weights)

    def to_weight_matrix(self) -> list[list[int | float]]:
        n = len(self.adjacency_list)
        matrix: list[list[int | float]] = [
            [0 if i == j else math.inf for j in range(n)] for i in range(n)
        ]
        for edge in self.weights:
            matrix[edge.from_][edge.to] = edge.weight
        return matrix

    def print_weight_matrix(self) -> None:
        _print_matrix(self.to_weight_matrix())

    def distance_matrix(self) -> list[list[int | float]]:
        from graph.shortest_paths import johnson

        return johnson(self)

    def print_distance_matrix(self) -> None:
        _print_matrix(self.distance_matrix())

    @classmethod
    def random_graph(
        cls, n: int, p: float, w_min: int, w_max: int
    ) -> "WeightedDiGraph":
        graph = super().random_graph(n, p)
        weights: list[Edge] = []

        for u in graph.adjacency_list:
            for v in graph.adjacency_list[u]:
                weights.append(Edge(from_=u, to=v, weight=random.randint(w_min, w_max)))

        return WeightedDiGraph(graph.adjacency_list, weights)

    @classmethod
    def random_strong_graph(
        cls, n: int, p: float, w_min: int, w_max: int, max_tries: int = 1000
    ) -> "WeightedDiGraph":
        for _ in range(max_tries):
            graph = cls.random_graph(n, p, w_min, w_max)
            components = kosaraju(graph)
            if len(components) == 1:
                return graph
        raise ValueError("No strong graph found")

    def print_pretty(self) -> None:
        for v, edges in self.adjacency_list.items():
            print(f"{v + 1}:", end="")
            print(
                "".join(
                    [f"|{edge + 1} W({self.find_edge(v, edge).weight})|" for edge in edges]
                )
            )

    def visualize(self, min_distance: float = 1, seed: int = 42) -> None:
        labels = {(e.from_, e.to): e.weight for e in self.weights}
        _draw_digraph(self.adjacency_list, labels, min_distance, seed)


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
    components: dict[int, list[int]] = {c: [] for c in sorted(comp.values())}
    for v, c in comp.items():
        components[c].append(v + 1)
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
