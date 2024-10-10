# Contains the Board class and board state management
# board.py

"""
place_piece(piece, position): Places a piece on the board at the given position.
move_piece(start_pos, end_pos): Moves a piece from one position to another, updating its location on the board.
get_adjacent_positions(position): Returns a list of all positions adjacent to the given one. In Hive, the board is hexagonal, so this accounts for the six neighboring spaces.
is_legal_move(piece, target_position): Checks if moving a piece to a target position is legal. This method will be extended as you implement more game rules (e.g., sliding, disconnection).
get_spider_moves(position, player): Returns valid moves for a spider, which can move exactly 3 spaces without backtracking.
get_grasshopper_moves(position): Determines valid moves for the Grasshopper, which jumps in a straight line over adjacent pieces.
get_ant_moves(position): Returns valid moves for the Ant, which can move any number of spaces around the board.
get_beetle_climbing_moves(position): Returns valid moves for a Beetle climbing onto adjacent pieces.
get_perimeter_moves(position, max_depth): A helper function to get all perimeter moves for pieces like the Ant or Spider.
next_position_in_line(position, direction): Given a direction, this method calculates the next position in a straight line (used for Grasshopper).
"""

from Marko.hive_game.utils.constants import PLAYER_1, PLAYER_2
from Marko.hive_game.utils.helpers import deep_copy_game_state

class Board():
    def __init__(self, grid_size=10):
        # Dictionary storing pieces at each position: { (x, y): Piece }
        self.grid = [[(i, j) for j in range(grid_size)] for i in range(grid_size)]

    def place_piece(self, piece, position):
        """Place a piece at the given position."""
        piece.position = position
        self.grid[position] = piece

    def move_piece(self, start_pos, end_pos):
        """Move a piece from start_pos to end_pos, updating the board."""
        piece = self.grid.pop(start_pos)
        piece.position = end_pos
        self.grid[end_pos] = piece

    def remove_piece(self, position):
        """Remove a piece from the board."""
        self.grid.pop(position, None)

    def get_piece(self, position):
        """Get the piece at a specific position."""
        return self.grid.get(position, None)

    def is_game_over(self):
        """Check if the game is over."""
        players = [1, 2]
        for player in players:
            if self.is_queen_surrounded(player):
                print(f"Player {player} has lost! Game Over.")
                return True
        return False

    def is_queen_surrounded(self, player):
        """Check if the given player's Queen is surrounded."""
        queen_position = self.find_queen(player)
        if not queen_position:
            return False  # No queen found for this player

        # Check adjacent positions for surrounding pieces
        adjacent_positions = self.get_adjacent_positions(queen_position)
        surrounding_count = sum(
            1 for pos in adjacent_positions if self.get_piece(pos) and self.get_piece(pos).player != player)

        return surrounding_count >= 6  # The Queen is surrounded if it has 6 opposing pieces around it

    def find_queen(self, player):
        """Find the Queen piece for the given player."""
        for position, piece in self.grid.items():
            if piece.type == 'Queen' and piece.player == player:
                return position
        return None

    def is_legal_move(self, piece, target_position):
        """Check if a move to the target position is legal."""
        # Example of a basic legality check (to be extended with Hive rules)
        if target_position in self.grid:
            return False  # Cannot move to an occupied space (except for Beetles)

        # Add additional logic for Hive-specific rules, e.g., sliding rule, one hive rule
        if not self.is_board_connected_after_move(piece, target_position):
            return False

        return True

    def get_adjacent_positions(self, position):
        """Get all positions adjacent to a given position."""
        x, y = position
        # In Hive, the board is a hexagonal grid, so we need to calculate neighbors
        adjacent_positions = [
            (x + 1, y), (x - 1, y),
            (x, y + 1), (x, y - 1),
            (x + 1, y - 1), (x - 1, y + 1)
        ]
        return adjacent_positions

    def is_board_connected_after_move(self, piece, target_position):
        """Ensure the move does not disconnect the board (one hive rule)."""
        # This method checks if removing the piece from its current position
        # and moving it to the target still keeps the board connected.
        temp_board = deep_copy_game_state(self)
        temp_board.remove_piece(piece.position)
        visited = set()

        # Find a random piece still on the board to start BFS/DFS
        start_position = next(iter(temp_board.grid.keys()), None)
        if not start_position:
            return True  # No pieces left on the board

        # Perform BFS/DFS to check connectivity
        self.bfs(start_position, visited, temp_board)

        # Check if we visited all remaining pieces
        return len(visited) == len(temp_board.grid)

    def bfs(self, start, visited, board):
        """Perform a BFS to check board connectivity."""
        queue = [start]
        visited.add(start)

        while queue:
            current = queue.pop(0)
            for neighbor in self.get_adjacent_positions(current):
                if neighbor in board.grid and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

    def get_spider_moves(self, position, player):
        """Spider moves exactly 3 spaces along the surface, without backtracking."""
        # Placeholder logic to be replaced with Spider-specific movement rules
        # In general, the spider can move 3 spaces along the hive perimeter
        return self.get_perimeter_moves(position, 3)

    def get_grasshopper_moves(self, position):
        """Grasshopper jumps in a straight line over adjacent pieces."""
        legal_moves = []
        directions = self.get_adjacent_positions(position)

        for direction in directions:
            current_pos = position
            while current_pos in self.grid:
                current_pos = self.next_position_in_line(current_pos, direction)

            if current_pos and current_pos not in self.grid:
                legal_moves.append(current_pos)

        return legal_moves

    def get_ant_moves(self, position):
        """Ant can move to any number of spaces along the perimeter."""
        # Ants move freely around the board without restrictions, as long as they slide.
        visited = set()
        return self.get_perimeter_moves(position, max_depth=None, visited=visited)

    def get_beetle_climbing_moves(self, position):
        """Beetles can climb onto adjacent pieces."""
        legal_moves = []
        adjacent_positions = self.get_adjacent_positions(position)

        for pos in adjacent_positions:
            if pos in self.grid:  # There is a piece adjacent
                legal_moves.append(pos)  # Beetle can climb on top of this piece

        return legal_moves

    def get_perimeter_moves(self, position, max_depth=None, visited=None):
        """A generic function to get perimeter moves."""
        if visited is None:
            visited = set()
        visited.add(position)

        legal_moves = []
        adjacent_positions = self.get_adjacent_positions(position)

        for pos in adjacent_positions:
            if pos not in self.grid and self.is_legal_move(None, pos):
                legal_moves.append(pos)
                if max_depth is None or len(visited) < max_depth:
                    legal_moves.extend(self.get_perimeter_moves(pos, max_depth, visited))

        return legal_moves

    def next_position_in_line(self, position, direction):
        """Calculate the next position in a line based on a given direction."""
        x, y = position
        dx, dy = direction
        return x + dx, y + dy