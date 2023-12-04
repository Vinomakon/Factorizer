import pygame
import func_block
import constant


class Test:
    def __init__(self, screen_size):
        self.surface = pygame.surface.Surface(screen_size)
        self.surface.fill((100, 100, 100))
        self.screen_size = screen_size
        self.functions = pygame.sprite.Group()
        self.constants = pygame.sprite.Group()

        function = func_block.Function("rotate_ccw", (0, 0), "CyRcSyWc")
        self.functions.add(function)
        function = func_block.Function("rotate_cw", (30, 30))
        self.functions.add(function)
        function = func_block.Function("rotate_ccw", (60, 60))
        self.functions.add(function)
        function = func_block.Function("rotate_ccw", (90, 90))
        self.functions.add(function)

        cons = constant.Constant((0, screen_size[1] / 2), "--Cu--Rr", False)
        self.constants.add(cons)
        function1 = func_block.Function("delete", (200, 200))
        self.functions.add(function1)
        # function2 = func_block.Function("delete", (50, 50))
        # self.functions.add(function2)

        self.functions.draw(self.surface)
        self.connections = []
        self.func_connections = []
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
        check_connected = True
        for func in range(len(self.functions)):
            current_func = self.functions.sprites()[len(self.functions) - func - 1]
            if current_func.rect.collidepoint(mouse_pos) and not op_done:
                on_dot, available, dot_pos, op_type, data_type,  op_func_dot = current_func.check(mouse_pos)
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
                    elif self.connecting:
                        # If one dot is being connected, the dot is available,
                        # one is an input and the other an output and both are the same type:
                        # Connect both of these dots and create connections between them.
                        if available and self.connection_type != op_type and self.data_type == data_type:
                            connection = (self.connection1, dot_pos) if op_type == 1 else (dot_pos, self.connection1)
                            self.op_func_dot.connection = connection
                            op_func_dot.connection = connection
                            self.connections.append(connection)
                            self.func_connections.append((self.op_func_dot, op_func_dot) if op_type == 1 else (op_func_dot, self.op_func_dot))
                            self.op_func_dot.connected = True
                            op_func_dot.connecting = True
                            op_func_dot.connected = True
                            self.connecting = False
                        # Else: disable the active connecting and make the dot available again
                        else:
                            check_connected = False

                    # Put the used functions in front of the others
                    self.op_func = current_func
                    self.functions.remove(self.op_func)
                    self.functions.add(self.op_func)
                # Else if not currently connecting: Remove all existing connections to this function
                elif not self.connecting:
                    self.connecting = False
                    del_connections = current_func.draggable(True, mouse_pos)
                    if len(self.connections) != 0:
                        for con in del_connections:
                            if len(self.connections) != 0 and con != ():
                                con_loc = self.connections.index(con)
                                for dot in self.func_connections[con_loc]:
                                    dot.connected = False
                                    dot.connecting = False
                                    dot.connection = ()
                                self.func_connections.pop(con_loc)
                                self.connections.pop(con_loc)
                    op_done = True
                    self.op_func = current_func
                    self.functions.remove(self.op_func)
                    self.functions.add(self.op_func)
                else:
                    check_connected = False

        for cons in range(len(self.constants)):
            current_cons = self.constants.sprites()[cons]
            on_dot, available, dot_pos, op_type, data_type, op_func_dot = current_cons.check(mouse_pos)
            if on_dot:
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
                    check_connected = True
                elif self.connecting:
                    # If one dot is being connected, the dot is available,
                    # one is an input and the other an output and both are the same type:
                    # Connect both of these dots and create connections between them.
                    if available and self.connection_type != op_type and self.data_type == data_type:
                        connection = (self.connection1, dot_pos) if op_type == 1 else (dot_pos, self.connection1)
                        self.op_func_dot.connection = connection
                        op_func_dot.connection = connection
                        self.connections.append(connection)
                        self.func_connections.append(
                            (self.op_func_dot, op_func_dot) if op_type == 1 else (op_func_dot, self.op_func_dot))
                        self.op_func_dot.connected = True
                        op_func_dot.connecting = True
                        op_func_dot.connected = True
                        self.connecting = False
                        check_connected = True
                    # Else: disable the active connecting and make the dot available again
                    else:
                        check_connected = False

        if not check_connected:
                self.connecting = False
                self.connection1 = ()
                if self.op_func_dot is not None:
                    self.op_func_dot.connecting = False
                    self.op_func_dot.connected = False
                    self.op_func_dot.connection = ()
                self.op_func_dot = None
                self.op_func = None

    def on_release(self, mouse_pos):
        for self.op_func in self.functions:
            self.op_func.draggable(False, mouse_pos)

    def refresh(self, mouse_pos):
        self.surface.fill((100, 100, 100))
        self.functions.update(mouse_pos)
        self.functions.draw(self.surface)
        self.constants.draw(self.surface)
        for connection in self.connections:
            pygame.draw.line(self.surface, (77, 0, 0),  connection[0], connection[1], 8)
        if self.connecting:
            pygame.draw.line(self.surface, (77, 0, 0), self.connection1, mouse_pos, 8)

    def tick(self):
        for func in self.functions:
            func.send_data()
        for con in self.func_connections:
            con[1].data = con[0].data
        for func in self.functions:
            func.receive_data()

    def execute(self):
        for func in self.functions:
            func.execute()
