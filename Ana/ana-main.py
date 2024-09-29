from board import *
from pieces import *

board = Board(12, 12)
whiteTurn = True
invalidMovementFlag = False
counter = 0

while not board.game_over():
    if whiteTurn:
        print('White Turn')
    else:
        print('Black Turn')
    if not invalidMovementFlag:
        counter += 1

    pieceName, x, y = input().split(' ')
    print(pieceName, (x, y))

    if counter == 3 and pieceName != 'queen':
        print('Must move the queen.')
    else:
        invalidMovementFlag = False

    piece = Piece(pieceName, (int(x), int(y)))
    try:
        board.add_piece(piece)
        whiteTurn = not whiteTurn
    except PositionErrorException as e:
        print(f"Error: {e}")
        invalidMovementFlag = True

print(board.occupied_positions())
