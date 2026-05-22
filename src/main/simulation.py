from agent import *
from environnement import *
from pathogene import *

class Simulation:
    # Constructeur
    def __init__(self, config):
        self.reset(config)

    def reset(self, config):
        random.seed(config['seed'])
        self.is_running = False
        self.tick = 0
        self.historique = []                        # Historique pour export avec json
        self.sains = []
        self.sains_shown = 0
        self.infectes = []
        self.infectes_shown = 0
        self.gueris = []
        self.gueris_shown = 0
        self.agentIDIterator = 0

        self.environnement = Environnement(config)
        self.pathogene = Pathogene(config)
        self.create_agents(config['range_nb_sains'][1], config['range_nb_infectes'][1], config['range_nb_gueris'][1])
        self.show_agents(config['nb_sains'], config['nb_infectes'], config['nb_gueris'])
        self.agents = [*self.sains, *self.infectes, *self.gueris]
    
    def create_agents(self, max_sains, max_infectes, max_gueris):
        for _ in range(max_sains):
            self.sains.append(Agent(self.agentIDIterator,
                                     round(random.uniform(0, self.environnement.largeur), 2),
                                     round(random.uniform(0, self.environnement.hauteur), 2),
                                     Etat.SAIN))
            self.agentIDIterator += 1
        for _ in range(max_infectes):
            self.infectes.append(Agent(self.agentIDIterator,
                                     round(random.uniform(0, self.environnement.largeur), 2),
                                     round(random.uniform(0, self.environnement.hauteur), 2),
                                     Etat.INFECTE))
            self.agentIDIterator += 1
        for _ in range(max_gueris):
            self.gueris.append(Agent(self.agentIDIterator,
                                     round(random.uniform(0, self.environnement.largeur), 2),
                                     round(random.uniform(0, self.environnement.hauteur), 2),
                                     Etat.GUERI))

    def modify_agents_nb(self, nb_sains, nb_infectes, nb_gueris):
        (nb_sains, nb_infectes, nb_gueris) = self.show_agents(nb_sains, nb_infectes, nb_gueris)
        self.unshow_agents(nb_sains, nb_infectes, nb_gueris)
        
    def show_agents(self, nb_sains, nb_infectes, nb_gueris):
        while nb_sains > 0 and self.sains_shown < len(self.sains):
            self.sains[self.sains_shown].shown = True
            self.sains_shown += 1
            nb_sains -= 1
        while nb_infectes > 0 and self.infectes_shown < len(self.infectes):
            self.infectes[self.infectes_shown].shown = True
            self.infectes_shown += 1
            nb_infectes -= 1
        while nb_gueris > 0 and self.gueris_shown < len(self.gueris):
            self.gueris[self.gueris_shown].shown = True
            self.gueris_shown += 1
            nb_gueris -= 1
        return (nb_sains, nb_infectes, nb_gueris)
    
    def unshow_agents(self, nb_sains, nb_infectes, nb_gueris):
        while nb_sains < 0 and self.sains_shown > 0:
            self.sains[self.sains_shown - 1].shown = False
            self.sains_shown -= 1
            nb_sains += 1
        while nb_infectes < 0 and self.infectes_shown > 0:
            self.infectes[self.infectes_shown - 1].shown = False
            self.infectes_shown -= 1
            nb_infectes += 1
        while nb_gueris < 0 and self.gueris_shown > 0:
            self.gueris[self.gueris_shown - 1].shown = False
            self.gueris_shown -= 1
            nb_gueris += 1

    def add_new_agents(self, sains, infectes, gueris):
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
    
    def start(self):
        self.is_running = True
        tmp = list(filter(lambda x: x is not None, self.agents))
        self.agents = tmp
    
    def stop(self):
        self.is_running = False

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




