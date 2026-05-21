from simulation import *
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# =============================
#region Paramètres (Input)
# =============================

## Simulation
max_tick = 100
seed = 0

## Environnement
largeur = 100
hauteur = 100

## Pathogène
rayon_contagion = 1
proba_contagion = 0.3
tick_guerison = 100

## Agents
nb_sains = 190
nb_infectes = 10
nb_gueris = 10

# =============================
#region Exécution
# =============================

## Simulation
print("La simulation va commencer...")
environnement = Environnement(largeur, hauteur)
pathogene = Pathogene(rayon_contagion, proba_contagion, tick_guerison)
sim = Simulation(max_tick, environnement, pathogene)

sim.add_agents(nb_sains, nb_infectes, nb_gueris)
sim.start(seed)
print("La simulation est fini")

## Ecriture sur fichier
print("Ecriture des données dans 'out.json'...")
json_dump = sim.build_json_dump()
with open('out.json', 'w') as fp:
    json.dump(json_dump, fp, indent=2)
print("Ecriture terminée !")

## Plot
print("Début plot des données du fichier...")
simulation = json_dump["simulation"]
historique = simulation["historique"]
ticks = [d["tick"] for d in historique]
sains = [d["sains"] for d in historique]
infectes = [d["infectes"] for d in historique]
gueris = [d["gueris"] for d in historique]

fig, ax = plt.subplots(figsize=(10, 6))
 
ax.plot(ticks, sains,    label="sains (S)",    color="#2196F3", linewidth=2)
ax.plot(ticks, infectes, label="infectés (I)", color="#F44336", linewidth=2)
ax.plot(ticks, gueris,   label="guéris (R)",   color="#4CAF50", linewidth=2)
 
ax.set_title("Simulation")
ax.set_xlabel("Ticks (T)")
ax.set_ylabel("Nombre d'individus (N)")
ax.grid(True, linestyle="--", alpha=0.4)                        # Quadrillage background
ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))    # Force les valeurs à être des int
 
plt.legend()
plt.tight_layout()                                              # Pour forcer le plot a prendre toute la zone de la fenêtre
# plt.savefig("simulation_SIR.png", dpi=150)
plt.show()
print("Plot dessiné !")
