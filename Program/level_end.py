import pygame
import button
import math

path = "data/images/"

font = "data/fonts/Bebas-Regular.ttf"


class Text:
    def __init__(self, size, text):
        self.lines = []
        line = ""
        self.text_surface = pygame.surface.Surface(size,
                                                   flags=pygame.SRCALPHA)
        for letter in text:
            if letter == "\n":
                self.lines.append(line)
                line = ""
            else:
                line += letter
        self.lines.append(line)
        for line in range(len(self.lines)):
            self.font_render = pygame.font.Font(font, int(size[1] / len(self.lines) * (1 / 3) + 15))
            self.text_render = self.font_render.render(self.lines[line], True, (255, 255, 255))
            self.text_rect = self.text_render.get_rect(
                center=(size[0] / 2, int(size[1] * (1 / 3) - 5)), y=(line * int(size[1] / len(self.lines) * (1 / 3) + 15)))
            self.text_surface.blit(self.text_render, self.text_rect)


class LevelEnd:
    def __init__(self, screen_size, level, quality, level_time):
        self.surface = pygame.surface.Surface(screen_size, pygame.SRCALPHA)
        self.surface.fill(pygame.Color(0, 0, 0, 100))

        ratio = screen_size[0] / 2560

        title = Text((int(2000 * ratio), int(800 * ratio)), f"Level {level + 1} Complete")
        self.surface.blit(title.text_surface, (screen_size[0] / 2 - title.text_rect.width / 2 - title.text_rect.x, screen_size[1] / 6))

        restart_button = button.Button((int(700 * ratio), int(150 * ratio)), (screen_size[0] / 2, screen_size[1] / 1.5), "Restart", "restart")
        next_button = button.Button((int(700 * ratio), int(150 * ratio)), (screen_size[0] / 2, screen_size[1] / 2), "Next Level", "next")
        exit_button = button.Button((int(250 * ratio), int(75 * ratio)), (screen_size[0] / 2, screen_size[1] / 1.1), "Menu", "menu")
        self.buttons = pygame.sprite.Group()
        self.buttons.add(restart_button, exit_button, next_button)
        self.buttons.draw(self.surface)
        if level != 0:
            quality_text = Text((int(900 * ratio), int(400 * ratio)), f"Used blocks: {quality[1]}\nRecord use of blocks: {quality[0]}")
            self.surface.blit(quality_text.text_surface, (screen_size[0] / 1.55, screen_size[0] / 2.6))

        seconds = str(math.floor(level_time[0]) % 60)
        if len(seconds) == 1:
            seconds = f"0{seconds}"
        minutes = str(math.floor(level_time[0] / 60))
        if len(minutes) == 1:
            minutes = f"0{minutes}"

        seconds_ = str(math.floor(level_time[1]) % 60)
        if len(seconds_) == 1:
            seconds_ = f"0{seconds_}"
        minutes_ = str(math.floor(level_time[1] / 60))
        if len(minutes_) == 1:
            minutes_ = f"0{minutes_}"
        time_text = Text((int(900 * ratio), int(400 * ratio)), f"Time spent: {minutes}:{seconds}\nRecord time: {minutes_}:{seconds_}")
        self.surface.blit(time_text.text_surface, (screen_size[0] / 60, screen_size[0] / 2.6))

    def on_click(self, click_pos):
        for but in self.buttons:
            if but.rect.collidepoint(click_pos):
                return but.func, "button"

    def refresh(self, mouse_pos):

        for but in self.buttons:
            if but.rect.collidepoint(mouse_pos):
                but.check(True)
            else:
                but.check(False)
            self.buttons.draw(self.surface)

