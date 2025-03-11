from typing import List
from puzzle.State import State

class Heuristic:
    """
    Abstract base class for heuristic functions.
    """
    def calculate(self, state: State, goal_states: List[State]) -> float:
        """
        Calculate the heuristic value for a given state.

        Args:
            state: Current state
            goal_states: List of goal states

        Returns:
            Heuristic value
        """
        raise NotImplementedError("Subclasses must implement this method")

    def is_admissible(self) -> str:
        """
        Explain why this heuristic is admissible.

        Returns:
            Explanation of admissibility
        """
        raise NotImplementedError("Subclasses must implement this method")

    def is_consistent(self) -> str:
        """
        Explain why this heuristic is consistent.

        Returns:
            Explanation of consistency
        """
        raise NotImplementedError("Subclasses must implement this method")
