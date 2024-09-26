from abc import abstractmethod


class Piece:
    def __init__(self, curr_pos, color):
        self.curr_pos = curr_pos
        self.color = color

    @abstractmethod
    def allowed_movements(self, board):
        pass

class Queen(Piece):
    def allowed_movements(self, board):
        adjacent_spaces = board.get_adjacent_spaces(self.curr_pos)
        valid_moves = []
        for space in adjacent_spaces:
            if (board.is_empty(space) and
                board.has_adjacent_piece(space) and
                not board.breaks_hive(self.curr_pos, space)):
                valid_moves.append(space)
        return valid_moves

class Beetle(Piece):
    def allowed_movements(self, board):
        adjacent_spaces = board.get_adjacent_spaces(self.curr_pos)
        valid_moves = []
        for space in adjacent_spaces:
            if (board.has_adjacent_piece(space) and
                not board.breaks_hive(self.curr_pos, space)):
                valid_moves.append(space)
        return valid_moves

class Spider(Piece):
    def allowed_movements(self, board):
        valid_moves = set()
        visited = {self.curr_pos}
        self._dfs(board, self.curr_pos, 0, visited, valid_moves)
        return list(valid_moves)

    def _dfs(self, board, current_pos, steps, visited, valid_moves):
        if steps == 3:
            valid_moves.add(current_pos)
            return

        for neighbor in board.get_adjacent_spaces(current_pos):
            if board.is_valid_slide(current_pos, neighbor) and neighbor not in visited:
                visited.add(neighbor)
                self._dfs(board, neighbor, steps + 1, visited, valid_moves)
                visited.remove(neighbor)