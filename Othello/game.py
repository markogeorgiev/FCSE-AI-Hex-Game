import pygame
import sys
import tkinter as tk
from tkinter import ttk
from copy import deepcopy
import random
import time

pygame.init()

SQUARE_SIZE = 60
BOARD_SIZE = 8
WINDOW_SIZE = BOARD_SIZE * SQUARE_SIZE
SCREEN = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Othello')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
GRAY = (128, 128, 128)


def choose_ai_algorithm():
    root = tk.Tk()
    root.title("Choose Mode")

    window_width = 300
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (window_width / 2)
    y = (screen_height / 2) - (window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')

    selected_algorithm = tk.StringVar(value="minimax")

    label = ttk.Label(root, text="Select Game Mode:", font=('Arial', 12))
    label.pack(pady=10)

    minimax_radio = ttk.Radiobutton(root, text="Human vs Minimax", variable=selected_algorithm, value="minimax")
    minimax_radio.pack()

    expectimax_radio = ttk.Radiobutton(root, text="Human vs Expectimax", variable=selected_algorithm,
                                       value="expectimax")
    expectimax_radio.pack()

    greedy_radio = ttk.Radiobutton(root, text="Human vs Greedy", variable=selected_algorithm, value="greedy")
    greedy_radio.pack()

    ai_vs_ai_radio = ttk.Radiobutton(root, text="Minimax vs Expectimax (10 Rounds)",
                                     variable=selected_algorithm, value="minimax_vs_expectimax")
    ai_vs_ai_radio.pack()

    def on_select():
        root.quit()

    select_button = ttk.Button(root, text="Start Game", command=on_select)
    select_button.pack(pady=20)

    root.mainloop()
    algorithm = selected_algorithm.get()
    root.destroy()
    return algorithm


def show_turn_passed_message(current_player):
    root = tk.Tk()
    root.title("Turn Passed")

    window_width = 300
    window_height = 100
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (window_width / 2)
    y = (screen_height / 2) - (window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')

    label = ttk.Label(root, text=f"{current_player} has no moves. Turn passed.", font=('Arial', 12))
    label.pack(pady=20)

    def on_ok():
        root.quit()
        root.destroy()

    ok_button = ttk.Button(root, text="OK", command=on_ok)
    ok_button.pack()

    root.mainloop()


class OthelloGame:
    def __init__(self, ai_algorithm):
        self.board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.board[3][3] = self.board[4][4] = 'W'
        self.board[3][4] = self.board[4][3] = 'B'
        self.current_player = 'B'
        self.game_over = False
        self.winner = None
        self.ai_algorithm = ai_algorithm
        self.WEIGHTS = [
            [100, -20, 10, 5, 5, 10, -20, 100],
            [-20, -30, -5, -5, -5, -5, -30, -20],
            [10, -5, 2, 2, 2, 2, -5, 10],
            [5, -5, 2, 1, 1, 2, -5, 5],
            [5, -5, 2, 1, 1, 2, -5, 5],
            [10, -5, 2, 2, 2, 2, -5, 10],
            [-20, -30, -5, -5, -5, -5, -30, -20],
            [100, -20, 10, 5, 5, 10, -20, 100],
        ]

    def evaluate_minimax(self, board, player):
        opponent = 'W' if player == 'B' else 'B'

        positional = 0
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == player:
                    positional += self.WEIGHTS[i][j] * 1.5
                elif board[i][j] == opponent:
                    positional -= self.WEIGHTS[i][j]

        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        corner_value = 0
        for (i, j) in corners:
            if board[i][j] == player:
                corner_value += 25
            elif board[i][j] == opponent:
                corner_value -= 25

        return positional + corner_value

    def evaluate_expectimax(self, board, player):
        opponent = 'W' if player == 'B' else 'B'

        positional = 0
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == player:
                    positional += self.WEIGHTS[i][j]
                elif board[i][j] == opponent:
                    positional -= self.WEIGHTS[i][j] * 0.8

        player_moves = len(self.get_valid_moves(board, player))
        opponent_moves = len(self.get_valid_moves(board, opponent))
        mobility = (player_moves - opponent_moves) * 3

        edge_penalty = 0
        for i in [1, 6]:
            for j in [1, 6]:
                if board[i][j] == player:
                    edge_penalty -= 15

        return positional + mobility + edge_penalty

    def greedy(self, board, player):
        """Chooses the move that flips the most pieces."""
        best_move = None
        max_flips = -1

        valid_moves = self.get_valid_moves(board, player)
        for move in valid_moves:
            new_board = deepcopy(board)
            self.make_move(new_board, move[0], move[1], player)
            flipped_count = sum(row.count(player) for row in new_board) - sum(row.count(player) for row in board)

            if flipped_count > max_flips:
                max_flips = flipped_count
                best_move = move

        return best_move

    def get_valid_moves(self, board, player):
        valid_moves = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == ' ' and self.is_valid_move(board, i, j, player):
                    valid_moves.append((i, j))
        return valid_moves

    def is_valid_move(self, board, row, col, player):
        if board[row][col] != ' ':
            return False

        opponent = 'W' if player == 'B' else 'B'
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0),
                      (1, 1), (-1, -1), (1, -1), (-1, 1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            temp_flips = []
            found = False
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                if board[r][c] == opponent:
                    temp_flips.append((r, c))
                elif board[r][c] == player:
                    if temp_flips:
                        found = True
                    break
                else:
                    break
                r += dr
                c += dc
            if found:
                return True
        return False

    def make_move(self, board, row, col, player):
        if not self.is_valid_move(board, row, col, player):
            return False

        board[row][col] = player
        opponent = 'W' if player == 'B' else 'B'
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0),
                      (1, 1), (-1, -1), (1, -1), (-1, 1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            flips = []
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == opponent:
                flips.append((r, c))
                r += dr
                c += dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
                for flip_r, flip_c in flips:
                    board[flip_r][flip_c] = player

        return True

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0:
            return self.evaluate_minimax(board, 'B' if maximizing_player else 'W'), None

        current_player = 'B' if maximizing_player else 'W'
        valid_moves = self.get_valid_moves(board, current_player)
        if not valid_moves:
            return self.evaluate_minimax(board, current_player), None

        best_move = None
        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                new_board = deepcopy(board)
                self.make_move(new_board, move[0], move[1], 'B')
                eval, _ = self.minimax(new_board, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in valid_moves:
                new_board = deepcopy(board)
                self.make_move(new_board, move[0], move[1], 'W')
                eval, _ = self.minimax(new_board, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def expectimax(self, board, depth, maximizing_player):
        if depth == 0:
            return self.evaluate_expectimax(board, 'B' if maximizing_player else 'W'), None

        current_player = 'B' if maximizing_player else 'W'
        valid_moves = self.get_valid_moves(board, current_player)
        if not valid_moves:
            return self.evaluate_expectimax(board, current_player), None

        best_move = None
        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                new_board = deepcopy(board)
                self.make_move(new_board, move[0], move[1], 'B')
                eval, _ = self.expectimax(new_board, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            total_eval = 0
            move_count = len(valid_moves)
            for move in valid_moves:
                new_board = deepcopy(board)
                self.make_move(new_board, move[0], move[1], 'W')
                eval, _ = self.expectimax(new_board, depth - 1, True)
                total_eval += eval
            avg_eval = total_eval / move_count if move_count != 0 else 0
            return avg_eval, valid_moves[0] if valid_moves else None

    def get_ai_move(self):
        if self.ai_algorithm == "minimax_vs_expectimax":
            if self.current_player == 'B':
                _, move = self.minimax(self.board, 6, float('-inf'), float('inf'), True)
            else:
                _, move = self.expectimax(self.board, 5, False)
        elif self.ai_algorithm == "minimax":
            _, move = self.minimax(self.board, 5, float('-inf'), float('inf'), False)
        elif self.ai_algorithm == "expectimax":
            _, move = self.expectimax(self.board, 4, False)
        elif self.ai_algorithm == "greedy":
            move = self.greedy(self.board, 'W')
        return move

    def draw_board(self):
        SCREEN.fill(GREEN)
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                pygame.draw.rect(SCREEN, BLACK,
                                 (j * SQUARE_SIZE, i * SQUARE_SIZE,
                                  SQUARE_SIZE, SQUARE_SIZE), 1)

                if self.board[i][j] != ' ':
                    color = BLACK if self.board[i][j] == 'B' else WHITE
                    center = (j * SQUARE_SIZE + SQUARE_SIZE // 2,
                              i * SQUARE_SIZE + SQUARE_SIZE // 2)
                    pygame.draw.circle(SCREEN, color, center, SQUARE_SIZE // 2 - 4)

    def check_game_over(self):
        black_moves = self.get_valid_moves(self.board, 'B')
        white_moves = self.get_valid_moves(self.board, 'W')

        if not black_moves and not white_moves:
            black_count = sum(row.count('B') for row in self.board)
            white_count = sum(row.count('W') for row in self.board)

            if black_count > white_count:
                self.winner = "Human" if self.ai_algorithm != "minimax_vs_expectimax" else "Minimax"
            elif white_count > black_count:
                self.winner = "AI" if self.ai_algorithm != "minimax_vs_expectimax" else "Expectimax"
            else:
                self.winner = "Draw"
            return True
        return False


import time  # Add this at the top with other imports

def main():
    ai_algorithm = choose_ai_algorithm()

    clock = pygame.time.Clock()

    game = OthelloGame(ai_algorithm)
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if ai_algorithm in ["minimax", "expectimax", "greedy"]:
                if not game.game_over and event.type == pygame.MOUSEBUTTONDOWN and game.current_player == 'B':
                    x, y = event.pos
                    row = y // SQUARE_SIZE
                    col = x // SQUARE_SIZE
                    if game.make_move(game.board, row, col, 'B'):
                        game.draw_board()
                        pygame.display.flip()
                        time.sleep(1)  # Wait after human move
                        game.current_player = 'W'
                        game.game_over = game.check_game_over()

        if not game.game_over:
            if ai_algorithm == "minimax_vs_expectimax" or (
                    game.current_player == 'W' and ai_algorithm in ["minimax", "expectimax", "greedy"]):
                ai_move = game.get_ai_move()
                if ai_move:
                    game.make_move(game.board, ai_move[0], ai_move[1], game.current_player)
                    game.draw_board()
                    pygame.display.flip()
                    time.sleep(1)  # Wait after AI move
                    game.current_player = 'B' if game.current_player == 'W' else 'W'
                    game.game_over = game.check_game_over()
                else:
                    current_player_name = "Minimax" if game.current_player == 'B' else "Expectimax" if ai_algorithm == "minimax_vs_expectimax" else "AI"
                    show_turn_passed_message(current_player_name)
                    game.current_player = 'B' if game.current_player == 'W' else 'W'
                    game.game_over = game.check_game_over()

        if not game.game_over:
            current_player_moves = game.get_valid_moves(game.board, game.current_player)
            if not current_player_moves:
                current_player_name = "Human" if game.current_player == 'B' else "Minimax" if game.current_player == 'B' and ai_algorithm == "minimax_vs_expectimax" else "Expectimax" if game.current_player == 'W' and ai_algorithm == "minimax_vs_expectimax" else "AI"
                show_turn_passed_message(current_player_name)
                game.current_player = 'W' if game.current_player == 'B' else 'B'
                game.game_over = game.check_game_over()

        game.draw_board()

        if game.check_game_over():
            winner_text = game.winner
            font_large = pygame.font.Font(None, 36)
            text = font_large.render(f"Winner: {winner_text}", True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_SIZE / 2, WINDOW_SIZE / 2))
            s = pygame.Surface((text_rect.width + 20, text_rect.height + 20))
            s.fill(BLACK)
            s.set_alpha(128)
            SCREEN.blit(s, (
                text_rect.centerx - text_rect.width // 2 - 10, text_rect.centery - text_rect.height // 2 - 10))
            SCREEN.blit(text, text_rect)
            pygame.display.flip()
            game_over = True

        pygame.display.flip()
        clock.tick(60)

    # Keep window open until manually closed
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()



if __name__ == "__main__":
    main()