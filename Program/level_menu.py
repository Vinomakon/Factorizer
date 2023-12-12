import pygame
import button

path = "images/"

font = f"fonts/Bebas-Regular.ttf"


class LevelMenu:
    def __init__(self, screen_size):
        title = pygame.image.load("images/pause.png").convert_alpha()
        title_size = title.get_size()
        title = pygame.transform.scale(title,
                                       ((title_size[0] / 4) * (screen_size[0] / 2560),
                                        (title_size[1] / 4) * (screen_size[0] / 2560)))
        title_size = title.get_size()
        title_pos = (screen_size[0] / 2 - title_size[0] / 2, screen_size[1] / 5 - title_size[1] / 2)
        self.surface = pygame.surface.Surface(screen_size, pygame.SRCALPHA)
        self.surface.fill(pygame.Color(0, 0, 0, 100))
        self.surface.blit(title, (title_pos[0], title_pos[1]))

        restart_button = button.Button((700, 150), (screen_size[0] / 2, screen_size[1] / 2), "Restart", "restart")
        back_button = button.Button((700, 150), (screen_size[0] / 2, screen_size[1] / 2 + 200), "Menu", "menu")

        exit_button = button.Button((250, 75), (screen_size[0] / 2, screen_size[1] / 1.1), "Back", "back")
        self.buttons = pygame.sprite.Group()
        self.buttons.add(restart_button, back_button, exit_button)
        self.buttons.draw(self.surface)

    def on_click(self, click_pos):
        for but in self.buttons:
            if but.rect.collidepoint(click_pos):
                return but.func

    def refresh(self, mouse_pos):

        for but in self.buttons:
            if but.rect.collidepoint(mouse_pos):
                but.check(True)
            else:
                but.check(False)
            self.buttons.draw(self.surface)
