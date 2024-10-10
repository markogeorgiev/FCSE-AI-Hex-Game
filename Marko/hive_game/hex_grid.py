import pygame, numpy
from board import PLAYER_1_TOKEN, PLAYER_2_TOKEN
from pygame.locals import *

class HiveGame(object):
    window_width: int
    window_height: int

    board_width: int
    board_height: int
    board_width_in_tiles: int
    tile_width: int

    board_size: int
    click_board: tuple[tuple[pygame.Rect, ...], ...]


def draw_grid():
        """
        Draw an empty grid
        """
        self.