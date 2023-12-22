import pygame
import func_block
import constant
import spawner
import level_menu
import level_end
import time

functions = ["delete", "rotate_cw", "rotate_ccw", "rotate_full", "cut", "color", "paint", "merge"]


class Test:
    def __init__(self, screen_size):
        self.surface = pygame.surface.Surface(screen_size)
        self.surface.fill((100, 100, 100))
        self.background = pygame.image.load("images/background.png")
        self.background = pygame.transform.scale(self.background, (2560, self.background.get_size()[1] / (self.background.get_size()[0] / 2560)))
        self.background_rect = self.background.get_rect()
        self.screen_size = screen_size
        self.functions = pygame.sprite.Group()
        self.constants = pygame.sprite.Group()

        self.complete = False

        cons = constant.Constant((0, screen_size[1] / 2), "SyCuWcRr", False)
        self.constants.add(cons)

        self.goal = constant.Constant((screen_size[0] - 150, screen_size[1] / 2), "--Rr--Cu", True)
        self.constants.add(self.goal)

        self.spawner = spawner.Spawner(screen_size, [1, 1, 1, 1, 1, 1, 1, 1])
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
            if self.spawner.rect.collidepoint(mouse_pos):
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
        if self.goal.check_goal():
            self.complete = True
        return self.complete, 0, 0

    def execute(self):
        for func in self.functions:
            func.execute()

    def spawn(self, func, mouse_pos):
        function = func_block.Function(functions[func], mouse_pos)
        function.draggable(True, (mouse_pos[0] + function.rect.w / 2, mouse_pos[1] + function.rect.h / 2))
        self.dragging = function

    def delete_func(self, mouse_pos):
        for func in self.functions:
            if func.rect.collidepoint(mouse_pos):
                func.deletion()
                self.functions.remove(func)
                self.redo_connections()

    """
    def start(self, main_display, fps):
        fps_clock = pygame.time.Clock()
        tick = 0
        tick_duration = 0.25
        tick_time = time.time()

        menu_screen = level_menu.LevelMenu(self.screen_size)
        level_screen = level_end.LevelEnd(self.screen_size)

        function = None
        on_menu = False

        while True:
            for event in pygame.event.get():
                if self.complete:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed()[0]:
                            function = level_screen.on_click(event.pos)
                            if function == "menu":
                                return "menu"
                            elif function == "restart":
                                return "restart"
                elif on_menu:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed()[0]:
                            function = menu_screen.on_click(event.pos)
                            if function == "menu":
                                return "menu"
                            elif function == "back":
                                on_menu = False
                            elif function == "restart":
                                return "restart"
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            on_menu = not on_menu
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed()[0]:
                            self.on_click(event.pos)
                        elif pygame.mouse.get_pressed()[2]:
                            self.delete_func(event.pos)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.on_release(event.pos)
                    elif event.type == pygame.KEYDOWN:
                        if 49 <= event.key <= 57:
                            self.spawn(event.key - 49, pygame.mouse.get_pos())
                        if event.key == pygame.K_ESCAPE:
                            on_menu = not on_menu

            if self.complete:
                main_display.blit(pygame.transform.scale(self.surface, self.screen_size, (0, 0)))
                level_screen.refresh(pygame.mouse.get_pos())
                main_display.blit(level_screen.surface, (0, 0))
            elif on_menu:
                main_display.blit(pygame.transform.scale(self.surface, self.screen_size), (0, 0))
                menu_screen.refresh(pygame.mouse.get_pos())
                main_display.blit(menu_screen.surface, (0, 0))
            else:
                self.refresh(pygame.mouse.get_pos())
                main_display.blit(pygame.transform.scale(self.surface, self.screen_size), (0, 0))
                if time.time() - tick_time >= tick_duration:
                    if tick == 0:
                        goal_reached, level, quality = self.tick()
                        if goal_reached:
                            level_screen = level_end.LevelEnd(self.screen_size, 0)
                        tick = 1
                    else:
                        self.execute()
                        tick = 0
                    tick_time = time.time()

            pygame.display.update()
            fps_clock.tick(fps)
    """
