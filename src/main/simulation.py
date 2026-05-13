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
        self.agents = self.create_agents(nb_agents)

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
            agent.state = State.INFECTE

    def update(self):
        self.move_agents()
        self.update_contagion()
        self.print_snapshot()
        self.tick += 1
    
    def move_agents(self):
        for agent in self.agents:
            agent.move(self)

    def update_contagion(self):
        nouveaux_infectes = []

        for agent in self.agents:
            agent.tick_in_state += 1
            if (agent.state == State.INFECTE):
                # Guérison
                if (agent.tick_in_state == self.tick_guerison):
                    agent.state = State.GUERI
                    agent.tick_in_state = 0
                else:
                    # Infection des voisins
                    for voisin in self.agents:
                        if voisin.state == State.SAIN:
                            dist = (voisin.x - agent.x)**2 - (voisin.y - agent.y)**2
                            if dist <= self.rayon_contagion**2:
                                if (random.random() < self.proba_contagion):
                                    nouveaux_infectes.append(voisin)

        
        for agent in nouveaux_infectes:
            agent.state = State.INFECTE
            agent.tick_in_state = 0

    def print_snapshot(self):
        sains = 0
        infectes = 0
        gueris = 0
        for agent in self.agents:
            if (agent.state == State.INFECTE):
                infectes += 1
            elif (agent.state == State.SAIN):
                sains += 1
            elif (agent.state == State.GUERI):
                gueris += 1
        
        print(f"Tick {self.tick} : Sains {sains}, Infectés {infectes}, Guéris {gueris}")




