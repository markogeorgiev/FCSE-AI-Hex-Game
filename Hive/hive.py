#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading

import pygame as pg

import game_state
import ai
from tile import Tile, initialize_grid, draw_drag
from move_checker import is_valid_move, game_is_over, \
    player_has_no_moves
from menus import start_menu, end_menu, no_move_popup
from game_state import Game_State
from inventory_frame import Inventory_Frame
from turn_panel import Turn_Panel
from settings import BACKGROUND, WIDTH, HEIGHT
from move_checker import move_obeys_queen_by_4


def Hive():
    pg.font.init()

    # Create the screen

    screen = pg.display.set_mode((WIDTH, HEIGHT))
    background = pg.Surface(screen.get_size())

    # Title and Icon

    pg.display.set_caption('Hive')
    icon = pg.image.load('images/icon.png')
    pg.display.set_icon(icon)

    state = Game_State(initialize_grid(HEIGHT - 200, WIDTH, radius=20))
    white_inventory = Inventory_Frame((0, 158), 0, white=True)
    black_inventory = Inventory_Frame((440, 158), 1, white=False)

    while state.running:
        while state.menu_loop:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    state.quit()
                    break
                start_menu(screen, state, event)

        if move_obeys_queen_by_4(state):
            while state.move_popup_loop:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        state.quit()
                        break
                    no_move_popup(screen, background, state, event)
        else:
            state.close_popup()

        while state.main_loop:
            #print([piece.__str__() for piece in state.get_tiles_with_pieces()])
            #print([piece.__str__() for piece in state.get_tiles_in_inventory()])
            # for tile in state.get_all_tiles():
            #     print(f'{tile.__str__()}')
            # print('==============================================\n\n\n\n\n\n\n\n\n\n')
            # if state.turn % 2 == 1:
            #     ai.testing(state)
            #     for tile in state.get_tiles_with_pieces(include_inventory=False):
            #         if tile.has_pieces():
            #             if tile.pieces[0].__class__.__name__ == 'Queen':
            #                 for adj_tile in ai.generate_all_possible_moves(state):
            #                     print(f'{adj_tile.__str__()}')
            #                 print('==============================================\n\n\n\n\n\n\n\n\n\n')
            
            if state.turn % 2 == 1:
                ai.choose_best_move(state)
                ai.testing(state)

            pos = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    state.quit()
                    break
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        state.quit()
                        break
                if event.type == pg.MOUSEBUTTONDOWN:
                    state.click()
                if event.type == pg.MOUSEBUTTONUP:
                    state.unclick()
                    if state.moving_piece and state.is_player_turn():
                        old_tile = next(tile for tile in state.board_tiles if tile.has_pieces() and tile.pieces[-1] == state.moving_piece)
                        new_tile = next((tile for tile in state.board_tiles if tile.under_mouse(pos)), None)
                        if is_valid_move(state, old_tile, new_tile):
                            old_tile.move_piece(new_tile)
                            state.next_turn()
                            if player_has_no_moves(state):
                                state.open_popup()
                    state.remove_moving_piece()

            background.fill(BACKGROUND)
            white_inventory.draw(background, pos)
            black_inventory.draw(background, pos)

            for tile in state.board_tiles:
                if state.clicked:
                    tile.draw(background, pos, state.clicked)
                    if tile.under_mouse(pos) and state.moving_piece is None and tile.has_pieces():
                        state.add_moving_piece(tile.pieces[-1])
                else:
                    tile.draw(background, pos)
            if state.moving_piece:
                draw_drag(background, pos, state.moving_piece)
            state.turn_panel.draw(background, state.turn)
            screen.blit(background, (0, 0))
            pg.display.flip()

            if game_is_over(state):
                state.end_game()

        while state.end_loop:
            end_menu(screen, state, event)  # drawing takes precedence over the close window button
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    state.quit()
                    break
    return state.play_new_game

def main():
    run_game = True
    while run_game:
        run_game = Hive()


if __name__ == '__main__':
    main()