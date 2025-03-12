from Search.Heuristic import Heuristic
from puzzle.State import State
from typing import List

class ManhattanDistanceHeuristic(Heuristic):
    """
    Manhattan distance heuristic for the 8-puzzle.
    """
    def calculate(self, state: State, goal_states: List[State]) -> float:
        """
        Calculate the minimum Manhattan distance to any goal state.

        Args:
            state: Current state
            goal_states: List of goal states

        Returns:
            Minimum Manhattan distance to any goal state
        """
        min_distance = float('inf')

        for goal_state in goal_states:
            distance = self._calculate_for_single_goal(state, goal_state)
            min_distance = min(min_distance, distance)

        return min_distance

    def _calculate_for_single_goal(self, state: State, goal_state: State) -> float:
        """
        Calculate Manhattan distance to a single goal state.

        Args:
            state: Current state
            goal_state: Goal state

        Returns:
            Manhattan distance to the goal state
        """
        total_distance = 0

        for i in range(1, 9):  # For each tile (excluding blank)
            # Get positions in current state and goal state
            current_pos = state.get_tile_position(i)
            goal_pos = goal_state.get_tile_position(i)

            # If the tile is not found in either state, skip
            if current_pos == (-1, -1) or goal_pos == (-1, -1):
                continue

            # Calculate Manhattan distance for this tile
            distance = abs(current_pos[0] - goal_pos[0]) + abs(current_pos[1] - goal_pos[1])
            total_distance += distance

        return total_distance

    def is_admissible(self) -> str:
        """
        Explain why Manhattan distance heuristic is admissible.

        Returns:
            Explanation of admissibility
        """
        return (
            "The Manhattan distance heuristic is admissible because it represents the minimum "
            "number of moves required to move each tile from its current position to its goal "
            "position, assuming no restrictions on tile movements. Since each tile must move "
            "at least its Manhattan distance to reach its goal position, and each move can "
            "only reduce this distance by at most 1, the heuristic never overestimates the "
            "actual cost to reach the goal. Additionally, with our special swapping rule, "
            "the Manhattan distance still does not overestimate, because the swapping can "
            "only reduce the number of moves needed."
        )

    def is_consistent(self) -> str:
        """
        Explain why Manhattan distance heuristic is consistent.

        Returns:
            Explanation of consistency
        """
        return (
            "The Manhattan distance heuristic is consistent because for any state and its "
            "successor, the difference in heuristic values is at most the cost of the action "
            "(which is 1 for a single move). In other words, when we make a move, the Manhattan "
            "distance can decrease by at most 1, increase by at most 1, or stay the same. "
            "This satisfies the triangle inequality: h(n) <= c(n,n') + h(n') for any successor n' "
            "of n, where c(n,n') is the cost of the action. Even with our special swapping rule, "
            "consistency is maintained because the swapping can only decrease the total Manhattan "
            "distance or leave it unchanged."
        )