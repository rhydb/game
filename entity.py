import pygame
import game
from pygame.math import Vector2
import os


class Entity():
    def __init__(self, imagedirec, position):
        self.size = 24
        self.ent = pygame.image.load(os.path.join("Assets", imagedirec))
        self.ent = pygame.transform.scale(self.ent, (self.size, self.size))
        self.position = Vector2(position)
        self.velocity = Vector2(0, 0)
        self.lookleft = False
        self.grounded = False
        self.bounce = 10

    def render(self):
        game.display.blit(self.ent, (self.position.x - game.camera_x, self.position.y))
        pygame.draw.rect(game.display, (255, 0, 0), (self.position.x - game.camera_x, self.position.y, self.size, self.size), 1)
