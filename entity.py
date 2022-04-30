import pygame
import os

class entity():
    def __init__(self,imagedirec,startlocal,acceleration ):
        self.size=32
        self.ent=pygame.image.load(os.path.join("Assets",imagedirec))
        self.ent=pygame.transform.scale(self.ent,(self.size,self.size))
        self.entfliped=pygame.transform.flip(self.ent, True, False)
        self.position=startlocal
        self.acceleration=acceleration
        self.velocity=[0,0]
        self.lookleft=False
        entities.append(self)



global entities
entities=[]

vampire = entity("Theguy.png",[1,1],2)
#yomumma =entity("Theguy.png",[100,100],10)




if __name__ ==("__main__"):
    print("hello")

