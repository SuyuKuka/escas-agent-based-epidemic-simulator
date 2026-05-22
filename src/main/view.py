import pygame
import pygame.gfxdraw
import os
import pygame_gui
import json
from simulation import *
from pathlib import Path

BASE_DIR = Path(__file__).parent

W, H = 1200, 700
SIM_X = 200                         # zone simulation commence ici
SIM_W = 750                         # largeur zone simulation
PANEL_W = W - SIM_X - SIM_W         # largeur panneau info agent (droite)
FPS = 60
COULEURS = {Etat.SAIN: (70, 130, 220),
            Etat.INFECTE: (220, 60, 60),
            Etat.GUERI: (50, 180, 100)}
RADIUS_DRAW_AGENT = 8

def get_agent_couleur(agent):
    return COULEURS.get(agent.etat, (0, 0, 0))


class View:
    def __init__(self, config):
        self.config = config
        self.init_pygame()
        
        self.is_running = True          # Si faux, l'application termine
        self.sim_running = False

        self.init_sim()
        self.init_ui()
        # self.runloop() appelé par main
    
    def init_pygame(self):
        pygame.init()
        pygame.display.set_caption(self.config['name'])
        self.ecran = pygame.display.set_mode((W, H), pygame.SCALED)
        self.clock = pygame.time.Clock()
        theme_path = BASE_DIR / 'res' / 'theme' / 'theme.json'
        self.manager = pygame_gui.UIManager((W, H), theme_path)
    
    def init_sim(self):
        self.sim = Simulation(self.config)

    def init_ui(self):
        config = self.config
        manager = self.manager

        # Variables utiles pour la vue
        self.agent_selectionne = None
        self.agent_info_ouvert = False

        # Panneau Configuration sim (gauche)
        # Dictionnaire des sliders + leurs valeurs (pour être modifé autre part dans le code)
        self.sliders = {}
        self.valeurs_labels = {}

        self.import_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(10, 10, 85, 30),
            text='Import',
            manager=manager
        )
        self.export_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(105, 10, 85, 30),
            text='Export',
            manager=manager
        )

        controles = [
            {"id": "exec_tick", "label": "Tick", "default": config['exec_tick'], "range": config['range_exec_tick']},
            {"id": "seed", "label": "Seed", "default": config['seed'], "range": config['range_seed']},

            {"id": "update_speed", "label": "Update par seconde", "default": config['update_speed'], "range": config['range_update_speed']},
            {"id": "update_step", "label": "Update par update", "default": config['update_step'], "range": config['range_update_step']},

            {"id": "largeur", "label": "Largeur", "default": config['largeur'], "range": config['range_largeur']},
            {"id": "hauteur", "label": "Hauteur", "default": config['hauteur'], "range": config['range_hauteur']},

            {"id": "rayon_contagion", "label": "Rayon contagion", "default": config['rayon_contagion'], "range": config['range_rayon_contagion']},
            {"id": "proba_contagion", "label": "Proba contagion", "default": config['proba_contagion'], "range": config['range_proba_contagion']},
            {"id": "tick_guerison", "label": "Tick Guérison", "default": config['tick_guerison'], "range": config['range_tick_guerison']},

            {"id": "nb_sains", "label": "nb sains", "default": config['nb_sains'], "range": config['range_nb_sains']},
            {"id": "nb_infectes", "label": "nb infectés", "default": config['nb_infectes'], "range": config['range_nb_infectes']},
            {"id": "nb_gueris", "label": "nb guéris", "default": config['nb_gueris'], "range": config['range_nb_gueris']},
        ]

        largeur_scroll_list = SIM_X - 10
        hauteur_scroll_list = H - 145

        hauteur_interne_scroll = len(controles) * 85 # Nombre de pixel alloué pour le scroll
        
        # Scroll container
        self.scroll_container = pygame_gui.elements.UIScrollingContainer(
            relative_rect=pygame.Rect(10, 50, largeur_scroll_list, hauteur_scroll_list),
            manager=manager
        )

        # On ajuste la zone virtuelle de défilement
        self.scroll_container.set_scrollable_area_dimensions(
            (largeur_scroll_list - 25, hauteur_interne_scroll)
        )

        start_x = 0
        current_y = 5
        spacing = 5

        for ctrl in controles:
            # TODO: Désactiver les sliders durant la simulation et les reactiver quand elle ne run plus
            if ctrl["id"] == "proba_contagion":
                pas = 0.05
            else:
                pas = 1
            
            width_title = 140
            width_value = 40
            height_box = 30

            # Label Nom
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(start_x, current_y, width_title, height_box),
                text=ctrl["label"],
                manager=manager,
                container=self.scroll_container
            )

            self.valeurs_labels[ctrl["id"]] = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(start_x + width_title - 12, current_y, width_value, height_box),
                text=str(ctrl["default"]),
                manager=manager,
                container=self.scroll_container
            )
            current_y += height_box

            self.sliders[ctrl["id"]] = pygame_gui.elements.UIHorizontalSlider(
                relative_rect=pygame.Rect(start_x, current_y, 170, height_box),
                start_value=ctrl["default"],
                value_range=ctrl["range"],
                manager=manager,
                container=self.scroll_container,
                click_increment=pas
            )
            current_y += 30

            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(start_x, current_y, 50, 20),
                text=str(ctrl["range"][0]),
                manager=manager,
                container=self.scroll_container
            )
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(start_x + 115, current_y, 50, 20),
                text=str(ctrl["range"][1]),
                manager=manager,
                container=self.scroll_container
            )
            current_y += 20 + spacing

        current_y = H - 105

        # Bouton bottom
        bouton_x = (SIM_X - 170) // 2
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(bouton_x, current_y + 25, 170, 30),
            text='Start Simulation',
            manager=manager
        )
        self.reset_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(bouton_x, current_y + 55, 170, 30),
            text='Reset',
            manager=manager
        )

        self.graph_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(W - PANEL_W + 20, H - 50, PANEL_W - 40, 30),
            text='Afficher le graphique',
            manager=manager
        )
    
    def runloop(self):
        manager = self.manager
        ecran = self.ecran
        update_speed = self.config['update_speed']
        update_step = self.config['update_step']
        max_exec_tick = self.config['range_exec_tick'][1]

        # Accumule le temps pour sim_update()
        time_per_sim_update = 1.0 / update_speed
        sim_accumulator = 0.0

        # Gameloop
        while self.is_running:
            dt = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():
                # L'utilisateur à appuyé sur le bouton quitter de la fenêtre
                if event.type == pygame.QUIT: 
                    self.is_running = False
                # L'utilisateur à appuyé sur un bouton, il faut vérifier lequel a été appuyé
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    self.check_button_click(event)
                # L'utilisateur à modifié la valeur d'un slider, il faut vérifier lequel a été appuyé
                if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    self.check_slider_move(event)
                # L'utilisateur à fait clique gauche
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    if mx >= SIM_X and mx <= W - PANEL_W:
                        # print(f"click : ({mx}, {my})")
                        self.return_agent_click(mx, my)

                manager.process_events(event)

            manager.update(dt)

            if self.sim_running and update_speed > 0:
                sim_accumulator += dt

                while sim_accumulator >= time_per_sim_update:
                    self.sim.update(min(update_step, max_exec_tick - self.sim.tick))
                    sim_accumulator -= time_per_sim_update
                
                    if (self.sim.tick == self.config['exec_tick']):
                        self.sim_running = False
                        self.start_button.set_text('Start')
                        self.set_sliders(True)
                        sim_accumulator = 0.0
                        break

            self.draw(dt)
            self.update_graph()
            manager.draw_ui(ecran)
            pygame.display.flip()

    def check_button_click(self, event):
        if event.ui_element == self.start_button:
            # print(self.config['exec_tick'])
            self.sim_running = not self.sim_running
            if self.sim_running:
                self.start_button.set_text('Pause')
                self.set_sliders(False)
            else:
                self.start_button.set_text('Start')
                self.set_sliders(True)
        elif event.ui_element == self.reset_button:
            self.sim.reset(self.config)
            self.sim_running = False
            self.start_button.set_text('Start')
            self.agent_selectionne = None 
            self.agent_info_ouvert = False
        elif event.ui_element == self.export_button:
            with open('res/input/config.json', 'w') as f:
                json.dump(self.config, f, indent=4)
            print("Configuration sauvegardée dans 'config.json' !")
        elif event.ui_element == self.import_button:
            if os.path.exists('res/input/config.json'):
                with open('res/input/config.json', 'r') as f:
                    nouvelle_config = json.load(f)
                    for cle, valeur in nouvelle_config.items():
                        self.config[cle] = valeur
                    
                    for ctrl_id, slider in self.sliders.items():
                        if ctrl_id in self.config:
                            slider.set_current_value(self.config[ctrl_id])
                            self.valeurs_labels[ctrl_id].set_text(str(self.config[ctrl_id]))

                    self.sim.reset(self.config)
                    self.sim_running = False
                    self.start_button.set_text('Start')
                    self.agent_selectionne = None
                    self.agent_info_ouvert = False
                print("Configuration chargée avec succès !")
            else:
                print("Erreur : Aucun fichier 'res/input/config.json' trouvé.")
        elif event.ui_element == self.graph_button:
            self.open_graph()
    
    def check_slider_move(self, event):
        for ctrl_id, slider in self.sliders.items():
            if event.ui_element == slider:
                # Variable pour mis à jour nombre d'agent
                old_nb_sains = self.config["nb_sains"]
                old_nb_infectes = self.config["nb_infectes"]
                old_nb_gueris = self.config["nb_gueris"]

                if ctrl_id == "proba_contagion":
                    valeur = round(float(event.value), 2)
                else:
                    valeur = int(event.value)
                self.config[ctrl_id] = valeur
                self.valeurs_labels[ctrl_id].set_text(str(valeur))

                if ctrl_id == "seed" or ctrl_id == "largeur" or ctrl_id == "hauteur":
                    self.sim.reset(self.config)
                elif ctrl_id == "nb_sains":
                    self.sim.modify_agents_nb(self.config[ctrl_id] - old_nb_sains, 0, 0)
                elif ctrl_id == "nb_infectes":
                    self.sim.modify_agents_nb(0, self.config[ctrl_id] - old_nb_infectes, 0)
                elif ctrl_id == "nb_gueris":
                    self.sim.modify_agents_nb(0, 0, self.config[ctrl_id] - old_nb_gueris)

    
    def return_agent_click(self, mx, my):
        clique = None
        
        rayon_ecran_carre = RADIUS_DRAW_AGENT ** 2

        for a in self.sim.agents:
            if not a.shown:
                continue

            ax_ecran, ay_ecran = self.sim_pos_to_screen_pos((a.x, a.y))
            # print((ax_ecran, ay_ecran))
            distance_carre = (ax_ecran - mx)**2 + (ay_ecran - my)**2
        
            if distance_carre < rayon_ecran_carre:
                clique = a
        if clique:
            self.agent_selectionne = clique
            self.agent_info_ouvert    = True
        else:
            self.agent_selectionne = None
            self.agent_info_ouvert    = False

    def draw(self, dt):
        ecran = self.ecran
        px = SIM_X + SIM_W
        
        # Fond
        ecran.fill((20, 20, 30))

        # Zone simulation
        pygame.draw.rect(ecran, (30, 30, 45), (SIM_X, 0, SIM_W, H))
        pygame.draw.line(ecran, (60, 60, 80), (SIM_X, 0), (SIM_X, H))

        for a in self.sim.agents:
            if a.shown:
                self.draw_agent(a, ecran, a is self.agent_selectionne)

        # Panneau gauche (fond)
        pygame.draw.rect(ecran, (25, 25, 40), (0, 0, SIM_X, H))

        # Panneau droite (fond)
        pygame.draw.rect(ecran, (35, 35, 55), (px + 1, 0, PANEL_W, H))
        pygame.draw.line(ecran, (60, 60, 80), (W - PANEL_W, 0), (W - PANEL_W, H))

        font_titre = pygame.font.SysFont("monospace", 22, bold=True)
        titre_surf = font_titre.render("Informations", True, (255, 255, 255))
        titre_rect = titre_surf.get_rect(center=(px + (PANEL_W // 2), 30))
        ecran.blit(titre_surf, titre_rect)

        pygame.draw.line(ecran, (80, 80, 100), (px + 20, 50), (px + PANEL_W - 20, 50))
        font_texte = pygame.font.SysFont("monospace", 16)
        # Panneau infos droite (apparaît si agent sélectionné)
        if self.agent_info_ouvert and self.agent_selectionne:
            a = self.agent_selectionne
            state = a.etat.name if hasattr(a.etat, 'name') else str(a.etat)
            infos = [
                f"Agent #{a.id}",
                f"État : {state}",
                f"Pos : ({round(a.x, 2)}, {round(a.y, 2)})",
            ]

            for i, ligne in enumerate(infos):
                surf = font_texte.render(ligne, True, (255, 255, 255))
                ecran.blit(surf, (px + 15, 70 + i * 35))
        else:
            lignes_defaut = [
                "Rien à afficher,",
                "cliquez sur un agent",
                "pour plus d'infos."
            ]
            for i, ligne in enumerate(lignes_defaut):
                surf = font_texte.render(ligne, True, (255, 255, 255))
                rect = surf.get_rect(center=(px + (PANEL_W // 2), 120 + i * 25))
                ecran.blit(surf, rect)

    def draw_agent(self, agent, ecran, est_selection):
        pos = self.sim_pos_to_screen_pos((agent.x, agent.y))
        couleur = get_agent_couleur(agent)
        
        pygame.gfxdraw.aacircle(ecran, pos[0], pos[1], RADIUS_DRAW_AGENT, couleur)
        pygame.gfxdraw.filled_circle(ecran, pos[0], pos[1], RADIUS_DRAW_AGENT, couleur)
        
        if (est_selection):
            pygame.gfxdraw.aacircle(ecran, pos[0], pos[1], RADIUS_DRAW_AGENT + 4, (255, 220, 0))

    def set_sliders(self, enabled: bool):
        for slider in self.sliders.values():
            if enabled:
                slider.enable()
            else:
                slider.disable()
        
    def sim_pos_to_screen_pos(self, xy):
        scale_x = SIM_W / self.sim.environnement.largeur
        scale_y = H / self.sim.environnement.hauteur
        
        screen_x = xy[0] * scale_x + SIM_X
        screen_y = xy[1] * scale_y
        
        return (int(screen_x), int(screen_y))

    
    def screen_pos_to_sim_pos(self, xy):
        scale_x = self.sim.environnement.largeur / SIM_W
        scale_y = self.sim.environnement.hauteur / H
        
        sim_x = (xy[0] - SIM_X) * scale_x
        sim_y = xy[1] * scale_y
        
        return (float(sim_x), float(sim_y))

    def open_graph(self):
        if hasattr(self, 'fenetre_graphe') and self.fenetre_graphe is not None:
            self.fenetre_graphe.kill()
            
        rect_fenetre = pygame.Rect((W // 2 - 300, H // 2 - 200), (600, 400))
        
        self.fenetre_graphe = pygame_gui.elements.UIWindow(
            rect=rect_fenetre,
            manager=self.manager,
            window_display_title="Évolution de la population (Modèle SIR)",
            resizable=False
        )
        
        self.graph_w = 568
        self.graph_h = 330
        
        self.graph_surface = pygame.Surface((self.graph_w, self.graph_h))
        self.graph_surface.fill((30, 30, 40))
        
        self.graph_image = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(0, 0, self.graph_w, self.graph_h),
            image_surface=self.graph_surface,
            manager=self.manager,
            container=self.fenetre_graphe
        )

    def update_graph(self):
        if not hasattr(self, 'fenetre_graphe') or not self.fenetre_graphe.alive():
            return
            
        historique = self.sim.historique
        if len(historique) < 2:
            return

        self.graph_surface.fill((30, 30, 40))
        
        for i in range(1, 5):
            y_ligne = i * (self.graph_h / 5)
            pygame.draw.line(self.graph_surface, (50, 50, 60), (0, y_ligne), (self.graph_w, y_ligne))

        max_pop = max([d["sains"] + d["infectes"] + d["gueris"] for d in historique])
        if max_pop == 0: max_pop = 1
        
        min_tick = historique[0]["tick"]
        max_tick = historique[-1]["tick"]
        delta_tick = max_tick - min_tick
        if delta_tick == 0: delta_tick = 1

        scale_x = self.graph_w / delta_tick
        scale_y = (self.graph_h - 10) / max_pop 

        points_sains = []
        points_infectes = []
        points_gueris = []

        for data in historique:
            x = (data["tick"] - min_tick) * scale_x
            
            y_sain = self.graph_h - (data["sains"] * scale_y)
            y_infecte = self.graph_h - (data["infectes"] * scale_y)
            y_gueri = self.graph_h - (data["gueris"] * scale_y)
            
            points_sains.append((x, y_sain))
            points_infectes.append((x, y_infecte))
            points_gueris.append((x, y_gueri))

        pygame.draw.lines(self.graph_surface, (70, 130, 220), False, points_sains, 2)
        pygame.draw.lines(self.graph_surface, (220, 60, 60), False, points_infectes, 2)
        pygame.draw.lines(self.graph_surface, (50, 180, 100), False, points_gueris, 2)
        
        self.graph_image.set_image(self.graph_surface)