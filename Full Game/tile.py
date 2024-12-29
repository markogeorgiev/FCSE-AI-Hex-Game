#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import pygame as pg
from pieces import Queen, Grasshopper, Spider, Beetle, Ant
from settings import WHITE, RED, BLUE


class Tile:

    def __init__(self, coord_pair, axial_coords, radius, color, piece=None):
        self.coords = coord_pair
        self.axial_coords = axial_coords
        self.radius = radius
        self.hex = get_hex_points(coord_pair, radius)
        self.hex_select = get_hex_points(coord_pair, radius * 1.1)
        self.color = color
        self.adjacent_tiles = []
        if piece:
            self.pieces = [piece]
        else:
            self.pieces = []

    def draw(self, surface, pos, clicked=False):
        if self.under_mouse(pos):
            if clicked:
                pg.draw.polygon(surface, RED, self.hex)
            else:
                pg.draw.polygon(surface, RED, self.hex_select)
                pg.draw.polygon(surface, self.color, self.hex)
        else:
            pg.draw.polygon(surface, self.color, self.hex)
        if self.has_pieces():
            self.pieces[-1].draw(surface, self.coords)

    def under_mouse(self, pos):
        if distance(self.coords, pos) < self.radius - 1:
            return True
        else:
            return False

    def __str__(self):
        if self.pieces:
            pieces_str = ", ".join([str(p) for p in self.pieces])
            return f"Hex tile with pieces: {pieces_str}"
        else:
            return "Hex tile with no pieces"

    def add_piece(self, piece):
        self.pieces.append(piece)
        self.pieces[-1].update_pos(self.coords)
        self.color = self.pieces[-1].color

    def remove_piece(self):
        self.pieces.pop(-1)
        if self.has_pieces():
            self.color = self.pieces[-1].color
        elif type(self) is Inventory_Tile:
            pass
        else:
            self.color = WHITE

    def move_piece(self, new_tile):
        new_tile.add_piece(self.pieces[-1])
        self.remove_piece()

    def has_pieces(self):
        if len(self.pieces) > 0:
            return True
        else:
            return False

    def set_coords_inventory(self, coord_pair):
        self.coords = coord_pair

    def is_hive_adjacent(self, state):
        for tile in self.adjacent_tiles:
            if tile.has_pieces():
                return True
        return False

    def set_adjacent_tiles(self, board_tiles):  # tiles don't move, only pieces do
        (q, r) = self.axial_coords
        adjacent_tiles = []
        for tile in board_tiles:
            if tile.axial_coords in [
                (q, r - 1),
                (q + 1, r - 1),
                (q + 1, r),
                (q, r + 1),
                (q - 1, r + 1),
                (q - 1, r),
                ]:
                adjacent_tiles.append(tile)

        self.adjacent_tiles = adjacent_tiles


class Inventory_Tile(Tile):

    def __init__(self, coord_pair, axial_coords, radius, color, piece):
        super().__init__(coord_pair, axial_coords, radius, color, piece)


class Start_Tile(Tile):
    def __init__(self, coord_pair, axial_coords, radius, color, piece):
        super().__init__(coord_pair, axial_coords, radius, BLUE, piece)

    def __str__(self):
        coord_info = f"Axial: {self.axial_coords}"
        radius_info = f"Radius: {self.radius}"
        color_info = f"Color: {self.color}"
        if self.pieces:
            pieces_str = ", ".join([str(p) for p in self.pieces])
            pieces_info = f"Pieces: {pieces_str}"
        else:
            pieces_info = "Pieces: None"
        return f"Start Tile [{coord_info}, {pieces_info}]"

def distance(pair_one, pair_two):
    (x1, y1) = pair_one
    (x2, y2) = pair_two
    return np.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


def get_hex_points(coord_pair, radius):
    (x, y) = coord_pair

    return (  # has to be in counterclockwise order for drawing
        (x, y + radius),  # top
        (x - ((radius * np.sqrt(3))/2), y + (radius / 2)),  # top-left
        (x - ((radius * np.sqrt(3))/2), y - (radius / 2)),  # bottom-left
        (x, y - radius),  # bottom
        (x + ((radius * np.sqrt(3))/2), y - (radius / 2)),  # bottom-right
        (x + ((radius * np.sqrt(3))/2), y + (radius / 2))  # top-right
    )


def initialize_grid(height, width, radius):
    hex_radius = radius

    # location of the tiles in pygame/cartesian pixels

    pixel_y = list(range(height + hex_radius, 0, -2 * hex_radius + 6))
    pixel_x = list(range(0, width + hex_radius, 2 * hex_radius))

    # axial hexagonal coordinates used for move finding

    axial_r = list(range(len(pixel_y) // 2 - 1, -(1 * len(pixel_y)
                   // 2) - 1, -1))
    odd_y = pixel_y[1::2]
    tiles = []
    for j in range(0, len(pixel_y)):
        for k in range(0, len(pixel_x)):
            if pixel_y[j] in odd_y:
                tiles.append(Tile((pixel_x[k] + hex_radius,
                             pixel_y[j]), ((j + 1) // 2 + k - 16,
                             axial_r[j]), hex_radius + 1, WHITE))
            else:
                if pixel_x[k] == 440 and pixel_y[j] == 380:  # middle tile
                    tiles.append(Start_Tile((pixel_x[k], pixel_y[j]),
                                 ((j + 1) // 2 + k - 16, axial_r[j]),
                                 hex_radius + 1, WHITE, None))
                else:
                    tiles.append(Tile((pixel_x[k], pixel_y[j]), ((j
                                 + 1) // 2 + k - 16, axial_r[j]),
                                 hex_radius + 1, WHITE))

    for tile in tiles:
        tile.set_adjacent_tiles(tiles)

    return tiles


def draw_drag(background, pos, piece=None):
    pg.draw.line(background, pg.Color('red'), pos, piece.old_pos)
