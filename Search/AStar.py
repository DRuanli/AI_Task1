from Heuristic import Heuristic
from puzzle.Node import Node
import heapq


class AStar:
    def __init__(self, heuristic: Heuristic):
        self.heuristic = heuristic
        self.expanded_nodes = []
        self.nodes_expanded = 0
        self.max_frontier_size = 0

    def search(self, initial_state, goal_states, max_iterations = 1000):
        open_set = []
        closed_set = set()

        start_node = Node(
            state = initial_state,
            g=0,
            h = self.heuristic.calculate(initial_state,goal_states)
        )

        heapq.heappush(open_set, start_node)

        iterations = 0

        while open_set and iterations < max_iterations:
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
                # Skip if already explored
                if successor_state in closed_set:
                    continue

                # Create a new node
                g = current_node.g + 1  # Cost is 1 per move
                h = self.heuristic.calculate(successor_state, goal_states)
                successor_node = Node(
                    state=successor_state,
                    parent=current_node,
                    g=g,
                    h=h
                )

                # Check if already in open set with a better path
                existing_better = False
                for i, node in enumerate(open_set):
                    if node.state == successor_state and node.g <= g:
                        existing_better = True
                        break

                if not existing_better:
                    heapq.heappush(open_set, successor_node)

            iterations += 1

            # If no solution found
            return None, {
                "path_length": None,
                "nodes_expanded": self.nodes_expanded,
                "max_frontier_size": self.max_frontier_size
            }

