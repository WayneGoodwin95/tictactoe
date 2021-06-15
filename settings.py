import pygame as pg


class Settings():
    """A class to store all the settings of tic tac toe"""

    def __init__(self):
        """initialise game settings"""
        self.screen_width = 800
        self.screen_height = 800
        self.bg_color = (255, 255, 255)

        # load assets  images for markers for each player
        self.image_x = 'images/X-tictactoe3.bmp'
        self.image_o = 'images/O-tictactoe4.bmp'

        # game board rows and cols
        self.rows = 3
        self.cols = 3

        # game state
        self.player = 1
        self.game_active = True

        self.turn_counter = 1

        self.game_over_msg = ''

    def change_player(self):
        if self.player == 1:
            self.player = 2
        elif self.player == 2:
            self.player = 1
        self.turn_counter += 1
        print('Turn ' + str(self.turn_counter) + ': Player ' + str(self.player))


class Tile(Settings):

    def __init__(self, screen, row, col):
        Settings.__init__(self)

        self.screen = screen

        self.width = int(self.screen_width / 3)
        self.height = int(self.screen_height / 3)

        self.x_pos = int(self.width * row)
        self.y_pos = int(self.height * col)

        # Build the button's rect object and center it.
        self.rect = pg.Rect(self.x_pos, self.y_pos, self.width, self.height)

        self.active = True
        self.player = 0
        self.image = ''

    def update_tile(self, player):
        self.player = player
        if self.player == 1:
            self.image = self.image_x
        elif self.player == 2:
            self.image = self.image_o

    def draw_tile(self):
        # Draw empty tile
        pg.draw.rect(self.screen, self.bg_color, self.rect)
        # if tile has been played on... draw the image
        if not self.image == '':
            image = pg.image.load(self.image)
            image_rect = image.get_rect()
            image_rect.center = self.rect.center
            self.screen.blit(image, image_rect)


class Lines(Settings):

    def __init__(self, screen):
        Settings.__init__(self)

        self.screen = screen

        # game board lines
        self.line_color = (0, 0, 0)
        self.line_width = int((self.screen_height + self.screen_width) / 200)
        self.line_1_y = int(self.screen_height / 3)
        self.line_2_y = int(self.line_1_y * 2)
        self.line_3_x = int(self.screen_width / 3)
        self.line_4_x = int(self.line_3_x * 2)

        self.winning_line_start_xy = ()
        self.winning_line_end_xy = ()
        self.winning_line_color = 'Green'
        self.winning_line_width = 3 * self.line_width

    def draw_lines(self):
        pg.draw.line(self.screen, self.line_color, (0, self.line_1_y),
                     (self.screen_width, self.line_1_y), self.line_width)
        # second horizontal line
        pg.draw.line(self.screen, self.line_color, (0, self.line_2_y),
                     (self.screen_width, self.line_2_y), self.line_width)
        # first vertical line
        pg.draw.line(self.screen, self.line_color, (self.line_3_x, 0),
                     (self.line_3_x, self.screen_height), self.line_width)
        # second vertical line
        pg.draw.line(self.screen, self.line_color, (self.line_4_x, 0),
                     (self.line_4_x, self.screen_height), self.line_width)

    def draw_winning_line(self):
        # first horizontal line
        pg.draw.line(self.screen, self.winning_line_color, self.winning_line_start_xy,
                     self.winning_line_end_xy, self.winning_line_width)