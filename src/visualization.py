import os
import matplotlib.pyplot as plt
import networkx as nx


def save_graph_visualization(graph):
    os.makedirs("results/figures", exist_ok=True)

    pos = nx.spring_layout(graph, seed=42)

    plt.figure(figsize=(8, 6))

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_size=1200,
        font_size=12
    )

    edge_labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(
        graph,
        pos,
        edge_labels=edge_labels
    )

    plt.title("Opti-Q: Weighted Max-Cut Graph")

    plt.savefig(
        "results/figures/weighted_graph.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()
    print("Graph image saved successfully!")


def save_benchmark_chart(results):
    os.makedirs("results/figures", exist_ok=True)

    processors = [item["processor"] for item in results]
    depths = [item["circuit_depth"] for item in results]
    swaps = [item["swap_count"] for item in results]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    axes[0].bar(processors, depths)
    axes[0].set_title("Circuit Depth")
    axes[0].set_ylabel("Depth")

    axes[1].bar(processors, swaps)
    axes[1].set_title("SWAP Count")
    axes[1].set_ylabel("SWAP Gates")

    plt.tight_layout()
    plt.savefig(
        "results/figures/processor_comparison.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()
    print("Benchmark chart saved successfully!")