import os

class animation():
    def __init__(self,fps,directory=[]):

        self.fps=fps
        frames = os.listdir(os.path.join(directory))
        self.formatframe = []

        for i in frames:
            self.formatframe.append(pygame.image.load(os.path.join(directory,i)))
        for i in range(len(self.walkingimages)):
            self.formatframe[i] = pygame.transform.scale(self.formatframe[i], (self.size, self.size))

    def animationrender(self,position,duration):
        self.count=0
        while self.count< duration:
            for i in range(len(self.formatframe)):
                game.display.blit(self.formatframe[int(self.count) % len(self.walkingimages)], (position.x - game.camera_x, position.y))
                self.count+=game.dt * self.fps


