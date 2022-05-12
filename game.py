import pygame
from pygame.math import Vector2

FPS = 60
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720
dt = 0
camera_x = 0
camera_padding = 200
print("Initialising font")
pygame.font.init()
font = pygame.font.Font(pygame.font.match_font("monospace"), 18)
antialias = True
print("Creating display")
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
available_modes = pygame.display.list_modes()
display = pygame.Surface(available_modes[0])
resolutions = [f"{width}x{height}" for (width, height) in available_modes]
entities = []

vampire = None


def text(text, pos, colour=(0, 0, 0), antialias=antialias, center=False):
    pos = Vector2(pos)
    surface = font.render(text, antialias, colour)
    if center:
        rect = surface.get_rect()
        pos.x -= rect.w / 2
        pos.y -= rect.h / 2
    display.blit(surface, pos)
