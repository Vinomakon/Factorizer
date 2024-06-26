import math
import pygame
import button
import slider


class GameEnd:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        ratio = screen_size[0] / 2560  # For different screen sizes

        # Loading of all images
        self.play = pygame.image.load("data/images/menu/play.png").convert_alpha()
        play_size = self.play.get_size()
        self.play = pygame.transform.scale(self.play, (play_size[0] / 2.8 * (screen_size[0] / 2560),
                                                       play_size[0] / 2.8 * (screen_size[1] / 2560)))
        self.play_pos = (-55 * (screen_size[0] / 2560), -55 * (screen_size[0] / 2560))

        self.end_png = pygame.transform.scale(pygame.image.load("data/images/menu/end.png"), (screen_size[0], ratio * 1440))

        # Image from // https://famouscookies.com/product/chocolate-chip-cookies/
        self.cookie = pygame.image.load("data/images/menu/cookie.png")
        self.cookie_size = self.cookie.get_size()
        self.cookie = pygame.transform.scale(self.cookie, (self.cookie_size[0] / 1.5 * ratio, self.cookie_size[1] / 1.5 * ratio))
        self.cookie_size = self.cookie.get_size()

        self.surface = pygame.surface.Surface(screen_size, pygame.SRCALPHA)

        # Setup which sub-screen the player is on
        self.menu_type = 0

        ratio = screen_size[0] / 2560

        # All objects for the game end
        menu_button = button.Button((int(250 * ratio), int(100 * ratio)), (screen_size[0] / 2, screen_size[1] / 1.1), "Menu", "menu")
        exit_button = button.Button((int(700 * ratio), int(150 * ratio)), (screen_size[0] / 2, screen_size[1] / 1.35), "Exit", "exit")
        back_button = button.Button((int(250 * ratio), int(70 * ratio)), (screen_size[0] / 10, screen_size[1] / 1.1),
                                    "Cookie", 1)
        self.menu_buttons = pygame.sprite.Group()
        self.menu_buttons.add(menu_button, exit_button, back_button)

        # A button to come back from the cookie screen
        cookie_button = button.Button((int(400 * ratio), int(130 * ratio)), (screen_size[0] / 10, screen_size[1] / 1.1), "Back", 0)
        self.cookie_buttons = pygame.sprite.Group()
        self.cookie_buttons.add(cookie_button)

    def on_click(self, click_pos):
        # Based on which subsection the player is on, different buttons are shown and used.
        # So for each subsection, a different approach is taken
        if self.menu_type == 0:  # Main end screen
            # For each and every button it gets checked if the mouse is on the button when the mouse-button was pressed
            for but in self.menu_buttons:
                if but.rect.collidepoint(click_pos):
                    # If it is, it checks whether it refers to a subsection or a different screen
                    if isinstance(but.func, int):
                        self.menu_type = but.func
                    else:
                        return but.func, "button"
            return None, None
        elif self.menu_type == 1: # Cookie screen
            # For each and every button it gets checked if the mouse is on the button when the mouse-button was pressed
            for but in self.cookie_buttons:
                if but.rect.collidepoint(click_pos):
                    # If it is, it checks whether it refers to a subsection or a different screen
                    if isinstance(but.func, int):
                        self.menu_type = but.func
                    else:
                        return but.func, "button"
            return None, None

    def refresh(self, mouse_pos):
        # First the background gets displayed
        self.surface.blit(self.play, (self.play_pos[0], self.play_pos[1]))
        # Then per subsection, the appropriate GUI is displayed
        if self.menu_type == 0:
            self.surface.blit(self.end_png, (0, 0))
            # Checking if the mouse is over the button to create a hover effect
            for but in self.menu_buttons:
                if but.rect.collidepoint(mouse_pos):
                    but.check(True)
                else:
                    but.check(False)
            self.menu_buttons.draw(self.surface)
        elif self.menu_type == 1:
            self.surface.blit(self.cookie, (self.screen_size[0] / 2 - self.cookie.get_rect().center[0], self.screen_size[1] / 2 - self.cookie.get_rect().center[1]))
            # Checking if the mouse is over the button to create a hover effect
            for but in self.cookie_buttons:
                if but.rect.collidepoint(mouse_pos):
                    but.check(True)
                else:
                    but.check(False)
            self.cookie_buttons.draw(self.surface)
