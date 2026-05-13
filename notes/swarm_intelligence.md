# Swarm intelligence

Swarm intelligence systems consist typically of a population of simple agents or boids interacting locally with one another and with their environment.

The agents follow very simple rules, and although there is no centralized control structure dictating how individual agents should behave, local, and to a certain degree random, interactions between such agents lead to the emergence of "intelligent" global behavior, unknown to the individual agents.

Exemples d'algorithmes :
- Nid d'abeilles, colonie de fourmies

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