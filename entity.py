import pygame
import game
from pygame.math import Vector2
import os
import glob


class Entity():
    def __init__(self, imagedirec, position):
        self.size = 30
        self.ent = pygame.image.load(os.path.join("Assets", imagedirec))
        self.ent = pygame.transform.scale(self.ent, (self.size, self.size))
        self.position = Vector2(position)
        self.velocity = Vector2(0, 0)
        self.lookleft = False
        self.grounded = False
        self.bounce = 10
        self.fps = 20
        self.count = 0

        walkingnames = os.listdir(os.path.join("Assets","Soldier1","Walking"))
        self.walkingimages = []
        for i in walkingnames:
            self.walkingimages.append(pygame.image.load(os.path.join("Assets", "Soldier1", "Walking",i)))
        for i in range(len(self.walkingimages)):
            self.walkingimages[i] = pygame.transform.scale(self.walkingimages[i], (self.size, self.size))

    def update(self):
        self.position += self.velocity * game.dt

    def render(self):
        pygame.draw.rect(game.display, (255, 0, 0),
                         (self.position.x - game.camera_x, self.position.y, self.size, self.size), 1)

        if self.velocity.x == 0 or self.grounded == False:
            game.display.blit(self.ent, (self.position.x - game.camera_x, self.position.y))
            self.count=0
        elif self.grounded == True:
            game.display.blit(self.walkingimages[int(self.count)],
                              (self.position.x - game.camera_x, self.position.y))
            self.count += game.dt * self.fps
            self.count %= len(self.walkingimages)

