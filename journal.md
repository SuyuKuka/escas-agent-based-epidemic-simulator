# 17/10/2025

- [x] Trouver l'état de l'art sur les algorithmes de swarm intelligence (https://en.wikipedia.org/wiki/Swarm_intelligence)
- [x] Trouver l'état de l'art sur le cellular automata (https://en.wikipedia.org/wiki/Cellular_automaton)
- [x] Comment utiliser les idées de ces domains pour réaliser une simulation ?
# Etat de l'Art
Désigne le niveau de développement le plus avancé dans un domaine scientifique ou artistique jamais atteint.
## Etat de l'art sur les algorithmes de swarm intelligence
(= Intelligence distribuée) L'Intelligence distribuée s'inspire du comportement collectif d'animaux sociaux pour résoudre des problèmes complexes de manière décentralisée. Dans ce domaine les "agents" agissent de manière locale sans pour autant perdre de la cohérence dans le comportement global du groupe.

1987 :
- Boids :
	- Programme informatique qui simule les nuées d'oiseaux en vol de manière très cohérente
    	- 3 règles simples suffisent (Séparation, Alignement et Cohésion)
        	- Modèle simpliste pouvant être plus complexe en ajoutant des règles
            	- Inspiration de beaucoup de modèles modernes
                	- A inspiré de nombreux modèles modernes, notamment dans la robotique collective et les effets visuels (art numérique)
                    1992 :
                    - Ant Colony Optimization :
                    	- Inspiré du comportement des fourmis cherchant de la nourriture
                        	- Les agents déposent une phéromone virtuelle pour signaler la présence de nourriture
                            	- L’intensité de la trace guide les autres agents : les chemins les plus courts sont renforcés au fil du temps
                                	- Utilisé pour résoudre des problèmes d’optimisation combinatoire, comme le problème du voyageur de commerce ou la planification de routes
                                    1995 :
                                    - Self-propelled particles :
                                    	-  Chaque particule se déplace avec une vitesse constante en s’alignant avec ses voisins proches
                                        	- Sert de base à de nombreuses simulations biologiques (bancs de poisson, bactéries)
                                            2005 :
                                            - Artificial Bee Colony Algorithm :
                                            	- Inspiré du comportement de recherche de nourriture chez les abeilles.
                                                	- Trois agents différents (employed bees, onlooker bees et scout bees)
                                                    	- L’exploration et l’exploitation des sources de nourriture sont optimisées collectivement
                                                        	- Utilisé pour des problèmes d’optimisation continue et la recherche de maxima/minima de fonctions complexes.

                                                            ## Etat de l'art sur le cellular automata
                                                            (= Automates Cellulaires) Les Automates Cellulaires étudient l'évolution d'état d'une grille de cellules en fonction de règles locales simples.

                                                            1970 :
                                                            - Game Of Life :
                                                            	- Simulation simpliste qui met en valeur un comportement complexe à partir de règles simples
                                                                	- 3 règles suffisent pour un modèle simple (naissance, survie et mort)
                                                                    	- Peut produire des structures stables, oscillantes ou mobiles (gliders, pulsars, spaceships)
                                                                        	- A inspiré de nombreuses études la vie artificielle

                                                                            ## Avec ces idées, comment réaliser une simulation ?

                                                                            1. Définir l'environnement
                                                                            	- Grille 2D
                                                                                	- OU Espace continu 2D
                                                                                    2. Définir l'agent
                                                                                    	- Attributs
                                                                                        3. Définir les règles d'évolution
                                                                                        	- Comprend l'évolution de l'agent et de l'environnement
                                                                                            4. Définir la boucle de simulation
                                                                                            	- Met à jour les agents et l'environnement selon leurs règles
                                                                                                5. Visualisation 
                                                                                                	- Résultat et interprétation de la simulation