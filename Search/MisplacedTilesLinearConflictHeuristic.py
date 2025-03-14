from Heuristic import Heuristic
from puzzle.State import State

class MisplacedTilesLinearConflictHeuristic(Heuristic):
    def calculate(self, state, goal_states):
        values = []
        for goal_state in goal_states:
            misplaced = self._calculate_misplace_tiles(state, goal_state)
            conflicts = self._calculate_linear_conflicts(state, goal_state)
            values.append(misplaced + conflicts)

        return min(values) if values else 0

    def _calculate_misplace_tiles(self, state, goal_state):
        return sum(
            1 for row in range(3) for col in range(3)
            if (tile := state.board[row, col]) != 0 and goal_state.get_tile_position(tile) != (row, col)
        )

    def calculate_linear_conflicts(self, state: State, goal_state: State) -> int:
        """Calculate linear conflicts."""
        conflicts = 0

        # Check conflicts in rows and columns
        for axis in range(2):  # 0 for rows, 1 for columns
            for i in range(3):
                # Get tiles in this row/column (excluding blank)
                if axis == 0:  # rows
                    tiles = [(t, state.get_tile_position(t)[1]) for t in
                             [state.board[i, j] for j in range(3)] if t != 0]
                else:  # columns
                    tiles = [(t, state.get_tile_position(t)[0]) for t in
                             [state.board[j, i] for j in range(3)] if t != 0]

                # Check for conflicts between pairs
                for idx1, (tile1, pos1) in enumerate(tiles):
                    goal1 = goal_state.get_tile_position(tile1)
                    if not goal1 or goal1[axis] != i:
                        continue

                    for idx2 in range(idx1 + 1, len(tiles)):
                        tile2, pos2 = tiles[idx2]
                        goal2 = goal_state.get_tile_position(tile2)
                        if not goal2 or goal2[axis] != i:
                            continue

                        # Check if tiles are in reverse order
                        if (pos1 < pos2 and goal1[1 - axis] > goal2[1 - axis]) or \
                                (pos1 > pos2 and goal1[1 - axis] < goal2[1 - axis]):
                            conflicts += 1

        return conflicts * 2