import game_state
import move_checker
from settings import directions, WHITE, BLACK
import random
from move_checker import no_black_neighbours

def generate_all_possible_moves(state):
    possible_placement_tiles = []
    inventory_tiles = state.get_tiles_in_inventory()

    # 1. All piece placement
    #       - Get all possible places where you can place a piece.
    tiles_where_you_can_place = state.get_available_to_place_tiles()



    # 2. All movements
    #       - Queen Movement
    #       - Beetle Movement
    #       - Ant Movement
    #       - Spider Movement
    #       - Grasshopper Movement
    return possible_placement_tiles


def testing(state):
    # 50/50 Choice between placing a piece and moving it.
    chosen_piece = get_random_piece(state)
    valid_moves = ...
    if random.random() > 0.5 or state.turn == 1:
    # 1. Place a piece
        # ii. Choose a tile to move to:
        where_to_move = random.choice(state.get_available_to_place_tiles( no_black_neighbours_check=True))
        # iii. Find the old tile
    else:
    # 2. Move a piece
        # ii. Choose where to move it to.
        where_to_move = random.choice(state.get_available_to_place_tiles( no_black_neighbours_check=False))

    # iii. Find the old tile
    old_tile = state.get_tile_by_piece(chosen_piece)
    # iv. Move piece form old to new Tile
    old_tile.move_piece(where_to_move)
    # v. Change turn
    state.next_turn()

    return None

def testing_v1(state):
    # i. Choose a piece
    chosen_piece = random.choice(state.get_non_placed_piece())
    # ii. Choose a tile to move to:
    where_to_move = random.choice(state.get_available_to_place_tiles( no_black_neighbours_check=True))
    # iii. Find the old tile
    old_tile = state.get_tile_by_piece(chosen_piece)
    # iv. Move piece form old to new Tile
    old_tile.move_piece(where_to_move)
    # v. Change turn
    state.next_turn()
    return None


def all_adjacent_positions(state):
    # for curr_tile in state.get_tiles_with_pieces():
    #
    #     for direction in directions:
    #         potential_tile = state.get_tile((current_tile_axial_coords[0] + direction[0], current_tile_axial_coords[1] + direction[1]))
    ...




def get_random_piece(state):
    move_not_place = random.choice([True, False])
    if not state.queen_check():
        return state.get_specific_piece(piece_name='Queen', include_board=False)
    if state.turn == 1 or not move_not_place:
        return random.choice(state.get_non_placed_piece(only_white=True))
    if move_not_place:
        return random.choice(state.get_tiles_with_pieces(include_inventory=False, only_white=True)).pieces[-1]


