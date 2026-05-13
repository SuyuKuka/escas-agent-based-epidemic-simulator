import random
from enum import Enum
from utils import *

class State(Enum):
    SAIN = 1
    INFECTE = 2
    GUERI = 3

class Agent:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.state = State.SAIN
        self.tick_in_state = 0
    
    def move(self, sim):
        move_x = round(random.uniform(0, 1), 2)
        move_y = round(random.uniform(0, 1), 2)

        self.x = clamp(self.x + move_x, 0, sim.width)
        self.y = clamp(self.y + move_y, 0, sim.height)
    
    def __str__(self):
        return f"Agent {self.id} ({str(self.state)}): ({self.x}, {self.y})"
