# Bactérie et Virus

Biologiquement les bactéries (B) et virus (V) sont très différentes :
- Les bactéries sont des organismes vivants (mangent, respirent, autonome)
- Les virus ne le sont pas (besoin d'un hôte pour se reproduire)

## ... Et modèles mathématiques

A l'état de l'art actuel, le modèle SIR est le plus utilisé pour simuler des épidémies. Or, celui-ci ne fait pas de distinction entre virus et bactérie, il utilise pour cela le `taux de transmission` et le `taux de guérison`.

https://fr.wikipedia.org/wiki/Mod%C3%A8les_compartimentaux_en_%C3%A9pid%C3%A9miologie

Pour modéliser les virus et bactéries séparemment, il faudra ajouter d'autres compartiments.