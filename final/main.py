import random
from board import *

class HiveAI:
    def __init__(self, hive):
        self.hive = hive

    def minimax(self, state, depth, maximizing_player):
        if depth == 0 or self.hive.check_valid(state) is False:
            return self.evaluate(state)

        if maximizing_player:
            max_eval = float('-inf')
            for _, new_state in self.hive.successor(state).items():
                eval = self.minimax(new_state, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for _, new_state in self.hive.successor(state).items():
                eval = self.minimax(new_state, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def evaluate(self, state):
        return len(state[1])  # Simplified evaluation

    def best_move(self, state):
        best_value = float('-inf')
        best_move = None
        for move, new_state in self.hive.successor(state).items():
            move_value = self.minimax(new_state, 3, False)
            if move_value > best_value:
                best_value = move_value
                best_move = move
        return best_move


def main():
    board = Hive(12, 12)
    ai = HiveAI(board)
    state = (board.show(), {})
    human_turn = True

    while not board.game_over():
        if human_turn:
            print("Human's turn")
            move = input("Enter move (piece x y): ").split()
            piece_name = move[0]
            new_pos = (int(move[1]), int(move[2]))
            if piece_name in state[1]:
                state = board.generate_new_state(state, piece_name, new_pos)
            else:
                print("Invalid move. Try again.")
                continue
        else:
            print("AI's turn")
            move = ai.best_move(state)
            if move:
                state = board.generate_new_state(state, move[0], move[1])
                print(f"AI moved {move[0]} to {move[1]}")

        human_turn = not human_turn

    print("Game Over!")


if __name__ == "__main__":
    main()
