import numpy as np
from typing import List, Tuple, Optional


class State:
    def __init__(self, board: np.ndarray):
        self.board = board
        self.blank_position = self._find_blank_position()

    def _find_blank_position(self) -> Tuple[int, int]:
        """Find the position of the blank (0) in the board."""
        pos = np.where(self.board == 0)
        return (pos[0][0], pos[1][0])

    def copy(self) -> 'State':
        """Create a deep copy of the state."""
        return State(self.board.copy())

    def get_blank_position(self) -> Tuple[int, int]:
        """Return the position of the blank."""
        return self.blank_position

    def get_tile_position(self, tile: int) -> Optional[Tuple[int, int]]:
        """Find the position of a specific tile."""
        pos = np.where(self.board == tile)
        if len(pos[0]) == 0:
            return None
        return (pos[0][0], pos[1][0])

    def are_adjacent(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> bool:
        """Check if two positions are adjacent horizontally or vertically."""
        return (abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])) == 1

    def make_move(self, direction: str) -> Optional['State']:
        """Make a move in the specified direction."""
        directions = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1)
        }

        if direction not in directions:
            return None

        delta_row, delta_col = directions[direction]
        blank_row, blank_col = self.blank_position
        new_row, new_col = blank_row + delta_row, blank_col + delta_col

        # Check if the move is valid
        if new_row < 0 or new_row >= self.board.shape[0] or new_col < 0 or new_col >= self.board.shape[1]:
            return None

        # Create a new state
        new_state = self.copy()

        # Record which tile is moving
        moving_tile = new_state.board[new_row, new_col]

        # Move the tile to the blank position
        new_state.board[blank_row, blank_col] = moving_tile
        new_state.board[new_row, new_col] = 0
        new_state.blank_position = (new_row, new_col)

        # Apply special swap rule based on which tile moved
        new_state = new_state.apply_special_swap_rule(moving_tile)

        return new_state

    def apply_special_swap_rule(self, moved_tile: int) -> 'State':
        """Apply the special swap rules based on which tile moved."""
        # Check for tile 1 or 3 movement
        if moved_tile == 1 or moved_tile == 3:
            pos1 = self.get_tile_position(1)
            pos3 = self.get_tile_position(3)

            if pos1 and pos3 and self.are_adjacent(pos1, pos3):
                # Swap tiles 1 and 3
                self.board[pos1] = 3
                self.board[pos3] = 1

        # Check for tile 2 or 4 movement
        if moved_tile == 2 or moved_tile == 4:
            pos2 = self.get_tile_position(2)
            pos4 = self.get_tile_position(4)

            if pos2 and pos4 and self.are_adjacent(pos2, pos4):
                # Swap tiles 2 and 4
                self.board[pos2] = 4
                self.board[pos4] = 2

        return self

    def get_successors(self) -> List['State']:
        """Generate all possible successor states."""
        directions = ['up', 'down', 'left', 'right']
        successors = []

        for direction in directions:
            successor = self.make_move(direction)
            if successor:
                successors.append(successor)

        return successors

    def is_goal(self, goal_states: List['State']) -> bool:
        """Check if this state matches any of the goal states."""
        for goal_state in goal_states:
            if np.array_equal(self.board, goal_state.board):
                return True
        return False

    def __eq__(self, other):
        """Check if two states are equal."""
        if not isinstance(other, State):
            return False
        return np.array_equal(self.board, other.board)

    def __hash__(self):
        """Hash function for using states in sets or dictionaries."""
        return hash(self.board.tobytes())

    def __str__(self):
        """String representation of the state."""
        result = ""
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i, j] == 0:
                    result += "_ "
                else:
                    result += str(self.board[i, j]) + " "
            result += "\n"
        return result