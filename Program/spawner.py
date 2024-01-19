import pygame

path = "data/images/spawner/"
functions = ["delete", "rotate_cw", "rotate_ccw", "rotate_full", "cut", "merge", "paint", "color"]


class Func(pygame.sprite.Sprite):  # This class is used to display the buttons for each of the function-spawners
    def __init__(self, screen_size, func, ratio, bar_rect):
        pygame.sprite.Sprite.__init__(self)

        # Initialization of specific values
        self.func = func
        self.image = pygame.image.load(f"{path}{functions[func]}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * (ratio * (screen_size[0] / 2560)), self.image.get_size()[1] * (ratio * (screen_size[0] / 2560))))
        self.rect = self.image.get_rect()
        self.rect.x = (16 * (screen_size[0] / 2560) + 7 * func * (screen_size[0] / 2560) + self.image.get_size()[0] * func)
        self.rect.y = (bar_rect.h / 8)
        self.l_rect = self.image.get_rect()
        self.l_rect.x = (16 * (screen_size[0] / 2560) + 7 * func * (screen_size[0] / 2560) + self.image.get_size()[0] * func) + bar_rect.x
        self.l_rect.y = (bar_rect.h / 8) + bar_rect.y


class Spawner(pygame.sprite.Sprite):
    def __init__(self, screen_size, allowance):
        pygame.sprite.Sprite.__init__(self)

        # Initialization of specific values
        self.allowance = allowance

        self.bar = pygame.image.load(f"{path}bar.png").convert_alpha()
        ratio = 1000 / 2560  # For different display sizes
        self.bar = pygame.transform.scale(self.bar, (self.bar.get_size()[0] * ratio * (screen_size[0] / 2560), self.bar.get_size()[1] * ratio * (screen_size[0] / 2560)))

        self.image = pygame.surface.Surface(self.bar.get_size(), flags=pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = screen_size[0] / 2 - self.bar.get_size()[0] / 2
        self.rect.y = screen_size[1] - self.bar.get_size()[1]

        self.func_buttons = pygame.sprite.Group()

        all_empty = True
        # For every level only specific function-blocks are allowed
        # Through a list is known which functions are allowed.
        for func in range(8):
            if allowance[func] == 1:
                self.func_buttons.add(Func(screen_size, func, ratio, self.rect))
                all_empty = False
        # If at least one function is available, then show the bar.
        if not all_empty:
            self.image.blit(self.bar, (0, 0))
        self.func_buttons.draw(self.image)

    def check(self, mouse_pos):
        # On click on one of the function-buttons, return to spawn it
        for but in self.func_buttons:
            if but.l_rect.collidepoint(mouse_pos):
                return but.func
        return None
