from puzzle.State import State
from puzzle.Node import Node
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple, Optional
import networkx as nx

class SearchTreeVisualizer:
    def __init__(self, max_nodes: int = 50):
        self.max_nodes = max_nodes

    def _determine_move_direction(self, parent_state: State, child_state: State) -> str:
        """Determine the move direction between parent and child states."""
        # Get blank positions
        parent_blank = parent_state.get_blank_position()
        child_blank = child_state.get_blank_position()

        # Calculate the difference
        diff_row = parent_blank[0] - child_blank[0]
        diff_col = parent_blank[1] - child_blank[1]

        # Determine direction
        if diff_row == 1 and diff_col == 0:
            return "U"  # Tile moved up (blank moved down)
        elif diff_row == -1 and diff_col == 0:
            return "D"  # Tile moved down (blank moved up)
        elif diff_row == 0 and diff_col == 1:
            return "L"  # Tile moved left (blank moved right)
        elif diff_row == 0 and diff_col == -1:
            return "R"  # Tile moved right (blank moved left)
        else:
            return "?"  # Unknown direction (shouldn't happen)

    def _create_tree_layout(self, nodes: List[Node], n_nodes: int) -> Tuple[nx.DiGraph, Dict, Dict]:
        """Create a graph layout for the search tree."""
        G = nx.DiGraph()

        # Limit to n_nodes or all nodes if n_nodes is larger
        nodes = nodes[:min(n_nodes, len(nodes))]

        # Add nodes
        for i, node in enumerate(nodes):
            # Format state as a string representation
            state_str = ''.join([''.join(str(cell) if cell != 0 else '_' for cell in row) for row in node.state.board])
            state_str = state_str[:3] + '\n' + state_str[3:6] + '\n' + state_str[6:]
            G.add_node(i, state=node.state, f=node.f, g=node.g, h=node.h, state_str=state_str)

        # Add edges with direction labels
        edge_labels = {}
        for i, node in enumerate(nodes):
            if node.parent:
                try:
                    parent_idx = nodes.index(node.parent)
                    # Determine move direction
                    direction = self._determine_move_direction(node.parent.state, node.state)
                    G.add_edge(parent_idx, i)
                    edge_labels[(parent_idx, i)] = direction
                except ValueError:
                    # Parent node might not be in the list if we limited the nodes
                    pass

        # Use hierarchical layout
        try:
            # Try to use graphviz for hierarchical layout
            import pydot
            pos = nx.nx_pydot.graphviz_layout(G, prog='dot')
        except:
            # Fall back to regular layout if graphviz not available
            pos = nx.shell_layout(G)

        return G, pos, edge_labels

    def visualize(self, nodes: List[Node], solution_path: Optional[List[State]] = None, n_nodes: int = None) -> None:
        """
        Visualize the search tree.

        Args:
            nodes: List of expanded nodes
            solution_path: List of states in the solution path (optional)
            n_nodes: Number of nodes to display (uses all nodes if None)
        """
        if not nodes:
            print("No nodes to visualize")
            return

        # If n_nodes is not specified, use self.max_nodes
        if n_nodes is None:
            n_nodes = self.max_nodes

        # Create the tree layout
        G, pos, edge_labels = self._create_tree_layout(nodes, n_nodes)

        # Calculate how many nodes we're actually displaying
        num_nodes = len(G.nodes())

        # Adjust figure size based on the number of nodes
        # More nodes need a larger figure
        if num_nodes <= 10:
            figsize = (10, 8)
        elif num_nodes <= 25:
            figsize = (14, 10)
        elif num_nodes <= 50:
            figsize = (18, 14)
        else:
            figsize = (24, 18)

        # Create figure
        plt.figure(figsize=figsize)

        # Adjust node size based on number of nodes
        node_size = max(300, 1000 - num_nodes * 5)  # Decreases as number of nodes increases

        # Draw nodes (all in white)
        nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color='white', edgecolors='black')

        # Draw edges
        nx.draw_networkx_edges(G, pos, arrows=True, width=1.0)

        # Draw edge labels (directions)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=max(8, 12 - num_nodes // 10))

        # Draw node labels
        node_labels = {i: data['state_str'] for i, data in G.nodes(data=True)}
        nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=max(6, 10 - num_nodes // 15))

        plt.title(f"A* Search Tree (Showing first {num_nodes} expanded nodes)")
        plt.axis('off')
        plt.tight_layout()
        plt.show()

def print_solution_path(solution_path):
    """Print the step-by-step solution path from initial state to goal state."""
    if not solution_path or len(solution_path) <= 1:
        print("No solution path to display.")
        return

    print("\n===== SOLUTION PATH =====")
    print(f"Total Moves: {len(solution_path)-1}")

    # Print initial state
    print("\nInitial State:")
    print(solution_path[0])

    # Determine which goal state was reached
    reached_goal = solution_path[-1]

    # Print each step
    for i in range(1, len(solution_path)):
        current = solution_path[i]
        previous = solution_path[i-1]

        # Determine move direction
        prev_blank = previous.get_blank_position()
        curr_blank = current.get_blank_position()

        diff_row = prev_blank[0] - curr_blank[0]
        diff_col = prev_blank[1] - curr_blank[1]

        if diff_row == 1 and diff_col == 0:
            direction = "UP"
        elif diff_row == -1 and diff_col == 0:
            direction = "DOWN"
        elif diff_row == 0 and diff_col == 1:
            direction = "LEFT"
        elif diff_row == 0 and diff_col == -1:
            direction = "RIGHT"
        else:
            direction = "UNKNOWN"

        # Get the tile that moved
        if direction != "UNKNOWN":
            moved_tile = current.board[prev_blank]
        else:
            moved_tile = "?"

        print(f"\nMove {i}: Tile {moved_tile} moved {direction}")
        print(current)

    print("\nGoal State Reached!")
    return