# Utility functions (e.g., deep copying game states)

# helpers.py

import copy

def deep_copy_game_state(board):
    """Deep copy the board state to ensure Minimax or other algorithms don't modify the original."""
    return copy.deepcopy(board)

def within_bounds(position, width=10, height=10):
    """Check if a position is within the bounds of the board."""
    x, y = position
    return 0 <= x < width and 0 <= y < height

def manhattan_distance(pos1, pos2):
    """Calculate Manhattan distance between two positions in a hexagonal grid."""
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)

def is_adjacent(pos1, pos2):
    """Check if two positions are adjacent on a hexagonal grid."""
    x1, y1 = pos1
    x2, y2 = pos2
    return (x1 == x2 and abs(y1 - y2) == 1) or (y1 == y2 and abs(x1 - x2) == 1) or (x1 + y1 == x2 + y2 and abs(x1 - x2) == 1)

