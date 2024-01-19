import copy
import pygame
from func_block import Function
from constant import Constant
from spawner import Spawner
from level_setup import levels as level_setups
from spec_button import SpecButton

functions = ["delete", "rotate_cw", "rotate_ccw", "rotate_full", "cut", "merge", "paint", "color"]


class Level:
    def __init__(self, screen_size, level):
        # Initializing screen-specific variables
        self.surface = pygame.surface.Surface(screen_size)
        self.surface.fill((100, 100, 100))
        self.background = pygame.image.load("data/images/level/background.png")
        self.background = pygame.transform.scale(self.background, (
            screen_size[0], self.background.get_size()[1] / (self.background.get_size()[1] / screen_size[1])))
        self.background_rect = self.background.get_rect()
        self.corners = pygame.transform.scale(pygame.image.load("data/images/level/corners.png").convert_alpha(), (
            screen_size[0], self.background.get_size()[1] / (self.background.get_size()[1] / screen_size[1])))
        self.background.blit(self.corners, (0, 0))
        self.screen_size = screen_size
        # Arrays and sprite-group to have all functions and constants in one place
        self.functions = pygame.sprite.Group()
        self.constants = pygame.sprite.Group()
        self.goals = []

        self.ratio = screen_size[0] / 2560  # For different screen-sizes

        # Array to save if every goal has been reached
        self.complete = []
        self.setup = level_setups[level]

        # Setup for all existing constant outputs and goals
        for outputs in range(len(self.setup[0])):
            cons = Constant(screen_size, (0, (screen_size[1] / (len(self.setup[0]) + 1)) * (outputs + 1)),
                                     self.setup[0][outputs], False)
            self.constants.add(cons)
        for goals in range(len(self.setup[1])):
            self.goal = Constant(screen_size, (screen_size[0] - 150,
                                           (screen_size[1] / (len(self.setup[1]) + 1)) * (goals + 1)),
                                          self.setup[1][goals], True)
            self.constants.add(self.goal)
            self.goals.append(self.goal)
            self.complete.append(False)

        # Setting up the spawner
        self.spawner = Spawner(screen_size, self.setup[2])
        self.dragging = None

        # Setup of the buttons
        self.buttons = pygame.sprite.Group()
        self.buttons.add(SpecButton((int(150 * self.ratio), int(150 * self.ratio)), (screen_size[0] / 2 - int(90 * self.ratio), screen_size[1] / 14.5), "menu"))
        self.buttons.add(SpecButton((int(150 * self.ratio), int(150 * self.ratio)), (screen_size[0] / 2 + int(90 * self.ratio), screen_size[1] / 14.5), "refresh"))

        # Initializing of specific variables
        self.connections = []
        self.connecting = False
        self.connection1 = ()
        self.connection_type = None
        self.op_func = None
        self.op_func_dot = None
        self.data_type = None

    def on_click(self, mouse_pos, delete=False):
        # Failed Attempt N.1
        # Using this kind of approach of connecting the functions was quite challenging
        # Since a lot of other processes needed to be done when something was clicked on,
        # it was better to rewrite the whole process of connecting, deleting, spawning, clicking, etc.
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

        # If the spawner is pressed, then spawn the function and don't do anything else
        func_ = self.spawner.check(mouse_pos)
        if func_ is not None:
            self.spawn(func_, mouse_pos)
            return None, "spawn"
        # If a button is pressed, return the button function and don't do anything else
        for but in self.buttons:
            if but.rect.collidepoint(mouse_pos):
                return but.func, "button"

        # First going through every function available
        op_done = False
        for func in range(len(self.functions)):
            current_func = self.functions.sprites()[len(self.functions) - func - 1]
            # If the function-block is clicked/pressed/held on
            if current_func.rect.collidepoint(mouse_pos):
                # If a function needs to be deleted, it does this and doesn't do anything else
                if delete:
                    self.delete_func(current_func)
                    self.connecting = False
                    return "delete", None
                on_dot, available, dot_pos, op_type, data_type, op_func_dot = current_func.check(mouse_pos)
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

                            self.redo_connections()
                            return None, "connect"

                    elif self.connecting:
                        # If one dot is being connected, the dot is available,
                        # one is an input and the other an output, and both are the same type:
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
                            return None, "connect"
                        # Else: disable the active connecting and make the dot available again

                    # Put the used functions in front of the others
                    self.op_func = current_func
                    self.functions.remove(self.op_func)
                    self.functions.add(self.op_func)
                # Else if not currently connecting: Remove all existing connections to this function
                elif not self.connecting:
                    self.op_func = current_func
                    current_func.draggable(True, mouse_pos)
                    self.functions.remove(current_func)
                    self.dragging = current_func

                    self.redo_connections()
                    return None, "connect"

        # If the function needed to be deleted, nothing else needs to be done
        if delete:
            return None, None

        # Secondly, going through every function available
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

                        self.redo_connections()
                        return None, "connect"
                elif self.connecting:
                    # If one dot is being connected, the dot is available,
                    # one is an input and the other an output, and both are the same type:
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
                        self.forget()

                        self.redo_connections()
                        return None, "connect"

        # Otherwise, nothing is being connected and the functions revert to its previous state or unconnected
        if self.op_func_dot is not None:
            self.op_func_dot.connecting = False
            self.op_func_dot.connected = False
        self.forget()

        # Reload all connections
        self.redo_connections()
        return None, None

    def redo_connections(self):
        # Clearing the array
        self.connections.clear()

        # For every function-block, the connection is read and is added into the array
        for func in self.functions:
            for out in func.outputs:
                if out.connection_pos != ():
                    self.connections.append(out.connection_pos)
        # Same for all the constants
        for cons in self.constants:
            if cons.dot.connection_pos != ():
                self.connections.append(cons.dot.connection_pos)

    def on_release(self, mouse_pos):
        # Only if a function-block has been dragged...
        if self.dragging:
            # ...and if the function-block is on top of the spawner...
            if self.spawner.rect.colliderect(self.dragging.rect):
                # ...the function-block gets deleted
                self.functions.remove(self.dragging)
                self.forget()
                return "delete"
            # Otherwise...
            else:
                # ...add the function onto the screen
                self.dragging.draggable(False, mouse_pos)
                func_ = copy.copy(self.dragging)
                self.functions.add(func_)
                self.functions.sprites()[len(self.functions) - 1].refresh()
                self.forget()

    def refresh(self, mouse_pos):
        # Update the function-blocks on any new states
        for func in self.functions:
            func.update(mouse_pos)

        # Redraw everything onto the screen
        self.surface.blit(self.background, self.background_rect)
        self.functions.update(mouse_pos)
        self.functions.draw(self.surface)
        self.constants.draw(self.surface)
        self.surface.blit(self.goal.image, self.goal.rect)
        self.surface.blit(self.spawner.image, self.spawner.rect)

        # For every connection that is made, a line is drawn
        for connection in self.connections:
            pygame.draw.line(self.surface, (77, 77, 77), connection[0], connection[1], 8)
            pygame.draw.line(self.surface, (130, 130, 130), connection[0], connection[1], 2)
        # If functions are being connected, the line to it is also shown
        if self.connecting:
            pygame.draw.line(self.surface, (77, 77, 77), self.connection1, mouse_pos, 8)
            pygame.draw.line(self.surface, (130, 130, 130), self.connection1, mouse_pos, 2)
        # If a function-block is being dragged, that function-block is also shown
        if self.dragging:
            self.dragging.update(mouse_pos)
            self.surface.blit(self.dragging.image, self.dragging.rect)
        # For every button, check if the mouse is on it, and show the hover-image
        for but in self.buttons:
            if but.rect.collidepoint(mouse_pos):
                but.check(True)
            else:
                but.check(False)
        self.buttons.draw(self.surface)

    def tick(self):
        # This section is for the communication between the function-blocks
        # For every function-block and constant that exists, the data gets sent or received
        for cons in self.constants:
            cons.send_data()
        for func in self.functions:
            func.send_data()
        for func in self.functions:
            func.receive_data()

        complete = True
        # If any of the goals has reached their required number of shapes, it returns True
        # As soon as all goals are complete, the function returns as complete
        for goal in range(len(self.goals)):
            if self.goals[goal].check_goal():
                self.complete[goal] = True
            else:
                self.complete[goal] = False
                complete = False
        return complete, len(self.functions)

    def execute(self):
        # For every function, the data inside is being processed
        for func in self.functions:
            func.execute()

    def spawn(self, func, mouse_pos):
        # Checks if the function is allowed in the current level, and if it is, it spawns it
        if self.setup[2][func]:
            function = Function(functions[func], mouse_pos)
            self.dragging = function
            function.draggable(True, (mouse_pos[0] + function.rect.w / 2, mouse_pos[1] + function.rect.h / 2))

    def refresh_data(self):
        # All the function data is emptied to restart the cycle
        for func in self.functions:
            func.refresh()
        # Refreshes the goals to their start-state
        for goal in self.goals:
            goal.del_data()

    def delete_func(self, func):
        # Deletes the function, the connection entirely
        func.deletion()
        self.functions.remove(func)
        self.redo_connections()
        return "delete"

    def forget(self):
        # Resets all variables to connecting or dragging functions
        self.connecting = None
        self.connection1 = None
        self.connection_type = None
        self.data_type = None
        self.op_func_dot = None
        self.dragging = None
