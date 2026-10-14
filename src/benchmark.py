import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from problem import load_graph
from qaoa_circuit import create_qaoa_circuit
from routing import benchmark_routing
from visualization import save_benchmark_chart


def main():
    graph = load_graph()
    circuit = create_qaoa_circuit(graph, gamma=0.6, beta=0.5)

    results = []

    for filename in [
        "processors/processor_A.json",
        "processors/processor_B.json"
    ]:
        with open(filename, "r") as file:
            processor = json.load(file)

        result = benchmark_routing(
            circuit,
            processor["coupling_edges"],
            processor["name"]
        )

        result["topology_status"] = processor["status"]
        results.append(result)

        print("\n", processor["name"])
        for key, value in result.items():
            print(f"{key}: {value}")

    os.makedirs("results/tables", exist_ok=True)

    with open("results/tables/processor_comparison.json", "w") as file:
        json.dump(results, file, indent=4)

    save_benchmark_chart(results)

    print("\nBenchmark saved to results/tables/processor_comparison.json")
    print("These are illustrative topology simulations,")
    print("not verified official processor or hardware results.")


if __name__ == "__main__":
    main()