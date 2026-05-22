import math
from enum import Enum
from utils import *

AGENT_DEBUG = 0

# Maladie
class Etat(Enum):
    SAIN = 1
    INFECTE = 2
    GUERI = 3

# Social
class Attitude(Enum):
    NORMAL = 1
    PANIQUE = 2
    CONFINE = 3

class Agent:
    def __init__(self, id, x, y, etat=Etat.SAIN, attitude=random_enum(Attitude)):
        self.id = id
        self.x = x
        self.y = y
        self.shown = False
        self.etat = etat
        self.tick_etat = 0                      # Nombre de tick en étant dans l'état actuel
        self.attitude = attitude
        self.tick_attitude = 0                  # Nombre de tick en étant dans l'attitude actuel
    
    def move(self, max_largeur, max_hauteur):
        if (self.attitude == Attitude.NORMAL):
            RADIUS = 1
        elif (self.attitude == Attitude.PANIQUE):
            RADIUS = 1.4
        else:
            RADIUS = 0.4
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, RADIUS)

        move_x = round(distance * math.cos(angle), 2)
        move_y = round(distance * math.sin(angle), 2)

        # DEBUG
        if (AGENT_DEBUG and self.attitude == Attitude.PANIQUE and ((move_x + move_y) > 1)):
            print(f"=== {self.id} a beaucoup bougé car panique")

        self.x = clamp(self.x + move_x, 0, max_largeur)
        self.y = clamp(self.y + move_y, 0, max_hauteur)
    
    def __str__(self):
        return f"Agent {self.id} ({str(self.etat)}): ({self.x}, {self.y})"
