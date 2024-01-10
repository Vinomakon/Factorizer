import time
import screeninfo
import pygame
import os
import sys
from save_load_system import SaveLoadSystem
from main_menu import MainScreen
from quick_start import QuickStart
from level import Level
from level_end import LevelEnd
from level_menu import LevelMenu

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
    "uncolored": (190, 190, 190)  # Uncolored
}


def reload_music():
    return os.listdir("data/music")


saver_loader = SaveLoadSystem(".txt", "data/saves")
save_data = saver_loader.load_data("save_data", default=[])

if len(save_data) == 0:
    save_data = [0, [[0, 0] for i in range(16)], [1, 0]]
    print("ey")


screens = screeninfo.get_monitors()
canvas_w = screens[0].width
canvas_h = screens[0].height
screen_size = (canvas_w, canvas_h)

pygame.init()
icon = pygame.image.load("data/images/icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Factorizer")

fps_clock = pygame.time.Clock()
fps = 1000

screen_location = 0
levels_done = save_data[0]
current_level = 0

quick = QuickStart()
loader_time = time.time()
while time.time() - loader_time <= 1:
    pass

fps_clock = pygame.time.Clock()
tick = 0
tick_duration = 0.25
tick_time = time.time()

music_list = reload_music()
music_index = 0
pygame.mixer.music.load(f"data/music/{music_list[0]}")
pygame.mixer.music.play()
pygame.mixer.music.set_volume(save_data[2][0])

menu = MainScreen(screen_size, levels_done)
game = None
level_time = None
menu_screen = LevelMenu(screen_size)
level_screen = None

goal_reached = False
on_menu = False

main_display = pygame.display.set_mode(screen_size, flags=pygame.FULLSCREEN | pygame.HWSURFACE, depth=32, vsync=True)

action = None

reload_music()


def end_game():
    save_data[0] = levels_done
    save_data[2] = [pygame.mixer.music.get_volume(), 0]
    saver_loader.save_data(save_data, "save_data")
    pygame.quit()
    sys.exit()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_game()

        if screen_location == 0:
            if event.type == pygame.MOUSEBUTTONDOWN:
                function = menu.on_click(event.pos)
                if function == "exit":
                    end_game()
                elif isinstance(function, list):
                    screen_location = 1
                    execute_time = time.time()
                    tick_time = time.time() + 0.4
                    current_level = function[0]
                    game = Level(screen_size, current_level)
                    level_time = time.time()
            elif event.type == pygame.MOUSEBUTTONUP:
                menu.on_release(event.pos)

        elif screen_location == 1:
            if goal_reached:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        function = level_screen.on_click(event.pos)
                        if function == "next":
                            goal_reached = False
                            current_level += 1
                            game = Level(screen_size, current_level)
                        elif function == "menu":
                            screen_location = 0
                            goal_reached = False
                            menu = MainScreen(screen_size, levels_done)
                        elif function == "restart":
                            execute_time = time.time()
                            tick_time = time.time() + 0.4
                            goal_reached = False
                            game = Level(screen_size, levels_done)
            elif on_menu:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        function = menu_screen.on_click(event.pos)
                        if function == "menu":
                            on_menu = False
                            screen_location = 0
                            menu = MainScreen(screen_size, levels_done)
                        elif function == "back":
                            on_menu = False
                        elif function == "restart":
                            on_menu = False
                            execute_time = time.time()
                            tick_time = time.time() + 0.4
                            game = Level(screen_size, current_level)
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
                    if event.key == pygame.K_r:
                        game.refresh_data()
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
                    goal_reached, quality = game.tick()
                    if goal_reached:
                        level_screen = LevelEnd(screen_size, 0, quality, time.time() - level_time)
                        if levels_done < current_level + 1:
                            levels_done += 1
                    tick = 1
                else:
                    game.execute()
                    tick = 0
                tick_time = time.time()

    pygame.display.update()
    fps_clock.tick(fps)
