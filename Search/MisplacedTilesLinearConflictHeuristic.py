from Heuristic import Heuristic
from puzzle.State import State
from typing import List

class MisplacedTilesLinearConflictHeuristic(Heuristic):
    """
    Misplaced tiles plus linear conflict heuristic for the 8-puzzle.
    """
    def calculate(self, state: State, goal_states: List[State]) -> float:
        """
        Calculate the minimum heuristic value across all goal states.

        Args:
            state: Current state
            goal_states: List of goal states

        Returns:
            Minimum heuristic value
        """
        min_heuristic = float('inf')

        for goal_state in goal_states:
            # Calculate misplaced tiles
            misplaced = self._calculate_misplaced_tiles(state, goal_state)

            # Calculate linear conflicts
            conflicts = self._calculate_linear_conflicts(state, goal_state)

            # Each linear conflict requires at least 2 additional moves
            heuristic = misplaced + 2 * conflicts

            min_heuristic = min(min_heuristic, heuristic)

        return min_heuristic

    def _calculate_misplaced_tiles(self, state: State, goal_state: State) -> int:
        """
        Count the number of misplaced tiles.

        Args:
            state: Current state
            goal_state: Goal state

        Returns:
            Number of misplaced tiles
        """
        count = 0

        for i in range(1, 9):  # For each tile (excluding blank)
            current_pos = state.get_tile_position(i)
            goal_pos = goal_state.get_tile_position(i)

            # If positions are different, the tile is misplaced
            if current_pos != goal_pos:
                count += 1

        return count

    def _calculate_linear_conflicts(self, state: State, goal_state: State) -> int:
        """
        Count the number of linear conflicts.

        A linear conflict occurs when two tiles are in their goal row/column
        but are in reverse order relative to their goal positions.

        Args:
            state: Current state
            goal_state: Goal state

        Returns:
            Number of linear conflicts
        """
        conflicts = 0

        # Check rows for conflicts
        for row in range(3):
            # Get tiles in this row in current state
            tiles_in_row = [state.board[row, col] for col in range(3) if state.board[row, col] != 0]

            # Check if each tile has its goal position in this row
            for i, tile_i in enumerate(tiles_in_row):
                goal_pos_i = goal_state.get_tile_position(tile_i)

                # If this tile's goal position is not in this row, skip
                if goal_pos_i[0] != row:
                    continue

                # Check for conflict with other tiles in this row
                for j in range(i + 1, len(tiles_in_row)):
                    tile_j = tiles_in_row[j]
                    goal_pos_j = goal_state.get_tile_position(tile_j)

                    # If the other tile also has its goal position in this row
                    if goal_pos_j[0] == row:
                        # Check if they are in reverse order
                        if goal_pos_i[1] > goal_pos_j[1]:
                            conflicts += 1

        # Check columns for conflicts
        for col in range(3):
            # Get tiles in this column in current state
            tiles_in_col = [state.board[row, col] for row in range(3) if state.board[row, col] != 0]

            # Check if each tile has its goal position in this column
            for i, tile_i in enumerate(tiles_in_col):
                goal_pos_i = goal_state.get_tile_position(tile_i)

                # If this tile's goal position is not in this column, skip
                if goal_pos_i[1] != col:
                    continue

                # Check for conflict with other tiles in this column
                for j in range(i + 1, len(tiles_in_col)):
                    tile_j = tiles_in_col[j]
                    goal_pos_j = goal_state.get_tile_position(tile_j)

                    # If the other tile also has its goal position in this column
                    if goal_pos_j[1] == col:
                        # Check if they are in reverse order
                        if goal_pos_i[0] > goal_pos_j[0]:
                            conflicts += 1

        return conflicts

    def is_admissible(self) -> str:
        """
        Explain why misplaced tiles + linear conflict heuristic is admissible.

        Returns:
            Explanation of admissibility
        """
        return (
            "The misplaced tiles + linear conflict heuristic is admissible because:\n"
            "1. Each misplaced tile requires at least one move to reach its goal position.\n"
            "2. Each linear conflict requires at least two additional moves beyond the Manhattan "
            "distance. This is because tiles in linear conflict must 'move around each other', "
            "which requires additional moves.\n"
            "Since both components never overestimate the actual cost to reach the goal, their "
            "sum is also admissible. Even with the special swapping rule, this heuristic remains "
            "admissible because the swapping can only reduce the number of moves needed to reach "
            "the goal state."
        )

    def is_consistent(self) -> str:
        """
        Explain why misplaced tiles + linear conflict heuristic is consistent.

        Returns:
            Explanation of consistency
        """
        return (
            "The misplaced tiles + linear conflict heuristic is consistent because:\n"
            "1. For misplaced tiles, a single move can at most place one tile correctly or "
            "misplace one correct tile. Therefore, the difference in misplaced tiles between "
            "a state and its successor is at most 1.\n"
            "2. For linear conflicts, a single move can at most resolve one conflict or create "
            "one new conflict. Since each conflict contributes 2 to the heuristic, the difference "
            "in the heuristic value due to linear conflicts is at most 2.\n"
            "However, when a move resolves a linear conflict, it must either keep the same number "
            "of misplaced tiles or increase it by 1. Similarly, when a move creates a linear "
            "conflict, it must either keep the same number of misplaced tiles or decrease it by 1.\n"
            "Therefore, the total change in the heuristic value between a state and its successor "
            "is at most the cost of the action (which is 1). This satisfies the triangle inequality: "
            "h(n) <= c(n,n') + h(n') for any successor n' of n, where c(n,n') is the cost of the action."
        )
