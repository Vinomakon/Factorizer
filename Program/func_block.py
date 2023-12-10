import pygame
import shape
import dot

images = {"delete": ["delete.png", [0], []],
          "cut": ["cut.png", [0], [0, 0]],
          "paint": ["paint.png", [0, 1], [0]],
          "color": ["color.png", [1, 1], [1]],
          "merge": ["merge.png", [0, 0], [0]],
          "rotate_cw": ["rotate_cw.png", [0], [0]],
          "rotate_ccw": ["rotate_ccw.png", [0], [0]],
          "rotate_full": ["rotate_full.png", [0], [0]]}

path = "images/"


class Function(pygame.sprite.Sprite):
    def __init__(self, func_type, pos=(0, 0)):
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
        self.in1_data = None
        self.in2_data = None

        self.full = False
        self.can_send = [False, False]

        self.allow_execute = False

        self.display_shape = shape.Shape(self.in1_data)

        self.image.blit(self.func_image, (0, 0))
        self.image.blit(pygame.transform.scale(self.display_shape.surface, (40, 40)), (self.func_image.get_size()[0] / 2 - 20, self.func_image.get_size()[1] / 2 - 10))

        for inp in range(len(images[func_type][1])):
            if images[func_type][1][inp] == 1:
                dot1 = dot.Dot(1, (20 if len(images[func_type][1]) > 1 else 0) * ((-1) ** inp), self.rect.size, pos, True)
                self.inputs.add(dot1)
            if images[func_type][1][inp] == 0:
                dot2 = dot.Dot(0, (20 if len(images[func_type][1]) > 1 else 0) * ((-1) ** inp), self.rect.size, pos, True)
                self.inputs.add(dot2)
        self.inputs.draw(self.image)

        for inp in range(len(images[func_type][2])):
            if images[func_type][2][inp] == 1:
                dot3 = dot.Dot(1, (20 if len(images[func_type][2]) > 1 else 0) * ((-1) ** inp), self.rect.size, pos, False)
                self.outputs.add(dot3)
            if images[func_type][2][inp] == 0:
                dot4 = dot.Dot(0, (20 if len(images[func_type][2]) > 1 else 0) * ((-1) ** inp), self.rect.size, pos, False)
                self.outputs.add(dot4)
        self.outputs.draw(self.image)

        self.dragging = False
        self.init_pos = pos
        self.start_drag = (0, 0)

    def check(self, mouse_pos):
        # Failed Attempt N. 1
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
                available = True  # not (inp.connecting or inp.connected)
                inp.del_connection()
                dot_pos = inp.rect.center
                op_type = 1
                data_type = inp.type
                from_dot = inp
        for out in self.outputs:
            if out.rect.collidepoint(mouse_pos):
                on_dot = True
                available = True  # not (out.connecting or out.connected)
                out.del_connection()
                dot_pos = out.rect.center
                op_type = 0
                data_type = out.type
                from_dot = out
        return on_dot, available, dot_pos, op_type, data_type, from_dot


    def draggable(self, state, mouse_pos):
        self.dragging = state
        if state:
            self.start_drag = mouse_pos
            for inp in self.inputs:
                inp.del_connection()
                inp.data = None
            for out in self.outputs:
                out.del_connection()
                out.data = None
            self.out1_data = None
            self.out2_data = None
            self.in1_data = None
            self.in2_data = None
        else:
            self.init_pos = (self.rect.x, self.rect.y)
            self.inputs.update((self.rect.x, self.rect.y))
            self.outputs.update((self.rect.x, self.rect.y))

    def update(self, mouse_pos):
        if self.dragging:
            self.rect.x = self.init_pos[0] - self.start_drag[0] + mouse_pos[0]
            self.rect.y = self.init_pos[1] - self.start_drag[1] + mouse_pos[1]

    def check_surround(self):
        if self.function != "delete":
            self.can_send = [False, False]
        else:
            self.can_send = [True, True]
        if self.function == "rotate_cw" or self.function == "rotate_ccw" or self.function == "rotate_full":
            if self.outputs.sprites()[0].sent:
                self.outputs.sprites()[0].sent = False
            self.can_send[1] = True
            if self.outputs.sprites()[0].connected_dot is not None and not self.outputs.sprites()[0].connected_dot.full:
                if not self.outputs.sprites()[0].sent:
                    self.can_send[0] = True
                else:
                    self.can_send[0] = False
            else:
                self.can_send[0] = False
        for inp in self.inputs:
            if self.can_send[0] and self.can_send[1]:
                self.full = False
                inp.full = False


    def receive_data(self):
        for inp in self.inputs:
            if not (self.can_send[0] and self.can_send[1]):
                self.full = False
                inp.full = True
        self.allow_execute = True
        if not self.full:
            if self.function == "rotate_cw" or self.function == "rotate_ccw" or self.function == "rotate_full" or self.function == "cut" or self.function == "delete":
                if self.in1_data is None and self.inputs.sprites()[0].data:
                    self.in1_data = self.inputs.sprites()[0].data
                    self.inputs.sprites()[0].data = None
                    self.allow_execute = True and self.allow_execute
                if self.in1_data is None:
                    self.allow_execute = False
        if self.allow_execute:
            self.image.fill((200, 200, 200),
                            (self.func_image.get_size()[0] / 2 - 20, self.func_image.get_size()[1] / 2, 40, 40))
            if self.in1_data:
                self.display_shape.update(self.in1_data)
            self.image.blit(pygame.transform.scale(self.display_shape.surface, (40, 40)),
                            (self.func_image.get_size()[0] / 2 - 20, self.func_image.get_size()[1] / 2))

        # Failed Attempt N. 2
        """
        all_sent = True
        update_image = False
        for out in self.outputs:
            all_sent = all_sent and out.sent
        if self.function == "rotate_cw" or self.function == "rotate_ccw" or self.function == "rotate_full":
            if self.in1_data is None:
                self.in1_data = self.inputs.sprites()[0].data
                self.inputs.sprites()[0].data = None
            if self.inputs.sprites()[0].data is None and self.in1_data is not None:
                self.allow_execute = True
            elif self.outputs.sprites()[0].connected_dot is not None and self.in1_data is not None:
                all_sent = all_sent or self.outputs.sprites()[0].connected_dot.full
            else:
                self.allow_execute = False

        if self.function == "delete":
            if self.in1_data is None:
                self.in1_data = self.inputs.sprites()[0].data
                self.inputs.sprites()[0].data = None
            if self.inputs.sprites()[0].data is None and self.in1_data is not None:
                self.allow_execute = True

        if not all_sent:
            self.image.fill((255, 255, 255),
                            (self.func_image.get_size()[0] / 2 - 20, self.func_image.get_size()[1] / 2, 40, 40))
            self.allow_execute = False
            for inp in self.inputs:
                inp.full = True
        else:
            self.allow_execute = self.allow_execute and True
            update_image = self.allow_execute and True
            for inp in self.inputs:
                inp.full = False
            for out in self.outputs:
                out.sent = False

        if update_image:
            self.image.fill((200, 200, 200),
                            (self.func_image.get_size()[0] / 2 - 20, self.func_image.get_size()[1] / 2, 40, 40))
            if self.in1_data:
                self.display_shape.update(self.in1_data)
            self.image.blit(pygame.transform.scale(self.display_shape.surface, (40, 40)),
                            (self.func_image.get_size()[0] / 2 - 20, self.func_image.get_size()[1] / 2))
        """
        # Failed Attempt N. 1
        """if (self.out1_data is None) or (len(self.outputs.sprites()) != 0 and self.outputs.sprites()[0].connected) or self.function == "delete":
            if self.function == "rotate_cw" or "rotate_ccw" or "rotate_full" or "delete":
                self.in1_data = self.inputs.sprites()[0].data
                for inp in self.inputs:
                    inp.full = False
        else:
            for inp in self.inputs:
                inp.full = True

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
                                """
    
    def send_data(self):
        if self.function == "rotate_cw" or self.function == "rotate_ccw" or self.function == "rotate_full":
            if self.outputs.sprites()[0].connected and self.can_send[0]:
                if self.outputs.sprites()[0].send_data(self.out1_data):
                    self.out1_data = None
    
    def execute(self):
        # Defines execution
        if not self.allow_execute:
            if self.function == "rotate_cw" or self.function == "rotate_ccw" or self.function == "rotate_full":
                self.image.fill((255, 255, 255),
                                (self.func_image.get_size()[0] / 2 - 20, self.func_image.get_size()[1] / 2, 40, 40))
                if self.out1_data:
                    self.display_shape.update(self.out1_data)
                self.image.blit(pygame.transform.scale(self.display_shape.surface, (40, 40)),
                                (self.func_image.get_size()[0] / 2 - 20, self.func_image.get_size()[1] / 2))
            return
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
        self.image.fill((255, 255, 255),
                        (self.func_image.get_size()[0] / 2 - 20, self.func_image.get_size()[1] / 2, 40, 40))
        if self.out1_data is not None:
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
        for layer in range(len(layers)):
            self.out1_data += layers[layer][6:8] + layers[layer][0:6]
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
        for layer in range(len(layers)):
            self.out1_data += layers[layer][2:8] + layers[layer][0:2]
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
        for layer in range(len(layers)):
            self.out1_data += layers[layer][4:8] + layers[layer][0:4]
            self.out1_data += ":"
        self.out1_data = self.out1_data[:-1]

    def delete(self):
        self.out1_data = "--------"
