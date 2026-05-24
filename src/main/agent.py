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
        self.angle = random.uniform(0, 2 * math.pi)
        self.healing_factor = random.uniform(0.2, 4.0)
    
    def move(self, max_largeur, max_hauteur):
        if (self.attitude == Attitude.NORMAL):
            RADIUS = 1
        elif (self.attitude == Attitude.PANIQUE):
            RADIUS = 1.4
        else:
            RADIUS = 0.2
        self.angle += random.uniform(-0.5, 0.5)
        distance = random.uniform(0, RADIUS)

        move_x = round(RADIUS * math.cos(self.angle), 2)
        move_y = round(RADIUS * math.sin(self.angle), 2)

        futur_x = self.x + move_x
        futur_y = self.y + move_y

        if futur_x < 0 or futur_x > max_largeur:
            self.angle = math.pi - self.angle
            futur_x = clamp(futur_x, 0, max_largeur)

        if futur_y < 0 or futur_y > max_hauteur:
            self.angle = -self.angle
            futur_y = clamp(futur_y, 0, max_hauteur)

        # DEBUG
        if (AGENT_DEBUG and self.attitude == Attitude.PANIQUE and ((move_x + move_y) > 1)):
            print(f"=== {self.id} a beaucoup bougé car panique")

        self.x = futur_x
        self.y = futur_y
    
    def __str__(self):
        return f"Agent {self.id} ({str(self.etat)}): ({self.x}, {self.y})"
