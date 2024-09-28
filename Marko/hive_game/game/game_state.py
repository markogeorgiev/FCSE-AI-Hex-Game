#  Contains game state handling and game-over conditions


# game_state.py
class GameState:
    def __init__(self):
        self.board = Board()
        self.pieces = {
            1: [],  # Player 1 pieces
            2: []   # Player 2 pieces
        }
        self.turn = 1  # Start with player 1

    def is_game_over(self):
        # Check if either player's Queen Bee is surrounded
        pass

    def apply_move(self, move):
        # Update the game state based on the move
        pass