import pygame

path = "images/spawner/"
functions = ["delete", "rotate_cw", "rotate_ccw", "rotate_full", "cut", "color", "paint", "merge"]

class Func(pygame.sprite.Sprite):
    def __init__(self, func, ratio, bar_rect):
        pygame.sprite.Sprite.__init__(self)
        self.func = func
        self.image = pygame.image.load(f"{path}{functions[func]}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * (ratio / 2560), self.image.get_size()[1] * (ratio / 2560)))
        self.rect = self.image.get_rect()
        self.rect.x = 18 + 9 * func + self.image.get_size()[0] * func
        self.rect.y = 71 / 4
        self.l_rect = self.image.get_rect()
        self.l_rect.x = 18 + 9 * func + self.image.get_size()[0] * func + bar_rect.x
        self.l_rect.y = 71 / 4 + bar_rect.y


class Spawner:
    def __init__(self, allowance):
        self.allowance = allowance

        self.bar = pygame.image.load(f"{path}bar.png").convert_alpha()
        size_w = 1000
        self.bar = pygame.transform.scale(self.bar, (size_w, self.bar.get_size()[1] * (size_w / 2560)))

        self.image = pygame.surface.Surface(self.bar.get_size(), flags=pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = 2560 / 2 - self.bar.get_size()[0] / 2
        self.rect.y = 1440 - self.bar.get_size()[1]

        self.func_buttons = pygame.sprite.Group()

        for func in range(8):
            if allowance[func] == 1:
                self.func_buttons.add(Func(func, size_w, self.rect))

        self.image.blit(self.bar, (0, 0))
        self.func_buttons.draw(self.image)

    def check(self, mouse_pos):
        for but in self.func_buttons:
            if but.l_rect.collidepoint(mouse_pos):
                return but.func
        return None
