import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from problem import load_graph, find_classical_optimum
from qaoa_circuit import optimize_qaoa
from visualization import save_graph_visualization


def main():
    print("=" * 45)
    print("       OPTI-Q: QUANTUM MAX-CUT")
    print("=" * 45)

    # Load the six-node weighted graph
    graph = load_graph()

    # Find the exact classical optimum
    classical_value, classical_partition = find_classical_optimum(graph)

    print("\nCLASSICAL RESULTS")
    print("Nodes:", graph.number_of_nodes())
    print("Edges:", graph.number_of_edges())
    print("Classical optimum:", classical_value)
    print("Best partition:", classical_partition)

    # Run QAOA
    print("\nRunning QAOA p=1...")
    qaoa_results = optimize_qaoa(graph)

    expected_cut = qaoa_results["expected_cut"]
    approximation_ratio = (
        expected_cut / classical_value if classical_value else 0.0
    )

    print("\nQAOA RESULTS")
    for key, value in qaoa_results.items():
        print(f"{key}: {value}")

    print("Approximation ratio:", round(approximation_ratio, 4))

    # Save results
    os.makedirs("results/tables", exist_ok=True)

    output = {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "classical_optimum": classical_value,
        "classical_partition": classical_partition,
        "qaoa": qaoa_results,
        "approximation_ratio": approximation_ratio,
        "note": "Local Aer simulation; not physical quantum hardware results."
    }

    with open("results/tables/qaoa_results.json", "w") as file:
        json.dump(output, file, indent=4)

    # Save graph visualization
    save_graph_visualization(graph)

    print("\nResults saved to results/tables/qaoa_results.json")
    print("Project run completed!")


if __name__ == "__main__":
    main()