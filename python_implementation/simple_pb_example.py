"""
Example pour simplfier le pb : 

Nous disposons d'une journée pour jouer, un samedi.
Il y a donc deux créneaux de jeux : 
- samedi après-midi
- samedi soir

Il y a 10 joueurs : 
- Alice : voudrait jouer à D&D ou Scion.
- Bob : voudrait jouer à Alien ou Scion.
- Clément : voudrait joueur à Scion ou Alien.
- David : voudrait jouer à Alien ou Scion.
- Emilie : Voudrait jouer à Ryuutama ou D&D.
- Fanny : Voudrait jouer à Ryuutama ou Scion.
- Godric : Voudrait jouer à Scion ou D&D.
- Hermione : Voudrait jouer à Ryuutama et avoir une pause.
- Ingrid : Voudrait jouer à Alien et avoir une pause.
- Joe : Voudrait jouer à D&D et avoir une pause. 

Il y a quatre parties de proposées : 
- Alice en propose une, à 4 joueurs, le soir : Alien RPG.
- David en propose deux, une à 5 joueurs, une à 6 joueurs, peu importe quand : Ryuutama et D&D.
- Fanny en propose une à 5 joueurs, peu importe quand : Scion.
"""

from constraint import *

planning = Problem()

# --- Définition des créneaux horaires --- #
# TODO

# --- Définition des contraintes de MJ/parties --- #
# Parties proposées
# TODO
# Préférences horaires (après-midi/soir)
# TODO

# --- Définition des contraintes de joueurs --- #
# Disponibilité (si certains joueurs ne sont pas présent tous les jours)
# TODO
# Parties demandées (choix exprimés)
# TODO
# Pauses demandées (nombre exprimé)
# TODO