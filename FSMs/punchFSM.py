from . import AbstractGameFSM
from statemachine import State

class PunchFSM(AbstractGameFSM):
    idle     = State(initial=True)
    punching = State()
    
    punch  = idle.to(punching)
    finish = punching.to(idle)
    
    def __init__(self, obj):
        self.punchTimer = 0
        self.punchDuration = 0.4
        super().__init__(obj)
    
    def update(self, seconds):
        if self.current_state.id == "punching":
            self.punchTimer += seconds
            if self.punchTimer >= self.punchDuration:
                self.punchTimer = 0
                self.obj.bringHit = False
                self.finish()