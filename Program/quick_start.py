import os
import pygame
import win32api
import win32con
import win32gui

class QuickStart:
    def __init__(self):
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()

        quick_screen = pygame.display.set_mode((400, 400), flags=pygame.NOFRAME, depth=32, vsync=True)

        logo = pygame.image.load("Logo@4x.png").convert_alpha()
        logo_size = logo.get_size()
        logo = pygame.transform.scale(logo, (logo_size[0] / 4, logo_size[1] / 4))
        # Make an invisible window // https://www.geeksforgeeks.org/how-to-make-a-fully-transparent-window-with-pygame/
        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                               win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*(255, 0, 128)), 0, win32con.LWA_COLORKEY)

        quick_screen.fill((255, 0, 128))
        pygame.draw.circle(quick_screen, (26, 26, 26), (200, 200), logo_size[0] / 8 + 2)
        quick_screen.blit(logo, (200 - logo_size[0] / 8, 200 - logo_size[1] / 8))

        pygame.display.update()