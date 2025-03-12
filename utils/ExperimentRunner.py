from Search.MisplacedTilesLinearConflictHeuristic import MisplacedTilesLinearConflictHeuristic
from Search.MahattanDistanceHeuristic import ManhattanDistanceHeuristic
from typing import Dict, List
from Search.AStar import AStar
from Game.PuzzleGame import PuzzleGame
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

class ExperimentRunner:
    """
    Runs experiments to evaluate heuristic performance.
    """
    def __init__(self, num_trials: int = 100):
        """
        Initialize the experiment runner.

        Args:
            num_trials: Number of random initial states to generate
        """
        self.num_trials = num_trials
        self.heuristics = [
            ManhattanDistanceHeuristic(),
            MisplacedTilesLinearConflictHeuristic()
        ]
        self.results = {}

    def run_experiment(self, max_iterations: int = 10000) -> Dict:
        """
        Run experiments to compare heuristic performance.

        Args:
            max_iterations: Maximum number of iterations for each A* search

        Returns:
            Dictionary of results
        """
        # Initialize results
        self.results = {
            "Manhattan Distance": {
                "path_lengths": [],
                "nodes_expanded": [],
                "max_frontier_sizes": [],
                "times": [],
                "success_rate": 0
            },
            "Misplaced Tiles + Linear Conflict": {
                "path_lengths": [],
                "nodes_expanded": [],
                "max_frontier_sizes": [],
                "times": [],
                "success_rate": 0
            }
        }

        # Generate random initial states
        initial_states = []
        for _ in range(self.num_trials):
            game = PuzzleGame()
            initial_states.append(game.initial_state)

        goal_states = game.goal_states

        # Run A* with each heuristic on each initial state
        for heuristic_idx, heuristic in enumerate(self.heuristics):
            heuristic_name = "Manhattan Distance" if heuristic_idx == 0 else "Misplaced Tiles + Linear Conflict"

            successes = 0

            for state_idx, initial_state in enumerate(initial_states):
                print(f"Running trial {state_idx + 1}/{self.num_trials} with {heuristic_name}...")

                a_star = AStar(heuristic)
                path, stats = a_star.search(initial_state, goal_states, max_iterations)

                if path is not None:
                    successes += 1
                    self.results[heuristic_name]["path_lengths"].append(stats["path_length"])

                self.results[heuristic_name]["nodes_expanded"].append(stats["nodes_expanded"])
                self.results[heuristic_name]["max_frontier_sizes"].append(stats["max_frontier_size"])
                self.results[heuristic_name]["times"].append(stats["time_taken"])

            # Calculate success rate
            self.results[heuristic_name]["success_rate"] = successes / self.num_trials

        return self.results

    def visualize_results(self) -> None:
        """
        Visualize the experiment results.
        """
        if not self.results:
            print("No results to visualize. Run the experiment first.")
            return

        # Create figure with subplots
        fig = plt.figure(figsize=(15, 12))
        gs = gridspec.GridSpec(2, 2)

        # Plot path lengths
        ax1 = plt.subplot(gs[0, 0])
        self._plot_comparison(
            ax1,
            "Path Length",
            [r["path_lengths"] for r in self.results.values() if r["path_lengths"]],
            list(self.results.keys())
        )

        # Plot nodes expanded
        ax2 = plt.subplot(gs[0, 1])
        self._plot_comparison(
            ax2,
            "Nodes Expanded",
            [r["nodes_expanded"] for r in self.results.values()],
            list(self.results.keys()),
            log_scale=True
        )

        # Plot max frontier size
        ax3 = plt.subplot(gs[1, 0])
        self._plot_comparison(
            ax3,
            "Max Frontier Size",
            [r["max_frontier_sizes"] for r in self.results.values()],
            list(self.results.keys()),
            log_scale=True
        )

        # Plot time taken
        ax4 = plt.subplot(gs[1, 1])
        self._plot_comparison(
            ax4,
            "Time Taken (s)",
            [r["times"] for r in self.results.values()],
            list(self.results.keys()),
            log_scale=True
        )

        plt.tight_layout()
        plt.show()

        # Print success rates
        print("Success Rates:")
        for heuristic_name, results in self.results.items():
            print(f"{heuristic_name}: {results['success_rate'] * 100:.2f}%")

    def _plot_comparison(self, ax, title: str, data_lists: List[List[float]], labels: List[str], log_scale: bool = False) -> None:
        """
        Create a box plot comparing different heuristics.

        Args:
            ax: Matplotlib axis
            title: Plot title
            data_lists: List of data lists to compare
            labels: List of labels for each data list
            log_scale: Whether to use log scale for y-axis
        """
        ax.boxplot(data_lists, labels=labels)
        ax.set_title(title)

        if log_scale and all(all(x > 0 for x in data) for data in data_lists):
            ax.set_yscale('log')

        # Add mean values as text
        for i, data in enumerate(data_lists):
            if data:
                mean_val = np.mean(data)
                ax.text(i + 1, np.median(data), f"Mean: {mean_val:.2f}",
                       horizontalalignment='center', size=10, color='red')
