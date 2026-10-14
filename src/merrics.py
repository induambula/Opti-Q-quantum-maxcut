def calculate_approximation_ratio(qaoa_cut, classical_optimum):
    if classical_optimum == 0:
        return 0.0

    return qaoa_cut / classical_optimum


def calculate_metrics(graph, circuit, classical_optimum):
    return {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "classical_optimum": classical_optimum,
        "circuit_depth": circuit.depth(),
        "total_gates": circuit.size(),
        "two_qubit_gates": circuit.num_nonlocal_gates()
    }


if __name__ == "__main__":
    qaoa_expected_cut = 9.99367
    classical_optimum = 16

    ratio = calculate_approximation_ratio(
        qaoa_expected_cut,
        classical_optimum
    )

    print("Expected cut value:", qaoa_expected_cut)
    print("Classical optimum:", classical_optimum)
    print("Approximation ratio:", round(ratio, 4))