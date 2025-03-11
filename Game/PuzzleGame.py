import numpy as np
import random
from typing import Optional, List
from puzzle.State import State


class PuzzleGame:
    """
    Manages the 8-puzzle game logic and rules.
    """
    def __init__(self, initial_state: Optional[State] = None):
        """
        Initialize the puzzle game with an initial state.

        Args:
            initial_state: The starting state of the puzzle
        """
        # Create goal states first
        self.goal_states = self._create_goal_states()

        # Then generate or use provided initial state
        self.initial_state = initial_state or self.generate_random_state()
        self.current_state = self.initial_state.copy()

    def _create_goal_states(self) -> List[State]:
        """
        Create the four possible goal states as defined in the problem.

        Returns:
            List of the four goal states
        """
        # Goal state 1: [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        goal1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

        # Goal state 2: [[8, 7, 6], [5, 4, 3], [2, 1, 0]]
        goal2 = np.array([[8, 7, 6], [5, 4, 3], [2, 1, 0]])

        # Goal state 3: [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        goal3 = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])

        # Goal state 4: [[0, 8, 7], [6, 5, 4], [3, 2, 1]]
        goal4 = np.array([[0, 8, 7], [6, 5, 4], [3, 2, 1]])

        return [State(goal1), State(goal2), State(goal3), State(goal4)]

    def generate_random_state(self) -> State:
        """
        Generate a random solvable initial state.

        Returns:
            A random solvable state
        """
        # Create a random permutation of 0-8
        tiles = list(range(9))  # 0-8, where 0 represents the blank space
        random.shuffle(tiles)

        # Convert to 3x3 grid
        board = np.array(tiles).reshape(3, 3)

        # Ensure the state is solvable
        state = State(board)
        while not self.is_solvable(state):
            # If not solvable, swap two non-blank tiles
            positions = np.argwhere(board != 0)
            i, j = random.sample(range(len(positions)), 2)
            pos_i, pos_j = positions[i], positions[j]
            board[pos_i[0], pos_i[1]], board[pos_j[0], pos_j[1]] = board[pos_j[0], pos_j[1]], board[pos_i[0], pos_i[1]]
            state = State(board)

        return state

    def is_solvable(self, state) -> bool:
        """
        Check if the puzzle is solvable by analyzing inversions relative to goal states.

        With special swapping rules, we need to check solvability against each goal state.

        Args:
            state: Current puzzle state

        Returns:
            True if the puzzle is solvable, False otherwise
        """
        # Convert state to 1D array for inversion counting (exclude blank)
        state_1d = [num for num in state.board.flatten() if num != 0]

        # Check solvability against each goal state
        for goal in self.goal_states:
            # Convert goal to 1D array (exclude blank)
            goal_1d = [num for num in goal.flatten() if num != 0]

            # Count inversions in state relative to this goal
            inversions = 0
            for i in range(len(state_1d)):
                for j in range(i + 1, len(state_1d)):
                    # Find positions of these tiles in goal state
                    pos_i = goal_1d.index(state_1d[i])
                    pos_j = goal_1d.index(state_1d[j])

                    # If they're in opposite order in the goal, count an inversion
                    if pos_i > pos_j:
                        inversions += 1

            # Account for blank position parity
            blank_row_state = state.blank_pos[0]
            blank_row_goal = np.where(goal == 0)[0][0]
            row_parity_diff = (blank_row_state - blank_row_goal) % 2

            # Special rule: account for 1-3 and 2-4 swaps
            # These swaps can change parity, so we check both possibilities
            if inversions % 2 == row_parity_diff or (inversions + 1) % 2 == row_parity_diff:
                return True

        return False

    def reset(self) -> None:
        """Reset the game to the initial state."""
        self.current_state = self.initial_state.copy()

    def make_move(self, direction: str) -> bool:
        """
        Make a move in the specified direction.

        Args:
            direction: One of "up", "down", "left", "right"

        Returns:
            True if the move was successful, False otherwise
        """
        new_state = self.current_state.make_move(direction)
        if new_state is not None:
            self.current_state = new_state
            return True
        return False

    def is_solved(self) -> bool:
        """
        Check if the current state is a goal state.

        Returns:
            True if the current state is a goal state, False otherwise
        """
        return self.current_state.is_goal(self.goal_states)

    def get_current_state(self) -> State:
        """Get the current state of the puzzle."""
        return self.current_state

    def get_initial_state(self) -> State:
        """Get the initial state of the puzzle."""
        return self.initial_state

    def get_goal_states(self) -> List[State]:
        """Get the goal states of the puzzle."""
        return self.goal_states