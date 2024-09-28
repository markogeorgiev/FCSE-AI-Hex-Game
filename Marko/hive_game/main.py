# The main entry point to start and run the game

# main.py
from game.game_state import GameState
from ai.minimax import minimax


def main():
    game_state = GameState()

    while not game_state.is_game_over():
        # Generate legal moves and let the player or AI choose a move
        if game_state.turn == 1:
            move = get_human_move()  # Human player
        else:
            move = minimax(game_state, depth=3, alpha=float('-inf'), beta=float('inf'), maximizing_player=False)

        game_state.apply_move(move)
        game_state.turn = 2 if game_state.turn == 1 else 1

    print("Game over!")


if __name__ == "__main__":
    main()
