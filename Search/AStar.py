from Search.Heuristic import Heuristic
from puzzle.Node import Node
import heapq


class AStar:
    def __init__(self, heuristic: Heuristic):
        self.heuristic = heuristic
        self.expanded_nodes = []
        self.nodes_expanded = 0
        self.max_frontier_size = 0

    def search(self, initial_state, goal_states, max_iterations=1000):
        open_set = []
        closed_set = set()

        heapq.heappush(open_set, Node(
            state=initial_state,
            g=0,
            h=self.heuristic.calculate(initial_state, goal_states)
        ))

        for _ in range(max_iterations):
            if not open_set:
                break

            self.max_frontier_size = max(self.max_frontier_size, len(open_set))
            current_node = heapq.heappop(open_set)
            self.expanded_nodes.append(current_node)

            if current_node.state.is_goal(goal_states):
                return current_node.get_path(), {
                    "path_length": current_node.g,
                    "nodes_expanded": self.nodes_expanded,
                    "max_frontier_size": self.max_frontier_size
                }

            closed_set.add(current_node.state)
            self.nodes_expanded += 1

            for successor_state in current_node.state.get_successors():
                if successor_state in closed_set:
                    continue

                g = current_node.g + 1
                successor_node = Node(
                    state=successor_state,
                    parent=current_node,
                    g=g,
                    h=self.heuristic.calculate(successor_state, goal_states)
                )

                if not any(node.state == successor_state and node.g <= g for node in open_set):
                    heapq.heappush(open_set, successor_node)

        return None, {
            "path_length": None,
            "nodes_expanded": self.nodes_expanded,
            "max_frontier_size": self.max_frontier_size
        }