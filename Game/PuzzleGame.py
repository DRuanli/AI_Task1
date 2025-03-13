import numpy as np
import random
from puzzle.State import State

class PuzzleGame:
    def __init__(self, initial_state = None):
        self.initial_state = initial_state or self.generate_random_state()
        self.goal_states = self._create_goal_states()
        self.current_state = self.initial_state.copy()

    def _create_goal_states(self):
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

    def generate_random_state(self):
        numbers = list(range(9))
        random.shuffle(numbers)

        board = np.array(numbers).reshape(3,3)

        return State(board)

    def is_solvable(self, state):
        """Will define in the future"""

        pass

    def reset(self):
        self.current_state = self.initial_state.copy()

    def make_move(self, direction):
        new_state = self.current_state.make_move(direction)
        if new_state:
            self.current_state = new_state
            return True
        return False

    def is_solved(self):
        return self.current_state.is_goal(self.goal_states)

    def get_current_state(self):
        return self.current_state

    def get_inital_state(self):
        return self.initial_state

    def get_goal_states(self):
        return self.goal_states

