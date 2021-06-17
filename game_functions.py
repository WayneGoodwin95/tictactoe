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


def check_button_pressed(lines, game_over, settings, board, play_button):
    # Watch for keyboard and mouse events.
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            can_play = False
            mouse_pos = pg.mouse.get_pos()
            # Check if game active and if player has clicked a allowable tle or button
            if settings.game_active:
                can_play = check_can_play(settings, board, mouse_pos)
            elif not settings.game_active:
                check_play_button(lines, game_over, settings, board, mouse_pos, play_button)
            return can_play


def check_can_play(settings, board, mouse_pos):
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
def check_play_button(lines, game_over, settings, board, mouse_pos, play_button):
    if play_button.rect.collidepoint(mouse_pos):
        reset_board(board)
        reset_settings(lines, game_over, settings)


def check_game_over(settings, board, game_over):
    if settings.turn_counter >= 9 and settings.game_active:
        # end game after al tiles are clicked
        settings.game_active = False
        game_over.msg = 'Draw'


def check_win_conditions(settings, lines, board, game_over):
    if settings.turn_counter >= 4:
        check_horizontal(settings, lines, board, game_over)
        check_vertical(settings, lines, board, game_over)
        check_botleft_topright(settings, lines, board, game_over)
        check_topleft_botright(settings, lines, board, game_over)


def check_horizontal(settings, lines, board, game_over):
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
                player_wins(settings, lines, board, line_win, game_over, row)
            if player2 == settings.rows:
                line_win = 'h'
                player_wins(settings, lines, board, line_win, game_over, row)


def check_vertical(settings, lines, board, game_over):
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
                player_wins(settings, lines, board, line_win, game_over, col)
            if player2 == settings.cols:
                line_win = 'v'
                player_wins(settings, lines, board, line_win, game_over, col)


def check_botleft_topright(settings, lines, board, game_over):
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
            player_wins(settings, lines, board, line_win, game_over, colrow=0)
        if player2 == settings.rows:
            line_win = 'd1'
            player_wins(settings, lines, board, line_win, game_over, colrow=0,)

        row -= 1


def check_topleft_botright(settings, lines, board, game_over):
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
            player_wins(settings, lines, board, line_win, game_over, colrow=0)
        if player2 == settings.rows:
            line_win = 'd2'
            player_wins(settings, lines, board, line_win, game_over, colrow=0)

        row += 1


def draw_board(board):
    for index, tile in np.ndenumerate(board):
        row, col = index[0], index[1]
        tile.draw_tile()


def reset_board(board):
    for index, value in np.ndenumerate(board):
        row, col = index[0], index[1]
        board[row][col].player = 0
        board[row][col].active = True
        board[row][col].image = ''


def reset_settings(lines, game_over, settings):
    settings.game_active = True
    settings.turn_counter = 1
    game_over.msg = ''
    lines.winning_line_start_xy = ()
    lines.winning_line_end_xy = ()


def player_wins(settings, lines, board, line_win, game_over, colrow):
    settings.game_active = False
    game_over.msg = 'Player ' + str(settings.player) + '- WINS'

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


def update_screen(settings, lines, board, play_button, game_over):
    draw_board(board)
    lines.draw_lines()
    if not settings.game_active:
        if game_over.msg == 'Player 1- WINS' or game_over.msg == 'Player 2- WINS':
            lines.draw_winning_line()
        game_over.prep_msg()
        game_over.draw_msg()
        play_button.draw_button()
    pg.display.update()
