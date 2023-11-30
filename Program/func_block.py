import pygame
import os
import sys

images = {"delete": "images/delete.png"}


class Function(pygame.sprite.Sprite):
    def __init__(self, func_type, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.spawn_pos = pos

        self.func_image = pygame.image.load(images["delete"])
        self.func_image = pygame.transform.scale(self.func_image, (200, self.func_image.get_size()[1] * (200 / self.func_image.get_size()[0])))

        self.dot_image = pygame.image.load("images/dot.png").convert_alpha()
        self.dot_image = pygame.transform.scale(self.dot_image, (20, self.dot_image.get_size()[1] * (20 / self.dot_image.get_size()[0])))
        self.dot_rect = self.dot_image.get_rect()
        self.dot_rect.center = (10, 10)
        self.dot_rect.x = 20 + pos[0]
        self.dot_rect.y = self.func_image.get_size()[1] / 2 - 10 + pos[1]

        self.image = pygame.surface.Surface((200, 150), pygame.SRCALPHA)

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.move_with_mouse = False
        self.init_pos = pos
        self.start_drag = (0, 0)
        self.image.blit(self.func_image, (0, 0))
        self.image.blit(self.dot_image, (20, self.func_image.get_size()[1] / 2 - 10))

    def check(self, mouse_pos):
        if self.dot_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            return True, self.dot_rect.center
        else:
            return False, (0, 0)

    def draggable(self, state, mouse_pos):
        self.move_with_mouse = state
        if state:
            self.start_drag = mouse_pos
        else:
            self.init_pos = (self.rect.x, self.rect.y)
            self.dot_rect.x = 20 + self.init_pos[0]
            self.dot_rect.y = self.func_image.get_size()[1] / 2 - 10 + self.init_pos[1]

    def update(self, mouse_pos):
        if self.move_with_mouse:
            self.rect.x = self.init_pos[0] - self.start_drag[0] + mouse_pos[0]
            self.rect.y = self.init_pos[1] - self.start_drag[1] + mouse_pos[1]
