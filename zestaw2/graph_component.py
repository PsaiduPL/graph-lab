

from graph.graph import Graph


def largest_connected_component(graph : Graph) -> tuple[list[int], list[list[int]]]:
    adjacency = graph.to_adjacency_list()
    
    visited : set[int] = set()
    largest : list[int] = []
    components : list[list[int]] = []
    for vertex in adjacency:
        if vertex in visited:
            continue
        queue = [vertex]
        visited.add(vertex)
        component : list[int] = []
        while len(queue) != 0:
            vertex = queue.pop()
            component.append(vertex)
            for u in adjacency[vertex]:
                if u not in visited:
                    queue.append(u)
                    visited.add(u)
            if len(largest) < len(component):
                largest = component
        components.append(sorted(component))
    return (sorted(largest), components)
       
def wrap_pretty(largest : list[int], components : list[list[int]]):
    idx = next(i for i in range(len(components)) if components[i] == largest)
    for i in range(len(components)):
        print(f"{i}) {components[i]}")
    print(f"Largest component index {idx}")
    
def main():
    graph = Graph.random_graph(10, 0.2)
    print(graph.to_adjacency_list())
    largest, components = largest_connected_component(graph)
    wrap_pretty(largest, components)
    if len(components) > 1:
        graph.visualize()
if __name__ == "__main__":
    main()