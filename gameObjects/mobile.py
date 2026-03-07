from . import Animated
from utils import vec, magnitude, scale

class Mobile(Animated):
    def __init__(self, position, fileName=""):
        super().__init__(position, fileName)
        self.velocity = vec(0,0)
        self.maxVelocity = 600
    
    def update(self, seconds):
        super().update(seconds)
        if abs(self.velocity[0]) > self.maxVelocity:
            self.velocity[0] = self.maxVelocity * (1 if self.velocity[0] > 0 else -1)
        self.position += self.velocity * seconds