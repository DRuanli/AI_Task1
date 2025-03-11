import numpy as np
from typing import Tuple, List, Optional


class State:
    """
    Represents a state in the 8-puzzle game.
    """
    def __init__(self, board: np.ndarray):
        """
        Initialize a puzzle state.

        Args:
            board: 3x3 numpy array representing the puzzle state (0 represents the blank space)
        """
        self.board = board
        self.blank_position = tuple(np.argwhere(self.board == 0)[0])

    def __eq__(self, other) -> bool:
        """Check if two states are equal."""
        if not isinstance(other, State):
            return False
        return np.array_equal(self.board, other.board)

    def __hash__(self) -> int:
        """Hash function for state to use in dictionaries and sets."""
        return hash(self.board.tobytes())

    def __str__(self) -> str:
        """String representation of the state."""
        return str(self.board)

    def copy(self) -> 'State':
        """Create a deep copy of the state."""
        return State(self.board.copy())

    def get_blank_position(self) -> Tuple[int, int]:
        """Get position of the blank space."""
        return self.blank_position

    def make_move(self, direction: str) -> Optional['State']:
        """
        Make a move in the specified direction and apply the special swapping rule.

        Args:
            direction: One of "up", "down", "left", "right"

        Returns:
            A new state after making the move, or None if the move is invalid
        """
        row, col = self.blank_position

        # Calculate new position based on direction
        if direction == "up" and row > 0:
            new_row, new_col = row - 1, col
        elif direction == "down" and row < 2:
            new_row, new_col = row + 1, col
        elif direction == "left" and col > 0:
            new_row, new_col = row, col - 1
        elif direction == "right" and col < 2:
            new_row, new_col = row, col + 1
        else:
            # Invalid move
            return None

        # Create a new state
        new_board = self.board.copy()
        # Move the tile to the blank position
        new_board[row, col] = new_board[new_row, new_col]
        # Update blank position
        new_board[new_row, new_col] = 0

        new_state = State(new_board)
        # Apply special swapping rule
        return new_state.apply_special_swap_rule()

    def apply_special_swap_rule(self) -> 'State':
        """
        Apply the special rule: If tiles 1 and 3 or 2 and 4 are adjacent,
        they are automatically swapped.

        Returns:
            A new state after applying the special swapping rule
        """
        # Check for adjacent tiles 1 and 3
        positions_1 = np.argwhere(self.board == 1)
        positions_3 = np.argwhere(self.board == 3)

        if len(positions_1) > 0 and len(positions_3) > 0:
            pos_1 = tuple(positions_1[0])
            pos_3 = tuple(positions_3[0])

            # Check if positions are adjacent (horizontally or vertically)
            if self._are_adjacent(pos_1, pos_3):
                new_board = self.board.copy()
                new_board[pos_1] = 3
                new_board[pos_3] = 1
                return State(new_board)

        # Check for adjacent tiles 2 and 4
        positions_2 = np.argwhere(self.board == 2)
        positions_4 = np.argwhere(self.board == 4)

        if len(positions_2) > 0 and len(positions_4) > 0:
            pos_2 = tuple(positions_2[0])
            pos_4 = tuple(positions_4[0])

            # Check if positions are adjacent (horizontally or vertically)
            if self._are_adjacent(pos_2, pos_4):
                new_board = self.board.copy()
                new_board[pos_2] = 4
                new_board[pos_4] = 2
                return State(new_board)

        # If no swapping occurred, return the original state
        return self

    def _are_adjacent(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> bool:
        """
        Check if two positions are adjacent horizontally or vertically.

        Args:
            pos1: First position as (row, col)
            pos2: Second position as (row, col)

        Returns:
            True if positions are adjacent, False otherwise
        """
        row1, col1 = pos1
        row2, col2 = pos2

        # Check horizontal adjacency
        if row1 == row2 and abs(col1 - col2) == 1:
            return True

        # Check vertical adjacency
        if col1 == col2 and abs(row1 - row2) == 1:
            return True

        return False

    def get_successors(self) -> List['State']:
        """
        Generate all possible successor states.

        Returns:
            List of all valid successor states
        """
        successors = []

        for direction in ["up", "down", "left", "right"]:
            successor = self.make_move(direction)
            if successor is not None:
                successors.append(successor)

        return successors

    def is_goal(self, goal_states: List['State']) -> bool:
        """
        Check if the current state is a goal state.

        Args:
            goal_states: List of goal states

        Returns:
            True if the current state matches any goal state, False otherwise
        """
        return any(self == goal_state for goal_state in goal_states)

    def get_tile_position(self, tile: int) -> Tuple[int, int]:
        """
        Get the position of a specific tile.

        Args:
            tile: The tile number to find

        Returns:
            Position as (row, col)
        """
        positions = np.argwhere(self.board == tile)
        if len(positions) == 0:
            return (-1, -1)  # Tile not found
        return tuple(positions[0])
