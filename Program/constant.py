import pygame
import shape


class Dot(pygame.sprite.Sprite):
    def __init__(self, type, func_size, pos, data, out=True):
        pygame.sprite.Sprite.__init__(self)
        self.func_size = func_size
        self.type = type
        self.inputs = input
        self.connecting = False
        self.connected = False
        self.connection = ()

        self.data = data

        if type == 0:
            self.image = pygame.image.load("images/dot.png").convert_alpha()
            self.image = pygame.transform.scale(self.image,
                                                (20, self.image.get_size()[1] * (20 / self.image.get_size()[0])))
            self.rect = self.image.get_rect()
            self.rect.center = (10, 10)
            self.loc_rect = self.image.get_rect()
            self.loc_rect.center = (10, 10)
        else:
            self.image = pygame.image.load("images/sdot.png").convert_alpha()
            self.image = pygame.transform.scale(self.image,
                                                (20, self.image.get_size()[1] * (20 / self.image.get_size()[0])))
            self.rect = self.image.get_rect()
            self.rect.center = (10, 10)
            self.loc_rect = self.image.get_rect()
            self.loc_rect.center = (10, 10)

        self.rect.x = 11 if not out else func_size[0] - 32
        self.rect.y = func_size[1] / 2 - 10
        self.loc_rect.x = 11 if not out else func_size[0] - 32 + pos[0]
        self.loc_rect.y = func_size[1] / 2 - 10 + pos[1]


class Constant(pygame.sprite.Sprite):
    def __init__(self, pos, data, inp=False):
        pygame.sprite.Sprite.__init__(self)

        self.l_image = pygame.image.load("images/constant.png").convert_alpha()
        self.l_image = pygame.transform.scale(self.l_image, (150, (150 / self.l_image.get_size()[0]) * self.l_image.get_size()[1]))
        if inp == 1:
            self.l_image = pygame.transform.rotate(self.l_image, 180)

        self.image = pygame.surface.Surface(self.l_image.get_size(), flags=pygame.SRCALPHA)
        self.display = None

        self.rect = self.image.get_rect()
        self.rect.center = (75, 75)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        if isinstance(data, str):
            type = 0
            self.display = shape.Shape(data)

        else:
            type = 1

        self.dot = Dot(type, self.rect.size, (self.rect.x, self.rect.y), data, not inp)

        self.image.blit(self.l_image, (0, 0))
        self.image.blit(self.dot.image, self.dot.rect)
        self.image.blit(pygame.transform.scale(self.display.surface, (80, 80)),
                        (self.image.get_size()[0] / 2 - 55, self.image.get_size()[1] / 2 - 40))

    def check(self, mouse_pos):
        on_dot = False
        available = False
        dot_pos = ()
        op_type = None
        data_type = None
        from_dot = None
        print(mouse_pos)
        print(self.dot.rect)
        if self.dot.loc_rect.collidepoint(mouse_pos):
            on_dot = True
            available = not (self.dot.connecting or self.dot.connected)
            dot_pos = self.dot.loc_rect.center
            op_type = 0
            data_type = self.dot.type
            from_dot = self.dot
        return on_dot, available, dot_pos, op_type, data_type, from_dot
