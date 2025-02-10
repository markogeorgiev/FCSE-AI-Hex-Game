import game_state
import move_checker


def generate_all_possible_moves(state):
    inventory_tiles = state.get_tiles_in_inventory()
    # 1. All piece placement
    #       - Get all possible places where you can place a piece.
    tiles_where_you_can_place = []
    for tile in state.get_tiles_with_pieces(include_inventory=False):
        ...

    for inv_tile in inventory_tiles:
        ...
    # 2. All movements
    #       - Queen Movement
    #       - Beetle Movement
    #       - Ant Movement
    #       - Spider Movement
    #       - Grasshopper Movement
    ...


def all_adjacent_positions(state):
    # for curr_tile in state.get_tiles_with_pieces():
    #
    #     for direction in directions:
    #         potential_tile = state.get_tile((current_tile_axial_coords[0] + direction[0], current_tile_axial_coords[1] + direction[1]))
    ...


def get_adjacent_tiles(state, tile):
    current_tile_axial_coords = tile.get_axial_coords()
    adjacent_tiles = []
    directions = [(0, -1), (1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0)]
    for direction in directions:
        potential = state.get_tile(
            (current_tile_axial_coords[0] + direction[0], current_tile_axial_coords[1] + direction[1]))
        if potential is not None:
            adjacent_tiles.append(potential)
    return adjacent_tiles
