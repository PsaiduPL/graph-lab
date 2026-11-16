def load_degree_sequence_sorted_desc(file_name: str) -> list[int]:
    with open(file_name, "r") as f:
        line = f.readline()
        return map_line_to_list(line)


def load_degree_sequence_sorted_desc_many(file_name: str) -> list[list[int]]:
    with open(file_name, "r") as f:
        return [map_line_to_list(line) for line in f]


def map_line_to_list(line: str) -> list[int]:
    return sorted(
        [int(x.strip()) for x in line.split() if x.strip() != ""], reverse=True
    )


def main():
    print(load_degree_sequence_sorted_desc("zestaw2/input/ciag-graficzny-2.txt"))


if __name__ == "__main__":
    main()
