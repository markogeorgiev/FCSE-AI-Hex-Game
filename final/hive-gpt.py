import pygame
import sys
import math
from board import Board
from pieces import Queen, Beetle, Spider
import random
import math


# Pygame helper functions
def grid_to_pixel(x, y, radius, offset_x=100, offset_y=100):
    hex_width = radius * math.sqrt(3)
    hex_height = 2 * radius
    pixel_x = x * hex_width + (y % 2) * (hex_width / 2)
    pixel_y = y * hex_height * 0.75
    return (int(pixel_x + offset_x), int(pixel_y + offset_y))


def create_hexagon(center, radius):
    points = []
    for i in range(6):
        angle_deg = 30 + 60 * i  # Flat-topped hexagons
        angle_rad = math.radians(angle_deg)
        x = center[0] + radius * math.cos(angle_rad)
        y = center[1] + radius * math.sin(angle_rad)
        points.append((x, y))
    return points


# def draw_board(screen, board, radius=30):
#     screen.fill((255, 255, 255))  # White background
#     color_map = {'white': (255, 255, 255), 'black': (0, 0, 0)}
#
#     for piece in board.pieces.values():
#         if not hasattr(piece, 'position') or piece.position is None:
#             continue
#         grid_x, grid_y = piece.position
#         color = piece.color
#         type_start = len(piece.color.capitalize())
#         text = piece.name[type_start] if type_start < len(piece.name) else '?'
#
#         # Convert grid to screen coordinates
#         screen_x, screen_y = grid_to_pixel(grid_x, grid_y, radius)
#         hex_points = create_hexagon((screen_x, screen_y), radius)
#
#         # Draw hexagon
#         pygame.draw.polygon(screen, color_map[color], hex_points, 0)
#
#         # Draw text
#         font = pygame.font.Font(None, 36)
#         text_color = (0, 0, 0) if color == 'white' else (255, 255, 255)
#         text_surface = font.render(text, True, text_color)
#         text_rect = text_surface.get_rect(center=(screen_x, screen_y))
#         screen.blit(text_surface, text_rect)
#
#     pygame.display.flip()
def draw_board(screen, board, radius=30):
    screen.fill((255, 255, 255))  # White background
    color_map = {'white': (255, 255, 255), 'black': (0, 0, 0)}

    font = pygame.font.Font(None, 20)  # Font za koordinati

    # Najdi golemina na tablata
    min_x = min((pos[0] for pos in board.occupied_positions()), default=-5) - 2
    max_x = max((pos[0] for pos in board.occupied_positions()), default=5) + 2
    min_y = min((pos[1] for pos in board.occupied_positions()), default=-5) - 2
    max_y = max((pos[1] for pos in board.occupied_positions()), default=5) + 2

    # Nacrtaj outline na site validni polinja
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            screen_x, screen_y = grid_to_pixel(x, y, radius)
            hex_points = create_hexagon((screen_x, screen_y), radius)

            pygame.draw.polygon(screen, (0, 0, 0), hex_points, 2)  # Crna linija za hexagon

            # Ako na poleto nema figura, iscrtaj gi koordinatite
            if (x, y) not in board.occupied_positions():
                text_surface = font.render(f"{x},{y}", True, (100, 100, 100))  # Siva boja za tekst
                text_rect = text_surface.get_rect(center=(screen_x, screen_y))
                screen.blit(text_surface, text_rect)

    # Nacrtaj gi figurite na tablata
    for piece in board.pieces.values():
        if not hasattr(piece, 'position') or piece.position is None:
            continue
        grid_x, grid_y = piece.position
        color = piece.color
        type_start = len(piece.color.capitalize())
        text = piece.name[type_start] if type_start < len(piece.name) else '?'

        screen_x, screen_y = grid_to_pixel(grid_x, grid_y, radius)
        hex_points = create_hexagon((screen_x, screen_y), radius)

        pygame.draw.polygon(screen, color_map[color], hex_points, 0)

        # Iscrtaj go tekstot na figurata
        font = pygame.font.Font(None, 36)
        text_color = (0, 0, 0) if color == 'white' else (255, 255, 255)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(screen_x, screen_y))
        screen.blit(text_surface, text_rect)

    pygame.display.flip()


def get_piece_class(piece_name):
    if 'Queen' in piece_name:
        return Queen
    elif 'Beetle' in piece_name:
        return Beetle
    elif 'Spider' in piece_name:
        return Spider
    else:
        raise ValueError("Invalid piece name")


def evaluate_state(board, color):
    opponent = 'black' if color == 'white' else 'white'
    return len(board.team_spaces[color]) - len(board.team_spaces[opponent])


def minimax(board, depth, maximizing_player, alpha, beta, color):
    if depth == 0 or board.game_over():
        return evaluate_state(board, color), None

    if maximizing_player:
        max_eval = -math.inf
        best_move = None
        state = (board.board, board.pieces)

        for move, new_state in board.successor(state).items():
            piece_name, new_pos = move
            eval_score, _ = minimax(board, depth - 1, False, alpha, beta, color)

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = (piece_name, new_pos)

            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break

        return max_eval, best_move
    else:
        min_eval = math.inf
        best_move = None
        state = (board.board, board.pieces)

        for move, new_state in board.successor(state).items():
            piece_name, new_pos = move
            eval_score, _ = minimax(board, depth - 1, True, alpha, beta, color)

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = (piece_name, new_pos)

            beta = min(beta, eval_score)
            if beta <= alpha:
                break

        return min_eval, best_move


def ai_move(board, color, queens_placed, turn):
    if not queens_placed[color] and len(board.pieces) >= 6:
        piece_type = 'Queen'
    else:
        piece_type = random.choice(['Queen', 'Beetle', 'Spider'])

    piece_name = f"{color.capitalize()}{piece_type}"

    try:
        PieceClass = get_piece_class(piece_name)
        piece = PieceClass(piece_name, turn)  # Pass the turn number here
        valid_positions = piece.place_piece(board, len(board.pieces) == 0, len(board.pieces) == 1)

        if valid_positions:
            position = random.choice(list(valid_positions))
            piece.update_position(position)
            board.move_add_piece(piece)
            return True, f"AI added {piece_name} at {position}"
    except ValueError:
        pass

    _, best_move = minimax(board, 3, True, -math.inf, math.inf, color)
    if best_move:
        piece_name, new_pos = best_move
        piece = board.pieces[piece_name]
        piece.update_position(new_pos)
        board.move_add_piece(piece)
        return True, f"AI moved {piece_name} to {new_pos}"

    return False, "AI couldn't make a valid move"


# Rest of your existing code remains the same, except the main function
def main():
    board = Board(12, 12)
    white_turn = True
    round_counter = {'white': 0, 'black': 0}
    queens_placed = {'white': False, 'black': False}
    total_turns = 0

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Hive Game")

    while not board.game_over():
        current_color = 'white' if white_turn else 'black'
        print(f"\n{'White' if white_turn else 'Black'} Turn")

        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if current_color == 'black':
            success, message = ai_move(board, current_color, queens_placed, total_turns)
            if not success:
                print("Game over - AI can't move")
                break
            print(message)
        else:
            # Player's turn (existing code)
            firstRound = total_turns == 0
            secondRound = total_turns == 1

            if round_counter[current_color] == 2 and not queens_placed[current_color]:
                print("You must place your Queen this turn!")
                action = 'add'
            else:
                action = input("Do you want to 'move' or 'add' a piece? ").lower()

            if action == 'move':
                if not queens_placed[current_color]:
                    print("You must place your Queen before moving any pieces!")
                    continue

                piece_name = input("Enter the name of the piece to move (e.g., 'WhiteBeetle1'): ")
                piece = board.pieces.get(piece_name)

                if piece is None:
                    print("Invalid piece name. Try again.")
                    continue

                if piece.color != current_color:
                    print("You can only move your own pieces. Try again.")
                    continue

                valid_moves = piece.allowed_movements(board)
                print(f"Valid moves: {valid_moves}")

                new_pos = input("Enter the new position (x y): ").split()
                new_pos = (int(new_pos[0]), int(new_pos[1]))

                if new_pos in valid_moves:
                    piece.update_position(new_pos)
                    board.move_add_piece(piece)
                    print(f"Moved {piece_name} to {new_pos}")
                else:
                    print("Invalid move. Try again.")
                    continue

            elif action == 'add':
                piece_type = input("Enter the type of piece to add (Queen/Beetle/Spider): ")
                piece_name = f"{current_color.capitalize()}{piece_type}"

                if 'Queen' in piece_name:
                    queens_placed[current_color] = True

                try:
                    PieceClass = get_piece_class(piece_name)
                    piece = PieceClass(piece_name, total_turns)  # Pass the turn number here
                except ValueError:
                    print("Invalid piece type. Try again.")
                    continue

                valid_positions = piece.place_piece(board, firstRound, secondRound)
                print(f"Valid positions: {valid_positions}")

                position = input("Enter the position to place the piece (x y): ").split()
                position = (int(position[0]), int(position[1]))

                if position in valid_positions:
                    piece.update_position(position)
                    board.move_add_piece(piece)
                    print(f"Added {piece_name} at {position}")
                else:
                    print("Invalid position. Try again.")
                    continue

            else:
                print("Invalid action. Please choose 'move' or 'add'.")
                continue

        # Update display after each move
        draw_board(screen, board)
        round_counter[current_color] += 1
        total_turns += 1
        white_turn = not white_turn

    pygame.quit()
    print("Game Over!")
    print("Final board state:")
    print(board.occupied_positions())


if __name__ == "__main__":
    main()