"""
Syntaxe classique de problème via python-constraints :

problem = Problem()
problem.addVariables(["a", "b"], [1, 2, 3])
problem.addConstraint(lambda a, b: b == a+1, ["a", "b"])
solutions = problem.getSolutions()
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