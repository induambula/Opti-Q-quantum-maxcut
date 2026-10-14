import json
import networkx as nx
from itertools import product


def load_graph(filename="data/weighted_graph.json"):
    with open(filename, "r") as file:
        data = json.load(file)

    graph = nx.Graph()
    graph.add_nodes_from(data["nodes"])

    for edge in data["edges"]:
        graph.add_edge(
            edge["source"],
            edge["target"],
            weight=edge["weight"]
        )

    return graph


def calculate_cut(graph, partition):
    cut_value = 0

    for u, v, data in graph.edges(data=True):
        if partition[u] != partition[v]:
            cut_value += data["weight"]

    return cut_value


def find_classical_optimum(graph):
    nodes = list(graph.nodes())
    best_value = -1
    best_partition = None

    for assignment in product([0, 1], repeat=len(nodes)):
        partition = dict(zip(nodes, assignment))
        value = calculate_cut(graph, partition)

        if value > best_value:
            best_value = value
            best_partition = partition

    return best_value, best_partition


if __name__ == "__main__":
    G = load_graph()
    optimum, partition = find_classical_optimum(G)

    print("Weighted Max-Cut Problem")
    print("Nodes:", G.number_of_nodes())
    print("Edges:", G.number_of_edges())
    print("Classical optimum cut value:", optimum)
    print("Best partition:", partition)