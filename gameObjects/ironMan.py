from . import Mobile
from FSMs import WalkingFSM, AccelerationFSM, JumpFSM
from FSMs import IronManWalkingFSM, IronManJumpFSM, IronManLRFSM
from utils import vec, RESOLUTION, SpriteManager

from pygame.locals import *

import pygame
import numpy as np


class IronMan(Mobile):
   def __init__(self, position):
      super().__init__(position, "ironMan.png")

      sm = SpriteManager.getInstance()

      self.image = sm.getSprite("ironMan.png", offset=(0, 0))
      self.rect = self.image.get_rect(center=position)
        
      self.framesPerSecond = 2 
      self.nFrames = 2
      
      self.nFramesList = {
         "moving"   : 1,
         "standing" : 1
      }
      
      self.rowList = {
         "moving"   : 1,
         "standing" : 0
      }
      
      self.framesPerSecondList = {
         "moving"   : 8,
         "standing" : 2
      }
            
      self.FSManimated = IronManWalkingFSM(self)
      self.jump = IronManJumpFSM(self)
      self.LR = IronManLRFSM(self, axis=0)
      
   def handleEvent(self, event):
      if event.type == KEYDOWN:
            
         if event.key == K_a:
            self.LR.decrease()
            
         elif event.key == K_d:
            self.LR.increase()

         if event.key == K_w and self.jump.current_state.id == "grounded":
            self.jump.start_jump()
            self.velocity[1] = self.jump.jumpForce
            
      elif event.type == KEYUP:
         if event.key == K_a and self.LR == "negative":
            self.LR.stop_decrease()
         elif event.key == K_d and self.LR == "positive":
            self.LR.stop_increase()
   
   def update(self, seconds): 
      self.LR.update(seconds)
      self.jump.update(seconds)
      super().update(seconds)
      self.jump.postUpdate(getattr(self, 'platforms', []))
   
   
   def updateMovement(self):
      pressed = pygame.key.get_pressed()
      
      if not pressed[pygame.K_a] and self.LR == "decrease":
         self.LR.stop_decrease()
      if not pressed[pygame.K_d] and self.LR == "increase":
         self.LR.stop_increase()
   
   
  