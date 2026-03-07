from . import AbstractGameFSM
from utils import vec, magnitude, EPSILON, scale, RESOLUTION

from statemachine import State

class JumpFSM(AbstractGameFSM):
    grounded = State(initial=True)
    jumping  = State()
    falling  = State()

    start_jump = grounded.to(jumping)
    peak       = jumping.to(falling)
    land       = falling.to(grounded)

    def __init__(self, obj):
        self.jumpForce = -750
        self.gravity   = 800
        super().__init__(obj)

    def update(self, seconds):
        if self.current_state.id == "jumping" or self.current_state.id == "falling":
            self.obj.velocity[1] += self.gravity * seconds
            if self.current_state.id == "jumping" and self.obj.velocity[1] >= 0:
                self.peak()

        size = self.obj.image.get_size()[1]
        ground = RESOLUTION[1] - size
        if self.obj.position[1] >= ground and self.obj.velocity[1] >= 0:
            self.obj.position[1] = ground
            self.obj.velocity[1] = 0
            if self.current_state.id == "falling":
                self.land()