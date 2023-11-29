import pygame
import os
import sys


class Function(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.surface.Surface((200, 150), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (800, 800)
        pygame.draw.rect(self.image, (255, 0, 0), (0, 0, 200, 133), 0)

    def check(self, hover=False):
        self.image = pygame.surface.Surface((200, 150), pygame.SRCALPHA)
        if hover:
            pygame.draw.rect(self.image, (200, 0, 0), (0, 0, 200, 133), 0)
        else:
            pygame.draw.rect(self.image, (255, 0, 0), (0, 0, 200, 133), 0)