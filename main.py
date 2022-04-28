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

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def loop(self):

        FPS = 60
        clock =pygame.time.Clock()
        while self.running:
            clock.tick(FPS)
            self.input()

            self.window.fill(self.bg)
            self.window.blit(entity.vampire.ent,entity.vampire.startlocation)
            pygame.display.flip()














Game().loop()
