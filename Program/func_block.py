import copy

import pygame
import os
import sys

images = {"delete": ["delete.png", [0], [1, 0]],
          "cut": ["cut.png", [0], [0, 0]],
          "paint": ["paint.png", [0, 1], [0]],
          "color": ["color.png", [1, 1], [1]],
          "merge": ["merge.png", [0, 0], [0]],
          "rotate_cw": ["rotate_cw.png", [0], [0]],
          "rotate_ccw": ["rotate_ccw.png", [0], [0]],
          "rotate_full": ["rotate_full.png", [0], [0]]}

path = "images/"

class Dot(pygame.sprite.Sprite):
    def __init__(self, type, config, func_size, input=True):
        pygame.sprite.Sprite.__init__(self)
        if type == 1:
            self.image = pygame.image.load("images/dot.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (20, self.image.get_size()[1] * (20 / self.image.get_size()[0])))
            self.rect = self.image.get_rect()
            self.rect.center = (10, 10)
        else:
            self.image = pygame.image.load("images/sdot.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (20, self.image.get_size()[1] * (20 / self.image.get_size()[0])))
            self.rect = self.image.get_rect()
            self.rect.center = (10, 10)

        self.rect.x = 20 if input else func_size[0] - 40
        self.rect.y = func_size[1] / 2 - 10 + config
        print(self.rect.y if not input else "huh")


class Function(pygame.sprite.Sprite):
    def __init__(self, func_type, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.function = func_type
        self.spawn_pos = pos

        self.func_image = pygame.image.load(path + images["delete"][0])
        self.func_image = pygame.transform.scale(self.func_image, (200, self.func_image.get_size()[1] * (200 / self.func_image.get_size()[0])))

        self.dot_image = pygame.image.load("images/dot.png").convert_alpha()
        self.dot_image = pygame.transform.scale(self.dot_image, (20, self.dot_image.get_size()[1] * (20 / self.dot_image.get_size()[0])))
        self.dot_rect = self.dot_image.get_rect()
        self.dot_rect.center = (10, 10)

        self.sdot_image = pygame.image.load("images/sdot.png").convert_alpha()
        self.sdot_image = pygame.transform.scale(self.sdot_image, (20, self.sdot_image.get_size()[1] * (20 / self.sdot_image.get_size()[0])))
        self.sdot_rect = self.sdot_image.get_rect()
        self.sdot_rect.center = (10, 10)

        self.image = pygame.surface.Surface(self.func_image.get_size(), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.input = pygame.sprite.Group()
        self.output = pygame.sprite.Group()

        self.image.blit(self.func_image, (0, 0))

        for inp in range(len(images[func_type][1])):
            if images[func_type][1][inp] == 1:
                dot1 = Dot(1, (20 if len(images[func_type][1]) > 1 else 0) * ((-1) ** inp), self.rect.size, True)
                self.input.add(dot1)
            if images[func_type][1][inp] == 0:
                dot2 = Dot(0, (20 if len(images[func_type][1]) > 1 else 0) * ((-1) ** inp), self.rect.size, True)
                self.input.add(dot2)
        self.input.draw(self.image)

        for inp in range(len(images[func_type][2])):
            if images[func_type][2][inp] == 1:
                dot3 = Dot(1, (20 if len(images[func_type][2]) > 1 else 0) * ((-1) ** inp), self.rect.size, False)
                self.output.add(dot3)
            if images[func_type][2][inp] == 0:
                dot4 = Dot(0, (20 if len(images[func_type][2]) > 1 else 0) * ((-1) ** inp), self.rect.size, False)
                self.output.add(dot4)
        self.output.draw(self.image)

        self.move_with_mouse = False
        self.init_pos = pos
        self.start_drag = (0, 0)

        # self.image.blit(self.dot_image, (20, self.func_image.get_size()[1] / 2 - 10))

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
