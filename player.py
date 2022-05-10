import pygame
import game
from pygame.math import Vector2
from animations import AnimatedSprite
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
        self.ent = AnimatedSprite(3, 3, 2, self.size, "Assets/ninja.png")

    def render(self):
        pygame.draw.rect(game.display, (255, 0, 0),
                         (self.position.x - game.camera_x, self.position.y, self.size, self.size), 1)

        self.ent.render(self.position)
