import pygame

colors = [(200, 200, 200), (150, 150, 150)]
actives = [(100, 100, 100), (200, 200, 200)]


class Button(pygame.sprite.Sprite):

    def __init__(self, size, pos, text, func, font="data/fonts/Bebas-Regular.ttf", active=True):
        pygame.sprite.Sprite.__init__(self)

        # Initialization of all variables
        self.image = pygame.surface.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - size[0] / 2
        self.rect.y = pos[1] - size[1] / 2
        self.position = pos
        self.text = text
        self.size = size
        self.font = font
        self.func = func
        self.active = active

        # Creating the text
        font = pygame.font.Font(self.font, self.size[1] - 10)
        self.text_render = font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_render.get_rect(center=(self.size[0] / 2, self.size[1] / 2 - 5))

        # Fill the button with the appropriate color if it's active or not
        self.image.fill(actives[self.active])
        pygame.draw.rect(self.image, (10, 10, 10), (0, 0, self.rect.w, self.rect.h), 7)
        self.image.blit(self.text_render, self.text_rect)

    def check(self, hover=False):
        # Only if it's active, you can hover over the button
        if self.active:
            if hover:
                self.image.fill(colors[1])
            else:
                self.image.fill(colors[0])
            pygame.draw.rect(self.image, (10, 10, 10), (0, 0, self.rect.w, self.rect.h), 7)
            self.image.blit(self.text_render, self.text_rect)
