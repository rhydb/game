import os
import pygame
import game



class AnimatedSprite:
    def __init__(self, fps, size, directory=[],):
        self.fps = fps
        self.size=size
        frames = os.listdir(os.path.join(directory))
        self.formatframe = []

        for i in frames:
            self.formatframe.append(pygame.image.load(os.path.join(directory, i)))
        for i in range(len(self.formatframe)):
            self.formatframe[i] = pygame.transform.scale(self.formatframe[i], (self.size, self.size))
        self.count=0

    def animationrender(self, position, duration):
        if self.count < duration*game.dt:
            game.display.blit(self.formatframe[int(self.count) % len(self.formatframe)],(position[0] - game.camera_x, position[1]))
            self.count += game.dt * self.fps
