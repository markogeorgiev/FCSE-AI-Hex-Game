# Defines the piece classes (Queen, Spider, Beetle, etc.)

# pieces.py
class Piece:
    def __init__(self, piece_type, player):
        self.piece_type = piece_type
        self.player = player
        self.position = None # Position on the board, set later

    def get_legal_moves(self, board):
        """This method will be overridden by each piece type."""
        raise NotImplementedError("This method should be overridden by each specific piece type")


class Queen(Piece):
    def __init__(self, player):
        super().__init__('queen', player)
    def get_legal_moves(self, board):
        # The Queen can move to any adjacent space, if allowed
        adjacent_positions = board.get_adjacent_positions(self.position)
        legal_moves = [pos for pos in adjacent_positions if board.is_legal_move(self, pos)]
        return legal_moves


class Spider(Piece):
    def __init__(self, player):
        super().__init__('spider', player)

    def get_legal_moves(self, board):
        # Spider moves exactly 3 spaces, staying on the surface
        legal_moves = board.get_spider_moves(self.position, self.player)
        return legal_moves


class Grasshopper(Piece):
    def __init__(self, player):
        super().__init__('grasshopper', player)

    def get_legal_moves(self, board):
        # Grasshopper jumps in a straight line over adjacent pieces
        legal_moves = board.get_grasshopper_moves(self.position)
        return legal_moves


class Beetle(Piece):
    def __init__(self, player):
        super().__init__('beetle', player)
        self.is_on_top = False  # A Beetle can move on top of another piece

    def get_legal_moves(self, board):
        # The Beetle can move like the Queen or move on top of adjacent pieces
        adjacent_positions = board.get_adjacent_positions(self.position)
        legal_moves = [pos for pos in adjacent_positions if board.is_legal_move(self, pos)]

        # Check if Beetle can climb onto adjacent pieces
        beetle_climbing_moves = board.get_beetle_climbing_moves(self.position)
        legal_moves.extend(beetle_climbing_moves)
        return legal_moves


class Ant(Piece):
    def __init__(self, player):
        super().__init__('ant', player)

    def get_legal_moves(self, board):
        # The Ant can move to any number of spaces around the board perimeter
        legal_moves = board.get_ant_moves(self.position)
        return legal_moves