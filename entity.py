import pygame
from pygame.math import Vector2
import os


class entity():
    def __init__(self, imagedirec, position, acceleration):
        self.size = 48
        self.ent = pygame.image.load(os.path.join("Assets", imagedirec))
        self.ent = pygame.transform.scale(self.ent, (self.size, self.size))
        self.entfliped = pygame.transform.flip(self.ent, True, False)
        self.position = Vector2(position)
        self.acceleration = acceleration
        self.velocity = Vector2(0, 0)
        self.lookleft = False
