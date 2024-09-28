# Contains move generation logic for different pieces

# move_generator.py

from utils.constants import QUEEN, SPIDER, BEETLE, GRASSHOPPER, ANT


def generate_all_moves(board, player):
    """
    Generate all possible legal moves for the current player.
    Returns a list of move dictionaries in the format {'start': (x, y), 'end': (x, y)}.
    """
    legal_moves = []

    for position, piece in board.grid.items():
        if piece.player == player:
            moves = generate_moves_for_piece(board, piece)
            for move in moves:
                legal_moves.append({'start': piece.position, 'end': move})

    return legal_moves


def generate_moves_for_piece(board, piece):
    """
    Generate all legal moves for a given piece based on its type.
    """
    if piece.type == QUEEN:
        return board.get_adjacent_positions(piece.position)  # Example: Queen moves to adjacent positions
    elif piece.type == SPIDER:
        return board.get_spider_moves(piece.position, piece.player)
    elif piece.type == BEETLE:
        return board.get_beetle_climbing_moves(piece.position)
    elif piece.type == GRASSHOPPER:
        return board.get_grasshopper_moves(piece.position)
    elif piece.type == ANT:
        return board.get_ant_moves(piece.position)

    return []