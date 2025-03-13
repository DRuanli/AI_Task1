import numpy as np


class State:
    def __init__(self, board):
        self.board = board
        self.blank_position = self._find_blank_position()

    def _find_blank_position(self):
        pos = np.where((self.board==0))
        return (pos[0][0],pos[1][0])

    def copy(self):
        return State(self.board.copy())

    def get_blank_position(self):
        return self.blank_position

    def get_title_position(self, tile):
        pos = np.where(self.board==tile)
        if len(pos[0]) == 0:
            return None
        return (pos[0][0], pos[0][1])

    def are_adjacent(self, pos1, pos2):
        return (abs(pos1[0] - pos2[0]) + abs(pos1[1]-pos2[1])) == 1

    def make_move(self,direction):
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

        if new_row < 0 or new_row >= self.board.shape[0] or new_col < 0 or new_col >= self.board.shape[1]:
            return None

        new_state = self.copy()

        moving_tile = new_state.board[new_row, new_col]

        new_state.board[blank_row,blank_col] = moving_tile
        new_state.board[new_row, new_col] = 0
        new_state.blank_position = (new_row, new_col)

        new_state = new_state.apply_special_swap_rule(moving_tile)

        return new_state


    def apply_special_swap_rule(self, moved_tile):
        if moved_tile == 1 or moved_tile == 3:
            pos1 = self.get_title_position(1)
            pos3 = self.get_title_position(3)

            if pos1 and pos3 and self.are_adjacent(pos1, pos3):
                self.board[pos1] = 3
                self.board[pos3] = 1

        if moved_tile == 2 or moved_tile == 4:
            pos2 = self.get_title_position(2)
            pos4 = self.get_title_position(4)

            if pos2 and pos4 and self.are_adjacent(pos2, pos4):
                self.board[pos2] = 4
                self.board[pos4] = 2

        return self


    def get_successors(self):
        directions = ['up', 'down', 'right', 'left']
        successors = []

        for direction in directions:
            successor = self.make_move(direction)
            if successors:
                successors.append(successor)

        return successors

    def is_goal(self, goal_states):
        for goal_state in goal_states:
            if np.array_equal(self.board, goal_state.board):
                return True
        return False

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return np.array_equal(self.board, other.board)

    def __hash__(self):
        return hash(self.board.tobytes())

    def __str__(self):
        result = ""
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i,j] == 0:
                    result += "_"
                else:
                    result += str(self.board[i,j]) + " "
            result += '\n'

        return result