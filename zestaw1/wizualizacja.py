import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from zestaw1.graf import load_macierz_sasiedztwa


def rysuj_graf(G: list[list[int]], filename: str | None):
    graf = nx.from_numpy_array(np.array(G))
    graf = nx.relabel_nodes(graf, {i: i + 1 for i in range(len(G))})
    plt.figure(figsize=(6, 6))
    nx.draw_circular(graf, with_labels=True, node_color="white", edgecolors="black")
    plt.axis("equal")
    plt.show()
    if filename is not None:
        plt.savefig(filename)
        plt.close()


def main():
    G = load_macierz_sasiedztwa("macierzsasiedztwa.txt")
    rysuj_graf(G, "wizualizacja.svg")
    print("zapisano wizualizacja.svg")


if __name__ == "__main__":
    main()
