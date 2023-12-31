import time
import screeninfo
import pygame
import os
import sys
import fractions
import main_menu
import quick_start
import level
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


def reload_music():
    return os.listdir("data/music")


screens = screeninfo.get_monitors()
canvas_w = screens[0].width
canvas_h = screens[0].height
screen_size = (canvas_w, canvas_h)
screen_ratio = list(format(fractions.Fraction(int(canvas_w), int(canvas_h))))
screen_ratio.pop(1)

pygame.init()
icon = pygame.image.load("data/images/icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Factorizer")

fps_clock = pygame.time.Clock()
fps = 1000

screen_location = 0
levels_done = 3
current_level = 0

quick = quick_start.QuickStart()
loader_time = time.time()
while time.time() - loader_time <= 1:
    pass

fps_clock = pygame.time.Clock()
tick = 0
tick_duration = 0.25
tick_time = time.time()

menu = main_menu.MainScreen(screen_size, levels_done)
game = None

music_list = reload_music()
music_index = 0
pygame.mixer.music.load(f"data/music/{music_list[0]}")
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0)

menu_screen = level_menu.LevelMenu(screen_size)
level_screen = level_end.LevelEnd(screen_size, levels_done)

goal_reached = False
on_menu = False

main_display = pygame.display.set_mode(screen_size, flags=pygame.FULLSCREEN | pygame.HWSURFACE, depth=32, vsync=True)

action = None

reload_music()

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
                elif isinstance(function, list):
                    screen_location = 1
                    execute_time = time.time()
                    tick_time = time.time() + 0.4
                    current_level = function[0]
                    game = level.Level(screen_size, current_level)
            elif event.type == pygame.MOUSEBUTTONUP:
                menu.on_release(event.pos)

        elif screen_location == 1:
            if goal_reached:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        function = level_screen.on_click(event.pos)
                        if function == "next":
                            goal_reached = False
                            if levels_done < levels_done + 1:
                                levels_done += 1
                            current_level += 1
                            game = level.Level(screen_size, levels_done)
                        elif function == "menu":
                            screen_location = 0
                            goal_reached = False
                            menu = main_menu.MainScreen(screen_size, levels_done)
                        elif function == "restart":
                            execute_time = time.time()
                            tick_time = time.time() + 0.4
                            goal_reached = False
                            game = level.Level(screen_size, levels_done)
            elif on_menu:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        function = menu_screen.on_click(event.pos)
                        if function == "menu":
                            on_menu = False
                            screen_location = 0
                            menu = main_menu.MainScreen(screen_size, levels_done)
                        elif function == "back":
                            on_menu = False
                        elif function == "restart":
                            on_menu = False
                            execute_time = time.time()
                            tick_time = time.time() + 0.4
                            game = level.Level(screen_size, levels_done)
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

    if not pygame.mixer.music.get_busy():
        music_index = (music_index + 1) % len(music_list)
        pygame.mixer.music.load(f"data/music/{music_list[music_index]}")
        pygame.mixer.music.play()

    main_display.fill((100, 100, 100))

    if screen_location == 0:
        menu.refresh(pygame.mouse.get_pos())
        main_display.blit(menu.surface, (0, 0))
            
    elif screen_location == 1:
        if goal_reached:
            main_display.blit(pygame.transform.scale(game.surface, screen_size), (0, 0))
            level_screen.refresh(pygame.mouse.get_pos())
            main_display.blit(level_screen.surface, (0, 0))
        elif on_menu:
            main_display.blit(pygame.transform.scale(game.surface, screen_size), (0, 0))
            menu_screen.refresh(pygame.mouse.get_pos())
            main_display.blit(menu_screen.surface, (0, 0))
        else:
            game.refresh(pygame.mouse.get_pos())
            main_display.blit(pygame.transform.scale(game.surface, screen_size), (0, 0))
            if time.time() - tick_time >= tick_duration:
                if tick == 0:
                    goal_reached, level, quality = game.tick()
                    if goal_reached:
                        level_screen = level_end.LevelEnd(screen_size, 0)
                    tick = 1
                else:
                    game.execute()
                    tick = 0
                tick_time = time.time()

    pygame.display.update()
    fps_clock.tick(fps)
