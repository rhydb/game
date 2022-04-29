import pygame
import json
import entity


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


    def render(self, display):
        for i, index in enumerate(self.tile_set):
            if index == 0:
                continue
            index -= 1
            x = (i % self.width) * self.tw
            y = (i // self.width) * self.th
            tile = self.tiles[index]
            display.blit(tile, (x, y), (0, 0, self.tw, self.th))




class Game:
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.display = pygame.display.set_mode((self.width, self.height))

        self.bg = (255, 255, 255)
        self.running = True
        self.level = Tilemap("map.tmj")


    def entityvelocity(self,character,axis,magnitude):
        #axis 0 = x       1 = y
        character.velocity[axis]=magnitude



    def charmovement(self,event):
        entity.vampire.position[0]+=entity.vampire.velocity[0]
        entity.vampire.position[1]+= entity.vampire.velocity[1]

        if event.type==pygame.KEYDOWN:
            if event.key== pygame.K_DOWN:
                self.entityvelocity(entity.vampire,1,entity.vampire.acceleration)
            if event.key== pygame.K_UP:
                self.entityvelocity(entity.vampire,1,-entity.vampire.acceleration)
            if event.key== pygame.K_RIGHT:
                self.entityvelocity(entity.vampire,0,entity.vampire.acceleration)
            if event.key== pygame.K_LEFT:
                self.entityvelocity(entity.vampire,0,-entity.vampire.acceleration)
        if event.type==pygame.KEYUP:
            if event.key ==pygame.K_LEFT or event.key ==pygame.K_RIGHT:
                self.entityvelocity(entity.vampire, 0, 0)
            if event.key ==pygame.K_DOWN or event.key ==pygame.K_UP:
                self.entityvelocity(entity.vampire, 1, 0)



    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.charmovement(event)

    def loop(self):
        FPS = 60
        clock =pygame.time.Clock()
        while self.running:
            clock.tick(FPS)
            self.input()

            self.display.fill(self.bg)
            self.level.render(self.display)

            self.display.blit(entity.vampire.ent,entity.vampire.position)
            self.display.blit(entity.vampire.ent,entity.vampire.position)

            pygame.display.flip()





Game().loop()
