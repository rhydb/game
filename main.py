import pygame
import xml.etree.ElementTree as ET

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
        self.width = 600
        self.height = 720
        self.window = pygame.display.set_mode((self.width, self.height))

        self.bg = (0, 255, 0)
        self.running = True

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def loop(self):
        while self.running:
            self.input()

            self.window.fill(self.bg)
            pygame.display.flip()


helloworld()
Game().loop()
