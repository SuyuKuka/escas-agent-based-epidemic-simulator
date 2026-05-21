from agent import *
from environnement import *
from pathogene import *

class Simulation:
    # Constructeur
    def __init__(self, max_tick, environnement, pathogene):
        self.started = False
        self.tick = 0                               
        self.max_tick = max_tick                # Nombre max de tick avant la fin de la sim
        self.historique = []                        # Historique pour export avec json
        self.agents = [] # Agents de la sim
        self.agentIDIterator = 0

        self.environnement = environnement
        self.pathogene = pathogene

    def add_agents(self, sains, infectes, gueris):
        for _ in range(sains):
            self.agents.append(Agent(self.agentIDIterator,
                                     round(random.uniform(0, self.environnement.largeur), 2),
                                     round(random.uniform(0, self.environnement.hauteur), 2),
                                     Etat.SAIN))
            self.agentIDIterator += 1
        for _ in range(infectes):
            self.agents.append(Agent(self.agentIDIterator,
                                     round(random.uniform(0, self.environnement.largeur), 2),
                                     round(random.uniform(0, self.environnement.hauteur), 2),
                                     Etat.INFECTE))
            self.agentIDIterator += 1
        for _ in range(gueris):
            self.agents.append(Agent(self.agentIDIterator,
                                     round(random.uniform(0, self.environnement.largeur), 2),
                                     round(random.uniform(0, self.environnement.hauteur), 2),
                                     Etat.GUERI))
            self.agentIDIterator += 1

    def start(self, seed):
        if self.started:
            return
        random.seed(seed)
        self.started = True
        for _ in range(self.max_tick):
            self.update()
    
    def update(self):
        self.move_agents()
        self.update_contagion()
        self.save_snapshot()
        self.tick += 1
    
    def move_agents(self):
        for agent in self.agents:
            agent.move(self.environnement.largeur, self.environnement.hauteur)

    def update_contagion(self):
        nouveaux_infectes = []

        for agent in self.agents:
            agent.tick_etat += 1
            if (agent.etat == Etat.INFECTE):
                # Guérison
                if (agent.tick_etat == self.pathogene.tick_guerison):
                    agent.etat = Etat.GUERI
                    agent.tick_etat = 0
                else:
                    # Infection des voisins
                    for voisin in self.agents:
                        if voisin.etat == Etat.SAIN:
                            dist = (voisin.x - agent.x)**2 + (voisin.y - agent.y)**2
                            if dist <= self.pathogene.rayon_contagion**2:
                                proba = self.pathogene.proba_contagion
                                if voisin.attitude == Attitude.PANIQUE:
                                    proba *= 1.3
                                elif voisin.attitude == Attitude.CONFINE:
                                    proba *= 0.4

                                if (random.random() < proba):
                                    nouveaux_infectes.append(voisin)

        
        for agent in nouveaux_infectes:
            agent.etat = Etat.INFECTE
            agent.tick_etat = 0

    def save_snapshot(self):
        sains = 0
        infectes = 0
        gueris = 0
        for agent in self.agents:
            if (agent.etat == Etat.INFECTE):
                infectes += 1
            elif (agent.etat == Etat.SAIN):
                sains += 1
            elif (agent.etat == Etat.GUERI):
                gueris += 1
        
        self.historique.append({"tick": self.tick, "sains": sains, "infectes": infectes, "gueris": gueris})
    
    def build_json_dump(self):
        return {"simulation" : {
            "historique" : self.historique
        }}




