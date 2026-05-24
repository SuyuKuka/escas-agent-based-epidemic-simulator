# Intelligence distribuée

Intelligence distribuée (ou Swarm intelligence) désigne un phénomène qui se produit lorsqu'au sein d'une population, les individus suivent tous des règles locales à eux-mêmes et qui à travers l'effet de groupe, font émerger un comportement collectif complexe et "intelligent".

Ces règles sont généralement très simples :
- Aucun chef au sein du groupe
- Le comportement dépend des autres individus proches et de l'environnement

Exemples :
- Banc d'oiseaux, nid d'abeilles, colonie de fourmies

https://fr.wikipedia.org/wiki/Intelligence_distribu%C3%A9e

## Etat de l'art

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