import sys
import pygame as pg
import numpy as np


def create_board(screen, settings, Tile):
    """ Create empty board 3x3"""
    board = np.empty((settings.rows, settings.cols), dtype=dict)

    # get the index and the value for each element of an array
    # for the first array 1, 2, 3 to the next array 3, 4, 6...
    for index, value in np.ndenumerate(board):
        # assign the index for 2d array first element is row 2nd is col
        row, col = index[0], index[1]
        # for the tile of the board in the array, create a playable tile
        board[row][col] = Tile(screen, row, col)
        print(index)
    # return the board which is now saturated with the tiles
    return board


def check_button_pressed(screen, settings, board, play_button):
    # Watch for keyboard and mouse events.
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            can_play = False
            mouse_pos = pg.mouse.get_pos()
            # Check if game active and if player has clicked a allowable tle or button
            if settings.game_active:
                can_play = check_can_play(screen, settings, board, mouse_pos)
            elif not settings.game_active:
                check_play_button(screen, settings, board, mouse_pos, play_button)
            return can_play


def check_can_play(screen, settings, board, mouse_pos):
    can_play = False
    # enumerate through list
    for index, value in np.ndenumerate(board):
        row, col = index[0], index[1]
        # check if player has selected a playable tile
        if board[row][col].rect.collidepoint(mouse_pos) and board[row][col].active:
            # update the tile
            board[row][col].update_tile(settings.player)
            can_play = True
    return can_play


# Check if player has clicked button to restart the game
def check_play_button(screen, settings, board, mouse_pos, play_button):
    if play_button.rect.collidepoint(mouse_pos):
        reset_board(screen, settings, board)
        reset_settings(settings)


def check_game_over(settings, board, game_over_screen):
    if settings.turn_counter >= 9 and settings.game_active:
        # end game after al tiles are clicked
        settings.game_active = False
        settings.game_over_msg = 'Draw'


def check_win_conditions(settings, lines, board):
    if settings.turn_counter >= 4:
        check_horizontal(settings, lines, board)
        check_vertical(settings, lines, board)
        check_botleft_topright(settings, lines, board)
        check_topleft_botright(settings, lines, board)
        print(settings.game_over_msg)


def check_horizontal(settings, lines, board):
    for row in range(settings.rows):
        player1 = 0
        player2 = 0
        for col in range(settings.cols):
            if board[row][col].player == 1:
                player1 += 1
            elif board[row][col].player == 2:
                player2 += 1

            if player1 == settings.rows:
                line_win = 'h'
                player_wins(settings, lines, board, line_win, row)
            if player2 == settings.rows:
                line_win = 'h'
                player_wins(settings, lines, board, line_win, row)


def check_vertical(settings, lines, board):
    for col in range(settings.cols):
        player1 = 0
        player2 = 0
        for row in range(settings.rows):
            if board[row][col].player == 1:
                player1 += 1
            elif board[row][col].player == 2:
                player2 += 1

            if player1 == settings.cols:
                line_win = 'v'
                player_wins(settings, lines, board, line_win, col)
            if player2 == settings.cols:
                line_win = 'v'
                player_wins(settings, lines, board, line_win, col)


def check_botleft_topright(settings, lines, board):
    player1 = 0
    player2 = 0
    row = 2
    for col in range(settings.cols):
        if board[row][col].player == 1:
            player1 += 1
        elif board[row][col].player == 2:
            player2 += 1

        if player1 == settings.rows:
            line_win = 'd1'
            player_wins(settings, lines, board, line_win, colrow=0)
        if player2 == settings.rows:
            line_win = 'd1'
            player_wins(settings, lines, board, line_win, colrow=0)

        row -= 1


def check_topleft_botright(settings, lines, board):
    player1 = 0
    player2 = 0
    row = 0
    for col in range(settings.cols):
        if board[row][col].player == 1:
            player1 += 1
        elif board[row][col].player == 2:
            player2 += 1

        if player1 == settings.rows:
            line_win = 'd2'
            player_wins(settings, lines, board, line_win, colrow=0)
        if player2 == settings.rows:
            line_win = 'd2'
            player_wins(settings, lines, board, line_win, colrow=0)

        row += 1


def draw_board(board):
    for index, tile in np.ndenumerate(board):
        row, col = index[0], index[1]
        tile.draw_tile()


def reset_board(screen, settings, board):
    for index, value in np.ndenumerate(board):
        row, col = index[0], index[1]
        board[row][col].player = 0
        board[row][col].active = True
        board[row][col].image = ''


def reset_settings(settings):
    settings.game_active = True
    settings.turn_counter = 1
    settings.game_over_msg = ''
    settings.winning_line_start_xy = ()
    settings.winning_line_end_xy = ()


def player_wins(settings, lines, board, line_win, colrow):
    settings.game_active = False
    settings.game_over_msg = 'Player ' + str(settings.player) + '- WINS'

    if line_win == 'v':
        lines.winning_line_start_xy = board[0][colrow].rect.center
        lines.winning_line_end_xy = board[settings.rows - 1][colrow].rect.center
    elif line_win == 'h':
        lines.winning_line_start_xy = board[colrow][0].rect.center
        lines.winning_line_end_xy = board[colrow][settings.cols - 1].rect.center
    elif line_win == 'd1':
        lines.winning_line_start_xy = board[settings.rows - 1][0].rect.center
        lines.winning_line_end_xy = board[0][settings.cols - 1].rect.center
    elif line_win == 'd2':
        lines.winning_line_start_xy = board[0][0].rect.center
        lines.winning_line_end_xy = board[settings.rows - 1][settings.cols - 1].rect.center


def update_screen(screen, settings, lines, board, play_button, game_over_screen):
    draw_board(board)
    lines.draw_lines()
    if not settings.game_active:
        if settings.game_over_msg == 'Player 1- WINS' or settings.game_over_msg == 'Player 2- WINS':
            lines.draw_winning_line()
        game_over_screen.msg = settings.game_over_msg
        game_over_screen.prep_msg()
        game_over_screen.draw_game_over_screen()
        play_button.draw_button()
    pg.display.update()
