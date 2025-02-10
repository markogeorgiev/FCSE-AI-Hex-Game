import game_state
import move_checker
from settings import directions, WHITE, BLACK
import random

def generate_all_possible_moves(state):


    possible_placement_tiles = []
    inventory_tiles = state.get_tiles_in_inventory()

    # 1. All piece placement
    #       - Get all possible places where you can place a piece.
    tiles_where_you_can_place = get_available_to_place_tiles(state)

    for tile in tiles_where_you_can_place:
        if no_black_neighbours(state, tile):
            possible_placement_tiles.append(tile)

def testing(state):
    if state.turn == 1:
        # 1. Choose a piece
        # 2. Choose a tile to move the selected piece
        # 3. Find old tile
        # 4. Move from old tile to new tile
        # 5. Change turn
        chosen_piece = random.choice(state.get_non_placed_piece())

        start_tile = state.get_start_tile()
        old_tile = state.get_tile_by_piece(chosen_piece)
        old_tile.move_piece(start_tile)
        state.next_turn()

    return None


    # 2. All movements
    #       - Queen Movement
    #       - Beetle Movement
    #       - Ant Movement
    #       - Spider Movement
    #       - Grasshopper Movement
    return possible_placement_tiles

def all_adjacent_positions(state):
    # for curr_tile in state.get_tiles_with_pieces():
    #
    #     for direction in directions:
    #         potential_tile = state.get_tile((current_tile_axial_coords[0] + direction[0], current_tile_axial_coords[1] + direction[1]))
    ...

def get_adjacent_tiles(state, tile):
    current_tile_axial_coords = tile.get_axial_coords()
    adjacent_tiles = []
    for direction in directions:
        potential = state.get_tile(
            (current_tile_axial_coords[0] + direction[0], current_tile_axial_coords[1] + direction[1]))
        if potential is not None:
            adjacent_tiles.append(potential)
    return adjacent_tiles

def get_available_to_place_tiles(state):
    if state.turn == 1:
        return state.get_start_tile()

    tiles_with_piece = state.get_tiles_with_pieces()
    free_adjacent_tiles = []
    for tile in tiles_with_piece:
        for adj_tile in get_adjacent_tiles(state, tile):
            if not adj_tile.has_pieces() and adj_tile not in free_adjacent_tiles:
                free_adjacent_tiles.append(adj_tile)
    return free_adjacent_tiles

def no_black_neighbours(state, tile):
    adjacent_tiles = get_adjacent_tiles(state, tile)
    for adj_tile in adjacent_tiles:
        if adj_tile.color == (71,71,71):
            return False
    return True


