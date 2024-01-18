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


def reload_music():  # Refresh the music library that is in /data/music
    return os.listdir("data/music")


def refresh_volume(volumes):  # Change the volumes of music and sounds
    for vol in volumes:
        if vol[0] == "music":
            pygame.mixer.music.set_volume(vol[1])
            save_data[2][0] = vol[1]
        elif vol[0] == "sound":
            # Changing the volume of every single sound... argh
            for sound_ in sounds.values():
                pygame.mixer.Sound.set_volume(sound_, save_data[2][1])
            save_data[2][1] = vol[1]


# Initializing the save-loader and saving the data in a variable
saver_loader = SaveLoadSystem(".txt", "data/saves")
save_data = saver_loader.load_data("save_data", default=[])

# If no save-file was created, completely new save-data is created
if len(save_data) == 0:
    save_data = [0, [[0, 0] for i in range(16)], [1, 1]]

# Getting the screen resolution, and if there are 2 or more screens, the first ones resolution is taken
screens = screeninfo.get_monitors()
canvas_w = screens[0].width
canvas_h = screens[0].height
screen_size = (canvas_w, canvas_h)

# Initialization of pygame
pygame.init()

# Set the icon and the Caption fo the window
icon = pygame.image.load("data/images/icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Factorizer")

# This is just to spice up the loading of the game
# It doesn't really represent the loading time, just and artificial loader
quick = QuickStart()
loader_time = time.time()
while time.time() - loader_time <= 1:
    pass

# Control of the fp2
fps_clock = pygame.time.Clock()
fps = 1000  # Putting as much as possible

# Variables to control the updating, sending, executing, etc. in the game
tick = 0
tick_duration = 0.25 + time.time()
tick_time = time.time()

# Loading up a music library, setting up the volume and playing the music,
# If there are several music-files in the folder, it lists through them one after one
# This allows the player to add his own music
music_list = reload_music()
music_index = 0
pygame.mixer.music.load(f"data/music/{music_list[0]}")
pygame.mixer.music.play()

# Loading the sounds
sound_volume = save_data[2][1]
sounds = {
    "spawn": pygame.mixer.Sound("data/sounds/spawn.mp3"),
    "delete": pygame.mixer.Sound("data/sounds/delete.mp3"),
    "connect": pygame.mixer.Sound("data/sounds/connect.mp3"),
    "button": pygame.mixer.Sound("data/sounds/button.wav")
}

# Setting up the volumes of the music and the sounds, based on the save-file
refresh_volume([["music", save_data[2][0]], ["sound", save_data[2][1]]])

# Setting up the level the user recently completed, and a variable that states which level the player is on
levels_done = save_data[0]
current_level = 0

# Variables that have the different screens
menu = MainScreen(screen_size, levels_done, save_data[2])
game = None
menu_screen = LevelMenu(screen_size)
tutorial_screen = None
level_screen = None
game_end_screen = GameEnd(screen_size)

# Different values to control on which screen the player is on, and measuring the time the user takes to finish a level
screen_location = 0
goal_reached = False
on_menu = False
show_tutorial = False
level_time = None
pause_time = None
sound = None

# Setup of the main screen
main_display = pygame.display.set_mode(screen_size, flags=pygame.FULLSCREEN | pygame.HWSURFACE, depth=32, vsync=True)


def end_game():  # Saving the variables to the save-file and closing the game
    save_data[0] = levels_done
    save_data[2] = [pygame.mixer.music.get_volume(), pygame.mixer.Sound.get_volume(list(sounds.values())[0])]
    saver_loader.save_data(save_data, "save_data")
    pygame.quit()
    sys.exit()


# Main loop that controls basically EVERYTHING
while True:
    # Runs through every pygame event that is happening
    for event in pygame.event.get():
        # When the pygame screen is closed, end_game() is called
        if event.type == pygame.QUIT:
            end_game()

        # This section is for having different event-handling based on the screen the player is on

        if screen_location == 0:  # Main Menu
            # When the mouse is pressed down
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If a button was pressed, the function returns what to do next and what sound to play
                function, sound = menu.on_click(event.pos)
                # Self-explanatory
                if function == "exit":
                    end_game()
                # Since there are several levels, when a level-button is pressed, a number is returned
                # The number states which level to load
                elif isinstance(function, list):
                    # Game Setup, changing game variables and starting the tick- and execute-time
                    screen_location = 1
                    current_level = function[0]
                    game = Level(screen_size, current_level)
                    game.refresh(pygame.mouse.get_pos())
                    tutorial_screen = Tutorial(screen_size, current_level)
                    show_tutorial = tutorial_screen.show_tutorial
                    level_time = time.time()
            # This is only used for the sliders on the main menu, which tell the slider to stop "sliding"
            elif event.type == pygame.MOUSEBUTTONUP:
                menu.on_release()
            # If the ESC button is pressed on a sub-screen of the main menu, it goes back to the "main" main menu
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                menu.menu_type = 0

        elif screen_location == 1:  # Main Game

            # The game also has sub-screens which are controlled by there variables
            if show_tutorial:  # If the level has a tutorial, it is shown
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        function, sound = tutorial_screen.on_click(event.pos)
                        if function == "back":
                            show_tutorial = False
                            level_time = time.time()
            elif goal_reached:  # If the level has been completed, the level complete screen is shown
                # If a mouse-button is pressed...
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # ...and the left mouse-button is pressed...
                    if pygame.mouse.get_pressed()[0]:
                        # ...and if a button was pressed, a function and a sound is returned
                        function, sound = level_screen.on_click(event.pos)
                        if function == "next":  # Going to the next level
                            # Changing the level and reset some variables
                            goal_reached = False
                            current_level += 1
                            level_time = time.time()
                            # If all the levels are complete (16), the End Screen of the game is shown
                            if current_level >= 16:
                                screen_location = 2
                            # Otherwise start the next level
                            else:
                                game = Level(screen_size, current_level)
                                game.refresh(pygame.mouse.get_pos())
                                tutorial_screen = Tutorial(screen_size, current_level)
                                show_tutorial = tutorial_screen.show_tutorial
                        elif function == "menu":  # Go back to the main menu
                            screen_location = 0
                            goal_reached = False
                            menu = MainScreen(screen_size, levels_done, save_data[2])
                        elif function == "restart":  # Restarting the level
                            goal_reached = False
                            level_time = time.time()
                            game = Level(screen_size, current_level)
            elif on_menu:  # Shows the level menu
                # If a mouse-button is pressed...
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # ...and the left mouse-button is pressed...
                    if pygame.mouse.get_pressed()[0]:
                        # ...and if a button was pressed, a function and a sound is returned
                        function, sound = menu_screen.on_click(event.pos)
                        if function == "menu":  # Going back to the main menu
                            on_menu = False
                            screen_location = 0
                            menu = MainScreen(screen_size, levels_done, save_data[2])
                        elif function == "back":  # Returning to the level
                            on_menu = False
                            level_time = time.time() - pause_time
                        elif function == "restart":  # Restarting the level
                            on_menu = False
                            level_time = time.time()
                            game = Level(screen_size, current_level)
                # When pressing ESC, the player can change between the level and the level-menu
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    on_menu = not on_menu
            else:  # This is just the main game
                # On mouse-button-press
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the left mouse-button was pressed
                    if pygame.mouse.get_pressed()[0]:
                        # From the main game, it gets if a button was pressed, and what sound to play
                        action, sound = game.on_click(event.pos)
                        # Hopefully self-explanatory
                        if action == "refresh":
                            game.refresh_data()
                            sound = "refresh"
                        elif action == "menu":
                            on_menu = True
                            # Since the menu is on, the level-time shouldn't continue,
                            # only until the player exits the menu
                            pause_time = time.time() - level_time
                        action = None
                    # The right mouse-button is supposed to only delete a function
                    elif pygame.mouse.get_pressed()[2]:
                        # So it's only getting a sound
                        sound = game.on_click(event.pos, True)[1]
                # When dragging a function-block, it should be known, when to stop dragging it
                elif event.type == pygame.MOUSEBUTTONUP:
                    sound = game.on_release(event.pos)
                # The function-blocks are mainly being brought onto the screen through the spawner
                # This allows to spawn the function through the number buttons
                # Also refreshing can be done through the "R" button, or opening the menu through ESC
                elif event.type == pygame.KEYDOWN:
                    if 49 <= event.key <= 57:  # Number --> Function-Block
                        game.spawn(event.key - 49, pygame.mouse.get_pos())
                        sound = "spawn"
                    if event.key == pygame.K_r:  # Refresh
                        game.refresh_data()
                        sound = "refresh"
                    if event.key == pygame.K_ESCAPE:  # Opening the menu
                        on_menu = not on_menu
                        pause_time = time.time() - level_time

        if screen_location == 2:  # End Screen
            # When a mouse-button is pressed...
            if event.type == pygame.MOUSEBUTTONDOWN:
                # ...and the left mouse-button is pressed...
                if pygame.mouse.get_pressed()[0]:
                    # ...and if a button is pressed, an action and the sound is returned
                    function, sound = game_end_screen.on_click(event.pos)
                    if function == "exit":
                        end_game()
                    elif function == "menu":
                        screen_location = 0
                        menu = MainScreen(screen_size, levels_done, save_data[2])

    # If no music is playing anymore, the next song is played
    if not pygame.mixer.music.get_busy():
        music_index = (music_index + 1) % len(music_list)
        pygame.mixer.music.load(f"data/music/{music_list[music_index]}")
        pygame.mixer.music.play()

    # This section displays the appropriate screens based on what screen the player is on,
    # and also controls some time-based variables
    if screen_location == 0:  # Main Menu
        # Slider values are always received from the main menu for changing the music/sound volume in real-time
        # Also allows checking if the mouse is over a button to create a hovering effect
        slider_values = menu.refresh(pygame.mouse.get_pos())
        # Only if the slider_values aren't empty
        if slider_values:
            refresh_volume(slider_values)
        main_display.blit(menu.surface, (0, 0))
    elif screen_location == 1:  # Main Game
        if show_tutorial:  # Showing the tutorial on top of the level
            main_display.blit(pygame.transform.scale(game.surface, screen_size), (0, 0))
            # Allows checking if the mouse is over a button to create a hovering effect
            tutorial_screen.refresh(pygame.mouse.get_pos())
            main_display.blit(tutorial_screen.surface, (0, 0))
        elif goal_reached:  # Showing the level-complete screen on top of the level
            main_display.blit(pygame.transform.scale(game.surface, screen_size), (0, 0))
            # Allows checking if the mouse is over a button to create a hovering effect
            level_screen.refresh(pygame.mouse.get_pos())
            main_display.blit(level_screen.surface, (0, 0))
        elif on_menu:  # Showing the menu on top of the level
            main_display.blit(pygame.transform.scale(game.surface, screen_size), (0, 0))
            # Allows checking if the mouse is over a button to create a hovering effect
            menu_screen.refresh(pygame.mouse.get_pos())
            main_display.blit(menu_screen.surface, (0, 0))
        else:  # Otherwise update the main game
            # This function is called to refresh and update everything happening in the level
            game.refresh(pygame.mouse.get_pos())
            main_display.blit(pygame.transform.scale(game.surface, screen_size), (0, 0))
            # A tick in this scenario is every 0.25 seconds and defines,
            # when the function-blocks should receive, execute and send
            if time.time() - tick_time >= tick_duration:
                # There are two states where a tick comes into play
                # One where the data between the function-blocks is shared to another
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
                # And the other makes the function-blocks execute and process the data that they have if they have any
                else:
                    game.execute()
                    tick = 0
                # Then the tick_time gets reset
                tick_time = time.time()
    elif screen_location == 2:  # End Screen
        # Allows checking if the mouse is over a button to create a hovering effect
        game_end_screen.refresh(pygame.mouse.get_pos())
        main_display.blit(game_end_screen.surface, (0, 0))

    # If a sound need to be played, it is first checked if the sound is even in the sound library,
    # and if it is, it gets played
    if sound and sound in sounds:
        print(sound)
        pygame.mixer.Sound.play(sounds[sound])
    sound = None

    # Basic functions that refresh the screen and limits the frame-rate
    pygame.display.update()
    fps_clock.tick(fps)
