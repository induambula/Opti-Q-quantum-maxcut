from qiskit import transpile
from qiskit.transpiler import CouplingMap


def benchmark_routing(circuit, coupling_edges, label):
    coupling_map = CouplingMap(couplinglist=coupling_edges)

    routed = transpile(
        circuit,
        basis_gates=["u", "cx"],
        coupling_map=coupling_map,
        optimization_level=1,
        seed_transpiler=42
    )

    swap_count = sum(
        1 for instruction in routed.data
        if instruction.operation.name == "swap"
    )

    two_qubit_count = sum(
        1 for instruction in routed.data
        if instruction.operation.num_qubits == 2
    )

    return {
        "processor": label,
        "circuit_depth": routed.depth(),
        "swap_count": swap_count,
        "two_qubit_gates": two_qubit_count
    }


if __name__ == "__main__":
    print("Routing benchmark module ready.")
    print("Use verified processor connectivity before benchmarking.")