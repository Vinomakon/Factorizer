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
from game_end import GameEnd
from tutorial import Tutorial

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


def refresh_volume(slider_values):
    for slid in slider_values:
        if slid[0] == "music":
            pygame.mixer.music.set_volume(slid[1])
            save_data[2][0] = slid[1]
        elif slid[0] == "sound":
            for sound_ in sounds.values():
                pygame.mixer.Sound.set_volume(sound_, save_data[2][1])
            save_data[2][1] = slid[1]


saver_loader = SaveLoadSystem(".txt", "data/saves")
save_data = saver_loader.load_data("save_data", default=[])

if len(save_data) == 0:
    save_data = [0, [[0, 0] for i in range(16)], [1, 1]]


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

sound_volume = save_data[2][1]
sounds = {
    "spawn": pygame.mixer.Sound("data/sounds/mixkit-game-ball-tap-2073.wav"),
    "delete": pygame.mixer.Sound("data/sounds/mixkit-small-hit-in-a-game-2072.wav")
}

refresh_volume([["music", save_data[2][0]], ["sound", save_data[2][1]]])


menu = MainScreen(screen_size, levels_done, save_data[2])
game = None
menu_screen = LevelMenu(screen_size)
tutorial_screen = None
level_screen = None
game_end_screen = GameEnd(screen_size)

goal_reached = False
on_menu = False
show_tutorial = False
level_time = None
pause_time = None

main_display = pygame.display.set_mode(screen_size, flags=pygame.FULLSCREEN | pygame.HWSURFACE, depth=32, vsync=True)

sound = None

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
                function, sound = menu.on_click(event.pos)
                if function == "exit":
                    end_game()
                elif isinstance(function, list):
                    screen_location = 1
                    execute_time = time.time()
                    tick_time = time.time() + 0.25
                    current_level = function[0]
                    game = Level(screen_size, current_level)
                    game.refresh(pygame.mouse.get_pos())
                    tutorial_screen = Tutorial(screen_size, current_level)
                    show_tutorial = tutorial_screen.show_tutorial
                    level_time = time.time()
            elif event.type == pygame.MOUSEBUTTONUP:
                menu.on_release(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu.menu_type = 0

        elif screen_location == 1:
            if show_tutorial:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        function, sound = tutorial_screen.on_click(event.pos)
                        if function == "back":
                            show_tutorial = False
                            level_time = time.time()
            elif goal_reached:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        function, sound = level_screen.on_click(event.pos)
                        if function == "next":
                            goal_reached = False
                            current_level += 1
                            level_time = time.time()
                            if current_level >= 16:
                                screen_location = 2
                            else:
                                game = Level(screen_size, current_level)
                                game.refresh(pygame.mouse.get_pos())
                                tutorial_screen = Tutorial(screen_size, current_level)
                                show_tutorial = tutorial_screen.show_tutorial
                        elif function == "menu":
                            screen_location = 0
                            goal_reached = False
                            menu = MainScreen(screen_size, levels_done, save_data[2])
                        elif function == "restart":
                            execute_time = time.time()
                            tick_time = time.time() + 0.25
                            goal_reached = False
                            level_time = time.time()
                            game = Level(screen_size, current_level)
            elif on_menu:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        function, sound = menu_screen.on_click(event.pos)
                        if function == "menu":
                            on_menu = False
                            screen_location = 0
                            menu = MainScreen(screen_size, levels_done, save_data[2])
                        elif function == "back":
                            on_menu = False
                            level_time = time.time() - pause_time
                        elif function == "restart":
                            on_menu = False
                            execute_time = time.time()
                            tick_time = time.time() + 0.25
                            level_time = time.time()
                            game = Level(screen_size, current_level)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        on_menu = not on_menu
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        sound, action = game.on_click(event.pos)
                        if action == "refresh":
                            game.refresh_data()
                            sound = "refresh"
                        elif action == "menu":
                            on_menu = True
                            pause_time = time.time() - level_time
                        action = None
                    elif pygame.mouse.get_pressed()[2]:
                        sound = game.on_click(event.pos, True)[1]
                elif event.type == pygame.MOUSEBUTTONUP:
                    sound = game.on_release(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if 49 <= event.key <= 57:
                        game.spawn(event.key - 49, pygame.mouse.get_pos())
                        sound = "spawn"
                    if event.key == pygame.K_r:
                        game.refresh_data()
                        sound = "refresh"
                    if event.key == pygame.K_ESCAPE:
                        on_menu = not on_menu
                        pause_time = time.time() - level_time

        if screen_location == 2:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    function, sound = game_end_screen.on_click(event.pos)
                    if function == "exit":
                        end_game()
                    elif function == "menu":
                        screen_location = 0
                        menu = MainScreen(screen_size, levels_done, save_data[2])

    if not pygame.mixer.music.get_busy():
        music_index = (music_index + 1) % len(music_list)
        pygame.mixer.music.load(f"data/music/{music_list[music_index]}")
        pygame.mixer.music.play()

    main_display.fill((100, 100, 100))

    if screen_location == 0:
        slider_values = menu.refresh(pygame.mouse.get_pos())
        if slider_values:
            refresh_volume(slider_values)
        main_display.blit(menu.surface, (0, 0))
            
    elif screen_location == 1:
        if show_tutorial:
            main_display.blit(pygame.transform.scale(game.surface, screen_size), (0, 0))
            tutorial_screen.refresh(pygame.mouse.get_pos())
            main_display.blit(tutorial_screen.surface, (0, 0))
        elif goal_reached:
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
                        if quality < save_data[1][current_level][0] or save_data[1][current_level][0] == 0:
                            save_data[1][current_level][0] = quality
                        if (time.time() - level_time < save_data[1][current_level][1] or
                                save_data[1][current_level][1] == 0):
                            save_data[1][current_level][1] = time.time() - level_time
                        level_screen = LevelEnd(screen_size, current_level, [quality, save_data[1][current_level][0]],
                                                [time.time() - level_time, save_data[1][current_level][1]])
                        if levels_done < current_level + 1:
                            levels_done += 1

                    tick = 1
                else:
                    game.execute()
                    tick = 0
                tick_time = time.time()

    elif screen_location == 2:
        game_end_screen.refresh(pygame.mouse.get_pos())
        main_display.blit(game_end_screen.surface, (0, 0))

    if sound and sound in sounds:
        pygame.mixer.Sound.play(sounds[sound])
    sound = None

    pygame.display.update()
    fps_clock.tick(fps)
