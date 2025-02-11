#!/usr/bin/python
# -*- coding: utf-8 -*-
from xml.dom.pulldom import START_DOCUMENT

from tile import Start_Tile
from tile import Inventory_Tile
from pieces import Queen, Grasshopper, Spider, Beetle, Ant
from inventory_frame import Inventory_Frame
from turn_panel import Turn_Panel
from settings import PIECE_WHITE, PIECE_BLACK
from move_checker import move_obeys_queen_by_4
from settings import directions

class Game_State:

    def __init__(self, tiles=[], white_inventory=None, black_inventory=None):

        # state attributes

        self.running = True
        self.menu_loop = True
        self.main_loop = False
        self.end_loop = False
        self.play_new_game = False
        self.move_popup_loop = False

        # board

        white_inventory = Inventory_Frame((0, 158), 0, white=True)
        black_inventory = Inventory_Frame((440, 158), 1, white=False)
        self.board_tiles = tiles + white_inventory.tiles + black_inventory.tiles

        self.turn_panel = Turn_Panel()

        # action attributes

        self.clicked = False
        self.moving_piece = None
        self.turn = 1

        # other

        self.winner = None

    def start_game(self):
        self.menu_loop = False
        self.main_loop = True

    def end_game(self):
        self.main_loop = False
        self.end_loop = True

    def new_game(self):
        self.main_loop = True
        self.end_loop = False

        self.turn = 1

    def quit(self):
        self.running = False
        self.menu_loop = False
        self.main_loop = False
        self.end_loop = False

    def play_again(self):
        self.play_new_game = True
        self.quit()

    def open_popup(self):
        self.main_loop = False
        self.move_popup_loop = True

    def close_popup(self):
        self.main_loop = True
        self.move_popup_loop = False
        if move_obeys_queen_by_4(self):
            self.next_turn()

    def add_moving_piece(self, piece):
        self.moving_piece = piece

    def remove_moving_piece(self):
        self.moving_piece = None

    def click(self):
        self.clicked = True

    def unclick(self):
        self.clicked = False

    def add_tiles(self, tiles):
        self.tiles = self.board_tiles.extend(tiles)

    def next_turn(self):
        self.turn += 1

    def is_player_turn(self):
        if self.moving_piece.color == PIECE_WHITE and self.turn % 2 == 1:
            return True
        elif self.moving_piece.color == PIECE_BLACK and self.turn % 2 == 0:
            return True
        else:
            return False

    def get_tiles_with_pieces(self, include_inventory=False, only_white=False):
        tiles = []
        for tile in self.board_tiles:
            if include_inventory:
                if tile.has_pieces():
                    if only_white:
                        if tile.color == PIECE_WHITE:
                            tiles.append(tile)
                    else:
                        tiles.append(tile)
            elif tile.has_pieces() and type(tile) is not Inventory_Tile:
                tiles.append(tile)
        return tiles

    def get_tile(self, axial_coords):
        for tile in self.board_tiles:
            if tile.axial_coords == axial_coords:
                return tile
        return None

    def get_tiles_in_inventory(self):
        inventory_tiles = []
        for tile in self.board_tiles:
            if type(tile) is Inventory_Tile and tile.has_pieces():
                inventory_tiles.append(tile)
        return inventory_tiles

    def get_all_tiles(self):
        return [tile for tile in self.board_tiles]

    def get_non_placed_piece(self, only_white=True):
        inventory_tiles = self.get_tiles_in_inventory()
        inventory_pieces = []
        for tile in inventory_tiles:
            for piece in tile.pieces:
                if piece.color == PIECE_WHITE:
                    inventory_pieces.append(piece)
        return inventory_pieces

    def get_start_tile(self):
        for tile in self.board_tiles:
            if type(tile) is Start_Tile:
                return tile

    def get_adjacent_tiles(self, tile):
        current_tile_axial_coords = tile.get_axial_coords()
        adjacent_tiles = []
        for direction in directions:
            potential = self.get_tile(
                (current_tile_axial_coords[0] + direction[0], current_tile_axial_coords[1] + direction[1]))
            if potential is not None:
                adjacent_tiles.append(potential)
        return adjacent_tiles

    def get_tile_by_piece(self, targe_piece):
        for tile in self.get_tiles_with_pieces(include_inventory=True):
            if targe_piece == tile.pieces[-1]:
                return tile
        return None

    def queen_check(self):
        if self.turn <=6:
            return True
        if 'Queen' in [piece.__class__.__name__ for piece in self.get_non_placed_piece(only_white=True)]:
            return False

    def get_specific_piece(self, piece_name='Queen', include_board=False):
        tiles_to_look = self.get_tiles_in_inventory()
        if include_board:
            tiles_to_look += self.get_tiles_with_pieces(include_inventory=False)
        for tile in tiles_to_look:
            for piece in tile.pieces:
                if piece.color == PIECE_WHITE:
                    if piece.__class__.__name__ == piece_name:
                        return piece
        return None

