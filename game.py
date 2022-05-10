import pygame
from pygame.math import Vector2

FPS = 60
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 480
dt = 0
camera_x = 0
camera_padding = 200
print("Initialising font")
pygame.font.init()
font = pygame.font.Font(pygame.font.match_font("monospace"), 18)
print("Creating display")
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

entities = []

vampire = None


def text(text, pos, colour=(0, 0, 0), antialias=False, center=False):
    pos = Vector2(pos)
    surface = font.render(text, antialias, colour)
    if center:
        rect = surface.get_rect()
        pos.x -= rect.w / 2
        pos.y -= rect.h / 2
    display.blit(surface, pos)
