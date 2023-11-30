import pygame
import copy
import math

max_layers = 2


class Shape:
    def __init__(self, start_shape):
        self.surface = None
        self.pos = (0, 0)
        self.layers = copy.deepcopy(start_shape)
        self.shapes = []
        self.shape_positions = [[(0, 0), (217, 0), (217, 217), (0, 217)], [(73, 73), (217, 73), (217, 217), (73, 217)]]

        self.update()

    def rotate(self, rotate_angle):
        help_shapes_list = []
        for layer in range(len(self.layers)):
            help_shapes_list.append([])
            for i in range(4):
                help_shapes_list[layer].append(self.layers[layer][math.floor((rotate_angle / 90) + i) % 4])
        self.layers = help_shapes_list
        self.update()

    def update(self):
        self.shapes = []
        for shape in range(4):
            self.shapes.append(pygame.image.load("/images/" + str(shape + 1) + ".png").convert_alpha())
        self.surface = pygame.Surface((448, 448), pygame.SRCALPHA | pygame.SCALED)
        for layer in range(len(self.layers)):
            for i in range(4):
                temp = copy.copy(self.shapes[self.layers[layer][i][0]])
                temp.fill(self.layers[layer][i][1] if self.layers[layer][i][1] != (0, 0, 0) else (255, 255, 255),
                          special_flags=pygame.BLEND_RGBA_MIN)
                self.surface.blit(pygame.transform.scale(pygame.transform.rotate(temp, -90 * i), (
                round(224 / ((layer + 2) / 2)), round(224 / ((layer + 2) / 2)))),
                                  self.shape_positions[layer][i],
                                  pygame.transform.scale(temp,
                                                         (round(224 / ((layer + 2) / 2)),
                                                          round(224 / ((layer + 2) / 2)))).get_rect())

    def merge(self, second_shape):
        if not len(second_shape.layers) + len(self.layers) > max_layers:
            for layer in range(len(second_shape.layers)):
                self.layers.append(second_shape.layers[layer])
        self.update()

    def unmerge(self):
        if len(self.layers) != 1:
            self.layers = self.layers[:-1]
        self.update()
