import math
import random

from graph.digraph import DiGraph

DIGRAF = DiGraph.from_adjacency_list({
    0: [4, 5, 8],
    1: [0, 2, 5],
    2: [1, 3, 4, 11],
    3: [2, 4, 7, 8, 10],
    4: [2, 6, 7, 8],
    5: [1, 6],
    6: [4, 5, 7],
    7: [3, 6, 8, 11],
    8: [3, 4, 7, 9],
    9: [8],
    10: [3, 8],
    11: [0, 7],
})

def _write_result(pr: list[float]) -> None:
    pr.sort()
    for v in range(len(pr)):
        print(f"{v}: PageRank = {pr[v]:.6f}")


def zad1a(d: float, N: int = 1_000_000, G: DiGraph | None = None) -> list[float]:
    G = DIGRAF if G is None else G
    adj = G.adjacency_list
    n = len(adj)
    licznik = [0] * n
    v = random.randrange(n)
    for _ in range(N):
        licznik[v] += 1
        if random.random() < d or not adj[v]:
            v = random.randrange(n)
        else:
            v = random.choice(adj[v])
    rank = [c / N for c in licznik]
    _write_result(rank)
    return rank


def zad1b(d: float, eps: float = 1e-10, max_iter: int = 10_000, G: DiGraph | None = None) -> list[float]:
    G = DIGRAF if G is None else G
    A = G.to_adjacency_matrix()
    n = len(A)
    p = [1.0 / n] * n
    for it in range(1, max_iter + 1):
        p_new = [d / n] * n
        for i in range(n):
            if A[i]:
                waga = (1.0 - d) * p[i] / sum(A[i])
                for j in range(n):
                    if A[i][j]:
                        p_new[j] += waga
        if math.dist(p, p_new) < eps:
            break
        p = p_new
    print(f"Zbieżność po {it} iteracjach")
    _write_result(p)
    return p


def _read_points(sciezka: str) -> list[tuple[float, float]]:
    punkty = []
    with open(sciezka) as f:
        for line in f:
            line = line.split()
            if len(line) == 2:
                punkty.append((float(line[0]), float(line[1])))
    return punkty


def _dlugosc(cykl: list[int], D: list[list[float]]) -> float:
    return sum(D[cykl[k]][cykl[(k + 1) % len(cykl)]] for k in range(len(cykl)))


def zad2(restarts: int = 8, max_it: int = 40_000, seed: int | None = None) -> tuple[list[int], float]:
    if seed is not None:
        random.seed(seed)
    punkty = _read_points("zestaw6/xqf131.dat")
    n = len(punkty)
    D = [[math.dist(punkty[i], punkty[j]) for j in range(n)] for i in range(n)]

    best_P: list[int] = []
    best_dl = math.inf
    for _ in range(restarts):
        P = list(range(n))
        random.shuffle(P)
        dl = _dlugosc(P, D)
        T = 30.0
        while T > 0.0005:
            for _ in range(max_it):
                a, c = sorted(random.sample(range(n), 2))
                b = (a + 1) % n
                d_ = (c + 1) % n
                if b == c:
                    continue
                delta = D[P[a]][P[c]] + D[P[b]][P[d_]] - D[P[a]][P[b]] - D[P[c]][P[d_]]
                if delta < 0 or random.random() < math.exp(-delta / T):
                    P[a + 1:c + 1] = P[a + 1:c + 1][::-1]  # operacja 2-opt
                    dl += delta
            T *= 0.87
        if dl < best_dl:
            best_dl, best_P = dl, P[:]
    return best_P, best_dl


def wizualizacja_zad2(P: list[int], punkty: list[tuple[float, float]]) -> None:
    import matplotlib.pyplot as plt

    xy = [punkty[v] for v in P] + [punkty[P[0]]]
    xs, ys = zip(*xy)
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.plot(xs, ys, "-", lw=0.8)
    ax.scatter(xs, ys, s=8)
    ax.set_aspect("equal")
    ax.set_title(f"Długość cyklu: {_dlugosc(P, [[math.dist(a, b) for b in punkty] for a in punkty]):.3f}")
    plt.show()


if __name__ == "__main__":
    print("\nzad1a: ")
    zad1a(0.15)
    print("\nzad1b: ")
    zad1b(0.15)
    print("\nzad2: ")
    P, dl = zad2()
    print(f"Długość cyklu: {dl:.3f}")
    wizualizacja_zad2(P, _read_points("zestaw6/xqf131.dat"))
