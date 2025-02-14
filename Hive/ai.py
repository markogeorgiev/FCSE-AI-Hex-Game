from traceback import print_tb

import game_state
import move_checker
from settings import directions, WHITE, BLACK
import random
from move_checker import no_black_neighbours
from mcts import monte_carlo_tree_search

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
    """This version of the ai.testing() function can get all possible moves for every piece, which has a valid move for that state."""
    can_be_moved = get_pieces_which_can_be_moved(state)
    print([curr_piece.__str__() for curr_piece in can_be_moved])
    for moveable_piece in can_be_moved:
        for valid_move in moveable_piece.get_all_valid_moves(state):
            print(f'{moveable_piece.__str__()} can move to {valid_move.__str__()}')
    return None

def choose_best_move(state):
    possible_moves = []
    for moveable_piece in get_pieces_which_can_be_moved(state):
        for valid_move in moveable_piece.get_all_valid_moves(state):
            possible_moves.append((moveable_piece, valid_move))

    if not possible_moves:
        return None  # No moves available

    return monte_carlo_tree_search(state, possible_moves)


def get_pieces_which_can_be_moved(state):
    moveable_pieces = []
    if state.turn == 7 and state.queen_not_placed():
        moveable_pieces.append(state.get_specific_piece(include_board=True, piece_name='Queen'))
    if state.turn <= 6:
        [moveable_pieces.append(curr_piece) for curr_piece in state.get_non_placed_piece(only_white=True)]
    else:
        [moveable_pieces.append(curr_piece) for curr_piece in state.get_tiles_with_pieces(include_inventory=True, only_white=True)]
    return moveable_pieces

def testing_v2(state):
    # 50/50 Choice between placing a piece and moving it.
    chosen_piece = get_random_piece(state)
    possible_moves = list(chosen_piece.get_all_valid_moves(state))
    checked_pieces = set()
    counter = 0
    checked_pieces.add(chosen_piece)
    while len(possible_moves) == 0:
        chosen_piece = get_random_piece(state)
        possible_moves = list(chosen_piece.get_all_valid_moves(state))
        checked_pieces.add(chosen_piece)
        if len(checked_pieces) == 11:
            state.next_turn()
            return None
        if counter > 0:
            print(f'Stuck: {chosen_piece.__str__()}')
    print(chosen_piece.__str__())
    where_to_move = random.choice(possible_moves)
    # iii. Find the old tile
    old_tile = state.get_tile_by_piece(chosen_piece)
    # iv. Move piece form old to new Tile
    old_tile.move_piece(where_to_move)
    # v. Change turn
    state.next_turn()
    print(state.queen_not_placed())
    return None


def testing_v1(state):
    # i. Choose a piece
    chosen_piece = random.choice(state.get_non_placed_piece())
    # ii. Choose a tile to move to:
    possible_moves = state.get_available_to_place_tiles(no_black_neighbours_check=True)
    while len(possible_moves) == 0:
        chosen_piece = random.choice(state.get_non_placed_piece())
        possible_moves = state.get_available_to_place_tiles(no_black_neighbours_check=True)
    where_to_move = random.choice(possible_moves)
    # iii. Find the old tile
    old_tile = state.get_tile_by_piece(chosen_piece)
    # iv. Move piece form old to new Tile
    old_tile.move_piece(where_to_move)
    # v. Change turn
    state.next_turn()
    return None


def get_random_piece(state):
    # move_not_place = random.choice([True, False])
    # It's either a queen or movement.
    if state.turn == 7 and state.queen_not_placed():
        return state.get_specific_piece(include_board=True, piece_name='Queen')
    elif state.turn <= 6:
        return random.choice(state.get_non_placed_piece(only_white=True))
    else:
        return random.choice(state.get_tiles_with_pieces(include_inventory=True, only_white=True)).pieces[-1]

