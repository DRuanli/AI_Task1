from typing import List, Tuple, Optional, Dict
from puzzle.State import State

class Node:
    """
    Node in the search tree for the A* algorithm.
    """
    def __init__(self, state: State, parent: Optional['Node'] = None, g: int = 0, h: float = 0):
        """
        Initialize a node in the search tree.

        Args:
            state: The state represented by this node
            parent: Parent node
            g: Cost from initial state to this node
            h: Heuristic value (estimated cost to goal)
        """
        self.state = state
        self.parent = parent
        self.g = g  # Cost from initial state to this node
        self.h = h  # Heuristic value
        self.f = g + h  # Total estimated cost

    def __lt__(self, other) -> bool:
        """Compare nodes for priority queue ordering."""
        if not isinstance(other, Node):
            return NotImplemented

        # Primary sort by f value
        if self.f != other.f:
            return self.f < other.f

        # Secondary sort by h value (prefer nodes with lower heuristic)
        return self.h < other.h

    def __eq__(self, other) -> bool:
        """Check if two nodes are equal."""
        if not isinstance(other, Node):
            return False
        return self.state == other.state and self.f == other.f

    def __hash__(self) -> int:
        """Hash function for node to use in dictionaries and sets."""
        return hash((hash(self.state), self.f))

    def get_path(self) -> List[State]:
        """
        Get the path from the initial state to this node.

        Returns:
            List of states from initial state to this node
        """
        path = []
        current = self

        while current is not None:
            path.append(current.state)
            current = current.parent

        path.reverse()  # Reverse to get path from initial to current

        return path