import pygame
import shape
import dot


class Constant(pygame.sprite.Sprite):
    def __init__(self, screen_size, pos, data, inp=False):
        pygame.sprite.Sprite.__init__(self)

        # Initialization of all images
        self.inp = inp
        self.data = data

        self.display = shape.Shape(self.data, 0, 0, 0, True)

        self.l_image = pygame.image.load("data/images/level/constants/constant.png").convert_alpha()
        self.l_image = pygame.transform.scale(self.l_image,
                                              (150, (150 / self.l_image.get_size()[0]) * self.l_image.get_size()[1]))
        if inp:
            self.l_image = pygame.transform.rotate(self.l_image, 180)
            self.received = 0

        self.done_image = pygame.image.load("data/images/level/constants/done.png").convert_alpha()
        self.done_image = pygame.transform.scale(self.done_image, (
            70, (70 / self.done_image.get_size()[0]) * self.done_image.get_size()[1]))

        self.nums = []
        for nums in range(4):
            num = pygame.image.load(f"data/images/level/constants/{nums + 1}.png").convert_alpha()
            num = pygame.transform.scale(num, ((70 / num.get_size()[1]) * num.get_size()[0], 70))
            self.nums.append(num)

        self.image = pygame.surface.Surface(self.l_image.get_size(), flags=pygame.SRCALPHA)

        # Set the size and the position of the constant
        self.rect = self.image.get_rect()
        self.rect.center = (75, 75)
        self.rect.x = pos[0]
        self.rect.y = pos[1] - self.l_image.get_size()[1] / 2
        self.rect_pos = (
            self.rect.x + self.rect.width - 34 if not inp else self.rect.x + 14, self.rect.y + self.rect.height / 2)

        # Check if the data is a color or a shape and put the specific dot accordingly
        if len(self.data) > 1:
            self.dot = dot.Dot(0, 0, self.rect.size, self.rect_pos, inp, const=True)
        elif len(self.data) == 1:
            self.dot = dot.Dot(1, 0, self.rect.size, self.rect_pos, inp, const=True)

        # Display the image, dot and shape
        self.image.blit(self.l_image, (0, 0))
        self.image.blit(self.dot.image, (self.rect.width - 34 if not inp else 14, self.rect.height / 2 - 10))
        self.image.blit(pygame.transform.scale(self.display.surface, (80, 80)),
                        (self.image.get_size()[0] / 2 - 57 if not inp else 55, self.image.get_size()[1] / 2 - 40))

    def check(self, mouse_pos):
        # Initial variables
        on_dot = False
        available = False
        dot_pos = ()
        op_type = None
        data_type = None
        from_dot = None
        # For each input, check if the mouse is on top of the input- or output-dot
        if self.dot.loc_rect.collidepoint(mouse_pos):
            on_dot = True
            available = True
            self.dot.del_connection()
            dot_pos = self.dot.loc_rect.center
            op_type = self.dot.input_
            data_type = self.dot.type
            from_dot = self.dot
        return on_dot, available, dot_pos, op_type, data_type, from_dot

    def send_data(self):
        # If the constant is not a goal, it sends data
        if not self.inp:
            self.dot.send_data(self.data)

    def del_data(self):
        # When refreshing all the function-blocks, the goals also get refreshed to 0
        self.received = 0
        self.dot.data = None
        self.image.fill((255, 255, 255), (
            self.image.get_size()[0] / 2 - 62 if not self.inp else 50, self.image.get_size()[1] / 2 - 45, 90, 90))
        self.image.blit(pygame.transform.scale(self.display.surface, (80, 80)),
                        (self.image.get_size()[0] / 2 - 57 if not self.inp else 55, self.image.get_size()[1] / 2 - 40))

    def check_goal(self):
        # Refresh the image and the shape needed
        self.image.fill((255, 255, 255), (
            self.image.get_size()[0] / 2 - 62 if not self.inp else 50, self.image.get_size()[1] / 2 - 45, 90, 90))
        self.image.blit(pygame.transform.scale(self.display.surface, (80, 80)),
                        (self.image.get_size()[0] / 2 - 57 if not self.inp else 55, self.image.get_size()[1] / 2 - 40))
        # If the goal got the data that it needed, ...
        if self.dot.data == self.data and self.inp:
            # ...the goal shows how much has been fed into the goal
            self.received += 1
            # If the goal received the needed shape 5 times, it returns as complete
            if self.received >= 5:
                self.image.blit(self.done_image,
                                (60,
                                 self.image.get_size()[1] / 2 - 35))
                return True
        # If the needed number of data is not reached, it shows how many have been received
        if self.received:
            self.image.blit(self.nums[self.received - 1],
                            (80,
                            self.image.get_size()[1] / 2 - 35))
            self.dot.data = None
