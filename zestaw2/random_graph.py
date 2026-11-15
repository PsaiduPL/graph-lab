
from graph.graph import Graph

from zestaw2.load_sequence import load_degree_sequence_sorted_desc 


def randomize_graph():
    print("Hello")







def main():
    
    graph = Graph.from_degree_sequence_file("zestaw2/input/ciag-graficzny-1.txt")
    graph = graph.randomize(10)
    graph.visualize()    
    Graph.random_graph(10, 0.2).visualize()
    


if __name__ == "__main__":
    main()
    