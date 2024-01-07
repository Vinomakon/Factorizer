import pygame
import shape
import dot


class Constant(pygame.sprite.Sprite):
    def __init__(self, pos, data, inp=False):
        pygame.sprite.Sprite.__init__(self)

        self.inp = inp
        self.data = data

        self.display = shape.Shape(self.data, 0, 0, 0, True)

        self.l_image = pygame.image.load("data/images/constant.png").convert_alpha()
        self.l_image = pygame.transform.scale(self.l_image, (150, (150 / self.l_image.get_size()[0]) * self.l_image.get_size()[1]))
        if inp:
            self.l_image = pygame.transform.rotate(self.l_image, 180)
            self.received = False

        self.image = pygame.surface.Surface(self.l_image.get_size(), flags=pygame.SRCALPHA)

        self.rect = self.image.get_rect()
        self.rect.center = (75, 75)
        self.rect.x = pos[0]
        self.rect.y = pos[1] - self.l_image.get_size()[1] / 2
        self.rect_pos = (self.rect.x + self.rect.width - 34 if not inp else self.rect.x + 14, self.rect.y + self.rect.height / 2)

        if len(self.data) > 1:
            self.dot = dot.Dot(0, 0, self.rect.size, self.rect_pos, inp, const=True)
        elif len(self.data) == 1:
            self.dot = dot.Dot(1, 0, self.rect.size, self.rect_pos, inp, const=True)

        self.image.blit(self.l_image, (0, 0))
        self.image.blit(self.dot.image, (self.rect.width - 34 if not inp else 14, self.rect.height / 2 - 10))

        self.image.blit(pygame.transform.scale(self.display.surface, (80, 80)),
                        (self.image.get_size()[0] / 2 - 57 if not inp else 55, self.image.get_size()[1] / 2 - 40))

    def check(self, mouse_pos):
        on_dot = False
        available = False
        dot_pos = ()
        op_type = None
        data_type = None
        from_dot = None
        if self.dot.loc_rect.collidepoint(mouse_pos):
            on_dot = True
            available = True  # not (self.dot.connecting or self.dot.connected)
            self.dot.del_connection()
            dot_pos = self.dot.loc_rect.center
            op_type = self.dot.input_
            data_type = self.dot.type
            from_dot = self.dot
        return on_dot, available, dot_pos, op_type, data_type, from_dot

    def send_data(self):
        if not self.inp:
            self.dot.send_data(self.data)

    def del_data(self):
        self.dot.data = None

    def check_goal(self):
        if self.dot.data == self.data and self.inp:
            return True
