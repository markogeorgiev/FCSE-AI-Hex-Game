# Contains the Board class and board state management

class Board:
    def __init__(self):
        self.grid = {}  # Store pieces on the board (coordinate -> piece)

    def place_piece(self, piece, position):
        self.grid[position] = piece

    def move_piece(self, start_pos, end_pos):
        piece = self.grid.pop(start_pos)
        self.grid[end_pos] = piece

    def get_piece(self, position):
        return self.grid.get(position, None)