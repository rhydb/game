import pygame
import os

class entity():
    def __init__(self,imagedirec,startlocal,velocity):
        self.ent=pygame.image.load(os.path.join("Assets",imagedirec))
        self.ent=pygame.transform.scale(self.ent,(200,200))
        self.startlocation=startlocal
        self.velocity=velocity






vampire = entity("Theguy.png",[0,0],50)


if __name__ ==("__main__"):
    print("hello")

