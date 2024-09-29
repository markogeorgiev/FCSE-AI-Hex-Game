from pieces import *

class Board:
    # Implement a counter for turns, after the 3rd round each player MUST have the Queen placed on the board.
    def __init__(self, n, m, firstRound):
        self.board = [(i, j) for i in range(0, n) for j in range(0, m)]
        self.team_spaces = {'white': [], 'black': []}

        # Objects of type Piece currently on the board
        # Every piece will be a stack, cause the Beetle can be on top of any piece.
        # self.pieces = []
        self.pieces = dict()

    def game_over(self):
        pass

    def add_piece(self, piece):
        self.pieces[piece.name] = piece
        self.team_spaces.get(piece.color).append(piece.position)

    def move_piece(self, piece, new_pos):
        # if it's valid, move the piece.
        pass

    def occupied_positions(self):
        positions = []
        for piece in self.pieces.values():
            positions.append(piece.position)

        return set(positions)

    def is_empty(self, position):
        return position not in self.occupied_positions()

    def has_adjacent_piece(self, position):
        adjacent_spaces = self.get_adjacent_spaces(position)
        return any(not self.is_empty(space) for space in adjacent_spaces)

    def get_adjacent_spaces(self, pos):
        x, y = pos
        offsets = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]
        return [(x + dx, y + dy) for dx, dy in offsets]

    def is_valid_slide(self, start, end):
        if end not in self.get_adjacent_spaces(start):
            return False

        if self.breaks_hive(start, end):
            return False

        # check if the end position is adjacent to at least one other piece
        adjacent_to_end = self.get_adjacent_spaces(end)
        for pos in adjacent_to_end:
            if pos != start and pos in self.occupied_positions():
                return True

        return False

    # need to check how its working
    # optimize it with sets instead of lists
    def breaks_hive(self, curr_pos, end_pos):
        occupied_positions = [pos for pos in self.occupied_positions()]

        #remove the piece we want to move
        occupied_positions.remove(curr_pos)

        # start the search with the first taken position
        start_pos = occupied_positions[0]

        # if there are no other pieces, the hive isn't broken
        if start_pos is None: return False

        # perform dfs to see if you will visit the rest of the taken positions in the hive
        visited = set()
        self.dfs(start_pos, occupied_positions, visited)

        # check if all pieces are still connected (each piece has been visited even after removing your target one)
        all_connected = set(occupied_positions) == visited

        return not all_connected

    def dfs(self, position, occupied_positions, visited):
        visited.add(position)

        for neighbor in self.get_adjacent_spaces(position):
            if neighbor in occupied_positions and neighbor not in visited:
                self.dfs(neighbor, occupied_positions, visited)

    def show(self):
        return self.board
