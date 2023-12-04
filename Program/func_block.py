import shape
import pygame

images = {"delete": ["delete.png", [0], []],
          "cut": ["cut.png", [0], [0, 0]],
          "paint": ["paint.png", [0, 1], [0]],
          "color": ["color.png", [1, 1], [1]],
          "merge": ["merge.png", [0, 0], [0]],
          "rotate_cw": ["rotate_cw.png", [0], [0]],
          "rotate_ccw": ["rotate_ccw.png", [0], [0]],
          "rotate_full": ["rotate_full.png", [0], [0]]}

path = "images/"


class Dot(pygame.sprite.Sprite):
    def __init__(self, type, config, func_size, pos, input=True):
        pygame.sprite.Sprite.__init__(self)
        self.config = config
        self.func_size = func_size
        self.type = type
        self.inputs = input
        self.connecting = False
        self.connected = False
        self.connection = ()
        
        self.data = None

        if type == 0:
            self.image = pygame.image.load("images/dot.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (20, self.image.get_size()[1] * (20 / self.image.get_size()[0])))
            self.rect = self.image.get_rect()
            self.rect.center = (10, 10)
            self.loc_rect = self.image.get_rect()
            self.loc_rect.center = (10, 10)
        else:
            self.image = pygame.image.load("images/sdot.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (20, self.image.get_size()[1] * (20 / self.image.get_size()[0])))
            self.rect = self.image.get_rect()
            self.rect.center = (10, 10)
            self.loc_rect = self.image.get_rect()
            self.loc_rect.center = (10, 10)

        self.rect.x = 20 if input else func_size[0] - 40
        self.rect.y = func_size[1] / 2 - 10 + config
        self.loc_rect.x = (20 if input else func_size[0] - 40) + pos[0]
        self.loc_rect.y = func_size[1] / 2 - 10 + config + pos[1]

    def update(self, pos):
        self.loc_rect.x = (20 if self.inputs else self.func_size[0] - 40) + pos[0]
        self.loc_rect.y = (self.func_size[1] / 2 - 10) + self.config + pos[1]
        self.rect.center = (10 + (20 if self.inputs else self.func_size[0] - 40) + pos[0], 10 + (self.func_size[1] / 2 - 10) + self.config + pos[1])


class Function(pygame.sprite.Sprite):
    def __init__(self, func_type, pos=(0, 0), start_shape="--------"):
        pygame.sprite.Sprite.__init__(self)
        self.function = func_type
        self.spawn_pos = pos

        self.func_image = pygame.image.load(path + images[func_type][0]).convert_alpha()
        self.func_image = pygame.transform.scale(self.func_image, (200, self.func_image.get_size()[1] * (200 / self.func_image.get_size()[0])))

        self.image = pygame.surface.Surface(self.func_image.get_size(), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.inputs = pygame.sprite.Group()
        self.outputs = pygame.sprite.Group()

        self.out1_data = None
        self.out2_data = None
        self.in1_data = start_shape
        self.in2_data = None

        self.display_shape = shape.Shape(self.in1_data)

        self.image.blit(self.func_image, (0, 0))
        self.image.blit(pygame.transform.scale(self.display_shape.surface, (40, 40)), (self.func_image.get_size()[0] / 2 - 20, self.func_image.get_size()[1] / 2))

        for inp in range(len(images[func_type][1])):
            if images[func_type][1][inp] == 1:
                dot1 = Dot(1, (20 if len(images[func_type][1]) > 1 else 0) * ((-1) ** inp), self.rect.size, pos, True)
                self.inputs.add(dot1)
            if images[func_type][1][inp] == 0:
                dot2 = Dot(0, (20 if len(images[func_type][1]) > 1 else 0) * ((-1) ** inp), self.rect.size, pos, True)
                self.inputs.add(dot2)
        self.inputs.draw(self.image)

        for inp in range(len(images[func_type][2])):
            if images[func_type][2][inp] == 1:
                dot3 = Dot(1, (20 if len(images[func_type][2]) > 1 else 0) * ((-1) ** inp), self.rect.size, pos, False)
                self.outputs.add(dot3)
            if images[func_type][2][inp] == 0:
                dot4 = Dot(0, (20 if len(images[func_type][2]) > 1 else 0) * ((-1) ** inp), self.rect.size, pos, False)
                self.outputs.add(dot4)
        self.outputs.draw(self.image)

        self.dragging = False
        self.init_pos = pos
        self.start_drag = (0, 0)

    def check(self, mouse_pos):
        """
        for dot in self.inputs:
            if dot.loc_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                if not dot.used:
                    dot.used = True
                    return True, dot.loc_rect.center, True and not dot.connected, 0
                return True, dot.loc_rect.center, False, 0
        for dot in self.outputs:
            if dot.loc_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                if not dot.used:
                    dot.used = True
                    return True, dot.loc_rect.center, True and not dot.connected, 1
                return True, dot.loc_rect.center, False, 1
        return False, (0, 0), False, 0
        """
        on_dot = False
        available = False
        dot_pos = ()
        op_type = None
        data_type = None
        from_dot = None
        for inp in self.inputs:
            if inp.rect.collidepoint(mouse_pos):
                on_dot = True
                available = not (inp.connecting or inp.connected)
                dot_pos = inp.rect.center
                op_type = 1
                data_type = inp.type
                from_dot = inp
        for out in self.outputs:
            if out.rect.collidepoint(mouse_pos):
                on_dot = True
                available = not (out.connecting or out.connected)
                dot_pos = out.rect.center
                op_type = 0
                data_type = out.type
                from_dot = out
        return on_dot, available, dot_pos, op_type, data_type, from_dot

    def draggable(self, state, mouse_pos):
        self.dragging = state
        if state:
            self.start_drag = mouse_pos
            re_pos = []
            for inp in self.inputs:
                re_pos.append(inp.connection)
                inp.data = None
            for out in self.outputs:
                re_pos.append(out.connection)
                out.data = None
            self.out1_data = None
            self.out2_data = None
            self.in1_data = None
            self.in2_data = None
            return re_pos
        else:
            self.init_pos = (self.rect.x, self.rect.y)
            self.inputs.update((self.rect.x, self.rect.y))
            self.outputs.update((self.rect.x, self.rect.y))

    def update(self, mouse_pos):
        if self.dragging:
            self.rect.x = self.init_pos[0] - self.start_drag[0] + mouse_pos[0]
            self.rect.y = self.init_pos[1] - self.start_drag[1] + mouse_pos[1]

    def receive_data(self):
        if (self.out1_data is None) or (len(self.outputs.sprites()) != 0 and self.outputs.sprites()[0].connected) or self.function == "delete":
            if self.function == "rotate_cw":
                self.in1_data = self.inputs.sprites()[0].data
            elif self.function == "rotate_ccw":
                self.in1_data = self.inputs.sprites()[0].data
            elif self.function == "rotate_full":
                self.in1_data = self.inputs.sprites()[0].data
            elif self.function == "delete":
                self.in1_data = self.inputs.sprites()[0].data
        if (self.in1_data is not None) or (
                len(self.outputs.sprites()) != 0 and self.outputs.sprites()[0].connected):
            self.image.fill((200, 200, 200),
                        (self.func_image.get_size()[0] / 2 - 20, self.func_image.get_size()[1] / 2, 40, 40))
        for out in self.outputs:
            out.data = None
        for inp in self.inputs:
            inp.data = None

        if self.in1_data is not None:
            if isinstance(self.in1_data, str) and len(self.in1_data) == 8:
                self.display_shape.update(self.in1_data)
                self.image.blit(pygame.transform.scale(self.display_shape.surface, (40, 40)),
                                (self.func_image.get_size()[0] / 2 - 20, self.func_image.get_size()[1] / 2))
        else:
            if isinstance(self.out1_data, str) and len(self.out1_data) == 8:
                self.display_shape.update(self.out1_data)
                self.image.blit(pygame.transform.scale(self.display_shape.surface, (40, 40)),
                                (self.func_image.get_size()[0] / 2 - 20, self.func_image.get_size()[1] / 2))
    
    def send_data(self):
        if self.function == "rotate_cw":
            if self.outputs.sprites()[0].connected:
                self.outputs.sprites()[0].data = self.out1_data
                self.out1_data = None
        elif self.function == "rotate_ccw":
            if self.outputs.sprites()[0].connected:
                self.outputs.sprites()[0].data = self.out1_data
                self.out1_data = None
        elif self.function == "rotate_full":
            if self.outputs.sprites()[0].connected:
                self.outputs.sprites()[0].data = self.out1_data
                self.out1_data = None
        for inp in self.inputs:
            inp.data = None
    
    def execute(self):
        # Defines execution
        for inp in self.inputs:
            inp.data = None
        for out in self.outputs:
            out.data = None
        if self.in1_data is not None:
            self.out1_data = self.in1_data
            self.in1_data = None
            if self.function == "rotate_cw":
                if self.out1_data is not None:
                    self.rotate_cw()
            elif self.function == "rotate_ccw":
                if self.out1_data is not None:
                    self.rotate_ccw()
            elif self.function == "rotate_full":
                if self.out1_data is not None:
                    self.rotate_full()
            elif self.function == "delete":
                if self.out1_data is not None:
                    self.delete()
            elif self.in2_data is not None:
                pass
        self.image.fill((255, 255, 255), (self.func_image.get_size()[0] / 2 - 20, self.func_image.get_size()[1] / 2, 40, 40))
        if isinstance(self.out1_data, str) and len(self.out1_data) == 8:
            self.display_shape.update(self.out1_data)
            self.image.blit(pygame.transform.scale(self.display_shape.surface, (40, 40)),
                        (self.func_image.get_size()[0] / 2 - 20, self.func_image.get_size()[1] / 2))

    def rotate_cw(self):
        temp_layer = ""
        layers = []
        for letter in self.out1_data:
            if letter == ":":
                layers.append(temp_layer)
                temp_layer = ""
            else:
                temp_layer += letter
        layers.append(temp_layer)
        self.out1_data = ""
        for layer in layers:
            self.out1_data = temp_layer[6:8] + temp_layer[0:6]
            self.out1_data += ":"
        self.out1_data = self.out1_data[:-1]

    def rotate_ccw(self):
        temp_layer = ""
        layers = []
        for letter in self.out1_data:
            if letter == ":":
                layers.append(temp_layer)
                temp_layer = ""
            else:
                temp_layer += letter
        layers.append(temp_layer)
        self.out1_data = ""
        for layer in layers:
            self.out1_data = temp_layer[2:8] + temp_layer[0:2]
            self.out1_data += ":"
        self.out1_data = self.out1_data[:-1]

    def rotate_full(self):
        temp_layer = ""
        layers = []
        for letter in self.out1_data:
            if letter == ":":
                layers.append(temp_layer)
                temp_layer = ""
            else:
                temp_layer += letter
        layers.append(temp_layer)
        self.out1_data = ""
        for layer in layers:
            self.out1_data = temp_layer[4:8] + temp_layer[0:4]
            self.out1_data += ":"
        self.out1_data = self.out1_data[:-1]

    def delete(self):
        self.out1_data = "--------"
