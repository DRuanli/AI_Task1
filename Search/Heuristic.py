from abc import ABC, abstractmethod

@abstractmethod
class Heuristic(ABC):
    def calculate(self, state, goal_states):
        pass
