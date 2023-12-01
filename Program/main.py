import time
import screeninfo
import pygame
import os
import sys
import fractions
import main_menu
import quick_start
import game_test

os.environ["SDL_VIDEO_CENTERED"] = "1"

colors = {
    "grey": (143, 143, 143),  # Grey
    "red": (237, 49, 36),  # Red
    "green": (33, 237, 67),  # Green
    "blue": (36, 103, 237),  # Blue
    "cyan": (56, 235, 229),  # Cyan
    "magenta": (237, 55, 219),  # Magenta
    "yellow": (240, 240, 36),  # Yellow
    "white": (255, 255, 255)  # White
}

screens = screeninfo.get_monitors()
canvas_w = screens[0].width
canvas_h = screens[0].height
screen_ratio = list(format(fractions.Fraction(int(canvas_w), int(canvas_h))))
screen_ratio.pop(1)

pygame.init()
quick = quick_start.QuickStart()
fps_clock = pygame.time.Clock()
fps_count = 500

screen_location = 1
#
loader_time = time.time()
while time.time() - loader_time <= 2:
    pass
#
menu = main_menu.MainScreen((canvas_w, canvas_h))
game = game_test.Test((canvas_w, canvas_h))

main_display = pygame.display.set_mode((canvas_w, canvas_h), flags=pygame.FULLSCREEN, depth=32, vsync=True)

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        if screen_location == 0:
            if event.type == pygame.MOUSEBUTTONDOWN:
                function = menu.on_click(event.pos)
                if function == "exit":
                    pygame.quit()
                    sys.exit()
                elif function == "start":
                    screen_location = 1
        elif screen_location == 1:
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.on_click(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                game.on_release(event.pos)

    main_display.fill((100, 100, 100))

    if screen_location == 0:
        main_display.blit(menu.surface, (0, 0))
        menu.refresh(pygame.mouse.get_pos())
        prev_mouse_pos = pygame.mouse.get_pos()
            
    elif screen_location == 1:
        game.refresh(pygame.mouse.get_pos())
        main_display.blit(game.surface, (0, 0))

    pygame.display.update()
    fps_clock.tick(500)
