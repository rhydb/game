import pygame
import xml.etree.ElementTree as ET
import entity

class Tileset:
    def __init__(self, file):
        xml = ET.parse(file)
        root = xml.getroot()
        for layer in root.findall("layer"):
            data = layer.find("data")
            self.data = []
            for row in data.text.strip().split("\n"):
                self.data.append([int(tile) for tile in row.split(",")[:-1]])
            print(self.data)


class Game:
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.window = pygame.display.set_mode((self.width, self.height))

        self.bg = (255, 255, 255)
        self.running = True


    def entityvelocity(self,character,axis,magnitude):
        #axis 0 = x       1 = y
        character.velocity[axis]=magnitude



    def charmovement(self,event):
        entity.vampire.position[0]+=entity.vampire.velocity[0]
        entity.vampire.position[1] += entity.vampire.velocity[1]

        if event.type==pygame.KEYDOWN:
            if event.key== pygame.K_DOWN:
                self.entityvelocity(entity.vampire,0,-entity.vampire.acceleration)
            if event.key== pygame.K_UP:
                self.entityvelocity(entity.vampire,1,entity.vampire.acceleration)
            if event.key== pygame.K_RIGHT:
                self.entityvelocity(entity.vampire,0,entity.vampire.acceleration)
            if event.key== pygame.K_LEFT:
                self.entityvelocity(entity.vampire,1,-entity.vampire.acceleration)
        if event.type==pygame.KEYUP:
            if event.key ==pygame.K_LEFT or event.key ==pygame.K_RIGHT:
                self.entityvelocity(entity.vampire, 0, 0)
            if event.key ==pygame.K_UP or event.key ==pygame.K_UP:
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


            self.window.fill(self.bg)
            self.window.blit(entity.vampire.ent,entity.vampire.position)
            pygame.display.flip()






Game().loop()
