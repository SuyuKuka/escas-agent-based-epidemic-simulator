import pygame
import os
import pygame_gui
from simulation import *

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
        self.manager = pygame_gui.UIManager((W, H))
    
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
        hauteur_scroll_list = H - 150

        hauteur_interne_scroll = len(controles) * 85 # Nombre de pixel alloué pour le scroll
        
        # Scroll container
        self.scroll_container = pygame_gui.elements.UIScrollingContainer(
            relative_rect=pygame.Rect(10, 20, largeur_scroll_list, hauteur_scroll_list),
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
            # 
            # Label Nom
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(start_x, current_y, 135, 25),
                text=ctrl["label"],
                manager=manager,
                container=self.scroll_container
            )

            # Label Valeur
            self.valeurs_labels[ctrl["id"]] = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(start_x + 115, current_y, 50, 25),
                text=str(ctrl["default"]),
                manager=manager,
                container=self.scroll_container
            )

            current_y += 25

            # Slider
            self.sliders[ctrl["id"]] = pygame_gui.elements.UIHorizontalSlider(
                relative_rect=pygame.Rect(start_x, current_y, 165, 30),
                start_value=ctrl["default"],
                value_range=ctrl["range"],
                manager=manager,
                container=self.scroll_container
            )
            current_y += 30

            # Label Range Min
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(start_x, current_y, 30, 20),
                text=str(ctrl["range"][0]),
                manager=manager,
                container=self.scroll_container
            )
            # Label Range Max
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(start_x + 115, current_y, 50, 20),
                text=str(ctrl["range"][1]),
                manager=manager,
                container=self.scroll_container
            )

            current_y += 20 + spacing

        current_y = H - 90
        # Bouton démarrer
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(start_x, current_y, 170, 30),
            text="Start Simulation",
            manager=manager
        )
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(start_x, current_y + 25, 170, 30),
            text='[>]',
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
                        sim_accumulator = 0.0
                        break

            self.draw(dt)

            manager.draw_ui(ecran)
            pygame.display.flip()

    def check_button_click(self, event):
        if event.ui_element == self.start_button:
            # print(self.config['exec_tick'])
            if (self.sim.tick == self.config['exec_tick']):
                self.sim.reset(self.config)
                return
            print(f"Simulation : {str(not self.sim_running)}")
            self.sim_running = not self.sim_running
    
    def check_slider_move(self, event):
        for ctrl_id, slider in self.sliders.items():
            if event.ui_element == slider:
                # Variable pour mis à jour nombre d'agent
                old_nb_sains = self.config["nb_sains"]
                old_nb_infectes = self.config["nb_infectes"]
                old_nb_gueris = self.config["nb_gueris"]

                valeur_entiere = int(event.value)
                self.config[ctrl_id] = valeur_entiere
                self.valeurs_labels[ctrl_id].set_text(str(valeur_entiere))

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

        for a in self.sim.get_agents():
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
        
        # Fond
        ecran.fill((20, 20, 30))

        # Zone simulation
        pygame.draw.rect(ecran, (30, 30, 45), (SIM_X, 0, SIM_W, H))
        pygame.draw.line(ecran, (60, 60, 80), (SIM_X, 0), (SIM_X, H))

        for a in self.sim.get_agents():
            if a.shown:
                self.draw_agent(a, ecran, a is self.agent_selectionne)

        # Panneau gauche (fond)
        pygame.draw.rect(ecran, (25, 25, 40), (0, 0, SIM_X, H))

        # Panneau droite (fond)
        pygame.draw.rect(ecran, (20, 20, 30), (SIM_X + SIM_W, 0, PANEL_W, H))

        # Panneau infos droite (apparaît si agent sélectionné)
        pygame.draw.line(ecran, (60, 60, 80), (W - PANEL_W, 0), (W - PANEL_W, H))
        if self.agent_info_ouvert and self.agent_selectionne:
            a = self.agent_selectionne
            px = SIM_X + SIM_W
            pygame.draw.rect(ecran, (35, 35, 55), (px + 1, 0, PANEL_W, H))

            font = pygame.font.SysFont("monospace", 18)
            infos = [
                f"Agent #{a.id}",
                f"État : {a.etat}",
                f"Pos : ({round(a.x, 2)}, {round(a.y, 2)})",
            ]
            for i, ligne in enumerate(infos):
                surf = font.render(ligne, True, (200, 200, 210))
                ecran.blit(surf, (px + 15, 40 + i * 35))

    def draw_agent(self, agent, ecran, est_selection):
        pos = self.sim_pos_to_screen_pos((agent.x, agent.y))
        pygame.draw.circle(ecran, get_agent_couleur(agent), (pos[0], pos[1]), RADIUS_DRAW_AGENT)
        if (est_selection):
            pygame.draw.circle(ecran, (255, 220, 0), (pos[0], pos[1]), 12, 2)
        
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