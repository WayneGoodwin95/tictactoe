import pygame as pg


class Tile():

    def __init__(self, screen, row, col, image_x, image_o):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.color = (255, 255, 255)
        self.width = int(self.screen_rect.width / 3)
        self.height = int(self.screen_rect.height / 3)

        self.image_x = image_x
        self.image_o = image_o

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
        pg.draw.rect(self.screen, self.color, self.rect)
        # if tile has been played on... draw the image
        if not self.image == '':
            image = pg.image.load(self.image)
            image_rect = image.get_rect()
            image_rect.center = self.rect.center
            self.screen.blit(image, image_rect)