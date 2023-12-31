import pygame
import copy
import math

max_layers = 2
shape_size = 448

colors = {
    "r": (237, 49, 36),  # Red
    "g": (33, 237, 67),  # Green
    "b": (36, 103, 237),  # Blue
    "c": (56, 235, 229),  # Cyan
    "m": (237, 55, 219),  # Magenta
    "y": (240, 240, 36),  # Yellow
    "w": (255, 255, 255),  # White
    "u": (150, 150, 150)  # Uncolored / Grey
}

shape_name = ["R", "C", "S", "W"]


class Shape:
    def __init__(self, start_shape, config, func_size, input_=False, const=False):
        self.surface = pygame.Surface((shape_size, shape_size), pygame.SRCALPHA | pygame.SCALED)
        self.pos = (0, 0)
        self.rect = self.surface.get_rect()
        if not const:
            self.rect.x = 50 if input_ else func_size[0] - 75
            self.rect.y = func_size[1] / 2 - 15 + config
        self.shapes = []
        self.shape = copy.deepcopy(start_shape)
        self.shape_position = [[(0, 0), (shape_size / 2, 0), (shape_size / 2, shape_size / 2), (0, shape_size / 2)],
                               [(shape_size / 2 - shape_size / 3, shape_size / 2 - shape_size / 3), (shape_size / 2, shape_size / 2 - shape_size / 3), (shape_size / 2, shape_size / 2), (shape_size / 2 - shape_size / 3, shape_size / 2)],
                               [(shape_size / 2 - shape_size / 4, shape_size / 2 - shape_size / 4), (shape_size / 2, shape_size / 2 - shape_size / 4), (shape_size / 2, shape_size / 2), (shape_size / 2 - shape_size / 4, shape_size / 2)]]

        self.layer_size = [(shape_size / 2, shape_size / 2), (shape_size / 3, shape_size / 3), (shape_size / 4, shape_size / 4)]
        if self.shape is not None:
            self.update(self.shape)
        else:
            self.update("--------")

    def update(self, shape):
        self.surface.fill((255, 255, 255))
        pygame.draw.circle(self.surface, (230, 230, 230), (shape_size / 2, shape_size / 2), shape_size / 2.4)
        if len(shape) == 1:
            color = pygame.image.load("data/images/col.png").convert_alpha()
            color.fill(colors[shape], special_flags=pygame.BLEND_RGBA_MIN)
            color = pygame.transform.scale(color, (shape_size / 1.2, shape_size * (color.get_size()[1] / color.get_size()[0]) / 1.2))
            self.surface.blit(color, (((1 - 1/1.2) * shape_size / 2), ((1 - 1/1.2) * shape_size / 2) + 10))
            return
        self.shape = shape
        shapes = []
        for shape in range(4):
            shapes.append(pygame.image.load("data/images/" + str(shape + 1) + ".png").convert_alpha())
        for shape in range(4):
            shapes.append(pygame.image.load("data/images/" + str(shape + 1) + "b.png").convert_alpha())

        temp_layer = ""
        layers = []
        for letter in self.shape:
            if letter == ":":
                layers.append(temp_layer)
                temp_layer = ""
            else:
                temp_layer += letter
        layers.append(temp_layer)
        for layer in layers:
            for pair in range(4):
                if layer[pair * 2] != "-":
                    temp = copy.copy(shapes[shape_name.index(layer[pair * 2]) + layers.index(layer) * 4])
                    temp.fill(colors[layer[pair * 2 + 1]], special_flags=pygame.BLEND_RGBA_MIN)
                    temp = pygame.transform.rotate(temp, pair * -90)
                    temp = pygame.transform.scale(temp, self.layer_size[layers.index(layer)])
                    self.surface.blit(temp, self.shape_position[layers.index(layer)][pair])
