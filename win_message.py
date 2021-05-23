import pygame.font


class Game_over():
    def __init__(self, screen, settings, game_over_msg):
        """Initialise button attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings

        # Set the dimensions and properties of the button.
        self.width = self.settings.screen_width / 10
        self.height = self.settings.screen_height / 10
        self.bg_color = settings.bg_color
        self.text_color = (255, 24, 24)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.centery -= (settings.screen_height / 10)

        # The button message needs to be prepped only once
        self.msg = settings.game_over_msg
        self.prep_msg()

    def prep_msg(self):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(self.msg, True, self.text_color, None)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_game_over_screen(self):
        # Draw blank button and then draw message.
        self.screen.blit(self.msg_image, self.msg_image_rect)
