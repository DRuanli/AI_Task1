def print_solution_path(solution_path):
    """Print the step-by-step solution path from initial state to goal state."""
    if not solution_path or len(solution_path) <= 1:
        print("No solution path to display.")
        return

    print("\n===== SOLUTION PATH =====")
    print(f"Total Moves: {len(solution_path)-1}")

    # Print initial state
    print("\nInitial State:")
    print(solution_path[0])

    # Determine which goal state was reached
    reached_goal = solution_path[-1]

    # Print each step
    for i in range(1, len(solution_path)):
        current = solution_path[i]
        previous = solution_path[i-1]

        # Determine move direction
        prev_blank = previous.get_blank_position()
        curr_blank = current.get_blank_position()

        diff_row = prev_blank[0] - curr_blank[0]
        diff_col = prev_blank[1] - curr_blank[1]

        if diff_row == 1 and diff_col == 0:
            direction = "UP"
        elif diff_row == -1 and diff_col == 0:
            direction = "DOWN"
        elif diff_row == 0 and diff_col == 1:
            direction = "LEFT"
        elif diff_row == 0 and diff_col == -1:
            direction = "RIGHT"
        else:
            direction = "UNKNOWN"

        # Get the tile that moved
        if direction != "UNKNOWN":
            moved_tile = current.board[prev_blank]
        else:
            moved_tile = "?"

        print(f"\nMove {i}: Tile {moved_tile} moved {direction}")
        print(current)

    print("\nGoal State Reached!")
    return