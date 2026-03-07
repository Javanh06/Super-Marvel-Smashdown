import pygame

from .drawable import Drawable
from .cap import Cap
from .ironMan import IronMan
from .platform import Platform
from utils import vec, RESOLUTION

class GameEngine(object):
    import pygame

    def __init__(self):       
        self.cap = Cap((450,150))
        self.ironMan = IronMan((150,150))
        self.size = vec(*RESOLUTION)
        self.background = Drawable((0,0), "background.jpg")
        self.platforms = [
            Platform((150, 180), 100, 20),
            Platform((450, 180), 100, 20)
        ]

        bgSize = self.background.getSize()
        self.background.position = vec(
            (RESOLUTION[0] - bgSize[0]) // 2,
            (RESOLUTION[1] - bgSize[1]) // 2
        )
    
    def draw(self, drawSurface):        
        self.background.draw(drawSurface)
        for platform in self.platforms:
            platform.draw(drawSurface)
        self.cap.draw(drawSurface)
        self.ironMan.draw(drawSurface)
            
    def handleEvent(self, event):
        self.cap.handleEvent(event)
        self.ironMan.handleEvent(event)
    
    def update(self, seconds):
        self.cap.update(seconds)
        self.ironMan.update(seconds)
        self._checkCollisions()
        self._checkPlatformCollisions()
        
        Drawable.updateOffset(self.cap, self.size)
        Drawable.updateOffset(self.ironMan, self.size)

    def _checkCollisions(self):
        collision = self.cap.getCollisionRect().clip(self.ironMan.getCollisionRect())
        
        if collision.width != 0 and collision.height != 0:
            if collision.width < collision.height:
                self.cap.velocity[0] = 0
                self.ironMan.velocity[0] = 0
                if self.cap.position[0] < self.ironMan.position[0]:
                    self.cap.position[0] -= collision.width / 2
                    self.ironMan.position[0] += collision.width / 2
                else:
                    self.cap.position[0] += collision.width / 2
                    self.ironMan.position[0] -= collision.width / 2
            else:
                self.cap.velocity[1] = 0
                self.ironMan.velocity[1] = 0
                if self.cap.position[1] < self.ironMan.position[1]:
                    self.cap.position[1] -= collision.height / 2
                    self.ironMan.position[1] += collision.height / 2
                else:
                    self.cap.position[1] += collision.height / 2
                    self.ironMan.position[1] -= collision.height / 2
        
    def _checkPlatformCollisions(self):
        for sprite in [self.cap, self.ironMan]:
            for platform in self.platforms:
                collision = sprite.getCollisionRect().clip(platform.getCollisionRect())
                if collision.width != 0 and collision.height != 0:
                    if sprite.velocity[1] >= 0 and collision.height < collision.width:
                        sprite.position[1] = platform.position[1] - sprite.image.get_size()[1]
                        sprite.velocity[1] = 0
                        if sprite.jump.current_state.id == "falling":
                            sprite.jump.land()
                        elif sprite.jump.current_state.id == "jumping":
                            sprite.jump.peak()
                            sprite.jump.land()
