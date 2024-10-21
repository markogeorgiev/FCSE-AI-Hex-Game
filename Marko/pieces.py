from abc import abstractmethod
from copy import deepcopy


class Piece:
    def __init__(self, name):
        self.name = name # (color + piece type) ex. WhiteBeetle1 ; queen will be Queen
        self.position = None
        self.color = 'white' if 'White' in self.name else 'black'

    def update_position(self, new_pos):
        self.position = new_pos

    def place_piece(self, board, firstRound, secondRound):
        if firstRound:
            return board.show()
        elif secondRound:
            first_piece = next(iter(board.pieces.values()))
            return board.get_adjacent_spaces(first_piece.position)
        else:
            own_team_pieces = set(board.team_spaces[self.color])
            opposite_team_pieces = set(board.team_spaces['black' if self.color == 'white' else 'white'])

            all_adjacent = set().union(*[set(board.get_adjacent_spaces(pos)) for pos in own_team_pieces])
            opposite_adjacent = set().union(*[set(board.get_adjacent_spaces(pos)) for pos in opposite_team_pieces])

            available_spaces = all_adjacent - opposite_adjacent - own_team_pieces - opposite_team_pieces

            return list(available_spaces)


    @abstractmethod
    def allowed_movements(self, board):
        pass

class Queen(Piece):
    def allowed_movements(self, board):
        adjacent_spaces = board.get_adjacent_spaces(self.position)
        valid_moves = []
        for space in adjacent_spaces:
            if (board.is_empty(space) and
                board.has_adjacent_piece(space) and
                not board.breaks_hive(self.position, space)):
                valid_moves.append(space)
        return valid_moves

class Beetle(Piece):
    def allowed_movements(self, board):
        adjacent_spaces = board.get_adjacent_spaces(self.position)
        valid_moves = []
        for space in adjacent_spaces:
            if (board.has_adjacent_piece(space) and
                not board.breaks_hive(self.position, space)):
                valid_moves.append(space)
        return valid_moves

class Spider(Piece):
    def allowed_movements(self, board):
        valid_moves = set()
        visited = set()
        self._dfs(board, self.position, 0, visited, valid_moves)
        return list(valid_moves)

    def _dfs(self, board, position, steps, visited, valid_moves):
        if steps == 3:
            if board.is_empty(position) and board.has_adjacent_piece(position):
                valid_moves.add(position)
            return

        visited.add(position)
        for neighbor in board.get_adjacent_spaces(position):
            if neighbor not in visited and board.is_valid_slide(position, neighbor):
                self._dfs(board, neighbor, steps + 1, visited, valid_moves)
        visited.remove(position)