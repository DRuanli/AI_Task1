from Search.Heuristic import Heuristic

class ManhattanDistanceHeuristic(Heuristic):
    def calculate(self, state, goal_states):
        return min(self._calculate_each_goal(state, goal_state) for goal_state in goal_states)

    def _calculate_each_goal(self, state, goal_state):
        return sum(
            abs(state.get_tile_position(i)[0] - goal_state.get_tile_position(i)[0]) +
            abs(state.get_tile_position(i)[1] - goal_state.get_tile_position(i)[1])
            for i in range(1, 9) if state.get_tile_position(i) and goal_state.get_tile_position(i)
        )