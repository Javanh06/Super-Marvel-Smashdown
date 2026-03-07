from . import Mobile
from FSMs import WalkingFSM, AccelerationFSM
from utils import vec, RESOLUTION

from pygame.locals import *

import pygame
import numpy as np


class Kirby(Mobile):
   def __init__(self, position):
      super().__init__(position, "kirby.png")
        
      # Animation variables specific to Kirby
      self.framesPerSecond = 2 
      self.nFrames = 2
      
      self.nFramesList = {
         "moving"   : 4,
         "standing" : 2
      }
      
      self.rowList = {
         "moving"   : 1,
         "standing" : 0
      }
      
      self.framesPerSecondList = {
         "moving"   : 8,
         "standing" : 2
      }
            
      self.FSManimated = WalkingFSM(self)
      self.LR = AccelerationFSM(self, axis=0)
      self.UD = AccelerationFSM(self, axis=1)
      
      
   def handleEvent(self, event):
      if event.type == KEYDOWN:
         if event.key == K_UP:
            self.UD.decrease()
             
         elif event.key == K_DOWN:
            self.UD.increase()
            
         elif event.key == K_LEFT:
            self.LR.decrease()
            
         elif event.key == K_RIGHT:
            self.LR.increase()
            
      elif event.type == KEYUP:
         if event.key == K_UP:
            self.UD.stop_decrease()
             
         elif event.key == K_DOWN:
            self.UD.stop_increase()
             
            
         elif event.key == K_LEFT:
            self.LR.stop_decrease()
            
         elif event.key == K_RIGHT:
            self.LR.stop_increase()
   
   def update(self, seconds): 
      self.LR.update(seconds)
      self.UD.update(seconds)
      
      super().update(seconds)
      
   
   
   def updateMovement(self):
      # For unpausing the game
      pressed = pygame.key.get_pressed()
      
      
      if not pressed[pygame.K_UP] and self.UD == "decrease":
         self.UD.stop_decrease()
      if not pressed[pygame.K_DOWN] and self.UD == "increase":
         self.UD.stop_increase()
         
      if not pressed[pygame.K_LEFT] and self.LR == "decrease":
         self.LR.stop_decrease()
      if not pressed[pygame.K_RIGHT] and self.LR == "increase":
         self.LR.stop_increase()
   
   
  