from puzzle.State import State
from typing import Optional, List


class Node:
    def __init__(self, state: State, parent: Optional['Node'] = None, g: int = 0, h: float = 0):
        self.state = state
        self.parent = parent
        self.g = g  # Cost from the start node to this node
        self.h = h  # Estimated cost from this node to the goal
        self.f = g + h  # Total estimated cost

    def __lt__(self, other):
        """Comparison function for priority queue."""
        return self.f < other.f

    def __eq__(self, other):
        """Check if two nodes are equal."""
        if not isinstance(other, Node):
            return False
        return self.state == other.state

    def __hash__(self):
        """Hash function for using nodes in sets or dictionaries."""
        return hash(self.state)

    def get_path(self) -> List[State]:
        """Get the path from the start node to this node."""
        path = []
        current = self
        while current:
            path.append(current.state)
            current = current.parent
        return list(reversed(path))