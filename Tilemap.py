import game
import pygame
import json


class Tilemap:
    def __init__(self, file):
        self.tiles = []

        with open(file) as f:
            data = json.load(f)
            self.tile_set = data["layers"][0]["data"]
            self.width = data["layers"][0]["width"]

            tile_set_info = data["tilesets"][0]
            self.columns = tile_set_info["columns"]
            self.tw = tile_set_info["tilewidth"]
            self.th= tile_set_info["tileheight"]
            self.image = pygame.image.load(tile_set_info["image"])
            self.image_rect = self.image.get_rect()


            for y in range(0, self.image_rect.h, self.th):
                for x in range(0, self.image_rect.w ,self.tw):
                    tile = pygame.Surface((self.tw, self.th))
                    tile.blit(self.image, (0, 0), (x, y, self.tw, self.th))
                    self.tiles.append(tile)


    def render(self):
        for i, index in enumerate(self.tile_set):
            if index == 0:
                continue
            index -= 1
            x = (i % self.width) * self.tw
            y = (i // self.width) * self.th
            tile = self.tiles[index]
            game.display.blit(tile, (x, y), (0, 0, self.tw, self.th))