from board import Board
from pieces import Queen, Beetle, Spider


def get_piece_class(piece_name):
    if 'Queen' in piece_name:
        return Queen
    elif 'Beetle' in piece_name:
        return Beetle
    elif 'Spider' in piece_name:
        return Spider
    else:
        raise ValueError("Invalid piece name")


def main():
    board = Board(12, 12, False)
    white_turn = True
    round_counter = {'white': 0, 'black': 0}
    queens_placed = {'white': False, 'black': False}
    total_turns = 0

    while not board.game_over():
        current_color = 'white' if white_turn else 'black'
        print(f"\n{'White' if white_turn else 'Black'} Turn")

        firstRound = total_turns == 0
        secondRound = total_turns == 1

        if round_counter[current_color] == 2 and not queens_placed[current_color]:
            print(f"{current_color.capitalize()} must place their Queen this turn!")
            action = 'add'
        else:
            action = input("Do you want to 'move' or 'add' a piece? ").lower()

        if action == 'move':
            if not queens_placed[current_color]:
                print("You must place your Queen before moving any pieces!")
                continue

            piece_name = input("Enter the name of the piece to move (e.g., 'WhiteBeetle1'): ")
            piece = next((p for p in board.pieces.values() if p.name == piece_name), None)

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
                piece = PieceClass(piece_name)
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

        round_counter[current_color] += 1
        total_turns += 1
        white_turn = not white_turn

    print("Game Over!")
    print("Final board state:")
    print(board.occupied_positions())


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
