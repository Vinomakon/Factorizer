import pygame

path = "data/images/functions/"


class Dot(pygame.sprite.Sprite):
    def __init__(self, type_, config, func_size, pos, input_=True, const=False):
        pygame.sprite.Sprite.__init__(self)

        # Initialization of all specific variables
        self.config = config
        self.func_size = func_size
        self.type = type_
        self.input_ = input_
        self.connecting = False
        self.connected = False
        self.connection_pos = ()
        self.connected_dot = None
        self.sent = False
        self.full = False
        self.const = const

        self.data = None

        # Get if the dot receives a shape or a color
        if self.type == 0:  # Shape
            self.image = pygame.image.load(f"{path}dot.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (20, self.image.get_size()[1] * (20 / self.image.get_size()[0])))
            self.rect = self.image.get_rect()
            self.rect.center = (10, 10)
            self.loc_rect = self.image.get_rect()
            self.loc_rect.center = (10, 10)
        else:  # Shape
            self.image = pygame.image.load(f"{path}sdot.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (20, self.image.get_size()[1] * (20 / self.image.get_size()[0])))
            self.rect = self.image.get_rect()
            self.rect.center = (10, 10)
            self.loc_rect = self.image.get_rect()
            self.loc_rect.center = (10, 10)

        # Set the position based if it's an input or an output and how many there are
        self.rect.x = (20 if input_ else func_size[0] - 40) if not const else pos[0]
        self.rect.y = (func_size[1] / 2 - 10 + config) if not const else pos[1]
        self.loc_rect.x = ((20 if input_ else func_size[0] - 40) + pos[0]) if not const else pos[0]
        self.loc_rect.y = (func_size[1] / 2 - 10 + config + pos[1]) if not const else pos[1] - 10

    def update(self, pos):
        # Redo the location of the dot on the screen
        self.loc_rect.x = (20 if self.input_ else self.func_size[0] - 40) + pos[0]
        self.loc_rect.y = (self.func_size[1] / 2 - 10) + self.config + pos[1]
        self.rect.center = (10 + (20 if self.input_ else self.func_size[0] - 40) + pos[0], 10 + (self.func_size[1] / 2 - 10) + self.config + pos[1])

    def send_data(self, data):
        # Try to send the data if the connected dot isn't full
        if self.connected and not self.connected_dot.full:
            self.connected_dot.data = data
            return True
        # Else tell not yet deleting the data
        return False

    def del_connection(self):
        # Disconnect all previous connections and clear the variables
        if self.connected_dot is not None:
            self.connected_dot.connected = False
            self.connected_dot.connecting = False
            self.connected_dot.connection_pos = ()
            self.connected_dot.connected_dot = None
            self.connected_dot.sent = False
        self.connecting = False
        self.connected = False
        self.connection_pos = ()
        self.connected_dot = None
        self.full = False
        self.sent = False
        self.data = None
