# Defines the evaluation function for scoring game states

# evaluation.py

from Marko.hive_game.utils.constants import QUEEN, SPIDER, BEETLE, GRASSHOPPER, ANT


def evaluate_game_state(board, player):
    """
    Evaluate the current board state and return a score for the given player.
    Positive score is good for the player, negative score is bad.
    """
    # Basic heuristic: give points for pieces remaining and their strategic position
    score = 0

    for position, piece in board.grid.items():
        if piece.player == player:
            score += piece_value(piece)  # Positive score for player's pieces
            score += positional_value(board, piece)
        else:
            score -= piece_value(piece)  # Negative score for opponent's pieces
            score -= positional_value(board, piece)

    # Additional rules or weights can be added here, such as priority for controlling the center of the board
    # or penalizing a player's queen being surrounded.

    return score


def piece_value(piece):
    """
    Assign a value to each piece type to prioritize certain pieces over others.
    """
    if piece.type == QUEEN:
        return 100  # Queen is the most important piece, so high value
    elif piece.type == SPIDER:
        return 20
    elif piece.type == BEETLE:
        return 25
    elif piece.type == GRASSHOPPER:
        return 15
    elif piece.type == ANT:
        return 30

    return 0  # Default value for any other pieces


def positional_value(board, piece):
    """
    Evaluate the positional value of a piece. For example, is the Queen in danger of being surrounded?
    Is the piece central to the hive or isolated?
    """
    # Example heuristic: penalize the Queen for being surrounded
    if piece.type == QUEEN:
        adjacent_positions = board.get_adjacent_positions(piece.position)
        surrounding_pieces = sum(1 for pos in adjacent_positions if board.get_piece(pos))
        if surrounding_pieces >= 5:  # Queen is almost surrounded
            return -50  # Penalize heavily

    # You can add more positional heuristics here, e.g., reward pieces that are near the center of the hive.
    return 0
