import pygame

colors = [(200, 200, 200), (150, 150, 150)]


class SpecButton(pygame.sprite.Sprite):

    def __init__(self, size, pos, func):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface(size, flags=pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - size[0] / 2
        self.rect.y = pos[1] - size[1] / 2
        self.position = pos
        self.size = size
        self.func = func

        if self.func == "menu":
            self.png = pygame.transform.scale(pygame.image.load("data/images/level/buttons/menu.png"), size).convert_alpha()
            self.png_hover = pygame.transform.scale(pygame.image.load("data/images/level/buttons/menu_hover.png"),
                                                    size).convert_alpha()
        elif self.func == "refresh":
            self.png = pygame.transform.scale(pygame.image.load("data/images/level/buttons/refresh.png"), size).convert_alpha()
            self.png_hover = pygame.transform.scale(pygame.image.load("data/images/level/buttons/refresh_hover.png"),
                                                    size).convert_alpha()

        self.image.blit(self.png, (0, 0))

    def check(self, hover=False):
        if hover:
            self.image.blit(self.png_hover, (0, 0))
        else:
            self.image.blit(self.png, (0, 0))

