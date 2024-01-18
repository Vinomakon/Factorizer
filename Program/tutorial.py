import pygame
import button
import cv2

path = "data/images/tutorial/"
videos = {
    "0": ["data/videos/intro.mp4", "intro.png"],
    "1": ["data/videos/rotate.mp4", "rotate.png"],
    "3": ["data/videos/cut.mp4", "cut.png"],
    "5": ["data/videos/merge.mp4", "merge.png"],
    "8": ["data/videos/paint.mp4", "paint.png"],
    "11": ["data/videos/color.mp4", "color.png"],
    "12": ["data/videos/refresh.mp4", "refresh.png"]
}

font = f"fonts/Bebas-Regular.ttf"


class Tutorial:
    def __init__(self, screen_size, level):

        # Video implementation using examples from stackoverflow
        # // https://stackoverflow.com/questions/21356439/how-to-load-and-play-a-video-in-pygame
        # as showcased by user "Red" // https://stackoverflow.com/users/13552470/red
        # ** From Here
        self.show_tutorial = False

        # Check if the level has a tutorial assigned to it
        if str(level) in videos:
            self.video = videos[str(level)][0]
            self.show_tutorial = True
            self.cap = cv2.VideoCapture(self.video)
            # ** to here
            self.img = self.cap.read()[1]
            self.shape = self.img.shape[1::-1]
            self.tut_text = pygame.transform.scale(pygame.image.load(f"{path}{videos[str(level)][1]}").convert_alpha(), screen_size)

        self.screen_size = screen_size

        self.surface = pygame.surface.Surface(screen_size, pygame.SRCALPHA)
        self.surface.fill(pygame.Color(0, 0, 0, 100))

        # A ratio is accessible, so if a different screen resolution is used,
        # it stays relative to how it should look like
        self.ratio = screen_size[0] / 2560

        # A simple button to continue to the level
        continue_button = button.Button((int(700 * self.ratio), int(150 * self.ratio)), (screen_size[0] / 2, screen_size[1] / 1.1), "Continue", "back")
        self.buttons = pygame.sprite.Group()
        self.buttons.add(continue_button)
        self.buttons.draw(self.surface)

    def on_click(self, click_pos):
        # For all buttons it gets checked, if the mouse is in the rect of the button
        for but in self.buttons:
            # If the button was pressed, return what to do next and the sound that should be played
            if but.rect.collidepoint(click_pos):
                return but.func, "button"
        # Otherwise return nothing
        return None, None

    def refresh(self, mouse_pos):
        # For every button, tell if the mouse is hovering over the button
        for but in self.buttons:
            if but.rect.collidepoint(mouse_pos):
                but.check(True)
            else:
                but.check(False)
            self.buttons.draw(self.surface)
        self.surface.blit(self.tut_text, (0, 0))

        success, self.img = self.cap.read()
        # Two variables are in use: success and the sel.img
        # self.img defines the current frame of the video and includes a surface which represents the frame
        # success defines if the frame was able to be read

        # So if the current frame of the video was read:
        if success:
            # It displays the video onto the screen
            self.surface.blit(pygame.transform.scale(pygame.image.frombuffer(self.img.tobytes(), self.shape, "BGR"),
                                                     (self.screen_size[0] / 2, self.ratio * 1440 / 2)), (self.screen_size[0] / 3.9, self.screen_size[1] / 20))
        # Otherwise the video is reloaded and played from the beginning
        else:
            self.cap = cv2.VideoCapture(self.video)
