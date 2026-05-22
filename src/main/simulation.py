from agent import *
from environnement import *
from pathogene import *

class Simulation:
    # Constructeur
    def __init__(self, config):
        self.reset(config)

    def reset(self, config):
        random.seed(config['seed'])
        self.tick = 0
        self.historique = []                        # Historique pour export avec json
        self.agents = []                            # Agents de la sim
        self.agentIDIterator = 0
        self.deleted_sains = [] 
        self.deleted_infectes = []
        self.deleted_gueris = []

        self.environnement = Environnement(config)
        self.pathogene = Pathogene(config)
        self.create_agents(config['nb_sains'], config['nb_infectes'], config['nb_gueris'])

    def create_agents(self, sains, infectes, gueris):
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
    
    def remove_agents(self, sains, infectes, gueris):
        for i in range(len(self.agents) - 1, -1, -1):
            agent = self.agents[i]
            if agent == None:
                continue

            if sains == 0 and infectes == 0 and gueris == 0:
                break

            if (sains != 0 and agent != None and agent.etat == Etat.SAIN):
                sains -= 1
                self.agents[i] = None
                self.deleted_sains.append((i, agent))
            elif (infectes != 0 and agent != None and agent.etat == Etat.INFECTE):
                infectes -= 1
                self.agents[i] = None
                self.deleted_infectes.append((i, agent))
            elif (gueris != 0 and agent != None and agent.etat == Etat.GUERI):
                gueris -= 1
                self.agents[i] = None
                self.deleted_gueris.append((i, agent))
    
    def add_agents(self, sains, infectes, gueris):
        if (sains > 0):
            for i in range(len(self.deleted_sains) - 1, -1, -1):
                val = self.deleted_sains[i]
                if val == None: continue

                id, agent = val
                self.agents[id] = agent

                self.deleted_sains.pop()
                sains -= 1
                if (sains == 0): break
        if (infectes > 0):
            for i in range(len(self.deleted_infectes) - 1, -1, -1):
                val = self.deleted_infectes[i]
                if val == None: continue

                id, agent = val
                self.agents[id] = agent

                self.deleted_infectes.pop()
                infectes -= 1
                if (infectes == 0): break
        if (gueris > 0):
            for i in range(len(self.deleted_gueris) - 1, -1, -1):
                val = self.deleted_gueris[i]
                if val == None: continue

                id, agent = val
                self.agents[id] = agent

                self.deleted_gueris.pop()
                gueris -= 1
                if (gueris == 0): break
        self.create_agents(sains, infectes, gueris)

    def update(self, step):
        for _ in range(step):
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




