import pygame


class MainScreen:
    def __init__(self, screen_size):
        title = pygame.image.load("Title@4x.png").convert_alpha()
        title_size = title.get_size()
        title = pygame.transform.scale(title, (title_size[0] / 4, title_size[1] / 4))
        title_pos = (1920 / 2, 200)
        self.surface = pygame.surface.Surface(screen_size, pygame.SRCALPHA)
        self.surface.blit(title, (title_pos[0] - title_size[0] / 8, title_pos[1] - title_size[1] / 8))
