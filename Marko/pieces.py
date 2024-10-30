from abc import abstractmethod
from copy import deepcopy


class Piece:
    def __init__(self, name):
        self.name = name  # (color + piece type) ex. WhiteBeetle1 ; queen will be Queen
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

            own_adjacent = set().union(*[set(board.get_adjacent_spaces(pos)) for pos in own_team_pieces])
            opposite_adjacent = set().union(*[set(board.get_adjacent_spaces(pos)) for pos in opposite_team_pieces])

            available_spaces = own_adjacent - opposite_adjacent - own_team_pieces - opposite_team_pieces

            return list(available_spaces)

    @abstractmethod
    def allowed_movements(self, board):
        return NotImplemented('This should not be called')

    def all_adjacent_pieces(self, board):  # only for ants, doesn't include current piece
        own = set(board.team_spaces[self.color])
        own.remove(tuple(self.position))
        opposite = set(board.team_spaces['black' if self.color == 'white' else 'white'])

        own_adj = set().union(*[set(board.get_adjacent_spaces(pos)) for pos in own])
        opposite_adj = set().union(*[set(board.get_adjacent_spaces(pos)) for pos in opposite])

        all_adj = own_adj | opposite_adj
        return list(set(all_adj))


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


class Grasshopper(Piece):
    def allowed_movements(self, board):
        valid_moves = []

        x, y = self.position
        offsets_even = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 0), (0, -1)]
        offsets_odd = [(0, -1), (-1, 0), (0, 1), (1, 1), (1, 0), (1, -1)]
        offsets = []
        if y % 2 == 0:
            offsets = offsets_even
        else:
            offsets = offsets_odd

        valid_neighbours_offsets = []

        # When we move once for a piece,

        for offset in offsets:
            if not board.is_empty((x + offset[0], y + offset[1])):
                valid_neighbours_offsets.append(offset)


        for valid_offset in valid_neighbours_offsets:
            start_offset = valid_offset
            while not board.is_empty((x + valid_offset[0], y + valid_offset[1])):
                valid_offset = (valid_offset[0] + start_offset[0], valid_offset[1] + start_offset[1])
            valid_moves.append(valid_offset)

        return valid_moves


class Ant(Piece):
    def allowed_movements(self, board):
        valid_moves = []
        all_adjacent = self.all_adjacent_pieces(board)
        for space in all_adjacent:
            if (board.is_empty(space) and
                    not board.breaks_hive(self.position, space)):
                valid_moves.append(space)
        return valid_moves
