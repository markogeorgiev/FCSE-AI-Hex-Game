from board import *
from pieces import *

################## THIS IS TEMPORARY FOR TESTING ONLY !!! ####################################

whiteTurn = True
invalidMovementFlag = False
counter = 0
firstRound = False
secondRound = False
board = Board(12, 12, firstRound)

while not board.game_over():
    if whiteTurn:
        print('White Turn')
    else:
        print('Black Turn')
    if counter == 0:
        firstRound = True
    elif counter == 1:
        firstRound = False
        secondRound = True
    else:
        firstRound, secondRound = False, False
    pieceName = input("Please enter input in format: {ColorFigure}")
    if 'Queen' in pieceName:
        piece = Queen(pieceName)
    if 'Beetle' in pieceName:
        piece = Beetle(pieceName)
    if 'Spider' in pieceName:
        piece = Spider(pieceName)

    print(f'Choose one of the following spaces\n: {piece.allowed_movements(board, firstRound, secondRound)}')
    x, y = input("Please enter in format: {x y}").split(' ')
    piece.update_position((int(x), int(y)))
    print(piece.__class__)

    if firstRound or secondRound:
        board.add_piece(piece)

    if not invalidMovementFlag:
        counter += 1
        whiteTurn = not whiteTurn

print(board.occupied_positions())
