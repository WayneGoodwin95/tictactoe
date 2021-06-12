import sys
import pygame as pg
import numpy as np


def create_board(screen, settings, Tile, image_x, image_o):
    """ Create board"""
    board = np.empty((settings.rows, settings.cols), dtype=dict)

    for index, value in np.ndenumerate(board):
        row, col = index[0], index[1]
        board[row][col] = Tile(screen, row, col, image_x, image_o)
        print(index)
    return board


def check_button_pressed(screen, settings, board, image_x, image_o, play_button):
    # Watch for keyboard and mouse events.
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            can_play = False
            mouse_pos = pg.mouse.get_pos()
            if settings.game_active:
                can_play = check_can_play(screen, settings, board, mouse_pos, image_x, image_o)
            elif not settings.game_active:
                check_play_button(screen, settings, board, mouse_pos, play_button)
            return can_play


def check_can_play(screen, settings, board, mouse_pos, image_x, image_o):
    can_play = False
    for index, value in np.ndenumerate(board):
        row, col = index[0], index[1]
        if board[row][col].rect.collidepoint(mouse_pos) and board[row][col].active:
            board[row][col].update_tile(settings.player)
            can_play = True
    return can_play


def check_play_button(screen, settings, board, mouse_pos, play_button):
    if play_button.rect.collidepoint(mouse_pos):
        reset_board(screen, settings, board)
        reset_settings(settings)


def check_game_over(settings, board, game_over_screen):
    if settings.turn_counter >= 9 and settings.game_active:
        # end game after al tiles are clicked
        settings.game_active = False
        settings.game_over_msg = 'Draw'


def check_win_conditions(settings, board):
    if settings.turn_counter >= 4:
        check_horizontal(settings, board)
        check_vertical(settings, board)
        check_botleft_topright(settings, board)
        check_topleft_botright(settings, board)
        print(settings.game_over_msg)


def check_horizontal(settings, board):
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
                player_wins(settings, board, line_win, row)
            if player2 == settings.rows:
                line_win = 'h'
                player_wins(settings, board, line_win, row)


def check_vertical(settings, board):
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
                player_wins(settings, board, line_win, col)
            if player2 == settings.cols:
                line_win = 'v'
                player_wins(settings, board, line_win, col)


def check_botleft_topright(settings, board):
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
            player_wins(settings, board, line_win, colrow=0)
        if player2 == settings.rows:
            line_win = 'd1'
            player_wins(settings, board, line_win, colrow=0)

        row -= 1


def check_topleft_botright(settings, board):
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
            player_wins(settings, board, line_win, colrow=0)
        if player2 == settings.rows:
            line_win = 'd2'
            player_wins(settings, board, line_win, colrow=0)

        row += 1


def draw_board(screen, settings, board):
    for index, tile in np.ndenumerate(board):
        row, col = index[0], index[1]
        tile.draw_tile()


def draw_lines(screen, settings):
    """Draw board lines to screen surface."""
    # first horizontal line
    pg.draw.line(screen, settings.line_color, (0, settings.line_1_y),
                 (settings.screen_width, settings.line_1_y), settings.line_width)
    # second horizontal line
    pg.draw.line(screen, settings.line_color, (0, settings.line_2_y),
                 (settings.screen_width, settings.line_2_y), settings.line_width)
    # first vertical line
    pg.draw.line(screen, settings.line_color, (settings.line_3_x, 0),
                 (settings.line_3_x, settings.screen_height), settings.line_width)
    # second vertical line
    pg.draw.line(screen, settings.line_color, (settings.line_4_x, 0),
                 (settings.line_4_x, settings.screen_height), settings.line_width)


def draw_winning_line(screen, settings):
    # first horizontal line
    pg.draw.line(screen, settings.winning_line_color, settings.winning_line_start_xy,
                 settings.winning_line_end_xy, settings.winning_line_width)


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


def player_wins(settings, board, line_win, colrow):
    settings.game_active = False
    settings.game_over_msg = 'Player ' + str(settings.player) + '- WINS'

    if line_win == 'v':
        settings.winning_line_start_xy = board[0][colrow].rect.center
        settings.winning_line_end_xy = board[settings.rows - 1][colrow].rect.center
    elif line_win == 'h':
        settings.winning_line_start_xy = board[colrow][0].rect.center
        settings.winning_line_end_xy = board[colrow][settings.cols - 1].rect.center
    elif line_win == 'd1':
        settings.winning_line_start_xy = board[settings.rows - 1][0].rect.center
        settings.winning_line_end_xy = board[0][settings.cols - 1].rect.center
    elif line_win == 'd2':
        settings.winning_line_start_xy = board[0][0].rect.center
        settings.winning_line_end_xy = board[settings.rows - 1][settings.cols - 1].rect.center


def change_player(settings):
    if settings.player == 1:
        settings.player = 2
    elif settings.player == 2:
        settings.player = 1
    settings.turn_counter += 1
    print('Turn ' + str(settings.turn_counter) + ': Player ' + str(settings.player))


def update_screen(screen, settings, board, play_button, game_over_screen):
    draw_board(screen, settings, board)
    draw_lines(screen, settings)
    if not settings.game_active:
        if settings.game_over_msg == 'Player 1- WINS' or settings.game_over_msg == 'Player 2- WINS':
            draw_winning_line(screen, settings)
        game_over_screen.msg = settings.game_over_msg
        game_over_screen.prep_msg()
        game_over_screen.draw_game_over_screen()
        play_button.draw_button()
    pg.display.update()
