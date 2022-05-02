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

        self.entities = []

        vampire = entity("Theguy.png", [1, 1], 10)

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


        #
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

            game.display.fill(self.bg)
            self.level.render()

            self.charactermovement(entity.entities)
            self.windowcolission()


            #displaying every entity
            for character in entity.entities:
                game.display.blit(character.ent,character.position)


            pygame.display.flip()





Game().loop()
