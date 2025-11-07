# Projet PPG7 2025-2026


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
 

## Idée : Simulateur de la vie et de la mort.

▶ À quel problème répond-t-il ?

https://fr.wikipedia.org/wiki/%C3%89pid%C3%A9miologie

Comment chaque espèce s’adapte en fonction de son environnement ?


Quelles sont les caractéristiques les plus avantageuses pour survivre ?

Peut-on utiliser le modèle représenté pour étudier les cas similaires dans le monde réel ? (Extinction, Décisions,...)

▶ Quels sont les objectifs principaux, intermédiaires, supplémentaires ?
Affichage simple   
A gauche la simulation  
Différenciation graphique des espèces  
A droite le gui pour lancer une simulation  
3 Espèces ou + (mouvement, mange, sans reproduction)  


▶ Testabilité : comment tester si le projet est réussi ? proposer des protocoles de test (de préférence automatiques, CI, . . . )   
Modèles simples :  
Mouvement  
Attaque/Fuite  
Reproduction  
Algorithmes :  
Déplacement dans un milieu : A*  
Décision la plus avantageuse : Arbre de décision pondéré  
Hérédité des caractéristiques avantageuses : Algorithme génétique  

▶ Originalité du projet. Que votre code ajoute à l'état de l’art ? 


▶ Pourquoi ce n’est pas qu’un collage d’API ? 

▶ Calendrier/Jalons : les grandes étapes du projet et des dates (approximatives) pour chacune


▶ Quelles sont les données en entrées ?   
▶ Quelles sont les données en sortie ? 

Animaux:  
Carnivores: mangent de la viande  
Herbivores: mangent des plantes  
Plantes: photosynthèse  
…

Algorithmes utilisables :  
A*, Dijkstra, DFS, BFS génétique

Saisons, temps, météo, température, dénivelé

Caractéristiques par famille :  
Animaux :  
Vitesse, Force, Fatigue, Soif, Dimension et Faim  
Méthode et vitesse de reproduction  
Autodéfense / Fuite / les 2  
Niveau de pacifisme/agressivité  
Milieu préféré  
Carnivores :  
Herbivores :  
Plantes :  
Vitesse de propagation / reproduction  
 
Chaque famille peut développer des capacités pour mieux survivre.  

Des animaux mangent des plantes qui se nourrissent de l’eau et du soleil. Chaque entité peut transmettre ses gènes pour mieux survivre.

=====================
## Idée 1 : Simulation de construction de bâtiments selon contraintes
Potentiel (Henri) : 4/10  
Potentiel (Michel) : 7/10
▶ À quel problème répond-t-il ?   
Manque de logement  
▶ Originalité du projet. Que votre code ajoute à l'état de l’art ? 
?

## Idée 2 : Fabricateur de menus sains selon des préférences
Potentiel (Henri) : 6/10
Potentiel (Michel) : 8/10  
▶ À quel problème répond-t-il ?
Eviter l’obésité
Perte de poids
Mangez sain
▶ Originalité du projet. Que votre code ajoute à l'état de l’art ?   
Existe déjà mais souvent payant

## Idée 3 : Concevoir le meilleur réseau de transport selon des contraintes
Potentiel (Henri) : 7/10  
Potentiel (Michel) : ?/10  
▶ À quel problème répond-t-il ?  
Se déplacer plus rapidement  
Optimiser et réduire le coût des trajets  
▶ Originalité du projet. Que votre code ajoute à l'état de l’art ?   
Aucune idée

## Idée 4 : Simulation de voyage de drones
Potentiel (Henri) : 1/10  
Potentiel (Michel) : 0/10  
▶ À quel problème répond-t-il ?


▶ Originalité du projet. Que votre code ajoute à l'état de l’art ? 



## Idée 5 : Simulation de migration climatique
Potentiel (Henri) : 3/10  
Potentiel (Michel) : 4/10  
▶ À quel problème répond-t-il ?  
Comment des espèces agissent lorsque leur milieu a été trop modifié au point ou ils préfèrent migrer ?  
▶ Originalité du projet. Que votre code ajoute à l'état de l’art ?   
Vagues de méduse à la plage  
Oiseaux qui ont changé de continent  
Algo ? Aucune idée   

## Idée 6 : Simulation de propagation de virus
Potentiel (Henri) : 6/10  
Potentiel (Michel) : 7/10  
▶ À quel problème répond-t-il ?  
Comment un élément perturbateur peut se propager au sein d’un groupe  
▶ Originalité du projet. Que votre code ajoute à l'état de l’art ?   
Des algorithmes existent déjà  

## Idée 7 : 
