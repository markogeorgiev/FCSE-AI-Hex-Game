# Contains move generation logic for different pieces

# move_generator.py
def generate_legal_moves(board, player_pieces):
    legal_moves = []
    for piece in player_pieces:
        legal_moves.extend(piece.get_legal_moves(board))
    return legal_moves