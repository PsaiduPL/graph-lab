def load_macierz_sasiedztwa(filename: str) -> list[list[int]]:
    result = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            result.append([int(x) for x in line.split()])
    return result


def load_lista_sasiedztwa(filename: str) -> dict[int, list[int]]:
    with open(filename) as f:
        result = {}
        for i, line in enumerate(f):
            line = line.strip()
            result[i + 1] = [int(x) for x in line.split()]
    return result


def load_macierz_incydencji(filename: str) -> list[list[int]]:
    result = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            result.append([int(x) for x in line.split()])
    return result


def macierz_sasiedztwa_do_listy_sasiedztwa(G: list[list[int]]) -> dict[int, list[int]]:
    result = {i + 1: [] for i in range(len(G))}
    for i, wiersz in enumerate(G):
        for j, value in enumerate(wiersz):
            if value == 1:
                result[i + 1].append(j + 1)
    return result


def lista_sasiedztwa_do_macierzy_sasiedztwa(G: dict[int, list[int]]) -> list[list[int]]:
    wierzcholki = sorted(set(G) | {v for sasiedzi in G.values() for v in sasiedzi})
    indeks = {w: i for i, w in enumerate(wierzcholki)}

    n = len(wierzcholki)
    result = [[0] * n for _ in range(n)]
    for w, sasiedzi in G.items():
        for v in sasiedzi:
            result[indeks[w]][indeks[v]] = 1
    return result


def macierz_sasiedztwa_do_macierzy_incydencji(G: list[list[int]]) -> list[list[int]]:
    n = len(G)
    krawedzie = []
    for i in range(n):
        for j in range(i + 1, n):
            if G[i][j] == 1:
                krawedzie.append((i, j))
    result = [[0] * len(krawedzie) for _ in range(n)]
    for l, (i, j) in enumerate(krawedzie):
        result[i][l], result[j][l] = 1, 1
    return result


def macierz_incydencji_do_macierzy_sasiedztwa(G: list[list[int]]) -> list[list[int]]:
    n = len(G)
    k = len(G[0]) if G else 0
    result = [[0] * n for _ in range(n)]
    for l in range(k):
        wierzcholki = [i for i in range(n) if G[i][l] == 1]
        i, j = wierzcholki
        result[i][j] = result[j][i] = 1
    return result


def macierz_incydencji_do_listy_sasiedztwa(G: list[list[int]]) -> dict[int, list[int]]:
    return macierz_sasiedztwa_do_listy_sasiedztwa(macierz_incydencji_do_macierzy_sasiedztwa(G))


def lista_sasiedztwa_do_macierzy_incydencji(G: dict[int, list[int]]) -> list[list[int]]:
    return macierz_sasiedztwa_do_macierzy_incydencji(lista_sasiedztwa_do_macierzy_sasiedztwa(G))


def main():
    g = load_macierz_sasiedztwa("macierzsasiedztwa.txt")
    f = load_lista_sasiedztwa("listasasiedztwa.txt")
    h = load_macierz_incydencji("macierzincydencji.txt")

    print("macierz_sasiedztwa_do_listy_sasiedztwa:")
    for v, sasiedzi in macierz_sasiedztwa_do_listy_sasiedztwa(g).items():
        print(v, ":", sasiedzi)
    print("lista_sasiedztwa_do_macierzy_sasiedztwa:")
    for l in lista_sasiedztwa_do_macierzy_sasiedztwa(f):
        print(l)
    print("macierz_sasiedztwa_do_macierzy_incydencji:")
    for l in macierz_sasiedztwa_do_macierzy_incydencji(g):
        print(l)
    print("macierz_incydencji_do_macierzy_sasiedztwa:")
    for l in macierz_incydencji_do_macierzy_sasiedztwa(h):
        print(l)
    print("macierz_incydencji_do_listy_sasiedztwa:")
    for v, sasiedzi in macierz_incydencji_do_listy_sasiedztwa(h).items():
        print(v, ":", sasiedzi)
    print("lista_sasiedztwa_do_macierzy_incydencji:")
    for l in lista_sasiedztwa_do_macierzy_incydencji(f):
        print(l)


if __name__ == "__main__":
    main()
