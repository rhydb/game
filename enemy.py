from entity import Entity
from pygame.math import Vector2

class Enemy(Entity):
    def __init__(self,hitbox,hurtbox):
        super().__init__(*args, **kwargs)
        self.hitbox=hitbox
        self.hurtbox=hurtbox
        self.state = self.idle()

    def idle(self):
        self.velocity.x = 0
        self.velocity.y = 0

    def following(self):
        pass

    def walk(self):
        if self.lookleft==True:
            self.position.x -= self.velocity
