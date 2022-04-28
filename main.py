import pygame


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

def helloworld():
    print("helloworld")


helloworld()
Game().loop()
