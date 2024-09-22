from pieces import *
from exceptions import *


class Board:
    def __init__(self, n, m):
        self.board = [(i, j) for i in range(0, n) for j in range(0, m)]
        self.positions_taken = {'white': [], 'black': []}
        self.pieces = []

    def add_piece(self, color, coords, piece):
        # check valid positioning first
        try:
            self.check_valid_positioning(color, coords)
        except PositionErrorException as e:
            print(e.message)

        self.positions_taken.get(color).append(coords)
        self.pieces.append(piece)

    def check_valid_move(self, piece, new_pos):
        # checks if it's valid by each figure's rules
        # checks if it breaks the hive in 2 (implement a method)
        # checks if it overlaps with a taken tile (not valid for the beetle)
        pass

    def move_piece(self, color, piece, new_pos):
        self.check_valid_move(piece, new_pos)
        # if it's valid, move the piece.
        pass

    def get_adjacent_coords(self, position):
        x, y = position[0], position[1]
        return [(x + i, y + j) for i in range(-1, 2) for j in range(-1, 2)]

    def check_valid_positioning(self, color, position):
        adj_coords = self.get_adjacent_coords(position)
        for (x, y) in adj_coords:
            if ((x, y) in self.positions_taken['white'] and color == 'black') or \
                    ((x, y) in self.positions_taken['black'] and color == 'white'):
                raise PositionErrorException("Invalid position")

    def show(self):
        return self.board

# board = Board(12, 12)
# print(board.show())
