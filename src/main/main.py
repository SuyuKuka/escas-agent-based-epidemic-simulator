from view import *
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# =============================
#region Paramètres (Input)
# =============================
name = "Epidemics and Social Contagion Agent-based Simulator (ESCAS)"

## Simulation
range_exec_tick = (1, 100000)
range_seed = (0, 30000)
exec_tick = 5000
seed = 0

range_update_speed = (1, 60)
range_update_step = (1, 100)         
update_speed = 20                   # Nombre d'update par seconde de la sim
update_step = 1                     # Nombre d'update à la fois par update de la sim

## Environnement
range_largeur = (10, 10000)
range_hauteur = (10, 10000)

largeur = 100
hauteur = 100

## Pathogène
range_rayon_contagion = (0, max(range_largeur[1], range_hauteur[1]))
range_proba_contagion = (0, 1)
range_tick_guerison = range_exec_tick

rayon_contagion = 1
proba_contagion = 0.3
tick_guerison = 100

## Agents
range_nb_sains = (0, 300)
range_nb_infectes = (0, 300)
range_nb_gueris = (0, 300)

nb_sains = 1
nb_infectes = 0
nb_gueris = 0

config = {
    "name": name,

    "range_exec_tick": range_exec_tick,
    "range_seed": range_seed,
    "exec_tick": exec_tick,
    "seed": seed,

    "range_update_speed": range_update_speed,
    "range_update_step": range_update_step,
    "update_speed": update_speed,
    "update_step": update_step,

    "range_largeur": range_largeur,
    "range_hauteur": range_hauteur,
    "largeur": largeur,
    "hauteur": hauteur,

    "range_rayon_contagion": range_rayon_contagion,
    "range_proba_contagion": range_proba_contagion,
    "range_tick_guerison": range_tick_guerison,
    "rayon_contagion": rayon_contagion,
    "proba_contagion": proba_contagion,
    "tick_guerison": tick_guerison,

    "range_nb_sains": range_nb_sains,
    "range_nb_infectes": range_nb_infectes,
    "range_nb_gueris": range_nb_gueris,
    "nb_sains": nb_sains,
    "nb_infectes": nb_infectes,
    "nb_gueris": nb_gueris
}

# =============================
#region Exécution
# =============================

## Simulation
print("La simulation va commencer...")
# environnement = Environnement(largeur, hauteur)
# pathogene = Pathogene(rayon_contagion, proba_contagion, tick_guerison)
# sim = Simulation(tick, environnement, pathogene, seed)
# sim.clear_and_create_agents(nb_sains, nb_infectes, nb_gueris)

view = View(config)
view.runloop()

# view.start()
# sim.start(seed)
# print("La simulation est fini")

# ## Ecriture sur fichier
# print("Ecriture des données dans 'out.json'...")
# json_dump = sim.build_json_dump()
# with open('out.json', 'w') as fp:
#     json.dump(json_dump, fp, indent=2)
# print("Ecriture terminée !")

# ## Plot
# print("Début plot des données du fichier...")
# simulation = json_dump["simulation"]
# historique = simulation["historique"]
# ticks = [d["tick"] for d in historique]
# sains = [d["sains"] for d in historique]
# infectes = [d["infectes"] for d in historique]
# gueris = [d["gueris"] for d in historique]

# fig, ax = plt.subplots(figsize=(10, 6))
 
# ax.plot(ticks, sains,    label="sains (S)",    color="#2196F3", linewidth=2)
# ax.plot(ticks, infectes, label="infectés (I)", color="#F44336", linewidth=2)
# ax.plot(ticks, gueris,   label="guéris (R)",   color="#4CAF50", linewidth=2)
 
# ax.set_title("Simulation")
# ax.set_xlabel("Ticks (T)")
# ax.set_ylabel("Nombre d'individus (N)")
# ax.grid(True, linestyle="--", alpha=0.4)                        # Quadrillage background
# ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))    # Force les valeurs à être des int
 
# plt.legend()
# plt.tight_layout()                                              # Pour forcer le plot a prendre toute la zone de la fenêtre
# # plt.savefig("simulation_SIR.png", dpi=150)
# plt.show()
# print("Plot dessiné !")
