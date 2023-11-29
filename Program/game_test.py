import pygame
import os
import sys
import func_block


class Test:
    def __init__(self, screen_size):
        self.surface = pygame.surface.Surface(screen_size, pygame.SRCALPHA)
        self.screen_size = screen_size
        self.functions = pygame.sprite.Group()
        function = func_block.Function()
        self.functions.add(function)
        self.functions.draw(self.surface)

    def res_change(self, screen_size):
        self.surface = pygame.surface.Surface(screen_size, pygame.SRCALPHA)

    def hover(self, mouse_pos):
        self.surface = pygame.surface.Surface(self.screen_size, pygame.SRCALPHA)
        for func in self.functions:
            if func.rect.collidepoint(mouse_pos):
                func.check(True)
            else:
                func.check(False)
        self.functions.draw(self.surface)
