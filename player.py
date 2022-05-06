from pygame.math import Vector2
from entity import Entity


class Player(Entity):
    def __init__(self, name, acceleration, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.acceleration = Vector2(acceleration)
