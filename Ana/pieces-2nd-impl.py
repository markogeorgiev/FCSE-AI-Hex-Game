from abc import abstractmethod


class Piece:
    def __init__(self, curr_pos):
        self.curr_pos = curr_pos

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