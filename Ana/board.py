from pieces import *
from exceptions import *

class Board:
    def __init__(self, n, m):
        self.board = [(i, j) for i in range(0, n) for j in range(0, m)]
        self.positions_taken = {'white': [], 'black': []}
        self.pieces = []

    def add_piece(self, color, coords, piece):
        # check valid positioning first
        try:
            self.check_valid_positioning(color, coords)
        except PositionErrorException as e:
            print(e.message)

        self.positions_taken.get(color).append(coords)
        self.pieces.append(piece)

    def check_valid_move(self, piece, new_pos):
        # checks if it's valid by each figure's rules
        # checks if it breaks the hive in 2 (implement a method)
        # checks if it overlaps with a taken tile (not valid for the beetle)
        pass

    def move_piece(self, color, piece, new_pos):
        self.check_valid_move(piece, new_pos)
        # if it's valid, move the piece.
        pass

    def get_adjacent_coords(self, position):
        x, y = position[0], position[1]
        return [(x + i, y + j) for i in range(-1, 2) for j in range(-1, 2)]

    def check_valid_positioning(self, color, position):
        adj_coords = self.get_adjacent_coords(position)
        for (x, y) in adj_coords:
            if ((x, y) in self.positions_taken['white'] and color == 'black') or \
                    ((x, y) in self.positions_taken['black'] and color == 'white'):
                raise PositionErrorException("Invalid position")

    # need to check how its working
    def breaks_hive(self, curr_pos, end_pos):
        all_positions_taken = [pos for pos in self.positions_taken['white']] + [pos for pos in self.positions_taken['black']]

        #remove the piece we want to move
        all_positions_taken.remove(curr_pos)

        # start the search with the first taken position
        start_pos = all_positions_taken[0]

        # if there are no other pieces, the hive isn't broken
        if start_pos is None: return False

        # perform dfs to see if you will visit the rest of the taken positions in the hive
        visited = []
        self.dfs(start_pos, all_positions_taken, visited)

        # check if all pieces are still connected (each piece has been visited even after removing your target one)
        all_connected = set(all_positions_taken) == set(visited)

        return not all_connected

    def dfs(self, position, all_positions_taken, visited):
        visited.append(position)

        for neighbor in self.get_adjacent_coords(position):
            if neighbor in all_positions_taken and neighbor not in visited:
                self.dfs(neighbor, all_positions_taken, visited)

    def show(self):
        return self.board

# board = Board(12, 12)
# print(board.show())
