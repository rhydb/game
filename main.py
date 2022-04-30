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

        self.bg = (200, 200, 200)
        self.running = True
        self.level = Tilemap("map.tmj")
        self.keys_y = 0
        self.keys_x = 0
        self.deceleration = 0.9


    def charinput(self,event):
        if event.type==pygame.KEYDOWN:
            if event.key== pygame.K_DOWN:
                self.keys_y +=1
            if event.key== pygame.K_UP:
                self.keys_y -= 1
            if event.key== pygame.K_RIGHT:
                self.keys_x += 1
            if event.key== pygame.K_LEFT:
                self.keys_x -=1

        if event.type==pygame.KEYUP:
            if event.key ==pygame.K_LEFT:
                self.keys_x += 1
            if event.key == pygame.K_RIGHT:
                self.keys_x -= 1
            if event.key ==pygame.K_DOWN:
                self.keys_y -=1
            if event.key == pygame.K_UP:
                self.keys_y += 1




    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.charinput(event)

    def charactermovement(self,entities):
        #acceleration by input
        for i in entities:
            if i.velocity[0] < 5 and i.velocity[0] > -5:
                i.velocity[0] += i.acceleration * self.keys_x
            if i.velocity[1] < 5 and i.velocity[1] > -5:
                i.velocity[1] += i.acceleration * self.keys_y

            #flipping
            if i.velocity[0] <0 and i.lookleft ==False:
                i.ent=pygame.transform.flip(i.ent,True,False)
                i.lookleft=True
            if i.velocity[0] >0 and i.lookleft ==True:
                i.ent = pygame.transform.flip(i.ent, True, False)
                i.lookleft = False


        # deceleration
        if abs(entity.vampire.velocity[0]) > 0.5:
            entity.vampire.velocity[0] = entity.vampire.velocity[0] * self.deceleration
        else:
            entity.vampire.velocity[0] = 0
        if abs(entity.vampire.velocity[1]) > 0.5:
            entity.vampire.velocity[1] = entity.vampire.velocity[1] * self.deceleration
        else:
            entity.vampire.velocity[1] = 0



    def windowcolission(self):
        for i in entity.entities:
            if i.position[0] + i.size>self.width:
                i.velocity[0]=abs(i.velocity[0])*-0.1
            if i.position[0]<0:
                i.velocity[0] = -abs(i.velocity[0]) * -0.1

            if i.position[1] + i.size>self.height:
                i.velocity[1]=abs(i.velocity[1])*-0.1
            if i.position[1]<0:
                i.velocity[1]=-abs(i.velocity[1])*-0.1







    def loop(self):
        FPS = 60
        clock =pygame.time.Clock()
        while self.running:
            clock.tick(FPS)
            self.input()

            entity.vampire.position[0] += entity.vampire.velocity[0]
            entity.vampire.position[1] += entity.vampire.velocity[1]

            self.display.fill(self.bg)
            self.level.render(self.display)

            self.charactermovement(entity.entities)
            self.windowcolission()


            #displaying every entity
            for character in entity.entities:
                self.display.blit(character.ent,character.position)


            pygame.display.flip()





Game().loop()
