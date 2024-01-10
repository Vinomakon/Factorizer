import pygame
import button
import math

path = "data/images/"

font = "data/fonts/Bebas-Regular.ttf"


class Text:
    def __init__(self, size, text):

        self.text_surface = pygame.surface.Surface(size, flags=pygame.SRCALPHA)
        self.font_render = pygame.font.Font(font, int(size[1] * (1 / 3) + 15))
        self.text_render = self.font_render.render(text, True, (255, 255, 255))
        self.text_rect = self.text_render.get_rect(
            center=(size[0] / 2, int(size[1] * (1 / 3) - 5)))
        self.text_surface.blit(self.text_render, self.text_rect)


class LevelEnd:
    def __init__(self, screen_size, level, quality, level_time):
        title = pygame.image.load("data/images/complete.png").convert_alpha()
        title_size = title.get_size()
        title = pygame.transform.scale(title,
                                       ((title_size[0] / 4) * (screen_size[0] / 2560),
                                        (title_size[1] / 4) * (screen_size[0] / 2560)))
        title_size = title.get_size()
        title_pos = (screen_size[0] / 2 - title_size[0] / 2, screen_size[1] / 5 - title_size[1] / 2)
        self.surface = pygame.surface.Surface(screen_size, pygame.SRCALPHA)
        self.surface.fill(pygame.Color(0, 0, 0, 100))
        self.surface.blit(title, (title_pos[0], title_pos[1]))

        restart_button = button.Button((700, 150), (screen_size[0] / 2, screen_size[1] / 1.5), "Restart", "restart")
        next_button = button.Button((700, 150), (screen_size[0] / 2, screen_size[1] / 2), "Next Level", "next")
        exit_button = button.Button((250, 75), (screen_size[0] / 2, screen_size[1] / 1.1), "Menu", "menu")
        self.buttons = pygame.sprite.Group()
        self.buttons.add(restart_button, exit_button, next_button)
        self.buttons.draw(self.surface)
        if level != 1:
            quality_text = Text((700, 150), f"Used blocks: {quality}")
            self.surface.blit(quality_text.text_surface, (0, 0))

        seconds = str(math.floor(level_time) % 60)
        if len(seconds) == 1:
            seconds = f"0{seconds}"
        minutes = str(math.floor(level_time / 60))
        if len(minutes) == 1:
            minutes = f"0{minutes}"
        time_text = Text((700, 150), f"Time spent: {minutes}:{seconds}")
        self.surface.blit(time_text.text_surface, (0, 300))

    def on_click(self, click_pos):
        for but in self.buttons:
            if but.rect.collidepoint(click_pos):
                return but.func

    def refresh(self, mouse_pos):

        for but in self.buttons:
            if but.rect.collidepoint(mouse_pos):
                but.check(True)
            else:
                but.check(False)
            self.buttons.draw(self.surface)

