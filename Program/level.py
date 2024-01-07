import pygame
import func_block
import constant
import spawner
import level_setup

functions = ["delete", "rotate_cw", "rotate_ccw", "rotate_full", "cut", "color", "paint", "merge"]


class Level:
    def __init__(self, screen_size, level):
        self.surface = pygame.surface.Surface(screen_size)
        self.surface.fill((100, 100, 100))
        self.background = pygame.image.load("data/images/background.png")
        self.background = pygame.transform.scale(self.background, (
            screen_size[0], self.background.get_size()[1] / (self.background.get_size()[0] / screen_size[0])))
        self.background_rect = self.background.get_rect()
        self.corners = pygame.transform.scale(pygame.image.load("data/images/corners.png").convert_alpha(), (
            screen_size[0], self.background.get_size()[1] / (self.background.get_size()[0] / screen_size[0])))
        self.background.blit(self.corners, (0, 0))
        self.screen_size = screen_size
        self.functions = pygame.sprite.Group()
        self.constants = pygame.sprite.Group()
        self.goals = []

        self.complete = []
        self.setup = level_setup.levels[level]
        for outputs in range(len(self.setup[0])):
            cons = constant.Constant((0, (screen_size[1] / (len(self.setup[0]) + 1)) * (outputs + 1)),
                                     self.setup[0][outputs], False)
            self.constants.add(cons)
        for goals in range(len(self.setup[1])):
            self.goal = constant.Constant((screen_size[0] - 150,
                                           (screen_size[1] / (len(self.setup[1]) + 1)) * (goals + 1)),
                                          self.setup[1][goals], True)
            self.constants.add(self.goal)
            self.goals.append(self.goal)
            self.complete.append(False)
        self.spawner = spawner.Spawner(screen_size, self.setup[2])
        self.dragging = None

        self.functions.draw(self.surface)
        self.connections = []
        self.connecting = False
        self.connection1 = ()
        self.connection_type = None
        self.op_func = None
        self.op_func_dot = None
        self.data_type = None

    def res_change(self, screen_size):
        self.surface = pygame.surface.Surface(screen_size, pygame.SRCALPHA)

    def on_click(self, mouse_pos):
        self.surface = pygame.surface.Surface(self.screen_size, pygame.SRCALPHA)
        # Failed Attempt N.1
        """
        connection_active = False
        dragging_object = False
        action_done = False
        for func_num in range(len(self.functions)):
            self.op_func = self.functions.sprites()[len(self.functions) - func_num - 1]
            on_dot, dot_pos, dot_available, connect_type = self.op_func.check(mouse_pos)
            print(self.connect_type, connect_type)
            if on_dot and not action_done:
                if self.connecting and dot_available and not (self.connect_type == connect_type):
                    self.connections.append((self.connect1, dot_pos))
                    for out in self.op_func.output:
                        out.check(self.connect1 if connect_type == 0 else dot_pos, 1)
                    for inp in self.op_func.input:
                        inp.check(self.connect1 if connect_type == 1 else dot_pos, 1)
                    self.connecting = False
                    self.connect_type = None
                    connection_active = False
                elif self.connecting and not dot_available:
                    connection_active = True
                    self.connecting = False
                    if self.connect1 is not None:
                        print(self.connect1)
                        for out in self.op_func.output:
                            out.check(self.connect1 if connect_type == 0 else dot_pos, 0)
                        for inp in self.op_func.input:
                            inp.check(self.connect1 if connect_type == 1 else dot_pos, 0)
                        self.connect1 = None
                    self.connect_type = None
                elif dot_available:
                    self.connecting = True
                    self.connect1 = dot_pos
                    connection_active = True
                    self.connect_type = connect_type
                elif self.connect_type == connect_type:
                    for out in self.op_func.output:
                        out.check(self.connect1 if self.connect_type == 1 else self.connect1, 0)
                    for inp in self.op_func.input:
                        inp.check(self.connect1 if self.connect_type == 0 else self.connect1, 0)
                action_done = True
            elif self.op_func.rect.collidepoint(mouse_pos) and not action_done:
                if not dragging_object:
                    self.op_func.draggable(True, mouse_pos)
                    dragging_object = True
                for pos in self.connections:
                    connection_available = 0
                    for out in self.op_func.output:
                        connection_available += out.check(pos[0], 2)
                        connection_available += out.check(pos[1], 2)
                    for inp in self.op_func.input:
                        connection_available += inp.check(pos[1], 2)
                        connection_available += inp.check(pos[0], 2)
                    if connection_available != 0:
                        self.connections.pop(self.connections.index(pos))
                action_done = True
        if not connection_active:
            for out in self.op_func.output:
                out.check(self.connect1, 0)
            for inp in self.op_func.input:
                inp.check(self.connect1, 0)
            self.connect1 = None
            self.connect_type = None
            self.connecting = False
            self.op_func = None
            """
        op_done = False
        touched = 0
        for func in range(len(self.functions)):
            current_func = self.functions.sprites()[len(self.functions) - func - 1]
            if current_func.rect.collidepoint(mouse_pos) and not op_done:
                touched += 1
                on_dot, available, dot_pos, op_type, data_type, op_func_dot = current_func.check(mouse_pos)
                if on_dot:
                    op_done = True
                    if not self.connecting:
                        # If nothing is being connected and the dot is available:
                        # Enable to be ready to connect to another dot.
                        if available:
                            self.connecting = True
                            self.connection1 = dot_pos
                            self.connection_type = op_type
                            self.data_type = data_type
                            op_func_dot.connecting = True
                            self.op_func_dot = op_func_dot

                            self.redo_connections()
                            return
                    elif self.connecting:
                        # If one dot is being connected, the dot is available,
                        # one is an input and the other an output and both are the same type:
                        # Connect both of these dots and create connections between them.
                        if available and self.connection_type != op_type and (
                                self.data_type == data_type or current_func.function == "delete"):
                            connection = (self.connection1, dot_pos) if op_type == 1 else (dot_pos, self.connection1)
                            self.op_func_dot.connection_pos = connection
                            op_func_dot.connection_pos = connection
                            self.connections.append(connection)
                            self.op_func_dot.connected_dot = op_func_dot
                            op_func_dot.connected_dot = self.op_func_dot
                            self.connections.append(connection)
                            op_func_dot.connecting = True
                            self.op_func_dot.connected = True
                            op_func_dot.connected = True
                            self.connecting = False

                            self.redo_connections()
                            return
                        # Else: disable the active connecting and make the dot available again

                    # Put the used functions in front of the others
                    self.op_func = current_func
                    self.functions.remove(self.op_func)
                    self.functions.add(self.op_func)
                # Else if not currently connecting: Remove all existing connections to this function
                elif not self.connecting:
                    self.op_func = current_func
                    self.functions.remove(self.op_func)
                    self.functions.add(self.op_func)
                    self.connecting = False
                    current_func.draggable(True, mouse_pos)
                    self.functions.remove(current_func)
                    self.dragging = current_func

                    self.redo_connections()
                    return

        for cons in range(len(self.constants)):
            current_cons = self.constants.sprites()[cons]
            on_dot, available, dot_pos, op_type, data_type, op_func_dot = current_cons.check(mouse_pos)
            if on_dot:
                touched += 1
                if not self.connecting:
                    # If nothing is being connected and the dot is available:
                    # Enable to be ready to connect to another dot.
                    if available:
                        self.connecting = True
                        self.connection1 = dot_pos
                        self.connection_type = op_type
                        self.data_type = data_type
                        op_func_dot.connecting = True
                        self.op_func_dot = op_func_dot

                        self.redo_connections()
                        return
                elif self.connecting:
                    # If one dot is being connected, the dot is available,
                    # one is an input and the other an output and both are the same type:
                    # Connect both of these dots and create connections between them.
                    if available and self.connection_type != op_type and self.data_type == data_type:
                        connection = (self.connection1, dot_pos) if op_type == 1 else (dot_pos, self.connection1)
                        self.op_func_dot.connection_pos = connection
                        op_func_dot.connection_pos = connection
                        self.connections.append(connection)
                        self.op_func_dot.connected_dot = op_func_dot
                        op_func_dot.connected_dot = self.op_func_dot
                        op_func_dot.connecting = False
                        self.op_func_dot.connecting = False
                        self.op_func_dot.connected = True
                        op_func_dot.connected = True
                        self.connecting = False

                        self.redo_connections()
                        return
                    # Else: disable the active connection and make the dot available again

        func = self.spawner.check(mouse_pos)
        if func is not None:
            self.spawn(func, mouse_pos)

        self.connecting = False
        self.connection1 = ()
        if self.op_func_dot is not None:
            self.op_func_dot.connecting = False
            self.op_func_dot.connected = False
        self.op_func_dot = None
        self.op_func = None

        self.redo_connections()

    def redo_connections(self):
        self.connections.clear()
        for func in self.functions:
            for out in func.outputs:
                if out.connection_pos != ():
                    self.connections.append(out.connection_pos)
        for cons in self.constants:
            if cons.dot.connection_pos != ():
                self.connections.append(cons.dot.connection_pos)

    def on_release(self, mouse_pos):
        if self.dragging:
            if self.spawner.rect.colliderect(self.dragging.rect):
                self.functions.remove(self.dragging)
                self.dragging = None
            else:
                self.dragging.draggable(False, mouse_pos)
                self.functions.add(self.dragging)
                self.dragging = None

    def refresh(self, mouse_pos):
        for func in self.functions:
            func.update(mouse_pos)
        self.surface.blit(self.background, self.background_rect)
        self.functions.update(mouse_pos)
        self.functions.draw(self.surface)
        self.constants.draw(self.surface)
        self.surface.blit(self.goal.image, self.goal.rect)
        self.surface.blit(self.spawner.image, self.spawner.rect)
        if self.dragging:
            self.dragging.update(mouse_pos)
            self.surface.blit(self.dragging.image, self.dragging.rect)
        for connection in self.connections:
            pygame.draw.line(self.surface, (77, 0, 0), connection[0], connection[1], 8)
        if self.connecting:
            pygame.draw.line(self.surface, (77, 0, 0), self.connection1, mouse_pos, 8)

    def tick(self):
        for func in self.functions:
            func.send_data()
        for cons in self.constants:
            cons.send_data()
        for func in self.functions:
            func.receive_data()
        complete = True
        for goal in range(len(self.goals)):
            if self.goals[goal].check_goal():
                self.complete[goal] = True
            else:
                self.complete[goal] = False
                complete = False
            self.goals[goal].del_data()
        return complete, len(self.functions)

    def execute(self):
        for func in self.functions:
            func.execute()

    def spawn(self, func, mouse_pos):
        if self.setup[2][func]:
            function = func_block.Function(functions[func], mouse_pos)
            function.draggable(True, (mouse_pos[0] + function.rect.w / 2, mouse_pos[1] + function.rect.h / 2))
            self.dragging = function

    def refresh_data(self):
        for func in self.functions:
            func.refresh()

    def delete_func(self, mouse_pos):
        for func in self.functions:
            if func.rect.collidepoint(mouse_pos):
                func.deletion()
                self.functions.remove(func)
                self.redo_connections()
