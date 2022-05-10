import os
import pygame
import game



class AnimatedSprite:
    def __init__(self, fps, rows, cols, size, file):
        self.fps = fps
        self.rows = rows
        self.row = 0
        self.cols = cols
        self.size = size
        self.formatframe = []
        self.frames = []
        self.flipped = False

        image = pygame.image.load(file)
        image_rect = image.get_rect()
        sprite_size_x = image_rect.w // cols
        sprite_size_y = image_rect.h // rows

        for row in range(self.rows):
            frame_row = []
            for col in range(self.cols):
                frame = pygame.Surface((sprite_size_x, sprite_size_y), pygame.SRCALPHA)
                frame.blit(image, (0, 0), (col * sprite_size_x, row * sprite_size_y, sprite_size_x, sprite_size_y))
                frame_row.append(pygame.transform.scale(frame, (self.size, self.size)))
            self.frames.append(frame_row)

        self.count = 0

    def render(self, position):
        frame = self.frames[self.row][int(self.count) % self.cols]
        if self.flipped:
            frame = pygame.transform.flip(frame, True, False)
        game.display.blit(frame, (position[0] - game.camera_x, position[1]))
        self.count += game.dt * self.fps
