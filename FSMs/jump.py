from . import AbstractGameFSM
from utils import RESOLUTION
from statemachine import State
import pygame

class JumpFSM(AbstractGameFSM):
    grounded = State(initial=True)
    jumping  = State()
    falling  = State()

    updateState = falling.to(grounded,  cond="canLand")  | \
                  grounded.to(falling,  cond="canFall")  | \
                  jumping.to(falling,   cond="canFall")  | \
                  jumping.to.itself(internal=True)       | \
                  grounded.to.itself(internal=True)      | \
                  falling.to.itself(internal=True)

    start_jump = grounded.to(jumping)            | \
                 jumping.to.itself(internal=True) | \
                 falling.to.itself(internal=True)

    fall = jumping.to(falling)                   | \
           falling.to.itself(internal=True)      | \
           grounded.to.itself(internal=True)

    def __init__(self, obj):
        self.jumpForce = -600
        self.gravity   = 800
        self.termVel   = 600
        self.hasGround = False
        self.bonked    = False
        super().__init__(obj)

    def canFall(self):
        return self.bonked or not self.hasGround

    def canLand(self):
        return self.hasGround

    def on_enter_grounded(self):
        self.obj.velocity[1] = 0

    def on_enter_falling(self):
        self.bonked = False

    def checkColliders(self, colliders):
        self.hasGround = False
        self.bonked    = False

        spriteRect   = self.obj.getCollisionRect()
        spriteHeight = self.obj.image.get_size()[1]
        spriteBottom = self.obj.position[1] + spriteHeight

        for collider in colliders:
            platRect = collider.getCollisionRect()

            if self.current_state.id in ("falling", "jumping"):
                clip = spriteRect.clip(platRect)
                if clip.width != 0 and clip.height != 0:
                    if platRect.centery >= spriteRect.centery and self.obj.velocity[1] >= 0:
                        self.obj.position[1] = platRect.top - spriteHeight
                        self.obj.velocity[1] = 0
                        self.hasGround = True

            elif self.current_state.id == "grounded":
                onPlat = (spriteBottom >= platRect.top - 4 and
                        spriteBottom <= platRect.top + 4 and
                        self.obj.position[0] + spriteRect.width > platRect.left and
                        self.obj.position[0] < platRect.right)
                if onPlat:
                    self.hasGround = True

        ground = RESOLUTION[1] - spriteHeight
        if self.current_state.id in ("falling", "jumping"):
            if self.obj.position[1] >= ground:
                self.obj.position[1] = ground
                self.obj.velocity[1] = 0
                self.hasGround = True
        elif self.current_state.id == "grounded":
            if self.obj.position[1] >= ground - 4:
                self.hasGround = True

    def update(self, seconds=0, colliders=None):
        seconds = min(0.03, seconds)

        if colliders is None:
            colliders = getattr(self.obj, 'platforms', [])

        if self.current_state.id == "falling":
            self.obj.velocity[1] += self.gravity * seconds
            self.obj.velocity[1] = min(self.termVel, self.obj.velocity[1])
        elif self.current_state.id == "jumping":
            self.obj.velocity[1] = self.jumpForce
        else:
            self.obj.velocity[1] = 0

        self._pendingColliders = colliders

    def postUpdate(self, colliders):
        self.checkColliders(colliders)
        self.updateState()