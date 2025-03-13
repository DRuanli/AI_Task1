from abc import ABC, abstractmethod

class Heuristic(ABC):
    @abstractmethod
    def calculate(self, state, goal_states):
        pass

    def is_admissible(self):
        pass

    def is_consistent(self):
        pass
