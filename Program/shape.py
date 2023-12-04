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
    def __init__(self, start_shape):
        self.surface = None
        self.pos = (0, 0)
        self.shapes = []
        self.shape = copy.deepcopy(start_shape)
        self.shape_position = [[(0, 0), (shape_size / 2, 0), (shape_size / 2, shape_size / 2), (0, shape_size / 2)],
                               [(shape_size / 2 - shape_size / 3, shape_size / 2 - shape_size / 3), (shape_size / 2, shape_size / 2 - shape_size / 3), (shape_size / 2, shape_size / 2), (shape_size / 2 - shape_size / 3, shape_size / 2)],
                               [(shape_size / 2 - shape_size / 4, shape_size / 2 - shape_size / 4), (shape_size / 2, shape_size / 2 - shape_size / 4), (shape_size / 2, shape_size / 2), (shape_size / 2 - shape_size / 4, shape_size / 2)]]

        self.layer_size = [(shape_size / 2, shape_size / 2), (shape_size / 3, shape_size / 3), (shape_size / 4, shape_size / 4)]
        self.update(self.shape)

    def update(self, shape):
        self.shape = shape
        self.shapes = []
        for shape in range(4):
            self.shapes.append(pygame.image.load("images/" + str(shape + 1) + ".png").convert_alpha())
        self.surface = pygame.Surface((shape_size, shape_size), pygame.SRCALPHA | pygame.SCALED)
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
                    temp = copy.copy(self.shapes[shape_name.index(layer[pair * 2])])
                    temp.fill(colors[layer[pair * 2 + 1]], special_flags=pygame.BLEND_RGBA_MIN)
                    temp = pygame.transform.rotate(temp, pair * -90)
                    temp = pygame.transform.scale(temp, self.layer_size[layers.index(layer)])
                    self.surface.blit(temp, self.shape_position[layers.index(layer)][pair])

"""
        self.shapes = []
        for shape in range(4):
            self.shapes.append(pygame.image.load("images/" + str(shape + 1) + ".png").convert_alpha())
        self.surface = pygame.Surface((shape_size, shape_size), pygame.SRCALPHA | pygame.SCALED)
        for layer in range(len(self.layers)):
            for i in range(4):
                if i != 4:
                    temp = copy.copy(self.shapes[self.layers[layer][i][0]])
                    temp.fill(self.layers[layer][i][1] if self.layers[layer][i][1] != (0, 0, 0) else (255, 255, 255),
                              special_flags=pygame.BLEND_RGBA_MIN)
                    self.surface.blit(pygame.transform.scale(pygame.transform.rotate(temp, -90 * i), (
                        round((shape_size / 2) / ((layer + 2) / 2)), round((shape_size / 2) / ((layer + 2) / 2)))),
                                      self.shape_positions[layer][i],
                                      pygame.transform.scale(temp,
                                                             (round((shape_size / 2) / ((layer + 2) / 2)),
                                                              round((shape_size / 2) / ((layer + 2) / 2)))).get_rect())
"""
"""
    def rotate(self, rotate_angle):
            help_shapes_list = []
            for layer in range(len(self.layers)):
                help_shapes_list.append([])
                for i in range(4):
                    help_shapes_list[layer].append(self.layers[layer][math.floor((rotate_angle / 90) + i) % 4])
            self.layers = help_shapes_list
            self.update()

    def merge(self, second_shape):
        if not len(second_shape.layers) + len(self.layers) > max_layers:
            for layer in range(len(second_shape.layers)):
                self.layers.append(second_shape.layers[layer])
        self.update()

    def unmerge(self):
        if len(self.layers) != 1:
            self.layers = self.layers[:-1]
        self.update()
"""
