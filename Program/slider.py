import pygame

colors = [(180, 180, 180), (100, 100, 100)]

font = "data/fonts/Bebas-Regular.ttf"


class Slider(pygame.sprite.Sprite):
    def __init__(self, size, pos, text, value, func, ):
        pygame.sprite.Sprite.__init__(self)

        self.actual_size = size
        self.size = (size[0], int(size[1] * (2/3)))
        self.pos = pos
        self.text = text
        self.value = value
        self.func = func

        self.sliding = False
        self.image = pygame.surface.Surface(self.actual_size, flags=pygame.SRCALPHA)

        self.slider = pygame.surface.Surface(self.size, flags=pygame.SRCALPHA)
        self.rect = pygame.rect.Rect(pos[0], pos[1], size[0], size[1])
        self.circle_size = self.size[1] / 5
        self.circle_rect = pygame.rect.Rect(
            self.circle_size + (self.size[0] - self.circle_size * 4) * self.value,
            self.size[1] / 2 - self.circle_size,
            self.circle_size * 2, self.circle_size * 2)
        self.loc_circle_rect = pygame.rect.Rect(
            self.circle_size + (self.size[0] - self.circle_size * 4) * self.value + self.pos[0],
            self.size[1] / 2 - self.circle_size + self.pos[1],
            self.circle_size * 2, self.circle_size * 2)
        self.min = self.pos[0] + self.circle_size * 2
        self.max = self.pos[0] + self.size[0] - self.circle_size * 2

        self.font_render = pygame.font.Font(font, int(self.size[1] * (1 / 3) + 15))
        self.text_render = self.font_render.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_render.get_rect(center=(self.size[0] / 2, self.actual_size[1] - int(self.size[1] * (1 /3) - 5)))

    def refresh(self, mouse_pos):
        self.image = pygame.surface.Surface(self.actual_size, flags=pygame.SRCALPHA)
        self.slider = pygame.surface.Surface(self.size, flags=pygame.SRCALPHA)
        self.slider.fill((50, 50, 50), (self.size[1] / 2, 0, self.size[0] - self.size[1], self.size[1]))
        pygame.draw.circle(self.slider, (50, 50, 50), (self.size[1] / 2, self.size[1] / 2), self.size[1] / 2)
        pygame.draw.circle(self.slider, (50, 50, 50), (self.size[0] - self.size[1] / 2, self.size[1] / 2),
                           self.size[1] / 2)
        pygame.draw.line(self.slider, (220, 220, 220), (self.circle_size * 2, self.size[1] / 2 - 1),
                         (self.circle_size * 2 + (self.size[0] - 2 * self.circle_size * 2) * 1, self.size[1] / 2 - 1),
                         int(self.size[0] / 43))
        pygame.draw.circle(self.slider, (220, 220, 220), (self.circle_size * 2, self.size[1] / 2),
                           int(self.size[0] / 43 / 1.95))
        pygame.draw.circle(self.slider, (220, 220, 220),
                           (self.circle_size * 2 + (self.size[0] - 2 * self.circle_size * 2) * 1, self.size[1] / 2),
                           int(self.size[0] / 43 / 1.95))

        pos = max(min(mouse_pos[0], self.max), self.min)
        if self.sliding:
            self.text_render = self.font_render.render(f"{round(self.value * 100)}%", True, (0, 0, 0))
            self.text_rect = self.text_render.get_rect(
                center=(self.size[0] / 2, self.actual_size[1] - int(self.size[1] * (1 / 3) - 5)))
            pygame.draw.circle(self.slider, colors[1],
                               (pos - self.pos[0], self.circle_rect.y + self.circle_size),
                               self.circle_size)
            self.circle_rect.x = pos - self.pos[0] - self.circle_size
            self.loc_circle_rect.x = pos - self.circle_size
            self.value = (self.circle_rect.x - self.circle_size) / (self.size[0] - self.circle_size * 4)
        else:

            if self.loc_circle_rect.collidepoint(mouse_pos):
                pygame.draw.circle(self.slider, colors[1],
                                   (self.circle_rect.x + self.circle_size, self.circle_rect.y + self.circle_size),
                                   self.circle_size)
                self.text_render = self.font_render.render(f"{round(self.value * 100)}%", True, (0, 0, 0))
                self.text_rect = self.text_render.get_rect(
                    center=(self.size[0] / 2, self.actual_size[1] - int(self.size[1] * (1 / 3) - 5)))
            else:
                pygame.draw.circle(self.slider, colors[0],
                                   (self.circle_rect.x + self.circle_size, self.circle_rect.y + self.circle_size),
                                   self.circle_size)
                self.text_render = self.font_render.render(self.text, True, (0, 0, 0))
                self.text_rect = self.text_render.get_rect(
                    center=(self.size[0] / 2, self.actual_size[1] - int(self.size[1] * (1 / 3) - 5)))
        self.image.blit(self.slider, (0, 0))
        self.image.blit(self.text_render, self.text_rect)
        return self.func, self.value
