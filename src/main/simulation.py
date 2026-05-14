from agent import *

class Simulation:
    # Constructeur
    def __init__(self, seed, max_tick, rayon_contagion, proba_contagion, tick_guerison, nb_agents, width, height, nb_infect):
        self.seed = seed                        # Graine pour random
        self.max_tick = max_tick                # Nombre max de tick avant la fin de la sim
        self.nb_infect = nb_infect        # Nombre d'infectés lors du début de la sim

        self.rayon_contagion = rayon_contagion  # Rayon contagion
        self.proba_contagion = proba_contagion  # Proba contagion ([0, 1])
        self.tick_guerison = tick_guerison      # Nombre de tick avant guérison

        self.width = width                      # Largeur de la "map"
        self.height = height                    # Hauteur de la "map"

        self.tick = 0                               
        self.historique = []                        # Historique pour export avec json
        self.agents = self.create_agents(nb_agents) # Agents de la sim

    def create_agents(self, nb_agents):
        agents = []
        for i in range(nb_agents):
            agents.append(Agent(i, round(random.uniform(0, self.width), 2), round(random.uniform(0, self.height), 2)))
        return agents
    
    def start(self):
        random.seed(self.seed)
        self.infect_random()
        for _ in range(self.max_tick):
            self.update()

    def infect_random(self):
        for _ in range(self.nb_infect):
            agent = self.agents[random.randint(0, len(self.agents) - 1)]
            agent.etat = Etat.INFECTE

    def update(self):
        self.move_agents()
        self.update_contagion()
        self.save_snapshot()
        self.tick += 1
    
    def move_agents(self):
        for agent in self.agents:
            agent.move(self)

    def update_contagion(self):
        nouveaux_infectes = []

        for agent in self.agents:
            agent.tick_etat += 1
            if (agent.etat == Etat.INFECTE):
                # Guérison
                if (agent.tick_etat == self.tick_guerison):
                    agent.etat = Etat.GUERI
                    agent.tick_etat = 0
                else:
                    # Infection des voisins
                    for voisin in self.agents:
                        if voisin.etat == Etat.SAIN:
                            dist = (voisin.x - agent.x)**2 + (voisin.y - agent.y)**2
                            if dist <= self.rayon_contagion**2:
                                proba = self.proba_contagion
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




