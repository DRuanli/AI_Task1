from Search.Heuristic import Heuristic

class ManhattanDistanceHeuristic(Heuristic):
    def calculate(self, state, goal_states):
        return min(self.calculate_for_single_goal(state, goal_state) for goal_state in goal_states)

    def calculate_for_single_goal(self, state, goal_state):
        total_distance = 0

        for i in range(1, 9):
            current_pos = state.get_title_position(i)
            goal_pos = goal_state.get_title_position(i)

            if current_pos and goal_pos:
                distance = abs(current_pos[0] - goal_pos[0]) + abs(current_pos[1] - goal_pos[1])
                total_distance += distance

        return total_distance

    def is_admissible(self):
        pass

    def is_consistent(self):
        pass