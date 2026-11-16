import copy

from graph.graph import Graph
from zestaw1.graf import lista_sasiedztwa_do_macierzy_sasiedztwa
from zestaw1.wizualizacja import rysuj_graf
from zestaw2.load_sequence import (
    load_degree_sequence_sorted_desc,
    load_degree_sequence_sorted_desc_many,
)


def build_graph_from_degree_sequence(
    degree_sequence_sorted: list[int],
) -> dict[int, list[int]]:
    """
    0 based
    """
    copied_sequence = copy.deepcopy(degree_sequence_sorted)
    vertex_count: int = len(degree_sequence_sorted)
    indices = [[i, degree_sequence_sorted[i]] for i in range(vertex_count)]
    neighbour_list: dict[int, list[int]] = { i : [] for i in range(vertex_count)}
    assert (
        is_valid_graph_from_degree_sequence(copy.deepcopy(degree_sequence_sorted))
        == True
    )
    while True:
        if all(x[1] == 0 for x in indices):
            break
        (first_idx, first_vertex) = indices.pop(0)
        for i in range(first_vertex):
            neighbour_list[first_idx].append(indices[i][0])
            neighbour_list[indices[i][0]].append(first_idx)
            indices[i][1] = indices[i][1] - 1
        indices.sort(key=lambda x: x[1], reverse=True)
    assert sorted((len(v) for v in neighbour_list.values()), reverse=True) == copied_sequence
    return neighbour_list


def is_valid_graph_from_degree_sequence(degree_sequence_sorted: list[int]) -> bool:
    max_degree = degree_sequence_sorted[0]
    vertex_count = len(degree_sequence_sorted)
    if max_degree > vertex_count - 1:
        return False
    if sum(degree_sequence_sorted) % 2 != 0:
        return False

    while True:
        if all(x == 0 for x in degree_sequence_sorted):
            return True
        if any(x < 0 for x in degree_sequence_sorted):
            return False
        first = degree_sequence_sorted.pop(0)
        for i in range(first):
            degree_sequence_sorted[i] = degree_sequence_sorted[i] - 1
        degree_sequence_sorted.append(0)
        degree_sequence_sorted.sort(reverse=True)


def test_batch():
    batch = {
        0 : True,
        1 : False,
        2 : False,
        3 : False,
        4 : True,
        5 : True,
        6 : False,
        7 : True,
        8 : False
    }
    sequences = load_degree_sequence_sorted_desc_many(
        "zestaw2/input/ciag-graficzny-many.txt"
    )
    idx = 0
    for sequence in sequences:
        is_valid = batch[idx]
        res = is_valid_graph_from_degree_sequence(copy.deepcopy(sequence))
        print(f"{idx} {is_valid} {res}")
        assert is_valid == res
        if is_valid:
            neighbour = build_graph_from_degree_sequence(sequence)
            print(neighbour)
            rysuj_graf(
                lista_sasiedztwa_do_macierzy_sasiedztwa(neighbour),
                f"zestaw2/output/batch/{idx}.svg",
            )
        idx+=1


def main():
    neightboor_list = Graph.from_degree_sequence_file("zestaw2/input/ciag-graficzny-1.txt")
    sequence = neightboor_list.degree_sequence()
    print(sequence)
    assert is_valid_graph_from_degree_sequence(sequence) == True
    neightboor_list.visualize()

    # test_batch()


if __name__ == "__main__":
    main()
