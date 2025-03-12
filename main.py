from Search.MisplacedTilesLinearConflictHeuristic import MisplacedTilesLinearConflictHeuristic
from Search.MahattanDistanceHeuristic import ManhattanDistanceHeuristic
from utils.ExperimentRunner import ExperimentRunner
from utils.SearchTreeVisualizer import SearchTreeVisualizer
from Search.AStar import AStar
from Game.PuzzleGame import PuzzleGame

def main():
    """
    Main function to demonstrate 8-puzzle solving with A* algorithm.
    """
    # Create a random puzzle
    game = PuzzleGame()
    initial_state = game.initial_state

    print("Initial State:")
    print(initial_state.board)
    print("\nGoal States:")
    for i, goal_state in enumerate(game.goal_states):
        print(f"Goal {i+1}:")
        print(goal_state.board)

    # Solve using Manhattan Distance heuristic
    print("\nSolving with Manhattan Distance heuristic...")
    manhattan_heuristic = ManhattanDistanceHeuristic()
    a_star_manhattan = AStar(manhattan_heuristic)

    path_manhattan, stats_manhattan = a_star_manhattan.search(initial_state, game.goal_states)

    if path_manhattan:
        print(f"Solution found in {stats_manhattan['path_length']} moves!")
        print(f"Nodes expanded: {stats_manhattan['nodes_expanded']}")
        print(f"Maximum frontier size: {stats_manhattan['max_frontier_size']}")
        print(f"Time taken: {stats_manhattan['time_taken']:.4f} seconds")
    else:
        print("No solution found.")

    # Solve using Misplaced Tiles + Linear Conflict heuristic
    print("\nSolving with Misplaced Tiles + Linear Conflict heuristic...")
    mtlc_heuristic = MisplacedTilesLinearConflictHeuristic()
    a_star_mtlc = AStar(mtlc_heuristic)

    path_mtlc, stats_mtlc = a_star_mtlc.search(initial_state, game.goal_states)

    if path_mtlc:
        print(f"Solution found in {stats_mtlc['path_length']} moves!")
        print(f"Nodes expanded: {stats_mtlc['nodes_expanded']}")
        print(f"Maximum frontier size: {stats_mtlc['max_frontier_size']}")
        print(f"Time taken: {stats_mtlc['time_taken']:.4f} seconds")
    else:
        print("No solution found.")

    # Visualize search tree
    print("\nVisualizing search tree...")
    visualizer = SearchTreeVisualizer(max_nodes=20)
    visualizer.visualize(a_star_manhattan.expanded_nodes, path_manhattan)

    # Run experiment
    print("\nWould you like to run an experiment comparing heuristics? (y/n)")
    #response = input()

    #if response.lower() == 'y':
    print("\nRunning experiment with 10 trials...")
    experimenter = ExperimentRunner(num_trials=10)
    experimenter.run_experiment()
    experimenter.visualize_results()

if __name__ == "__main__":
    main()