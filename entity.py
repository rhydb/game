import pygame
import os

class entity():
    def __init__(self,imagedirec,startlocal,acceleration ):
        self.ent=pygame.image.load(os.path.join("Assets",imagedirec))
        self.ent=pygame.transform.scale(self.ent,(24,24))
        self.position=startlocal
        self.acceleration=acceleration
        self.velocity=[0,0]
        entities.append(self)



entities=[]

vampire = entity("Theguy.png",[0,0],3)



if __name__ ==("__main__"):
    print("hello")

