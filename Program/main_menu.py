import pygame
import button


class MainScreen:
    def __init__(self, screen_size):
        play = pygame.image.load("images/play.png").convert_alpha()
        play_size = play.get_size()
        play = pygame.transform.scale(play, (play_size[0] / 2.8 * (screen_size[0] / 2560),
                                             play_size[0] / 2.8 * (screen_size[1] / 2560)))
        play_pos = (-55 * (screen_size[0] / 2560), -55 * (screen_size[0] / 2560))

        title = pygame.image.load("images/title.png").convert_alpha()
        title_size = title.get_size()
        title = pygame.transform.scale(title,
                                       ((title_size[0] / 4) * (screen_size[0] / 2560),
                                        (title_size[1] / 4) * (screen_size[0] / 2560)))
        title_size = title.get_size()
        title_pos = (screen_size[0] / 2 - title_size[0] / 2, screen_size[1] / 5 - title_size[1] / 2)
        self.surface = pygame.surface.Surface(screen_size, pygame.SRCALPHA)
        self.surface.blit(play, (play_pos[0], play_pos[1]))
        self.surface.blit(title, (title_pos[0], title_pos[1]))


        start_button = button.Button((700, 150), (screen_size[0] / 2, screen_size[1] / 2), "Start", "start")
        exit_button = button.Button((250, 75), (screen_size[0] / 2, screen_size[1] / 1.1), "Exit", "exit")
        self.buttons = pygame.sprite.Group()
        self.buttons.add(start_button, exit_button)
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

    """
    def start(self, main_display, fps):
        fps_clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    function = self.on_click(event.pos)
                    if function == "exit":
                        return "exit"
                    elif function == "start":
                        return "start"

            self.refresh(pygame.mouse.get_pos())
            main_display.blit(self.surface, (0, 0))
            pygame.display.update()
            fps_clock.tick(fps)
    """
