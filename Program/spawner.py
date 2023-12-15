import pygame

path = "images/spawner/"
functions = ["delete", "rotate_cw", "rotate_ccw", "rotate_full", "cut", "color", "paint", "merge"]


class Func(pygame.sprite.Sprite):
    def __init__(self, screen_size, func, ratio, bar_rect):
        pygame.sprite.Sprite.__init__(self)
        self.func = func
        self.image = pygame.image.load(f"{path}{functions[func]}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * (ratio * (screen_size[0] / 2560)), self.image.get_size()[1] * (ratio * (screen_size[0] / 2560))))
        self.rect = self.image.get_rect()
        self.rect.x = (18 + 36 * func + self.image.get_size()[0] * func) * (screen_size[0] / 2560)
        self.rect.y = (bar_rect.h / 5.8) * (screen_size[0] / 2560)
        self.l_rect = self.image.get_rect()
        self.l_rect.x = (18 + 36 * func + self.image.get_size()[0] * func) * (screen_size[0] / 2560) + bar_rect.x
        self.l_rect.y = (bar_rect.h / 5.8) * (screen_size[0] / 2560) + bar_rect.y


class Spawner(pygame.sprite.Sprite):
    def __init__(self, screen_size, allowance):
        pygame.sprite.Sprite.__init__(self)
        self.allowance = allowance

        self.bar = pygame.image.load(f"{path}bar.png").convert_alpha()
        ratio = 1000/2560
        print(self.bar.get_size())
        self.bar = pygame.transform.scale(self.bar, (self.bar.get_size()[0] * ratio * (screen_size[0] / 2560), self.bar.get_size()[1] * ratio * (screen_size[0] / 2560)))

        self.image = pygame.surface.Surface(self.bar.get_size(), flags=pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = screen_size[0] / 2 - self.bar.get_size()[0] / 2
        self.rect.y = screen_size[1] - self.bar.get_size()[1]

        self.func_buttons = pygame.sprite.Group()

        for func in range(8):
            if allowance[func] == 1:
                self.func_buttons.add(Func(screen_size, func, ratio, self.rect))
        
        self.image.blit(self.bar, (0, 0))
        self.func_buttons.draw(self.image)

    def check(self, mouse_pos):
        for but in self.func_buttons:
            if but.l_rect.collidepoint(mouse_pos):
                return but.func
        return None
