# Implements the minimax algorithm and alpha-beta pruning


from Marko.hive_game.ai.evaluation import evaluate_game_state
from Marko.hive_game.utils.helpers import deep_copy_game_state
from Marko.hive_game.game.move_generator import generate_all_moves

# minimax.py

# Minimax function with Alpha-Beta pruning
def minimax(board, depth, is_maximizing_player, alpha, beta, player):
    """Minimax algorithm with alpha-beta pruning."""
    if depth == 0 or board.is_game_over():
        return evaluate_game_state(board, player)

    if is_maximizing_player:
        max_eval = float('-inf')
        for move in generate_all_moves(board, player):
            # Make a copy of the board and apply the move
            new_board = deep_copy_game_state(board)
            new_board.move_piece(move['start'], move['end'])

            # Recurse into the Minimax function with the next depth
            eval = minimax(new_board, depth - 1, False, alpha, beta, player)

            # Take the best move for the maximizing player
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)

            # Alpha-Beta pruning
            if beta <= alpha:
                break

        return max_eval
    else:
        min_eval = float('inf')
        opponent = 1 if player == 2 else 2
        for move in generate_all_moves(board, opponent):
            # Make a copy of the board and apply the move
            new_board = deep_copy_game_state(board)
            new_board.move_piece(move['start'], move['end'])

            # Recurse into the Minimax function with the next depth
            eval = minimax(new_board, depth - 1, True, alpha, beta, player)

            # Take the best move for the minimizing player
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)

            # Alpha-Beta pruning
            if beta <= alpha:
                break

        return min_eval


def find_best_move(board, depth, player):
    """Find the best move for the AI player using the Minimax algorithm."""
    best_move = None
    best_value = float('-inf') if player == 1 else float('inf')
    is_maximizing_player = player == 1

    for move in generate_all_moves(board, player):
        # Make a copy of the board and apply the move
        new_board = deep_copy_game_state(board)
        new_board.move_piece(move['start'], move['end'])

        # Run the minimax algorithm for the given depth
        eval = minimax(new_board, depth - 1, not is_maximizing_player, float('-inf'), float('inf'), player)

        # Update the best move
        if is_maximizing_player:
            if eval > best_value:
                best_value = eval
                best_move = move
        else:
            if eval < best_value:
                best_value = eval
                best_move = move

    return best_move
