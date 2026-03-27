from . import Mobile
from FSMs import WalkingFSM, AccelerationFSM, JumpFSM, PunchFSM
from utils import vec, RESOLUTION, SpriteManager

from pygame.locals import *

import pygame
import numpy as np


class Cap(Mobile):
   def __init__(self, position):
      super().__init__(position, "cap2.png")

      sm = SpriteManager.getInstance()

      self.image = sm.getSprite("cap2.png", offset=(0, 0))
      self.rect = self.image.get_rect(center=position)
        
      self.framesPerSecond = 2 
      self.nFrames = 2
      
      self.nFramesList = {
         "moving"   : 8,
         "standing" : 1,
         "punching" : 8
      }
      
      self.rowList = {
         "moving"   : 0,
         "standing" : 3,
         "punching" : 1
      }
      
      self.framesPerSecondList = {
         "moving"   : 8,
         "standing" : 2,
         "punching" : 12
      }
            
      self.FSManimated = WalkingFSM(self)
      self.jump = JumpFSM(self)
      self.punch = PunchFSM(self)
      self.LR = AccelerationFSM(self, axis=0)
      
   def getPunchRect(self):
      rect = self.getCollisionRect()
      if self.velocity[0] >= 0:
         rect.x += rect.width
      else:
         rect.x -= rect.width
      return rect   
   
   def handleEvent(self, event):
      if event.type == KEYDOWN:
         if event.key == K_LEFT:
            self.LR.decrease()
            
         elif event.key == K_RIGHT:
            self.LR.increase()

         if event.key == K_UP:
            if self.jump.current_state.id == "grounded":
               self.jump.start_jump()
               self.velocity[1] = self.jump.jumpForce

         if event.key == K_z: 
            if self.punch.current_state.id == "idle":
               self.punch.punch()
               self.row = self.rowList["punching"]
               self.nFrames = self.nFramesList["punching"]
               self.framesPerSecond = self.framesPerSecondList["punching"]
               self.frame = 0
            
      elif event.type == KEYUP:
         if event.key == K_LEFT and self.LR == "negative":
            self.LR.stop_decrease()
         elif event.key == K_RIGHT and self.LR == "positive":
            self.LR.stop_increase()

      elif event.type == JOYAXISMOTION:
         if event.axis == 0:
            if event.value > 0.5:
                  self.LR.increase()
            elif event.value < -0.5:
                  self.LR.decrease()
            else:
                  if self.LR == "positive":
                     self.LR.stop_increase()
                  elif self.LR == "negative":
                     self.LR.stop_decrease()

      elif event.type == JOYBUTTONDOWN:
         if event.button == 0:
            if self.jump.current_state.id == "grounded":
                  self.jump.start_jump()
                  self.velocity[1] = self.jump.jumpForce
         if event.button == 1:
            if self.punch.current_state.id == "idle":
                  self.punch.punch()
                  self.row = self.rowList["punching"]
                  self.nFrames = self.nFramesList["punching"]
                  self.framesPerSecond = self.framesPerSecondList["punching"]
                  self.frame = 0
   
   def update(self, seconds): 
      self.LR.update(seconds)
      self.jump.update(seconds)
      self.punch.update(seconds)
      super().update(seconds)
      self.jump.postUpdate(getattr(self, 'platforms', []))
   
   def updateMovement(self):
      pressed = pygame.key.get_pressed()
      
      if not pressed[pygame.K_LEFT] and self.LR == "decrease":
         self.LR.stop_decrease()
      if not pressed[pygame.K_RIGHT] and self.LR == "increase":
         self.LR.stop_increase()
   
   
  