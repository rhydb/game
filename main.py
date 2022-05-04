import copy
from functools import reduce

import game
import pygame
from pygame.math import Vector2
from entity import Entity
from Tilemap import Tilemap


class Game:
    def __init__(self):

        self.bg = (200, 200, 200)
        self.running = True
        self.level = Tilemap("map.tmj")
        self.keys_y = 0
        self.keys_x = 0
        self.deceleration = 10  # percentage decrease

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
        for entity in entities:
            entity.position += entity.velocity * game.dt

        max_vel = Vector2(500)
        if abs(game.vampire.velocity.x) < max_vel.x:
            game.vampire.velocity.x += game.vampire.acceleration.x * self.keys_x * game.dt
        if abs(game.vampire.velocity.y) < max_vel.y:
            game.vampire.velocity.y += game.vampire.acceleration.y * self.keys_y * game.dt

        # flipping
        if game.vampire.velocity.x < 0 and game.vampire.lookleft == False:
            game.vampire.ent = pygame.transform.flip(game.vampire.ent, True, False)
            game.vampire.lookleft = True
        if game.vampire.velocity.x > 0 and game.vampire.lookleft == True:
            game.vampire.ent = pygame.transform.flip(game.vampire.ent, True, False)
            game.vampire.lookleft = False

        self.minspeed = 5
        if self.keys_x == 0:
            if abs(game.vampire.velocity.x) > self.minspeed:
                game.vampire.velocity.x -= game.vampire.velocity.x * self.deceleration * game.dt
            else:
                game.vampire.velocity.x = 0
        if self.keys_y == 0:
            if abs(game.vampire.velocity.y) > self.minspeed:
                game.vampire.velocity.y -= game.vampire.velocity.y * self.deceleration * game.dt
            else:
                game.vampire.velocity.y = 0

        self.resolve_tile_collision(game.vampire)

    def resolve_tile_collision(self, entity):
        next_x = entity.position.x + entity.velocity.x * game.dt
        collisions = self.tile_collision(Vector2(next_x, entity.position.y), entity.size)
        if collisions["tl"] or collisions["bl"] and not entity.grounded:
            next_x = self.get_tile_xy_at(*entity.position.xy).x
            entity.velocity.x = 0
        if collisions["tr"] or collisions["br"] and not entity.grounded:
            next_x = self.get_tile_xy_at(entity.position.x + self.level.tw // 2,
                                         entity.position.y).x - 1 + (self.level.tw - entity.size)
            entity.velocity.x = 0

        next_y = game.vampire.position.y + entity.velocity.y * game.dt
        collision = self.tile_collision(Vector2(entity.position.x, next_y), entity.size)
        if collision["tl"] or collision["tr"]:
            next_y = self.get_tile_xy_at(*entity.position.xy).y
            game.vampire.velocity.y = 0
        if collision["bl"]  or collision["br"]:
            next_y = self.get_tile_xy_at(entity.position.x,
                                         entity.position.y + self.level.th // 2).y + (self.level.th - entity.size)
            entity.grounded = True
        else:
            entity.grounded = False
        entity.position.xy = next_x, next_y


    def get_tile_xy_at(self, x, y):
        tile_x = int(x // self.level.tw) * self.level.tw
        tile_y = int(y // self.level.th) * self.level.th
        return Vector2(tile_x, tile_y)

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

    def tile_collision(self, position: Vector2, size: int):
        return {
            "tl": self.get_tile_at(*position.xy) > 0,
            "tr": self.get_tile_at(position.x + size,
                                   position.y) > 0,
            "bl": self.get_tile_at(position.x,
                                   position.y + size) > 0,
            "br": self.get_tile_at(position.x + size,
                                   position.y + size) > 0
        }

    def get_tile_at(self, x, y):
        tile_x = int(x // self.level.tw)
        tile_y = int(y // self.level.th)
        if 0 <= tile_x < self.level.width and 0 <= tile_y < self.level.height:
            tile_index = tile_x + tile_y * self.level.width
            return self.level.tile_set[tile_index]
        return -1

    def loop(self):
        clock = pygame.time.Clock()
        while self.running:
            game.dt = clock.tick(game.FPS) / 1000
            self.input()

            game.display.fill(self.bg)
            self.level.render()

            self.charactermovement(game.entities)
            self.windowcolission()

            # displaying every entity
            for entity in game.entities:
                game.display.blit(entity.ent, entity.position)
            game.display.blit(game.vampire.ent, game.vampire.position)
            pygame.draw.rect(game.display, (255, 0, 0), (*game.vampire.position.xy, game.vampire.size, game.vampire.size), 1)
            pygame.display.flip()


Game().loop()
