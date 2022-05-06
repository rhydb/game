import pygame
from pygame.math import Vector2
from entity import Entity
from player import Player

FPS = 60
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 480
dt = 0
print("Initialising font")
pygame.font.init()
font = pygame.font.Font(pygame.font.get_default_font(), 18)
print("Creating display")
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

entities = []

vampire = Player("player", 1000, "Theguy.png", (1, 1))

def text(text, pos, colour=(0,0,0), antialias=False):
    surface = font.render(text, antialias, colour)
    display.blit(surface, pos)

