import pygame
import button


class MainScreen:
    def __init__(self, screen_size):
        title = pygame.image.load("Title@4x.png").convert_alpha()
        title_size = title.get_size()
        title = pygame.transform.scale(title,
                                       ((title_size[0] / 4) * (screen_size[0] / 2560),
                                        (title_size[1] / 4) * (screen_size[1] / 1440)))
        title_size = title.get_size()
        title_pos = (screen_size[0] / 2 - title_size[0] / 2, screen_size[1] / 5 - title_size[1] / 2)
        self.surface = pygame.surface.Surface(screen_size, pygame.SRCALPHA)
        self.surface.blit(title, (title_pos[0], title_pos[1]))

        start_button = button.Button((700, 150), (screen_size[0] / 2, screen_size[1] / 2), "Start", "start")
        exit_button = button.Button((250, 75), (screen_size[0] / 2, screen_size[1] / 1.1), "Exit", "exit")
        self.buttons = pygame.sprite.Group()
        self.buttons.add(start_button, exit_button)
        self.surface.blit(start_button.surface, start_button.rect)
        self.surface.blit(exit_button.surface, exit_button.rect)

    def on_click(self, click_pos):
        for but in self.buttons:
            if but.rect.collidepoint(click_pos):
                return but.func

    def hover(self, mouse_pos):
        for but in self.buttons:
            if but.rect.collidepoint(mouse_pos):
                but.renew(True)
            else:
                but.renew(False)
            self.surface.blit(but.surface, but.rect)

