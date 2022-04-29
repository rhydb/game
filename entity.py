import pygame
import os

class entity():
    def __init__(self,imagedirec,startlocal,acceleration ):
        self.ent=pygame.image.load(os.path.join("Assets",imagedirec))
        self.ent=pygame.transform.scale(self.ent,(32,32))
        self.position=startlocal
        self.acceleration=acceleration
        self.velocity=[0,0]
        entities.append(self)



global entities
entities=[]

vampire = entity("Theguy.png",[0,0],10)
yomumma =entity("Theguy.png",[100,100],10)




if __name__ ==("__main__"):
    print("hello")

