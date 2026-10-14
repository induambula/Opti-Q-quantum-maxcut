import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from scipy.optimize import minimize

from problem import load_graph, calculate_cut


def create_qaoa_circuit(graph, gamma, beta):
    nodes = list(graph.nodes())
    n = len(nodes)
    qc = QuantumCircuit(n, n)

    # Initial superposition
    for qubit in range(n):
        qc.h(qubit)

    # Cost unitary for weighted Max-Cut
    for u, v, data in graph.edges(data=True):
        weight = data["weight"]
        qc.rzz(2 * gamma * weight, u, v)

    # Mixer unitary
    for qubit in range(n):
        qc.rx(2 * beta, qubit)

    # Measurement
    qc.measure(range(n), range(n))

    return qc


def evaluate_qaoa(graph, gamma, beta, shots=2048):
    qc = create_qaoa_circuit(graph, gamma, beta)

    simulator = AerSimulator()
    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts()

    expected_cut = 0
    best_cut = 0
    best_bitstring = None

    for bitstring, count in counts.items():
        bits = [int(bit) for bit in bitstring[::-1]]
        partition = dict(enumerate(bits))

        cut_value = calculate_cut(graph, partition)
        expected_cut += cut_value * count

        if cut_value > best_cut:
            best_cut = cut_value
            best_bitstring = bitstring

    expected_cut /= shots

    return expected_cut, best_cut, best_bitstring


def optimize_qaoa(graph):
    def objective(params):
        gamma, beta = params
        expected_cut, _, _ = evaluate_qaoa(
            graph, gamma, beta, shots=512
        )
        return -expected_cut

    result = minimize(
        objective,
        x0=[0.5, 0.5],
        method="COBYLA",
        options={"maxiter": 40}
    )

    gamma, beta = result.x

    expected_cut, best_cut, best_bitstring = evaluate_qaoa(
        graph, gamma, beta, shots=4096
    )

    return {
        "gamma": float(gamma),
        "beta": float(beta),
        "expected_cut": float(expected_cut),
        "best_cut": int(best_cut),
        "best_bitstring": best_bitstring,
        "optimizer_success": bool(result.success)
    }


if __name__ == "__main__":
    G = load_graph()
    print("Running QAOA p=1 simulation...")

    results = optimize_qaoa(G)

    print("\nQAOA Results")
    for key, value in results.items():
        print(f"{key}: {value}")