import math
import pygame
import button
import slider


class MainScreen:
    def __init__(self, screen_size, current_level, volumes):
        self.play = pygame.image.load("data/images/menu/play.png").convert_alpha()
        play_size = self.play.get_size()
        self.play = pygame.transform.scale(self.play, (play_size[0] / 2.8 * (screen_size[0] / 2560),
                                                       play_size[0] / 2.8 * (screen_size[1] / 2560)))
        self.play_pos = (-55 * (screen_size[0] / 2560), -55 * (screen_size[0] / 2560))

        self.title = pygame.image.load("data/images/menu/title.png").convert_alpha()
        title_size = self.title.get_size()
        self.title = pygame.transform.scale(self.title,
                                       ((title_size[0] / 4) * (screen_size[0] / 2560),
                                        (title_size[1] / 4) * (screen_size[0] / 2560)))
        title_size = self.title.get_size()
        self.title_pos = (screen_size[0] / 2 - title_size[0] / 2, screen_size[1] / 5 - title_size[1] / 2)

        self.surface = pygame.surface.Surface(screen_size, pygame.SRCALPHA)
        self.menu_type = 0

        ratio = screen_size[0] / 2560

        # All objects for the main menu
        start_button = button.Button((int(700 * ratio), int(150 * ratio)), (screen_size[0] / 2, screen_size[1] / 2.3), "Start", 1)
        options_button = button.Button((int(700 * ratio), int(150 * ratio)), (screen_size[0] / 2, screen_size[1] / 1.7), "Options", 2)
        credits_button = button.Button((int(700 * ratio), int(150 * ratio)), (screen_size[0] / 2, screen_size[1] / 1.35), "Credits", 3)
        exit_button = button.Button((int(250 * ratio), int(100 * ratio)), (screen_size[0] / 2, screen_size[1] / 1.1), "Exit", "exit")
        self.menu_buttons = pygame.sprite.Group()
        self.menu_buttons.add(start_button, exit_button, options_button, credits_button)

        # All objects for the level menu
        self.level_buttons = pygame.sprite.Group()
        for lev_but in range(16):
            but = button.Button((int(200 * ratio), int(200 * ratio)), (screen_size[0] / 3.5 + 400 * ratio * (lev_but % 4), screen_size[1] / 6 + 300 * ratio * math.floor(lev_but / 4)), str(lev_but + 1), [lev_but], active=True if lev_but <= current_level else False )
            self.level_buttons.add(but)
        back_button = button.Button((int(400 * ratio), int(130 * ratio)), (screen_size[0] / 10, screen_size[1] / 1.1), "Back", 0)
        self.level_buttons.add(back_button)

        # All objects for the options menu
        back_button = button.Button((int(400 * ratio), int(130 * ratio)), (screen_size[0] / 10, screen_size[1] / 1.1), "Back", 0)
        music_volume = slider.Slider((int(600 * ratio), int(160 * ratio)), (screen_size[0] / 1.53, screen_size[1] / 3), "Music volume", volumes[0], "music")
        sound_volume = slider.Slider((int(600 * ratio), int(160 * ratio)), (screen_size[0] / 7, screen_size[1] / 3),
                                     "Sound volume", volumes[1], "sound")
        self.options_buttons = pygame.sprite.Group()
        self.options_buttons.add(back_button)
        self.options_sliders = pygame.sprite.Group()
        self.options_sliders.add(music_volume)
        self.options_sliders.add(sound_volume)

        # All objects for the credits:
        self.credits_img = pygame.transform.scale(pygame.image.load("data/images/menu/credits.png").convert_alpha(), (screen_size[0], 1440 * ratio))
        back_button = button.Button((int(400 * ratio), int(130 * ratio)), (screen_size[0] / 10, screen_size[1] / 1.1), "Back", 0)
        self.credits_buttons = pygame.sprite.Group()
        self.credits_buttons.add(back_button)

    def on_click(self, click_pos):
        if self.menu_type == 0:
            for but in self.menu_buttons:
                if but.rect.collidepoint(click_pos):
                    if isinstance(but.func, int):
                        self.menu_type = but.func
                    else:
                        return but.func, "button"
            return None, None
        elif self.menu_type == 1:
            for but in self.level_buttons:
                if but.rect.collidepoint(click_pos):
                    if isinstance(but.func, int):
                        self.menu_type = but.func
                    else:
                        return but.func, "button"
            return None, None
        elif self.menu_type == 2:
            for but in self.options_buttons:
                if but.rect.collidepoint(click_pos):
                    if isinstance(but.func, int):
                        self.menu_type = but.func
                    else:
                        return but.func, "button"
            for slid in self.options_sliders:
                if slid.loc_circle_rect.collidepoint(click_pos):
                    slid.sliding = True
            return None, None
        elif self.menu_type == 3:
            for but in self.credits_buttons:
                if but.rect.collidepoint(click_pos):
                    if isinstance(but.func, int):
                        self.menu_type = but.func
                    else:
                        return but.func, "button"
            return None, None

    def on_release(self, mouse_pos):
        if self.menu_type == 2:
            for slid in self.options_sliders:
                slid.sliding = False

    def refresh(self, mouse_pos):
        self.surface.blit(self.play, (self.play_pos[0], self.play_pos[1]))
        if self.menu_type == 0:  # Main Menu
            self.surface.blit(self.title, (self.title_pos[0], self.title_pos[1]))
            for but in self.menu_buttons:
                if but.rect.collidepoint(mouse_pos):
                    but.check(True)
                else:
                    but.check(False)
            self.menu_buttons.draw(self.surface)
        elif self.menu_type == 1:  # Level Menu
            for but in self.level_buttons:
                if but.rect.collidepoint(mouse_pos):
                    but.check(True)
                else:
                    but.check(False)
            self.level_buttons.draw(self.surface)
        elif self.menu_type == 2:  # Options Menu
            for but in self.options_buttons:
                if but.rect.collidepoint(mouse_pos):
                    but.check(True)
                else:
                    but.check(False)
            slider_values = []
            for slid in self.options_sliders:
                slider_values.append(slid.refresh(mouse_pos))
            self.options_buttons.draw(self.surface)
            self.options_sliders.draw(self.surface)
            return slider_values
        elif self.menu_type == 3:
            for but in self.credits_buttons:
                if but.rect.collidepoint(mouse_pos):
                    but.check(True)
                else:
                    but.check(False)
            self.credits_buttons.draw(self.surface)
            self.surface.blit(self.credits_img, (0, 0))
