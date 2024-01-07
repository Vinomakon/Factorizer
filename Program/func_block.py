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

colors = {
    "r": (255, 0, 0),  # Red
    "y": (255, 255, 0),  # Yellow
    "g": (0, 255, 0),  # Green
    "c": (0, 255, 255),  # Cyan
    "b": (0, 0, 255),  # Blue
    "m": (255, 0, 255),  # Magenta
    "w": (255, 255, 255),  # White
    "u": (150, 150, 150)  # Uncolored / Grey
}

path = "data/images/"

max_layers = 2


def decode_shape(data):
    temp_layer = ""
    layers = []
    for letter in data:
        if letter == ":":
            layers.append(temp_layer)
            temp_layer = ""
        else:
            temp_layer += letter
    layers.append(temp_layer)
    return layers


def color(data1, data2):
    col1 = colors[data1]
    col2 = colors[data2]

    if col1 == (150, 150, 150):
        new_color = (min(col2[0], 255), min(col2[1], 255), min(col2[2], 255))
    elif col2 == (150, 150, 150):
        new_color = (min(col1[0], 255), min(col1[1], 255), min(col1[2], 255))
    else:
        new_color = (min(col1[0] + col2[0], 255), min(col1[1] + col2[1], 255), min(col1[2] + col2[2], 255))
    return list(colors)[list(colors.values()).index(new_color)]


class Function(pygame.sprite.Sprite):
    def __init__(self, func_type, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.function = func_type
        self.spawn_pos = pos

        self.func_image = pygame.image.load(path + images[func_type][0]).convert_alpha()
        self.func_image = pygame.transform.scale(self.func_image, (200, self.func_image.get_size()[1] * (200 / self.func_image.get_size()[0])))

        self.image = pygame.surface.Surface(self.func_image.get_size(), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - self.func_image.get_size()[0] / 2
        self.rect.y = pos[1] - self.func_image.get_size()[1] / 2

        self.inputs = pygame.sprite.Group()
        self.outputs = pygame.sprite.Group()

        self.out1_data = None
        self.out2_data = None
        self.in1_data = None
        self.in2_data = None

        self.full = False
        self.outs_full = [False, False]

        self.allow_execute = False

        self.in_displays = []
        self.out_displays = []

        self.image.blit(self.func_image, (0, 0))

        for inp in range(len(images[func_type][1])):
            if images[func_type][1][inp] == 1:
                dot1 = dot.Dot(1, 16 + 16 * (((-1) ** (inp + 1)) if len(images[func_type][1]) > 1 else 0), self.rect.size, pos, True)
                self.inputs.add(dot1)
                self.in_displays.append(shape.Shape("--------", 16 + 16 * (((-1) ** (inp + 1)) if len(images[func_type][1]) > 1 else 0), self.rect.size, 1))
            if images[func_type][1][inp] == 0:
                dot2 = dot.Dot(0, 16 + 16 * (((-1) ** (inp + 1)) if len(images[func_type][1]) > 1 else 0), self.rect.size, pos, True)
                self.inputs.add(dot2)
                self.in_displays.append(shape.Shape("--------", 16 + 16 * (((-1) ** (inp + 1)) if len(images[func_type][1]) > 1 else 0), self.rect.size, 1))
        self.inputs.draw(self.image)

        for out in range(len(images[func_type][2])):
            if images[func_type][2][out] == 1:
                dot3 = dot.Dot(1, 16 + 16 * (((-1) ** (out + 1)) if len(images[func_type][2]) > 1 else 0), self.rect.size, pos, False)
                self.outputs.add(dot3)
                self.out_displays.append(shape.Shape("--------", 16 + 16 * (((-1) ** (out + 1)) if len(images[func_type][2]) > 1 else 0), self.rect.size, 0))
            if images[func_type][2][out] == 0:
                dot4 = dot.Dot(0, 16 + 16 * (((-1) ** (out + 1)) if len(images[func_type][2]) > 1 else 0), self.rect.size, pos, False)
                self.outputs.add(dot4)
                self.out_displays.append(shape.Shape("--------", 16 + 16 * (((-1) ** (out + 1)) if len(images[func_type][2]) > 1 else 0), self.rect.size, 0))
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
                available = True
                inp.del_connection()
                dot_pos = inp.rect.center
                op_type = 1
                data_type = inp.type
                from_dot = inp
        for out in self.outputs:
            if out.rect.collidepoint(mouse_pos):
                on_dot = True
                available = True
                out.del_connection()
                dot_pos = out.rect.center
                op_type = 0
                data_type = out.type
                from_dot = out
        return on_dot, available, dot_pos, op_type, data_type, from_dot

    def draggable(self, state, mouse_pos):
        self.dragging = state
        if state:
            for shp in range(len(self.in_displays)):
                self.in_displays[shp].update("--------")
                self.image.blit(pygame.transform.scale(self.in_displays[shp].surface, (30, 30)),
                                self.in_displays[shp].rect)

            for shp in range(len(self.out_displays)):
                self.out_displays[shp].update("--------")
                self.image.blit(pygame.transform.scale(self.out_displays[shp].surface, (30, 30)),
                                self.out_displays[shp].rect)
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

    def refresh(self):
        for shp in range(len(self.in_displays)):
            self.in_displays[shp].update("--------")
            self.image.blit(pygame.transform.scale(self.in_displays[shp].surface, (30, 30)),
                            self.in_displays[shp].rect)

        for shp in range(len(self.out_displays)):
            self.out_displays[shp].update("--------")
            self.image.blit(pygame.transform.scale(self.out_displays[shp].surface, (30, 30)),
                            self.out_displays[shp].rect)
        for inp in self.inputs:
            inp.data = None
            inp.full = False
            inp.sent = False
        for out in self.outputs:
            out.data = None
            out.full = False
            out.sent = False
        self.out1_data = None
        self.out2_data = None
        self.in1_data = None
        self.in2_data = None
        self.full = False
        self.outs_full = [False, False]

    def deletion(self):
        for inp in self.inputs:
            inp.del_connection()
        for out in self.outputs:
            out.del_connection()

    def update(self, mouse_pos):
        if self.dragging:
            self.rect.x = self.init_pos[0] - self.start_drag[0] + mouse_pos[0]
            self.rect.y = self.init_pos[1] - self.start_drag[1] + mouse_pos[1]

        elif self.function == "delete":
            pass

        elif self.function == "rotate_cw" or self.function == "rotate_ccw" or self.function == "rotate_full" or self.function == "merge" or self.function == "paint" or self.function == "color":
            self.full = self.outs_full[0]

        elif self.function == "cut":
            self.full = self.outs_full[0] or self.outs_full[1]

        # Failed Attempt N.1
        # This allowed basic communication between the functions, but halted the process,
        # if the function wasn't part of a whole system, where it didn't do anything.
        # Only after the whole system was connected the receiving and sending would commence
        """
        if self.function == "delete":
            self.can_send = [True, True]
        else:
            self.can_send = [False, False]

        if self.function == "rotate_cw" or self.function == "rotate_ccw" or self.function == "rotate_full" or self.function == "merge" or self.function == "paint" or self.function == "color":
            if self.outputs.sprites()[0].sent:
                self.outputs.sprites()[0].sent = False
            self.can_send[1] = True
            if self.outputs.sprites()[0].connected_dot and not self.outputs.sprites()[0].connected_dot.full:
                if not self.outputs.sprites()[0].sent:
                    self.can_send[0] = True
                else:
                    self.can_send[0] = False
            else:
                self.can_send[0] = False

        if self.function == "cut":
            if self.outputs.sprites()[0].sent and self.outputs.sprites()[1].sent:
                self.outputs.sprites()[0].sent, self.outputs.sprites()[1].sent = False, False
            if self.outputs.sprites()[0].connected_dot and self.outputs.sprites()[1].connected_dot:
                if not self.outputs.sprites()[0].connected_dot.full and not self.outputs.sprites()[0].sent:
                    self.can_send[0] = True
                else:
                    self.can_send[0] = False

                if not self.outputs.sprites()[1].connected_dot.full and not self.outputs.sprites()[1].sent:
                    self.can_send[1] = True
                else:
                    self.can_send[1] = False

        if self.can_send[0] and self.can_send[1]:
            self.full = False
            for inp in self.inputs:
                inp.full = False
        """

    def receive_data(self):

        if self.function == "rotate_cw" or self.function == "rotate_ccw" or self.function == "rotate_full" or self.function == "cut" or self.function == "delete":
            if self.in1_data is None:
                if self.inputs.sprites()[0].data:
                    self.in1_data = self.inputs.sprites()[0].data
                    self.allow_execute = True
                    self.inputs.sprites()[0].full = True

                    self.in_displays[0].update(self.in1_data)
                    self.image.blit(pygame.transform.scale(self.in_displays[0].surface, (30, 30)),
                                    self.in_displays[0].rect)
                else:
                    self.allow_execute = False
            else:
                self.allow_execute = True

        elif self.function == "merge" or self.function == "paint" or self.function == "color":
            if self.in1_data is None and self.inputs.sprites()[0].data:
                self.in1_data = self.inputs.sprites()[0].data
                self.allow_execute = True
                self.inputs.sprites()[0].full = True

                self.in_displays[0].update(self.in1_data)
                self.image.blit(pygame.transform.scale(self.in_displays[0].surface, (30, 30)),
                                self.in_displays[0].rect)
            elif self.in1_data:
                self.allow_execute = True
            else:
                self.allow_execute = False

            if self.in2_data is None and self.inputs.sprites()[1].data:
                self.in2_data = self.inputs.sprites()[1].data
                self.allow_execute = True and self.allow_execute
                self.inputs.sprites()[1].full = True

                self.in_displays[1].update(self.in2_data)
                self.image.blit(pygame.transform.scale(self.in_displays[1].surface, (30, 30)),
                                self.in_displays[1].rect)
            elif self.in2_data:
                self.allow_execute = True and self.allow_execute
            else:
                self.allow_execute = False and self.allow_execute

        self.allow_execute = self.allow_execute and not self.full

        # Failed Attempt N.3
        # This system worked before, but it had some flaws, like not working properly and not receiving data, even when
        # the function outputs are completely empty and only fills up if a full system is set up.
        """
        self.allow_execute = True
        if not self.full:
            if self.function == "rotate_cw" or self.function == "rotate_ccw" or self.function == "rotate_full" or self.function == "cut" or self.function == "delete":
                if self.in1_data is None and self.inputs.sprites()[0].data:
                    self.in1_data = self.inputs.sprites()[0].data
                    self.inputs.sprites()[0].data = None

                if self.in1_data is None:
                    self.allow_execute = False
                else:
                    self.allow_execute = True

            elif self.function == "merge" or self.function == "paint" or self.function == "color":
                if self.in1_data is None and self.inputs.sprites()[0].data:
                    self.in1_data = self.inputs.sprites()[0].data
                    self.inputs.sprites()[0].data = None
                    self.allow_execute = True and self.allow_execute

                if self.in2_data is None and self.inputs.sprites()[1].data:
                    self.in2_data = self.inputs.sprites()[1].data
                    self.inputs.sprites()[1].data = None
                    self.allow_execute = True and self.allow_execute

                if self.in1_data is None or self.in2_data is None:
                    self.allow_execute = False
                else:
                    self.allow_execute = True

        else:
            self.allow_execute = False

        if not (self.can_send[0] and self.can_send[1]):
            self.full = True
            for inp in self.inputs:
                inp.full = True

        if self.allow_execute:
            for shp in range(len(self.in_displays)):
                if not shp and self.in1_data:
                    self.in_displays[shp].update(self.in1_data)
                    self.image.blit(pygame.transform.scale(self.in_displays[shp].surface, (30, 30)),
                                    self.in_displays[shp].rect)
                elif shp and self.in2_data:
                    self.in_displays[shp].update(self.in2_data)
                    self.image.blit(pygame.transform.scale(self.in_displays[shp].surface, (30, 30)),
                                    self.in_displays[shp].rect)
        """

        # Failed Attempt N.2
        # This system worked only for the basic functions, for which I needed to rewrite the whole system of receiving
        # data. Even then, there were some flaws, like the functions not communicating properly.
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

        # Failed Attempt N.1
        # This is the most basic of systems that was created just for basic prototyping,
        # since this was the starting stage of it all.
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
        if self.function == "rotate_cw" or self.function == "rotate_ccw" or self.function == "rotate_full" or self.function == "merge" or self.function == "paint" or self.function == "color":
            if self.out1_data:
                if self.outputs.sprites()[0].send_data(self.out1_data):
                    self.outs_full[0] = False
                    self.out1_data = None
                    self.out_displays[0].update("--------")
                    self.image.blit(pygame.transform.scale(self.out_displays[0].surface, (30, 30)),
                                    self.out_displays[0].rect)

        elif self.function == "cut":
            if self.out1_data:
                if self.outputs.sprites()[0].send_data(self.out1_data):
                    self.outs_full[0] = False
                    self.out1_data = None
                    self.out_displays[0].update("--------")
                    self.image.blit(pygame.transform.scale(self.out_displays[0].surface, (30, 30)),
                                    self.out_displays[0].rect)

            if self.out2_data:
                if self.outputs.sprites()[1].send_data(self.out2_data):
                    self.outs_full[1] = False
                    self.out2_data = None
                    self.out_displays[1].update("--------")
                    self.image.blit(pygame.transform.scale(self.out_displays[1].surface, (30, 30)),
                                    self.out_displays[1].rect)

    def execute(self):
        # Defines execution
        if not self.allow_execute:
            return
        for inp in self.inputs:
            inp.data = None
            inp.full = False
        for out in self.outputs:
            out.data = None

        if self.function == "rotate_cw" or self.function == "rotate_ccw" or self.function == "rotate_full" or self.function == "cut" or self.function == "delete":
            if self.in1_data is not None:
                if self.function == "rotate_cw":
                    self.rotate_cw()
                elif self.function == "rotate_ccw":
                    self.rotate_ccw()
                elif self.function == "rotate_full":
                    self.rotate_full()
                elif self.function == "cut":
                    self.out2_data = ""
                    self.cut()
                elif self.function == "delete":
                    self.delete()
                elif self.in1_data is not None:
                    pass
                self.in1_data = None

                if self.function != "delete":
                    self.outs_full[0] = True
                    self.out_displays[0].update(self.out1_data)
                    self.image.blit(pygame.transform.scale(self.out_displays[0].surface, (30, 30)),
                                    self.out_displays[0].rect)
                    if self.function == "cut":
                        self.outs_full[1] = True
                        self.out_displays[1].update(self.out2_data)
                        self.image.blit(pygame.transform.scale(self.out_displays[1].surface, (30, 30)),
                                        self.out_displays[1].rect)

        elif self.function == "merge" or self.function == "paint" or self.function == "color":
            if self.in1_data is not None and self.in2_data is not None:
                if self.function == "merge":
                    self.merge()
                elif self.function == "paint":
                    self.paint()
                elif self.function == "color":
                    self.out1_data = color(self.in1_data, self.in2_data)
                elif self.in2_data is not None:
                    pass
                self.in1_data = None
                self.in2_data = None
                self.outs_full[0] = True
                self.outs_full[1] = True

                self.out_displays[0].update(self.out1_data)
                self.image.blit(pygame.transform.scale(self.out_displays[0].surface, (30, 30)),
                                self.out_displays[0].rect)

        for shp in range(len(self.in_displays)):
            self.in_displays[shp].update("--------")
            self.image.blit(pygame.transform.scale(self.in_displays[shp].surface, (30, 30)),
                            self.in_displays[shp].rect)

    def rotate_cw(self):
        data = decode_shape(self.in1_data)
        self.out1_data = ""
        for layer in range(len(data)):
            self.out1_data += data[layer][6:8] + data[layer][0:6]
            self.out1_data += ":"
        self.out1_data = self.out1_data[:-1]

    def rotate_ccw(self):
        data = decode_shape(self.in1_data)
        self.out1_data = ""
        for layer in range(len(data)):
            self.out1_data += data[layer][2:8] + data[layer][0:2]
            self.out1_data += ":"
        self.out1_data = self.out1_data[:-1]

    def rotate_full(self):
        data = decode_shape(self.in1_data)
        self.out1_data = ""
        for layer in range(len(data)):
            self.out1_data += data[layer][4:8] + data[layer][0:4]
            self.out1_data += ":"
        self.out1_data = self.out1_data[:-1]

    def cut(self):
        data = decode_shape(self.in1_data)
        self.out1_data = ""
        for layer in range(len(data)):
            self.out1_data += f"{data[layer][0:4]}----"
            self.out1_data += ":"
            self.out2_data += f"----{data[layer][4:8]}"
            self.out2_data += ":"
        self.out1_data = self.out1_data[:-1]
        self.out2_data = self.out2_data[:-1]

    def merge(self):
        data1 = decode_shape(self.in1_data)
        data2 = decode_shape(self.in2_data)
        self.out1_data = ""
        which_layer = []
        temp_layers = []
        for layer in range(len(data2)):
            layers_combine = 0
            temp_combine = ""
            all_layers_tested = False
            no_issue = True
            while not all_layers_tested:
                if layers_combine + layer <= len(data1) - 1 and layers_combine + len(data2) - 1 <= max_layers - layer:
                    no_issue = True
                    for pos in range(4):
                        if data1[layers_combine + layer][pos * 2: (pos + 1) * 2] == "--":
                            temp_combine += data2[layer][pos * 2: (pos + 1) * 2]
                        elif data2[layer][pos * 2: (pos + 1) * 2] == "--":
                            temp_combine += data1[layer][pos * 2: (pos + 1) * 2]
                        else:
                            no_issue = False
                    layers_combine += 1
                elif no_issue:
                    all_layers_tested = True
                    which_layer.append(True)
                    temp_layers.append(temp_combine)
                else:
                    all_layers_tested = True
                    which_layer.append(False)

        can = True
        for i in which_layer:
            can = can and i
        if can:
            for layer in temp_layers:
                self.out1_data += layer
                self.out1_data += ":"
            self.out1_data = self.out1_data[:-1]
        else:
            which = 0
            for i in which_layer:
                if (which == i + 1 or not which) and not which_layer[i]:
                    which = i
            if which == len(data1) - 1:
                for layer in data1:
                    self.out1_data += layer
                    self.out1_data += ":"
                for layer in data2:
                    self.out1_data += layer
                    self.out1_data += ":"
                self.out1_data = self.out1_data[:-1]

    def paint(self):
        data1 = decode_shape(self.in1_data)
        data2 = self.in2_data

        self.out1_data = ""
        for layer in data1:
            for pos in range(4):
                self.out1_data += layer[pos * 2]
                if layer[2 * pos + 1] != "-":
                    self.out1_data += color(layer[2 * pos + 1], data2)
                else:
                    self.out1_data += "-"
            self.out1_data += ":"
        self.out1_data = self.out1_data[:-1]

    def delete(self):
        self.out1_data = "--------"
