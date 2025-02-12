#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import pygame as pg
from move_checker import axial_distance, move_is_not_blocked_or_jump, \
    path_exists, is_straight_line, placement_is_allowed
from settings import PIECE_WHITE
from move_checker import no_black_neighbours, move_does_not_break_hive, is_valid_move_v2
# from tile import Inventory_Tile
import tile


class Piece:

    def __init__(self, color=PIECE_WHITE):
        self.old_pos = None
        self.color = color

    def update_pos(self, pos):
        self.old_pos = pos

    def move_is_valid(self, state, old_tile, new_tile):
        pass

    def get_all_valid_moves(self, state):
        piece_tile = state.get_tile_by_piece(self)
        valid_tiles = set()
        if len(state.get_tiles_with_pieces(include_inventory=False)) == 0:
            valid_tiles.add(state.get_start_tile())
        for hive_member in state.get_tiles_with_pieces(include_inventory=True):
            for adjacent_tile in state.get_adjacent_tiles(hive_member):
                if is_valid_move_v2(state, piece_tile, adjacent_tile):
                    valid_tiles.add(adjacent_tile)
        return valid_tiles

    def __str__(self):
        if self.color == PIECE_WHITE:
            return f'White {self.__class__.__name__}: {self.old_pos}'
        return f'Black {self.__class__.__name__}: {self.old_pos}'


class Queen(Piece):

    def __init__(self, color=PIECE_WHITE):
        super().__init__(color)

    def draw(self, surface, hex_pos):
        image = \
            pg.image.load('images/{}.png'.format(type(self).__name__))
        (x, y) = hex_pos
        pos = (x - 16, y - 14)
        surface.blit(image, pos)

    def move_is_valid(self, state, old_tile, new_tile):
        dist = axial_distance(old_tile.axial_coords,
                              new_tile.axial_coords)
        if dist == 1 and move_is_not_blocked_or_jump(state, old_tile,
                                                     new_tile):
            return True
        else:
            return False

#   def get_all_valid_moves(self, state):
#       piece_tile = state.get_tile_by_piece(self)
#       valid_tiles = set()
#       for possible_tile in state.get_adjacent_tiles(piece_tile):
#           if is_valid_move_v2(state, piece_tile, possible_tile):
#               valid_tiles.add(possible_tile)
#       return valid_tiles


class Ant(Piece):

    def __init__(self, color=PIECE_WHITE):
        super().__init__(color)

    def draw(self, surface, hex_pos):
        image = \
            pg.image.load('images/{}.png'.format(type(self).__name__))
        (x, y) = hex_pos
        pos = (x - 16, y - 17)
        surface.blit(image, pos)

    def move_is_valid(self, state, old_tile, new_tile):
        if path_exists(state, old_tile, new_tile):
            return True
        else:
            return False


class Spider(Piece):
    def __init__(self, color=PIECE_WHITE):
        super().__init__(color)

    def draw(self, surface, hex_pos):
        image = \
            pg.image.load('images/{}.png'.format(type(self).__name__))
        (x, y) = hex_pos
        pos = (x - 16, y - 17)
        surface.blit(image, pos)

    def move_is_valid(self, state, old_tile, new_tile):
        if path_exists(state, old_tile, new_tile, spider=True) \
                and move_is_not_blocked_or_jump(state, old_tile, new_tile):
            return True
        else:
            return False


class Beetle(Piece):

    def __init__(self, color=PIECE_WHITE):
        super().__init__(color)

    def draw(self, surface, hex_pos):
        image = \
            pg.image.load('images/{}.png'.format(type(self).__name__))
        (x, y) = hex_pos
        pos = (x - 16, y - 16)
        surface.blit(image, pos)

    def move_is_valid(self, state, old_tile, new_tile):
        dist = axial_distance(old_tile.axial_coords,
                              new_tile.axial_coords)
        if dist == 1 and (move_is_not_blocked_or_jump(state, old_tile,
                                                      new_tile) or new_tile.has_pieces()
                          or len(old_tile.pieces) > 1):

            # can't slide into a blocked hex, but it can go up or down into one

            return True
        else:
            return False


class Grasshopper(Piece):

    def __init__(self, color=PIECE_WHITE):
        super().__init__(color)

    def draw(self, surface, hex_pos):
        image = \
            pg.image.load('images/{}.png'.format(type(self).__name__))
        (x, y) = hex_pos
        pos = (x - 12, y - 14)
        surface.blit(image, pos)

    def move_is_valid(self, state, old_tile, new_tile):

        # dist > 1, straight line, must hop over pieces

        dist = axial_distance(old_tile.axial_coords,
                              new_tile.axial_coords)

        if dist > 1:
            visited = [old_tile]
            queue = [old_tile]
            while queue and new_tile not in visited:
                current_tile = queue.pop(0)
                for neighbor_tile in [x for x in
                                      current_tile.adjacent_tiles if x.has_pieces()
                                                                     and is_straight_line(old_tile.axial_coords,
                                                                                          x.axial_coords)]:
                    if neighbor_tile not in visited:
                        visited.append(neighbor_tile)
                        queue.append(neighbor_tile)

            # have to check last tile seperately bc it will never have a piece

            for penultimate_tile in [x for x in new_tile.adjacent_tiles
                                     if x.has_pieces()]:
                if penultimate_tile in visited \
                        and is_straight_line(old_tile.axial_coords,
                                             new_tile.axial_coords):
                    return True
        else:
            return False
