import time
import screeninfo
import pygame
import random
import os
import sys
import fractions
import shape
import main_menu
import quick_start

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

loader_time = time.time()
while time.time() - loader_time <= 2:
    pass

menu = main_menu.MainScreen((canvas_w, canvas_h))

shape_list = [[]]
for i in range(4):
    shape_list[0].append([random.randint(0, 3), list(colors.values())[random.randint(0, len(colors) - 1)]])

shape_test = shape.Shape(shape_list)

prev_mouse_pos = pygame.mouse.get_pos()

main_display = pygame.display.set_mode((canvas_w, canvas_h), flags=pygame.FULLSCREEN, depth=32, vsync=True)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            function = menu.on_click(event.pos)
            if function == "exit":
                pygame.quit()
                sys.exit()

    main_display.fill((100, 100, 100))
    main_display.blit(menu.surface, (0, 0))
    if prev_mouse_pos != pygame.mouse.get_pos():
        menu.hover(pygame.mouse.get_pos())

    pygame.display.update()
    fps_clock.tick(500)
