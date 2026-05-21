
class Pathogene:
    def __init__(self, rayon_contagion, proba_contagion, tick_guerison):
        self.rayon_contagion = rayon_contagion  # Rayon contagion
        self.proba_contagion = proba_contagion  # Proba contagion ([0, 1])
        self.tick_guerison = tick_guerison      # Nombre de tick avant guérison