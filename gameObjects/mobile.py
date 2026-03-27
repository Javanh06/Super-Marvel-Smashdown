from . import Animated
from utils import vec, magnitude, scale

class Mobile(Animated):
    def __init__(self, position, fileName=""):
        super().__init__(position, fileName)
        self.velocity = vec(0,0)
        self.maxVelocity = 1000
        self.knockback = 0
        self.beingHit = False
    
    def getHit(self, attacker):
        if attacker.beingHit:
            return
        attacker.bringHit = True
        self.knockback += 10
        if self.position[0] >= attacker.position[0]:
            direction = 1
        else: 
            direction = -1
        force = 300 + (self.knockback * 5)
        self.velocity[0] = direction * force
        self.velocity[1] = -200
    
    def update(self, seconds):
        super().update(seconds)
        if abs(self.velocity[0]) > self.maxVelocity:
            self.velocity[0] = self.maxVelocity * (1 if self.velocity[0] > 0 else -1)
        self.position += self.velocity * seconds