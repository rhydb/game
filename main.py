import game
import pygame
from entity import entity
from Tilemap import Tilemap


class Game:
    def __init__(self):

        self.bg = (200, 200, 200)
        self.running = True
        self.level = Tilemap("map.tmj")
        self.keys_y = 0
        self.keys_x = 0
        self.deceleration = 0.9

    def charinput(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.keys_y += 1
            if event.key == pygame.K_UP:
                self.keys_y -= 1
            if event.key == pygame.K_RIGHT:
                self.keys_x += 1
            if event.key == pygame.K_LEFT:
                self.keys_x -= 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.keys_x += 1
            if event.key == pygame.K_RIGHT:
                self.keys_x -= 1
            if event.key == pygame.K_DOWN:
                self.keys_y -= 1
            if event.key == pygame.K_UP:
                self.keys_y += 1

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.charinput(event)

    def charactermovement(self, entities):
        # acceleration by input
        for i in entities:
            if i.velocity.x < 5 and i.velocity.x > -5:
                i.velocity.x += i.acceleration.x * self.keys_x * game.dt
            if i.velocity.y < 5 and i.velocity.y > -5:
                i.velocity.y += i.acceleration.y * self.keys_y * game.dt

            # flipping
            if i.velocity.x < 0 and i.lookleft == False:
                i.ent = pygame.transform.flip(i.ent, True, False)
                i.lookleft = True
            if i.velocity.x > 0 and i.lookleft == True:
                i.ent = pygame.transform.flip(i.ent, True, False)
                i.lookleft = False

        if self.keys_x == 0:
            if abs(game.vampire.velocity.x) > 0.5:
                game.vampire.velocity.x = game.vampire.velocity.x * self.deceleration * game.dt
            else:
                game.vampire.velocity.x = 0
        if self.keys_y == 0:
            if abs(game.vampire.velocity.y) > 0.5:
                game.vampire.velocity.y = game.vampire.velocity.y * self.deceleration * game.dt
            else:
                game.vampire.velocity.y = 0

        game.vampire.position += game.vampire.velocity * game.dt

    def windowcolission(self):
        for i in game.entities:
            if i.position.x + i.size > game.WINDOW_WIDTH:
                i.velocity.x = abs(i.velocity.x) * -0.1
            if i.position.x < 0:
                i.velocity.x = -abs(i.velocity.x) * -0.1

            if i.position.y + i.size > game.WINDOW_HEIGHT:
                i.velocity.y = abs(i.velocity.y) * -0.1
            if i.position.y < 0:
                i.velocity.y = -abs(i.velocity.y) * -0.1

    def loop(self):
        FPS = 60
        clock = pygame.time.Clock()
        while self.running:
            game.dt = clock.tick(FPS) / 1000
            self.input()


            game.display.fill(self.bg)
            self.level.render()

            self.charactermovement(game.entities)
            self.windowcolission()

            # displaying every entity
            for character in game.entities:
                game.display.blit(character.ent, character.position)

            pygame.display.flip()


Game().loop()
