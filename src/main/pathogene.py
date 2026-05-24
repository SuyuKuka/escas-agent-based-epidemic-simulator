
class Pathogene:
    def __init__(self, config):
        self.rayon_contagion = config['rayon_contagion']  # Rayon contagion
        self.proba_contagion = config['proba_contagion']  # Proba contagion ([0, 1])
        self.tick_guerison = config['tick_guerison']      # Nombre de tick avant guérison