class Board:
    # Implement a counter for turns, after the 3rd round each player MUST have the Queen placed on the board.
    def __init__(self, n, m):
        self.board = [(i, j) for i in range(0, n) for j in range(0, m)]
        self.team_spaces = {'white': [], 'black': []}

        # Objects of type Piece currently on the board
        # Every piece will be a stack, cause the Beetle can be on top of any piece.
        # self.pieces = []
        self.pieces = dict()

    def game_over(self):
        pass

    def move_add_piece(self, piece):
        # if it's valid, move the piece.
        self.pieces[piece.name] = piece
        self.team_spaces.get(piece.color).append(piece.position)
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

    @staticmethod
    def get_adjacent_spaces(pos):
        x, y = pos
        offsets_even = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 0), (0, -1)]
        offsets_odd = [(0, -1), (-1, 0), (0, 1), (1, 1), (1, 0), (1, -1)]
        if y % 2 == 0:
            return [(x + dx, y + dy) for dx, dy in offsets_even]
        else:
            return [(x + dx, y + dy) for dx, dy in offsets_odd]

    def is_valid_slide(self, start, end):
        if end not in self.get_adjacent_spaces(start):
            return False

        if self.breaks_hive(start, end):
            return False

        # Check if the end position is adjacent to at least one other piece
        adjacent_to_end = self.get_adjacent_spaces(end)
        for pos in adjacent_to_end:
            if pos != start and pos in self.occupied_positions():
                return True

        return False

    def breaks_hive(self, curr_pos, end_pos):
        occupied_positions = list(self.occupied_positions())
        if curr_pos in occupied_positions:
            occupied_positions.remove(curr_pos)

        if not occupied_positions:
            return False

        start_pos = occupied_positions[0]
        visited = set()
        self.dfs(start_pos, occupied_positions, visited)

        return set(occupied_positions) != visited

    def dfs(self, position, occupied_positions, visited):
        visited.add(position)

        for neighbor in self.get_adjacent_spaces(position):
            if neighbor in occupied_positions and neighbor not in visited:
                self.dfs(neighbor, occupied_positions, visited)

    def show(self):
        return self.board
