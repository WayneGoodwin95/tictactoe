import sys
import numpy as np
import pygame as pg

import game_functions as gf
from settings import Settings as game_settings
from button import Button
from win_message import Game_over
from settings import Tile
from settings import Lines


def run_game():
    # Initialise game, settings, and create screen object
    pg.init()
    settings = game_settings()
    screen = pg.display.set_mode((settings.screen_width, settings.screen_height))
    pg.display.set_caption("Tic Tac Toe")

    # create board
    board = gf.create_board(screen, settings, Tile)

    for index, value in np.ndenumerate(board):
        print(value.x_pos)

    # Draw the screen and game board
    screen.fill(settings.bg_color)
    gf.draw_board(board)
    lines = Lines(screen)
    lines.draw_lines()

    # Create play button
    play_button = Button(screen, settings, 'Play')

    # Create Game Over Screen
    game_over_screen = Game_over(screen, settings, settings.game_over_msg)

    # start the main loop
    while True:
        # check button pressed
        button_pressed = gf.check_button_pressed(screen, settings, board, play_button)
        if settings.game_active and button_pressed:
            # check if player has won
            gf.check_win_conditions(settings, lines, board)
            # Check game over
            gf.check_game_over(settings, board, game_over_screen)
            # Make the most recent screen visible
            if settings.turn_counter < 9 and settings.game_active:
                settings.change_player()

        gf.update_screen(screen, settings, lines, board, play_button, game_over_screen)

        # Limit the amount of cycles
        pg.time.wait(16)


run_game()


