import pygame
from utils import vec
from .drawable import Drawable

class Platform(object):
    def __init__(self, position, width, height, color=(139, 69, 19)):
        self.position = vec(*position)
        self.width = width
        self.height = height
        self.color = color
    
    def draw(self, drawSurface):
        rect = self.getCollisionRect()
        pygame.draw.rect(drawSurface, self.color, rect)
    
    def getCollisionRect(self):
        return pygame.Rect(int(self.position[0]), int(self.position[1]), 
                          self.width, self.height)
    
    def update(self, seconds):
        pass
    
    def handleEvent(self, event):
        pass