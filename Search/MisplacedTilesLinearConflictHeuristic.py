from Heuristic import  Heuristic

class MisplacedTilesLinearConflictHeuristic(Heuristic):
    def calculate(self, state, goal_states):
        values = []
        for goal_state in goal_states:
            misplaced = self._calculate_misplaced_tiles(state, goal_state)
            conflicts = self.calculate_linear_conflicts(state, goal_state)
            values.append(misplaced + conflicts)

        return min(values) if values else 0

    def _calculate_misplaced_tiles(self, state, goal_state):
        misplaced = 0

        for row in range(3):
            for col in range(3):
                tile = state.board[row, col]
                if tile != 0:
                    goal_pos = goal_state.get_tile_position(tile)
                    if goal_pos and (row, col) != goal_pos:
                        misplaced += 1

        return misplaced

    def _calculate_linear_conflicts(self, state: State, goal_state: State) -> int:
        """Calculate linear conflicts."""
        conflicts = 0

        # Check rows
        for row in range(3):
            # Get tiles in this row (excluding blank)
            tiles_in_row = [state.board[row, col] for col in range(3) if state.board[row, col] != 0]

            # For each pair of tiles in the row
            for i, tile_i in enumerate(tiles_in_row):
                goal_i = goal_state.get_tile_position(tile_i)

                # Skip if this tile doesn't belong in this row in the goal state
                if not goal_i or goal_i[0] != row:
                    continue

                for j in range(i + 1, len(tiles_in_row)):
                    tile_j = tiles_in_row[j]
                    goal_j = goal_state.get_tile_position(tile_j)

                    # Skip if this tile doesn't belong in this row in the goal state
                    if not goal_j or goal_j[0] != row:
                        continue

                    # Find current column positions
                    col_i = state.get_tile_position(tile_i)[1]
                    col_j = state.get_tile_position(tile_j)[1]

                    # Find goal column positions
                    goal_col_i = goal_i[1]
                    goal_col_j = goal_j[1]

                    # Check for conflict (tiles are in reverse order)
                    if (col_i < col_j and goal_col_i > goal_col_j) or (col_i > col_j and goal_col_i < goal_col_j):
                        conflicts += 1

        # Check columns
        for col in range(3):
            # Get tiles in this column (excluding blank)
            tiles_in_col = [state.board[row, col] for row in range(3) if state.board[row, col] != 0]

            # For each pair of tiles in the column
            for i, tile_i in enumerate(tiles_in_col):
                goal_i = goal_state.get_tile_position(tile_i)

                # Skip if this tile doesn't belong in this column in the goal state
                if not goal_i or goal_i[1] != col:
                    continue

                for j in range(i + 1, len(tiles_in_col)):
                    tile_j = tiles_in_col[j]
                    goal_j = goal_state.get_tile_position(tile_j)

                    # Skip if this tile doesn't belong in this column in the goal state
                    if not goal_j or goal_j[1] != col:
                        continue

                    # Find current row positions
                    row_i = state.get_tile_position(tile_i)[0]
                    row_j = state.get_tile_position(tile_j)[0]

                    # Find goal row positions
                    goal_row_i = goal_i[0]
                    goal_row_j = goal_j[0]

                    # Check for conflict (tiles are in reverse order)
                    if (row_i < row_j and goal_row_i > goal_row_j) or (row_i > row_j and goal_row_i < goal_row_j):
                        conflicts += 1

        # Each conflict requires at least 2 moves to resolve
        return conflicts * 2

    def is_admissible(self) -> str:
        return "This heuristic is admissible because misplaced tiles never overestimates the cost, and linear conflicts adds a minimum penalty of 2 moves for each conflict, which is the minimum number of moves needed to resolve a conflict."

    def is_consistent(self) -> str:
        return "This heuristic is consistent because the change in heuristic value between adjacent states never exceeds the cost of the move. Adding linear conflicts maintains consistency as it respects the triangle inequality."
