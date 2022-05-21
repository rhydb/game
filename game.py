import pygame
import json
from pygame.math import Vector2


FPS = 60
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720
dt = 0
camera_x = 0
camera_padding = 200


settings = {}
try:
    with open("settings.json", "r") as f:
        print("opened settings")
        try:
            settings = json.load(f)
            FPS = settings["FPS"]
            WINDOW_WIDTH = settings["WINDOW_WIDTH"]
            WINDOW_HEIGHT = settings["WINDOW_HEIGHT"]
            DISPLAY_WIDTH, DISPLAY_HEIGHT = settings["Resolution"].split("x")
            DISPLAY_WIDTH = int(DISPLAY_WIDTH)
            DISPLAY_HEIGHT = int(DISPLAY_HEIGHT)
        except json.decoder.JSONDecodeError as e:
            print("Failed reading settings.json", e)
except OSError:
    print("Error reading settings, creating default")
    settings = {
        "FPS": FPS,
        "WINDOW_WIDTH": WINDOW_WIDTH,
        "WINDOW_HEIGHT": WINDOW_HEIGHT,
        "Fullscreen": False,
        "Debug": True,
        "Resolution": f"{DISPLAY_WIDTH}x{DISPLAY_HEIGHT}",
    }
    with open("settings.json", "w") as f:
        json.dump(settings, f)

print("Initialising font")
pygame.font.init()
font = pygame.font.Font(pygame.font.match_font("monospace"), 18)
antialias = True
print("Creating display")
window = pygame.display.set_mode(
    (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
available_modes = pygame.display.list_modes()
display = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
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


def screen_to_world(pos: Vector2):
    pos.x = pos.x / WINDOW_WIDTH * DISPLAY_WIDTH + camera_x
    pos.y = pos.y / WINDOW_HEIGHT * DISPLAY_HEIGHT
    return pos
