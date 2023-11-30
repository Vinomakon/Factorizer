import pygame
import os
import sys
import func_block


class Test:
    def __init__(self, screen_size):
        self.surface = pygame.surface.Surface(screen_size)
        self.surface.fill((100, 100, 100))
        self.screen_size = screen_size
        self.functions = pygame.sprite.Group()

        function = func_block.Function("delete", (110, 110))
        self.functions.add(function)
        function1 = func_block.Function("delete")
        self.functions.add(function1)

        self.functions.draw(self.surface)
        self.connections = []
        self.connecting = False
        self.connect1 = None

    def res_change(self, screen_size):
        self.surface = pygame.surface.Surface(screen_size, pygame.SRCALPHA)

    def on_click(self, mouse_pos):
        self.surface = pygame.surface.Surface(self.screen_size, pygame.SRCALPHA)
        connection_active = False
        for func in self.functions:
            on_dot, dot_pos = func.check(mouse_pos)
            if on_dot:
                if self.connecting:
                    self.connections.append((self.connect1, dot_pos))
                    self.connecting = False
                else:
                    self.connecting = True
                    self.connect1 = dot_pos
                    connection_active = True
            elif func.rect.collidepoint(mouse_pos):
                func.draggable(True, mouse_pos)
                for pos in self.connections:
                    print(pos, func.dot_rect.center)
                    if pos[0] == func.dot_rect.center or pos[1] == func.dot_rect.center:
                        self.connections.pop(self.connections.index(pos))
        if not connection_active:
            self.connecting = False
            self.connect1 = None




    def on_release(self, mouse_pos):
        for func in self.functions:
            func.draggable(False, mouse_pos)

    def refresh(self, mouse_pos):
        self.surface.fill((100, 100, 100))
        self.functions.update(mouse_pos)
        self.functions.draw(self.surface)
        for connection in self.connections:
            pygame.draw.line(self.surface, (77, 0, 0),  connection[0], connection[1], 8)
        if self.connecting:
            print("drawing")
            pygame.draw.line(self.surface, (77, 0, 0), self.connect1, mouse_pos, 8)
        for func in self.functions:
            pass
