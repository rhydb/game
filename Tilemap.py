import game
import pygame
import json


class Tilemap:
    def __init__(self, file):
        self.tiles = []

        with open(file) as f:
            data = json.load(f)
            self.solids = data["layers"][0]["data"]
            self.detectors = data["layers"][1]["data"]
            self.passthrough = data["layers"][2]["data"]

            self.width = data["layers"][0]["width"]
            self.height = data["layers"][0]["height"]

            tile_set_info = data["tilesets"][0]
            self.columns = tile_set_info["columns"]
            self.tw = tile_set_info["tilewidth"]
            self.th = tile_set_info["tileheight"]
            self.image = pygame.image.load(tile_set_info["image"])
            self.image_rect = self.image.get_rect()

            for y in range(0, self.image_rect.h, self.th):
                for x in range(0, self.image_rect.w, self.tw):
                    tile = pygame.Surface((self.tw, self.th), pygame.SRCALPHA)
                    tile.blit(self.image, (0, 0), (x, y, self.tw, self.th))
                    self.tiles.append(tile)

    def render(self):
        rows_on_screen = game.WINDOW_HEIGHT // self.th
        cols_on_screen = game.WINDOW_WIDTH // self.tw
        total_tiles = self.width * self.height
        starting_column = game.camera_x // self.tw
        for layer in [self.solids, self.detectors, self.passthrough]:
            for i in range(rows_on_screen):
                if i * self.width >= total_tiles:
                    break
                for j in range(starting_column, starting_column + cols_on_screen + 1):
                    index = i * self.width + j
                    if index >= len(layer):
                        break
                    tile_id = layer[index]
                    if tile_id == 0:
                        continue
                    tile_id -= 1
                    x = (index % self.width) * self.tw
                    y = (index // self.width) * self.th
                    tile = self.tiles[tile_id]
                    game.display.blit(
                        tile, (x - game.camera_x, y), (0, 0, self.tw, self.th))
