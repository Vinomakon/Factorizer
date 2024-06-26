import pygame
import shape
from dot import Dot

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

path = "data/images/functions/"

max_layers = 2


def decode_shape(data):  # Rewrite the shape into lists
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


def color(data1, data2):  # Mix two colors through an addition of the color values
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

        # Initialization of all variables specific to the function-block
        self.function = func_type
        self.spawn_pos = pos

        self.func_image = pygame.image.load(path + images[func_type][0]).convert_alpha()
        self.func_image = pygame.transform.scale(self.func_image, (200, self.func_image.get_size()[1] * (200 / self.func_image.get_size()[0])))

        self.image = pygame.surface.Surface(self.func_image.get_size(), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - self.func_image.get_size()[0] / 2
        self.rect.y = pos[1] - self.func_image.get_size()[1] / 2

        # Creates a sprite-group for the inputs and outputs
        self.inputs = pygame.sprite.Group()
        self.outputs = pygame.sprite.Group()

        # Creates variables with which data can be processed
        self.out1_data = None
        self.out2_data = None
        self.in1_data = None
        self.in2_data = None

        # Creates States, whether the function-block can receive data or not
        self.full = False
        self.outs_full = [False, False]

        self.allow_execute = False

        self.in_displays = []
        self.out_displays = []

        self.image.blit(self.func_image, (0, 0))

        # For the number of inputs that are needed, input-dots are created with specific locations
        for inp in range(len(images[func_type][1])):
            if images[func_type][1][inp] == 1:
                dot = Dot(1, 16 + 16 * (((-1) ** (inp + 1)) if len(images[func_type][1]) > 1 else 0), self.rect.size, pos, True)
                self.inputs.add(dot)
                self.in_displays.append(shape.Shape("--------", 16 + 16 * (((-1) ** (inp + 1)) if len(images[func_type][1]) > 1 else 0), self.rect.size, 1))
            if images[func_type][1][inp] == 0:
                dot = Dot(0, 16 + 16 * (((-1) ** (inp + 1)) if len(images[func_type][1]) > 1 else 0), self.rect.size, pos, True)
                self.inputs.add(dot)
                self.in_displays.append(shape.Shape("--------", 16 + 16 * (((-1) ** (inp + 1)) if len(images[func_type][1]) > 1 else 0), self.rect.size, 1))
        self.inputs.draw(self.image)

        # For the number of outputs that are needed, output-dots are created with specific locations
        for out in range(len(images[func_type][2])):
            if images[func_type][2][out] == 1:
                dot = Dot(1, 16 + 16 * (((-1) ** (out + 1)) if len(images[func_type][2]) > 1 else 0), self.rect.size, pos, False)
                self.outputs.add(dot)
                self.out_displays.append(shape.Shape("--------", 16 + 16 * (((-1) ** (out + 1)) if len(images[func_type][2]) > 1 else 0), self.rect.size, 0))
            if images[func_type][2][out] == 0:
                dot = Dot(0, 16 + 16 * (((-1) ** (out + 1)) if len(images[func_type][2]) > 1 else 0), self.rect.size, pos, False)
                self.outputs.add(dot)
                self.out_displays.append(shape.Shape("--------", 16 + 16 * (((-1) ** (out + 1)) if len(images[func_type][2]) > 1 else 0), self.rect.size, 0))
        self.outputs.draw(self.image)

        # Some variables to control the dragging of the function-block
        self.dragging = False
        self.init_pos = pos
        self.start_drag = (0, 0)

    def check(self, mouse_pos):
        # Failed Attempt N. 1
        # This would've worked, but more information about the dot was needed
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
        # Initial variables
        on_dot = False
        available = False
        dot_pos = ()
        op_type = None
        data_type = None
        from_dot = None
        # For each input, check if the mouse is on top of the input- or output-dot
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
        # If the function-block is being dragged...
        if state:
            # ...set the start-position of the mouse to a variable
            self.start_drag = mouse_pos

            # Empties all the variables in the dots and the current data that is available
            self.refresh()
            self.deletion()
            self.out1_data = None
            self.out2_data = None
            self.in1_data = None
            self.in2_data = None
        # When stopped...
        else:
            # ...set the current positions of the function and the dots
            self.init_pos = (self.rect.x, self.rect.y)
            self.inputs.update((self.rect.x, self.rect.y))
            self.outputs.update((self.rect.x, self.rect.y))

    def refresh(self):
        # All the information of the connections, data, everything needs to be deleted
        # This section does exactly this

        # First all inputs and outputs get cleared
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
        for out in self.outputs:
            out.data = None
            out.full = False
            out.sent = False
        # Then everything inside the function-block get deleted as well
        self.out1_data = None
        self.out2_data = None
        self.in1_data = None
        self.in2_data = None
        self.full = False
        self.outs_full = [False, False]
        self.allow_execute = True

    def deletion(self):
        # All connections between the functions are disconnected
        for inp in self.inputs:
            inp.del_connection()
        for out in self.outputs:
            out.del_connection()

    def update(self, mouse_pos):
        # If the function-block is being dragged,
        # the current position of the mouse is taken and translated into the position of the function-block
        if self.dragging:
            self.rect.x = self.init_pos[0] - self.start_drag[0] + mouse_pos[0]
            self.rect.y = self.init_pos[1] - self.start_drag[1] + mouse_pos[1]

        # For each of the function-blocks, they get checked if they can receive data if their outputs aren't full
        elif (self.function == "rotate_cw" or self.function == "rotate_ccw" or self.function == "rotate_full" or
              self.function == "merge" or self.function == "paint" or self.function == "color"):
            self.full = self.outs_full[0]
        # Since the cut function has two outputs, both of the outputs get checked
        elif self.function == "cut":
            self.full = self.outs_full[0] or self.outs_full[1]

        # Failed Attempt N.1
        # This allowed basic communication between the functions, but halted the process,
        # if the function wasn't part of a whole system, where it didn't do anything.
        # Only after the whole system was connected, the receiving and sending would commence
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
        # Checks if data is available to take, and the input isn't full yet
        if self.in1_data is None and self.inputs.sprites()[0].data:
            self.in1_data = self.inputs.sprites()[0].data
            self.allow_execute = True
            self.inputs.sprites()[0].full = True

            self.in_displays[0].update(self.in1_data)
            self.image.blit(pygame.transform.scale(self.in_displays[0].surface, (30, 30)),
                            self.in_displays[0].rect)
        # If the input is already full but hasn't been emptied, the function is full
        elif self.in1_data is not None:
            self.allow_execute = True
            self.inputs.sprites()[0].full = True
        # Otherwise, it's not allowed to execute and isn't full
        else:
            self.allow_execute = False
            self.inputs.sprites()[0].full = False

        # Same for the second input, since there is a second one
        if self.function == "merge" or self.function == "paint" or self.function == "color":
            # Checks if data is available to take, and the input isn't full yet
            if self.in2_data is None and self.inputs.sprites()[1].data:
                self.in2_data = self.inputs.sprites()[1].data
                self.allow_execute = True and self.allow_execute
                self.inputs.sprites()[1].full = True

                self.in_displays[1].update(self.in2_data)
                self.image.blit(pygame.transform.scale(self.in_displays[1].surface, (30, 30)),
                                self.in_displays[1].rect)
            # If the input is already full but hasn't been emptied, the function is full
            elif self.in2_data is not None:
                self.allow_execute = True and self.allow_execute
                self.inputs.sprites()[1].full = True
            # Otherwise, it's not allowed to execute and isn't full
            else:
                self.allow_execute = False and self.allow_execute
                self.inputs.sprites()[1].full = False

        # Then tell if the function can process the shape
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
        # Since the delete-function has nothing to send, the function gets broken off
        if self.function == "delete":
            return
        # The function-block can only send data, if there is any available
        if self.out1_data:
            if self.outputs.sprites()[0].send_data(self.out1_data):
                # The 1st output isn't full anymore, which allows processing the incoming shapes
                self.outs_full[0] = False
                self.out1_data = None
                # Displaying an empty slot
                self.out_displays[0].update("--------")
                self.image.blit(pygame.transform.scale(self.out_displays[0].surface, (30, 30)),
                                self.out_displays[0].rect)

        # The cut function has 2 datas to send out, so the second is sent as well
        if self.function == "cut":
            if self.out2_data:
                if self.outputs.sprites()[1].send_data(self.out2_data):
                    # The 2nd output isn't full anymore, which allows processing the incoming shapes
                    self.outs_full[1] = False
                    self.out2_data = None
                    # Displaying an empty slot
                    self.out_displays[1].update("--------")
                    self.image.blit(pygame.transform.scale(self.out_displays[1].surface, (30, 30)),
                                    self.out_displays[1].rect)

    def execute(self):
        # Only if the function is even allowed to execute this function can commence
        if not self.allow_execute:
            return
        # Empty the input dots from any data and allow them to get data
        for inp in self.inputs:
            inp.data = None
            inp.full = False
        # Since the function-block isn't full, we can also empty the output-dots data
        for out in self.outputs:
            out.data = None

        # All the mentioned functions below only have one input
        if self.function == "rotate_cw" or self.function == "rotate_ccw" or self.function == "rotate_full" or self.function == "cut" or self.function == "delete":
            # So it only needs one input data to be present
            if self.in1_data is not None:
                # Based on the function assigned, the appropriate process is applied
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
                # Empty the input
                self.in1_data = None
                # Define that the output is full
                self.outs_full[0] = True

                # If it's the delete function, empty the input slot
                if self.function == "delete":
                    # Revert the function
                    self.outs_full[0] = False
                # Since the delete function doesn't have an output,
                # only if it's not the delete-function, it can show the shape
                else:
                    # Display what is currently in the output slot
                    self.out_displays[0].update(self.out1_data)
                    self.image.blit(pygame.transform.scale(self.out_displays[0].surface, (30, 30)),
                                    self.out_displays[0].rect)

                # Since the cut function has 2 outputs, the second
                if self.function == "cut":
                    # Also define the second output as full
                    self.outs_full = [True, True]
                    print(self.out1_data, self.out2_data, self.outs_full)
                    self.out_displays[1].update(self.out2_data)
                    self.image.blit(pygame.transform.scale(self.out_displays[1].surface, (30, 30)),
                                    self.out_displays[1].rect)
                print(self.function)
        # For these functions below two input datas are necessary
        elif self.function == "merge" or self.function == "paint" or self.function == "color":
            # So only if both input datas are present, it can continue
            if self.in1_data is not None and self.in2_data is not None:
                # Based on the function assigned, the appropriate process is applied
                if self.function == "merge":
                    self.merge()
                elif self.function == "paint":
                    self.paint()
                elif self.function == "color":
                    self.out1_data = color(self.in1_data, self.in2_data)
                elif self.in2_data is not None:
                    pass
                # Empty the inputs
                self.in1_data = None
                self.in2_data = None
                # Define that the outputs are full
                self.outs_full[0] = True
                self.outs_full[1] = True

                self.out_displays[0].update(self.out1_data)
                self.image.blit(pygame.transform.scale(self.out_displays[0].surface, (30, 30)),
                                self.out_displays[0].rect)

        # Show that the inputs are empty
        for shp in range(len(self.in_displays)):
            self.in_displays[shp].update("--------")
            self.image.blit(pygame.transform.scale(self.in_displays[shp].surface, (30, 30)),
                            self.in_displays[shp].rect)

    # After this section, the processing functions are defined. The names of the functions are self-explainable

    def rotate_cw(self):  # Clockwise rotation
        data = decode_shape(self.in1_data)
        self.out1_data = ""
        for layer in range(len(data)):
            self.out1_data += data[layer][6:8] + data[layer][0:6]
            self.out1_data += ":"
        self.out1_data = self.out1_data[:-1]

    def rotate_ccw(self):  # Counter-clockwise rotation
        data = decode_shape(self.in1_data)
        self.out1_data = ""
        for layer in range(len(data)):
            self.out1_data += data[layer][2:8] + data[layer][0:2]
            self.out1_data += ":"
        self.out1_data = self.out1_data[:-1]

    def rotate_full(self):  # A full rotation of 180 degrees
        data = decode_shape(self.in1_data)
        self.out1_data = ""
        for layer in range(len(data)):
            self.out1_data += data[layer][4:8] + data[layer][0:4]
            self.out1_data += ":"
        self.out1_data = self.out1_data[:-1]

    def cut(self):  # A horizontal split of a shape
        data = decode_shape(self.in1_data)
        self.out1_data = ""
        for layer in range(len(data)):
            self.out1_data += f"{data[layer][0:4]}----"
            self.out1_data += ":"
            self.out2_data += f"----{data[layer][4:8]}"
            self.out2_data += ":"
        self.out1_data = self.out1_data[:-1]
        self.out2_data = self.out2_data[:-1]

    def merge(self):  # Merge two shapes
        data2 = decode_shape(self.in1_data)
        data1 = decode_shape(self.in2_data)
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

    def paint(self):  # Paint a shape with the color that is getting fed into it
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

    def delete(self):  # Give an empty shape
        self.out1_data = "--------"
