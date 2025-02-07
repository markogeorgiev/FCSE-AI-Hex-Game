import pygame
import math
from board import Board
from pieces import Queen, Beetle, Spider


def draw_hexagon(surface, color, center, size):
    points = []
    for i in range(6):
        angle = i * math.pi / 3 + math.pi / 6
        x = center[0] + size * math.cos(angle)
        y = center[1] + size * math.sin(angle)
        points.append((x, y))
    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, (100, 100, 100), points, 2)


def get_hex_center(row, col, hex_size):
    x = col * hex_size * 1.5 + 50
    y = row * hex_size * math.sqrt(3) + (col % 2) * hex_size * math.sqrt(3) / 2 + 50
    return (int(x), int(y))


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Hive Game")

    board = Board(12, 12)
    hex_size = 30
    font = pygame.font.Font(None, 36)

    # Game state variables from your original code
    white_turn = True
    round_counter = {'white': 0, 'black': 0}
    queens_placed = {'white': False, 'black': False}
    total_turns = 0

    running = True
    while running:
        screen.fill((255, 255, 255))

        # Draw board
        for i in range(4):
            for j in range(7):
                center = get_hex_center(i, j, hex_size)
                color = (200, 200, 200)

                # If position has a piece, color it differently
                pos = (i, j)
                if pos in board.occupied_positions():
                    color = (255, 223, 128)  # Light yellow

                draw_hexagon(screen, color, center, hex_size)

                # Draw coordinates
                coord_text = f"{i},{j}"
                text = font.render(coord_text, True, (0, 0, 0))
                text_rect = text.get_rect(center=center)
                screen.blit(text, text_rect)

                # Draw piece symbol if exists
                for piece in board.pieces.values():
                    if piece.position == pos:
                        piece_text = piece.name[0]  # First letter of piece name
                        color = (0, 0, 255) if piece.color == 'white' else (255, 0, 0)
                        text = font.render(piece_text, True, color)
                        text_rect = text.get_rect(center=(center[0], center[1] + 10))
                        screen.blit(text, text_rect)

        # Update display
        pygame.display.flip()

        # Use your existing input-based game logic here
        current_color = 'white' if white_turn else 'black'
        print(f"\n{'White' if white_turn else 'Black'} Turn")

        if current_color == 'black':
            # AI logic here
            pass
        else:
            # Human input logic here
            action = input("Do you want to 'move' or 'add' a piece? ").lower()
            # Rest of your existing game logic...

        # Check for pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == "__main__":
    main()