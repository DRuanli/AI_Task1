from Search.Heuristic import Heuristic

class MisplacedTilesLinearConflictHeuristic(Heuristic):
    def calculate(self, state, goal_states):
        return min(
            (self._calculate_misplaced_tiles(state, goal_state) +
             self._calculate_linear_conflicts(state, goal_state))
            for goal_state in goal_states
        )

    def _calculate_misplaced_tiles(self, state, goal_state):
        return sum(
            1 for row in range(3) for col in range(3)
            if( (tile:=state.board[row, col]) != 0 and
                goal_state.get_tile_position(tile) != (row, col))
        )

    def _calculate_linear_conflicts(self, state, goal_state):
        conflict = 0

        for axis in range(2):
            for i in range(3):
                if axis == 0:
                    tiles = [state.board[i, j] for j in range(3)
                             if state.board[i, j] != 0]
                else:
                    tiles = [state.board[j, i] for j in range(3)
                             if state.board[j, i] != 0]

                for a, tile_a in enumerate(tiles):
                    goal_a = goal_state.get_tile_position(tile_a)
                    if not goal_a or goal_a[axis] != i:
                        continue

                    for b in range(a + 1, len(tiles)):
                        tile_b = tiles[b]
                        goal_b = goal_state.get_tile_position(tile_b)
                        if not goal_b or goal_b[axis] != i:
                            continue

                        pos_a = state.get_tile_postion(tile_a)[1 - axis]
                        pos_b = state.get_tile_postion(tile_b)[1 - axis]
                        goal_pos_a = goal_a[1 - axis]
                        goal_pos_b = goal_a[1 - axis]

                        if (pos_a < pos_b and goal_pos_a > goal_pos_b) or (pos_a > pos_b and goal_pos_a < goal_pos_b):
                            conflict += 1
        return conflict*2
