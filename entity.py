import pygame
import os


class entity():
    def __init__(self, imagedirec, startlocal, acceleration):
        self.size = 48
        self.ent = pygame.image.load(os.path.join("Assets", imagedirec))
        self.ent = pygame.transform.scale(self.ent, (self.size, self.size))
        self.entfliped = pygame.transform.flip(self.ent, True, False)
        self.position = startlocal
        self.acceleration = acceleration
        self.velocity = [0, 0]
        self.lookleft = False
