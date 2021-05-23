class Settings():
    """A class to store all the settings of tic tac toe"""

    def __init__(self):
        """initialise game settings"""
        self.screen_width = 800
        self.screen_height = 800
        self.bg_color = (255, 255, 255)

        # game board rows and cols
        self.rows = 3
        self.cols = 3

        # game board lines
        self.line_color = (0, 0, 0)
        self.line_width = int((self.screen_height + self.screen_width) / 200)
        self.line_1_y = int(self.screen_height / 3)
        self.line_2_y = int(self.line_1_y * 2)
        self.line_3_x = int(self.screen_width / 3)
        self.line_4_x = int(self.line_3_x * 2)

        # tile
        self.tile_color = (255, 255, 255)
        self.tile_length = self.line_1_y
        self.tile_height = self.line_3_x

        # game state
        self.player = 1
        self.game_active = True

        self.turn_counter = 1

        self.game_over_msg = ''

        self.winning_line_start_xy = ()
        self.winning_line_end_xy = ()
        self.winning_line_color = 'Green'
        self.winning_line_width = 3 * self.line_width
