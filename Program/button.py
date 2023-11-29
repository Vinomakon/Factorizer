import pygame
import os

colors = [(200, 200, 200), (150, 150, 150)]


class Button(pygame.sprite.Sprite):

    def __init__(self, size, pos, text, func, font="Bebas-Regular.ttf"):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - size[0] / 2
        self.rect.y = pos[1] - size[1] / 2
        self.position = pos
        self.text = text
        self.size = size
        self.font = font
        self.func = func

        font = pygame.font.Font(self.font, self.size[1] - 10)
        self.text_render = font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_render.get_rect(center=(self.size[0] / 2, self.size[1] / 2))
        self.check()

    def check(self, hover=False):
        if hover:
            self.image.fill(colors[1])
        else:
            self.image.fill(colors[0])
        self.image.blit(self.text_render, self.text_rect)




