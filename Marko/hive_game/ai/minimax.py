# Implements the minimax algorithm and alpha-beta pruning


# minimax.py
def minimax(game_state, depth, alpha, beta, maximizing_player):
    if depth == 0 or game_state.is_game_over():
        return evaluate(game_state)

    if maximizing_player:
        max_eval = float('-inf')
        for move in generate_legal_moves(game_state.board, game_state.pieces[1]):
            new_state = deepcopy(game_state)
            new_state.apply_move(move)
            eval = minimax(new_state, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in generate_legal_moves(game_state.board, game_state.pieces[2]):
            new_state = deepcopy(game_state)
            new_state.apply_move(move)
            eval = minimax(new_state, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval
