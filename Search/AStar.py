from Search.Heuristic import Heuristic
from typing import List, Tuple, Optional, Dict
from Search.Node import Node
from puzzle.State import State
import time
import heapq


class AStar:
    """
    A* search algorithm for the 8-puzzle.
    """
    def __init__(self, heuristic: Heuristic):
        """
        Initialize the A* search algorithm.

        Args:
            heuristic: Heuristic function to use
        """
        self.heuristic = heuristic
        self.expanded_nodes = []  # For visualization
        self.nodes_expanded = 0  # Counter for nodes expanded
        self.max_frontier_size = 0  # Maximum size of the frontier

    def search(self, initial_state: State, goal_states: List[State], max_iterations: int = 100000) -> Tuple[Optional[List[State]], Dict]:
        """
        Perform A* search from initial state to any goal state.

        Args:
            initial_state: Starting state
            goal_states: List of goal states
            max_iterations: Maximum number of iterations to prevent infinite loops

        Returns:
            Tuple of (path to goal if found, or None if no path found, search statistics)
        """
        # Calculate initial heuristic value
        initial_h = self.heuristic.calculate(initial_state, goal_states)

        # Create initial node
        initial_node = Node(initial_state, None, 0, initial_h)

        # Initialize open and closed sets
        open_set = []  # Priority queue
        heapq.heappush(open_set, initial_node)
        open_dict = {hash(initial_state): initial_node}  # For O(1) lookups in open set

        closed_set = set()  # Set of visited states

        # Initialize statistics
        self.expanded_nodes = [initial_node]
        self.nodes_expanded = 0
        self.max_frontier_size = 1
        start_time = time.time()

        iterations = 0

        while open_set and iterations < max_iterations:
            iterations += 1

            # Get node with lowest f value
            current_node = heapq.heappop(open_set)
            open_dict.pop(hash(current_node.state))

            # Check if goal state reached
            if current_node.state.is_goal(goal_states):
                end_time = time.time()

                # Collect search statistics
                stats = {
                    "path_length": len(current_node.get_path()) - 1,  # Number of moves
                    "nodes_expanded": self.nodes_expanded,
                    "max_frontier_size": self.max_frontier_size,
                    "time_taken": end_time - start_time
                }

                return current_node.get_path(), stats

            # Add current state to closed set
            closed_set.add(hash(current_node.state))

            # Expand current node
            self.nodes_expanded += 1

            for successor_state in current_node.state.get_successors():
                # Skip if successor is already in closed set
                if hash(successor_state) in closed_set:
                    continue

                # Calculate new g value
                new_g = current_node.g + 1

                # Calculate heuristic for successor
                new_h = self.heuristic.calculate(successor_state, goal_states)

                # Create successor node
                successor_node = Node(successor_state, current_node, new_g, new_h)

                # Check if successor is in open set
                if hash(successor_state) in open_dict:
                    existing_node = open_dict[hash(successor_state)]

                    # If new path is better, update the node
                    if new_g < existing_node.g:
                        existing_node.parent = current_node
                        existing_node.g = new_g
                        existing_node.f = new_g + existing_node.h

                        # Reorder the priority queue (heapify)
                        heapq.heapify(open_set)
                else:
                    # Add to open set
                    heapq.heappush(open_set, successor_node)
                    open_dict[hash(successor_state)] = successor_node

                    # Update maximum frontier size
                    self.max_frontier_size = max(self.max_frontier_size, len(open_set))

                    # Add to expanded nodes list for visualization
                    if len(self.expanded_nodes) < 1000:  # Limit for performance
                        self.expanded_nodes.append(successor_node)

        # If no path found
        end_time = time.time()
        stats = {
            "path_length": None,
            "nodes_expanded": self.nodes_expanded,
            "max_frontier_size": self.max_frontier_size,
            "time_taken": end_time - start_time
        }

        return None, stats