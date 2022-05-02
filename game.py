import pygame
from entity import entity

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
dt = 0
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

entities = []

vampire = entity("Theguy.png", [1, 1], 500)
entities.append(vampire)
