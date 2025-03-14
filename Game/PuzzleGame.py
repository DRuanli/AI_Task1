from puzzle.State import State
from typing import Optional, List
import random
import numpy as np


class PuzzleGame:
    def __init__(self, initial_state: Optional[State] = None):
        # Define the four goal states
        self.goal_states = self._create_goal_states()
        self.initial_state = initial_state or self.generate_random_state()
        self.current_state = self.initial_state.copy()

    def _create_goal_states(self) -> List[State]:
        """Create the four possible goal states."""
        # Goal state 1: Standard order
        goal1 = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ])

        # Goal state 2: Reverse order
        goal2 = np.array([
            [8, 7, 6],
            [5, 4, 3],
            [2, 1, 0]
        ])

        # Goal state 3: Spiral pattern
        goal3 = np.array([
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8]
        ])

        # Goal state 4: Reverse spiral pattern
        goal4 = np.array([
            [0, 8, 7],
            [6, 5, 4],
            [3, 2, 1]
        ])

        return [State(goal1), State(goal2), State(goal3), State(goal4)]

    def generate_random_state(self) -> State:
        """Generate a random initial state."""
        # Create a random permutation of numbers 0-8
        numbers = list(range(9))
        random.shuffle(numbers)

        # Convert to 3x3 board
        board = np.array(numbers).reshape(3, 3)

        return State(board)

    def is_solvable(self, state: State) -> bool:
        """Check if the puzzle is solvable."""
        # Flatten the board
        flat_board = state.board.flatten()

        # Count inversions
        inversions = 0
        for i in range(len(flat_board)):
            if flat_board[i] == 0:
                continue
            for j in range(i + 1, len(flat_board)):
                if flat_board[j] == 0:
                    continue
                if flat_board[i] > flat_board[j]:
                    inversions += 1

        # Get blank position's row from bottom (0-indexed)
        blank_row = 2 - state.blank_position[0]

        # For a 3x3 puzzle:
        # - If blank is on an even row from bottom, puzzle is solvable if inversions is odd
        # - If blank is on an odd row from bottom, puzzle is solvable if inversions is even
        if blank_row % 2 == 0:
            return inversions % 2 == 1
        else:
            return inversions % 2 == 0

    def reset(self) -> None:
        """Reset the game to the initial state."""
        self.current_state = self.initial_state.copy()

    def make_move(self, direction: str) -> bool:
        """Make a move in the current state."""
        new_state = self.current_state.make_move(direction)
        if new_state:
            self.current_state = new_state
            return True
        return False

    def is_solved(self) -> bool:
        """Check if the current state is a goal state."""
        return self.current_state.is_goal(self.goal_states)

    def get_current_state(self) -> State:
        """Get the current state."""
        return self.current_state

    def get_initial_state(self) -> State:
        """Get the initial state."""
        return self.initial_state

    def get_goal_states(self) -> List[State]:
        """Get the goal states."""
        return self.goal_states