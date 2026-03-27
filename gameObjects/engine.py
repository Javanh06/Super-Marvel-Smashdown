import pygame

from .drawable import Drawable
from .cap import Cap
from .ironMan import IronMan
from .platform import Platform
from utils import vec, RESOLUTION

class GameEngine(object):
    import pygame

    def __init__(self):       
        self.cap = Cap((650,600))
        self.ironMan = IronMan((350,600))
        self.size = vec(*RESOLUTION)
        self.background = Drawable((0,0), "background.jpg")
        self.platforms = [
            Platform((250, 700), 950, 20)
        ]

        bgSize = self.background.getSize()
        self.background.position = vec(
            (RESOLUTION[0] - bgSize[0]) // 2,
            (RESOLUTION[1] - bgSize[1]) // 2
        )

        self.cap.platforms = self.platforms
        self.ironMan.platforms = self.ironMan.platforms = self.platforms

        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
    
    def draw(self, drawSurface):        
        self.background.draw(drawSurface)
        for platform in self.platforms:
            platform.draw(drawSurface)
        self.cap.draw(drawSurface)
        self.ironMan.draw(drawSurface)
        font = pygame.font.SysFont(None, 36)
        capText = font.render(f"Cap: {self.cap.knockback}%", True, (255, 255, 255))
        ironManText = font.render(f"IronMan: {self.ironMan.knockback}%", True, (255, 255, 255))
        drawSurface.blit(capText, (50, 20))
        drawSurface.blit(ironManText, (RESOLUTION[0] - 200, 20))
            
    def handleEvent(self, event):
        self.cap.handleEvent(event)
        self.ironMan.handleEvent(event)

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
        
    def _checkPlatformCollisions(self, seconds):
        for sprite in [self.cap, self.ironMan]:
            for platform in self.platforms:
                platRect = platform.getCollisionRect()
                spriteRect = sprite.getCollisionRect()
                
                # Check horizontal overlap
                if (spriteRect.right < platRect.left or 
                    spriteRect.left > platRect.right):
                    continue
                
                spriteBottom = spriteRect.bottom
                platTop = platRect.top
                
                # Land if feet are at or below platform top
                if spriteBottom >= platTop and spriteBottom <= platTop + 30:
                    sprite.position[1] = platTop - sprite.image.get_size()[1]
                    sprite.velocity[1] = 0
                    if sprite.jump.current_state.id == "falling":
                        sprite.jump.land()
                    elif sprite.jump.current_state.id == "jumping":
                        sprite.jump.peak()
                        sprite.jump.land()
                    elif sprite.jump.current_state.id == "grounded":
                        pass
    
    def _checkPunchCollisions(self):
        if self.cap.punch.current_state.id == "punching":
            punchRect = self.cap.getPunchRect()
            if punchRect.colliderect(self.ironMan.getCollisionRect()):
                self.ironMan.getHit(self.cap)

    def update(self, seconds):
        self.cap.update(seconds)
        self.ironMan.update(seconds)
        self._checkCollisions()
        self._checkPunchCollisions()
        Drawable.updateOffset(self.cap, self.size)
        Drawable.updateOffset(self.ironMan, self.size)