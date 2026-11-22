import heapq
import math

from graph.digraph import Edge, WeightedDiGraph


def bellman_ford(graph: WeightedDiGraph, start: None | int = None):
    if start is None:
        start = next(iter(graph.adjacency_list))
    dist = {v: math.inf for v in graph.adjacency_list}
    dist[start] = 0.0
    pred: dict[int, None | int] = {v: None for v in graph.adjacency_list}
    n = len(graph.adjacency_list)
    for _ in range(n - 1):
        for edge in graph.weights:
            if dist[edge.from_] + edge.weight < dist[edge.to]:
                dist[edge.to] = dist[edge.from_] + edge.weight
                pred[edge.to] = edge.from_
    for edge in graph.weights:
        if dist[edge.from_] + edge.weight < dist[edge.to]:
            raise ValueError("Graph contains a negative-weight cycle")
    return dist, pred


def shortest_path(pred, start, target):
    path = []
    v = target
    while v is not None:
        path.append(v)
        v = pred[v]
    if path[-1] != start:
        return None
    return path[::-1]


def dijkstra(graph: WeightedDiGraph, source: int):
    neighbours: dict[int, list[tuple[int, float]]] = {
        v: [] for v in graph.adjacency_list
    }
    for edge in graph.weights:
        neighbours[edge.from_].append((edge.to, edge.weight))
    dist = {v: math.inf for v in neighbours}
    pred: dict[int, None | int] = {v: None for v in neighbours}
    dist[source] = 0.0
    heap = [(0.0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in neighbours[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                pred[v] = u
                heapq.heappush(heap, (dist[v], v))
    return dist, pred


def johnson(graph: WeightedDiGraph) -> list[list[int | float]]:
    vertices = list(graph.adjacency_list)
    n = len(vertices)
    source = n
    # add source to graph
    extended = WeightedDiGraph(
        {**graph.adjacency_list, source: list(vertices)},
        graph.weights + [Edge(from_=source, to=v, weight=0) for v in vertices],
    )
    # bellman
    d, _ = bellman_ford(extended, source)
    reweighted = WeightedDiGraph(
        graph.adjacency_list,
        [
            Edge(e.from_, e.to, e.weight + d[e.from_] - d[e.to])
            for e in graph.weights
        ],
    )
    distances: list[list[int | float]] = [[math.inf] * n for _ in range(n)]
    for u in vertices:
        d_hat, _ = dijkstra(reweighted, u)
        for v in vertices:
            if d_hat[v] != math.inf:
                distances[u][v] = int(d_hat[v] - d[u] + d[v])
    return distances
