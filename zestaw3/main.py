"""
    uv run python -m zestaw3.main                        # losowy spójny graf
    uv run python -m zestaw3.main --przyklad 
    uv run python -m zestaw3.main --plik moj.txt
    uv run python -m zestaw3.main -h
"""

import argparse
import os
import random

from graph.weighted import INF, WeightedGraph

HERE = os.path.dirname(__file__)
PRZYKLAD = os.path.join(HERE, "input", "przyklad.txt")
OUTPUT = os.path.join(HERE, "output")


def fmt(x: float) -> str:
    return "inf" if x == INF else str(int(x))


def zad1(g: WeightedGraph) -> None:
    print("=== Zad. 1: spójny graf z wagami ===")
    print(f"n = {g.n}, krawędzi = {len(g.edges())}")
    for u, v, w in g.edges():
        print(f"  {u + 1:>2} - {v + 1:<2}  waga {w}")
    print()


def zad2(g: WeightedGraph, s: int) -> None:
    print("=== Zad. 2: Dijkstra ===")
    ds, ps = g.dijkstra(s)
    width = len(str(g.n))
    print(f"START: s = {s + 1}")
    for v in range(g.n):
        path = WeightedGraph.path_to(ps, s, v)
        path_str = " - ".join(str(x + 1) for x in path) if path else "brak ścieżki"
        print(f"d({v + 1:>{width}}) = {fmt(ds[v]):>3} ==> [{path_str}]")
    print()


def zad3(g: WeightedGraph) -> None:
    print("=== Zad. 3: macierz odległości ===")
    D = g.distance_matrix()
    cell = max(len(fmt(x)) for row in D for x in row) + 1
    label = len(str(g.n))
    print(" " * (label + 2) + "".join(f"{k + 1:>{cell}}" for k in range(g.n)))
    for w, row in enumerate(D):
        print(f"{w + 1:>{label}} |" + "".join(f"{fmt(x):>{cell}}" for x in row))
    print()


def zad4(g: WeightedGraph) -> None:
    print("=== Zad. 4: centrum ===")
    c, total = g.center()
    m, far = g.minimax_center()
    print(f"Centrum = {c + 1} (suma odleglosci: {fmt(total)})")
    print(f"Centrum minimax = {m + 1} (odleglosc od najdalszego: {fmt(far)})")
    print()


def zad5(g: WeightedGraph) -> list[tuple[int, int, int]]:
    print("=== Zad. 5: minimalne drzewo rozpinające (Kruskal) ===")
    tree = g.mst_kruskal()
    for u, v, w in tree:
        print(f"  {u + 1:>2} - {v + 1:<2}  waga {w}")
    print(f"Suma wag MST: {sum(w for _, _, w in tree)}")
    print()
    return tree


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Zestaw 3: Dijkstra, macierz odległości, centrum, MST")
    src = p.add_mutually_exclusive_group()
    src.add_argument("--przyklad", action="store_true", help="graf z input_3.pdf (12 wierzchołków)")
    src.add_argument("--plik", help="plik z listą krawędzi: 'u v waga' w każdej linii")
    p.add_argument("-n", type=int, default=12, help="liczba wierzchołków grafu losowego (domyślnie 12)")
    p.add_argument("-p", type=float, default=0.3, help="prawdopodobieństwo krawędzi G(n,p) (domyślnie 0.3)")
    p.add_argument("--wmin", type=int, default=1, help="minimalna waga (domyślnie 1)")
    p.add_argument("--wmax", type=int, default=10, help="maksymalna waga (domyślnie 10)")
    p.add_argument("--seed", type=int, help="ziarno losowania — ten sam seed = ten sam graf")
    p.add_argument("-s", "--start", type=int, default=1, help="wierzchołek startowy Dijkstry (od 1)")
    p.add_argument("--bez-okien", action="store_true", help="nie otwieraj okien z rysunkami (tylko zapis SVG)")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    if args.seed is not None:
        random.seed(args.seed)

    if args.przyklad:
        g = WeightedGraph.from_edge_list_file(PRZYKLAD)
    elif args.plik:
        g = WeightedGraph.from_edge_list_file(args.plik)
    else:
        g = WeightedGraph.random_connected(args.n, args.p, args.wmin, args.wmax)

    if not 1 <= args.start <= g.n:
        raise SystemExit(f"--start musi być z zakresu 1..{g.n}")

    zad1(g)
    zad2(g, args.start - 1)
    zad3(g)
    zad4(g)
    tree = zad5(g)

    os.makedirs(OUTPUT, exist_ok=True)
    graf_svg = os.path.join(OUTPUT, "graf.svg")
    mst_svg = os.path.join(OUTPUT, "mst.svg")
    show = not args.bez_okien
    g.draw(graf_svg, title="Graf z wagami", show=show)
    g.draw(mst_svg, highlight=tree, title="MST (Kruskal)", show=show)
    print(f"Zapisano: {graf_svg}\n          {mst_svg}")


if __name__ == "__main__":
    main()
