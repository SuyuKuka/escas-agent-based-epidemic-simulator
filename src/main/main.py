from simulation import *

# Paramètres de départ
seed = 0
max_tick = 100
rayon_contagion = 10
proba_contagion = 1
tick_guerison = 10
nb_agents = 200
width = 100
height = 100
nb_infect = 1

# Execution

sim = Simulation(seed, max_tick, rayon_contagion, proba_contagion, tick_guerison, nb_agents, width, height, nb_infect)
sim.start()
