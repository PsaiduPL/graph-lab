import random

from graf import macierz_sasiedztwa_do_listy_sasiedztwa
from wizualizacja import rysuj_graf

 # Graf o n wierzchołkach, w którym losowo wybierane jest dokładnie l krawędzi ze wszystkich C(n, 2) możliwych par
def generuj_G_nl(n: int, l: int) -> list[list[int]]:
    G = [[0] * n for _ in range(n)]
    for i, j in random.sample([(i, j) for i in range(n) for j in range(i + 1, n)], l):
        G[i][j] = G[j][i] = 1
    return G


# Graf o n wierzchołkach, w którym każda możliwa krawędź niezależnie występuje z prawdopodobieństwem p
def generuj_G_np(n: int, p: float) -> list[list[int]]:
    G = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                G[i][j] = G[j][i] = 1
    return G


def main():
    G = generuj_G_nl(20, 4)
    for v, sasiedzi in macierz_sasiedztwa_do_listy_sasiedztwa(G).items():
        print(v, ":", sasiedzi)
    rysuj_graf(G, "losowy_nl.svg")

    G = generuj_G_np(20, 0.5)
    for v, sasiedzi in macierz_sasiedztwa_do_listy_sasiedztwa(G).items():
        print(v, ":", sasiedzi)
    rysuj_graf(G, "losowy_np.svg")

    print("zapisano losowy_nl.svg i losowy_np.svg")


if __name__ == "__main__":
    main()
