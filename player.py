from pygame.math import Vector2
from entity import Entity


class Player(Entity):
    def __init__(self, name, acceleration, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min_speed = 5
        self.max_vel = Vector2(250, 600)
        self.name = name
        self.acceleration = Vector2(acceleration)
        self.deceleration = 10
        self.gravity = 2000
        self.jump = 600
