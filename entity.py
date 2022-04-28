import pygame
import os

class entity():
    def __init__(self,imagedirec,startlocal):
        self.ent=pygame.image.load(os.path.join("Assets",imagedirec))
        self.ent=pygame.transform.scale(self.ent,(200,200))
        self.startlocation=startlocal






vampire = entity("Theguy.png",[0,0])


if __name__ ==("__main__"):
    print("hello")

