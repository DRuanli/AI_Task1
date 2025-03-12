from typing import List, Tuple, Optional, Dict
from Search.Node import Node
from puzzle.State import State
import networkx as nx
import matplotlib.pyplot as plt


class SearchTreeVisualizer:
    """
    Visualizes the search tree generated by the A* algorithm.
    """
    def __init__(self, max_nodes: int = 500):
        """
        Initialize the search tree visualizer.

        Args:
            max_nodes: Maximum number of nodes to display
        """
        self.max_nodes = max_nodes

    def _create_tree_layout(self, nodes: List[Node]) -> Tuple[nx.DiGraph, Dict]:
        """
        Create a graph representation of the search tree.

        Args:
            nodes: List of nodes expanded during search

        Returns:
            Tuple of (graph, node positions)
        """
        G = nx.DiGraph()

        # Add nodes to the graph
        for i, node in enumerate(nodes):
            # Add node
            G.add_node(i, state=node.state, f=node.f, g=node.g, h=node.h)

            # Find parent index
            if node.parent is not None:
                for j, potential_parent in enumerate(nodes):
                    if node.parent.state == potential_parent.state:
                        G.add_edge(j, i)
                        break

        # Use hierarchical layout
        pos = nx.nx_agraph.graphviz_layout(G, prog="dot")

        return G, pos

    def visualize(self, nodes: List[Node], solution_path: Optional[List[State]] = None) -> None:
        """
        Visualize the search tree.

        Args:
            nodes: List of nodes expanded during search
            solution_path: Solution path if found
        """
        # Limit number of nodes for visualization
        nodes = nodes[:self.max_nodes]

        # Create graph layout
        G, pos = self._create_tree_layout(nodes)

        # Create figure
        plt.figure(figsize=(15, 10))

        # Draw nodes
        node_colors = []
        for i in range(len(nodes)):
            if solution_path and any(nodes[i].state == s for s in solution_path):
                node_colors.append('lightgreen')  # Highlight solution path
            else:
                node_colors.append('lightblue')

        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=3000, alpha=0.8)

        # Draw edges
        nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, arrows=True, arrowsize=20)

        # Draw node state representations
        for i, (p, node) in enumerate(zip(pos.values(), [nodes[i] for i in G.nodes()])):
            plt.text(p[0], p[1] + 40, f"f={node.f}, g={node.g}, h={node.h}",
                    horizontalalignment='center', size=10)

            # Draw state representation
            self._draw_state_in_node(p[0], p[1], node.state)

        plt.axis('off')
        plt.title(f"A* Search Tree (showing {len(nodes)} of {len(nodes)} nodes)")
        plt.tight_layout()
        plt.show()

    def _draw_state_in_node(self, x: float, y: float, state: State) -> None:
        """
        Draw a puzzle state inside a node in the visualization.

        Args:
            x: X-coordinate of the node center
            y: Y-coordinate of the node center
            state: Puzzle state to draw
        """
        cell_size = 10
        offset_x = x - cell_size * 1.5
        offset_y = y - cell_size * 1.5

        for row in range(3):
            for col in range(3):
                # Draw cell
                rect = plt.Rectangle(
                    (offset_x + col * cell_size, offset_y + row * cell_size),
                    cell_size, cell_size,
                    fill=True, color='white', edgecolor='black', alpha=0.9
                )
                plt.gca().add_patch(rect)

                # Draw tile number (skip for blank)
                if state.board[row, col] != 0:
                    plt.text(
                        offset_x + col * cell_size + cell_size/2,
                        offset_y + row * cell_size + cell_size/2,
                        str(state.board[row, col]),
                        horizontalalignment='center',
                        verticalalignment='center',
                        size=8
                    )