import numpy as np
from puzzle.State import State


class PuzzleGame:
    """
    Manage the game play logics and rules
    """

    def __init__(self, initial_state):
        self.goal_states = self._create_goal_states()

        self.initial_state = initial_state or self.generate_random_state
        self.current_state = self.initial_state.copy()

    def _create_goal_states(self):
        # Goal state 1: [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        goal1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

        # Goal state 2: [[8, 7, 6], [5, 4, 3], [2, 1, 0]]
        goal2 = np.array([[8, 7, 6], [5, 4, 3], [2, 1, 0]])

        # Goal state 3: [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        goal3 = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])

        # Goal state 4: [[0, 8, 7], [6, 5, 4], [3, 2, 1]]
        goal4 = np.array([[0, 8, 7], [6, 5, 4], [3, 2, 1]])

        return [State(goal1), State(goal2), State(goal3), State(goal4)]

