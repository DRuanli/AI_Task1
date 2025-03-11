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

    def is_solvable(self, state: State) -> bool:
        """
        Check if a state is solvable (can reach at least one of the goal states).

        Note: This is a simplified approach based on inversion count parity.
        For the 8-puzzle with special rule, a more complex analysis might be needed.

        Args:
            state: The state to check

        Returns:
            True if the state is solvable, False otherwise
        """
        # Flatten the board excluding the blank space
        flat_board = state.board.flatten()

        # Count inversions for each goal state
        for goal_state in self.goal_states:
            flat_goal = goal_state.board.flatten()

            # Check parity of permutation between current state and goal state
            inversions = 0
            for i in range(9):
                if flat_board[i] == 0:
                    continue  # Skip blank space

                for j in range(i + 1, 9):
                    if flat_board[j] == 0:
                        continue  # Skip blank space

                    # Find positions in goal state
                    pos_i = np.where(flat_goal == flat_board[i])[0][0]
                    pos_j = np.where(flat_goal == flat_board[j])[0][0]

                    if pos_i > pos_j:
                        inversions += 1

            # For 3x3 puzzle, if blank is on even row (from bottom) and inversions is odd,
            # or if blank is on odd row and inversions is even, then it's solvable
            blank_row = 2 - state.blank_position[0]  # Row from bottom (0-indexed)

            if (blank_row % 2 == 0 and inversions % 2 == 1) or (blank_row % 2 == 1 and inversions % 2 == 0):
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