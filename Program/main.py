import time
import screeninfo
import pygame
import os
import sys
import fractions
import main_menu
import quick_start
import game_test
import level_end
import level_menu

os.environ["SDL_VIDEO_CENTERED"] = "1"

colors = {
    "grey": (143, 143, 143),  # Grey
    "red": (237, 49, 36),  # Red
    "green": (33, 237, 67),  # Green
    "blue": (36, 103, 237),  # Blue
    "cyan": (56, 235, 229),  # Cyan
    "magenta": (237, 55, 219),  # Magenta
    "yellow": (240, 240, 36),  # Yellow
    "white": (255, 255, 255),  # White
    "uncolored": (190, 190, 190) # Uncolored
}

screens = screeninfo.get_monitors()
canvas_w = screens[0].width
canvas_h = screens[0].height
screen_ratio = list(format(fractions.Fraction(int(canvas_w), int(canvas_h))))
screen_ratio.pop(1)

pygame.init()
icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Factorizer")

fps_clock = pygame.time.Clock()
fps_count = 500

screen_location = 0

quick = quick_start.QuickStart()
loader_time = time.time()
while time.time() - loader_time <= 1:
    pass

tick = 0
tick_duration = 0.25
tick_time = time.time()

menu = main_menu.MainScreen((canvas_w, canvas_h))
game = game_test.Test((canvas_w, canvas_h))
menu_screen = level_menu.LevelMenu((canvas_w, canvas_h))
on_menu = False
level_screen = None
goal_reached = False

main_display = pygame.display.set_mode((canvas_w, canvas_h), flags=pygame.FULLSCREEN, depth=32, vsync=True)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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
                    execute_time = time.time()
                    tick_time = time.time() + 0.4

        elif screen_location == 1:
            if goal_reached:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        function = level_screen.on_click(event.pos)
                        if function == "menu":
                            screen_location = 0
                            goal_reached = False
                            game = game_test.Test((canvas_w, canvas_h))
                        elif function == "restart":
                            execute_time = time.time()
                            tick_time = time.time() + 0.4
                            goal_reached = False
                            game = game_test.Test((canvas_w, canvas_h))
            elif on_menu:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        function = menu_screen.on_click(event.pos)
                        if function == "menu":
                            on_menu = False
                            screen_location = 0
                            game = game_test.Test((canvas_w, canvas_h))
                        elif function == "back":
                            on_menu = False
                        elif function == "restart":
                            on_menu = False
                            execute_time = time.time()
                            tick_time = time.time() + 0.4
                            game = game_test.Test((canvas_w, canvas_h))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        on_menu = not on_menu
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        game.on_click(event.pos)
                    elif pygame.mouse.get_pressed()[2]:
                        game.delete_func(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    game.on_release(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if 49 <= event.key <= 57:
                        game.spawn(event.key - 49, pygame.mouse.get_pos())
                    if event.key == pygame.K_ESCAPE:
                        on_menu = not on_menu

    main_display.fill((100, 100, 100))

    if screen_location == 0:
        menu.refresh(pygame.mouse.get_pos())
        main_display.blit(menu.surface, (0, 0))
        prev_mouse_pos = pygame.mouse.get_pos()
            
    elif screen_location == 1:

        if goal_reached:
            main_display.blit(pygame.transform.scale(game.surface, (canvas_w, canvas_h)), (0, 0))
            level_screen.refresh(pygame.mouse.get_pos())
            main_display.blit(level_screen.surface, (0, 0))
        elif on_menu:
            main_display.blit(pygame.transform.scale(game.surface, (canvas_w, canvas_h)), (0, 0))
            menu_screen.refresh(pygame.mouse.get_pos())
            main_display.blit(menu_screen.surface, (0, 0))
        else:
            game.refresh(pygame.mouse.get_pos())
            main_display.blit(pygame.transform.scale(game.surface, (canvas_w, canvas_h)), (0, 0))
            if time.time() - tick_time >= tick_duration:
                if tick == 0:
                    goal_reached, level, quality = game.tick()
                    if goal_reached:
                        level_screen = level_end.LevelEnd((canvas_w, canvas_h), 0)
                    tick = 1
                else:
                    game.execute()
                    tick = 0
                tick_time = time.time()

    pygame.display.update()
    fps_clock.tick(fps_count)
