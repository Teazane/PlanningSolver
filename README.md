# Planning Solver
Planning Solver est un outil de résolution de contraintes pour établir un planning.

Il a été codé sous Windows, la plupart des commandes conseillées sont donc adaptées à PowerShell ou Cmd mais sont largement adaptables à un environnement Linux.

> Ce projet est en cours d'exploration en Python et en Prolog pour trouver la solution le plus appropriée.

## Sommaire
1. [Objectifs du projet](#objectifs-du-projet)
1. [Prérequis](#prérequis)
1. [Initialiser le projet](#initialiser-le-projet)
1. [Problèmes connus](#problèmes-connus)

## Objectifs du projet
L'objectif théorique de ce projet est de proposer une plate-forme de résolution de contraintes pour établir un planning en fonction des souhaits des différentes personnes impliquées, des activités proposées et des horaires possibles. 

L'objectif appliqué de ce projet est la résolution des problématiques de planning pour répartir des parties de jeux de rôles en fonction des joueureuses, des MJs, des parties proposées et des souhaits exprimés (parties désirées et moments de repos à inclure).

## Prérequis
- Une version de [Git](https://git-scm.com/downloads) installée.

### Pour l'implémentation en Prolog
[TODO]

### Pour l'implémentation en Python 
- Une version de [Python 3](https://www.python.org/downloads/) installée (préférentiellement 3.9).
Les autres dépendances sont listées dans "pyproject.toml", le fichier utilisé par Poetry pour gérer les bibliothèques.

## Initialiser le projet
1. Télécharger les fichiers sources avec `git clone https://github.com/Teazane/PlanningSolver.git`

### Pour l'implémentation en Prolog
[TODO]

### Pour l'implémentation en Python 
1. Installer Poetry avec la commande : `pip install poetry`
1. Créer l'environnement virtuel et installer les dépendences : `poetry install`

[TODO]

## Problèmes connus
Aucun problème connu à ce jour.

## Documentation
Ressources python-constraint : 
- https://stackabuse.com/constraint-programming-with-python-constraint/
- http://python-constraint.github.io/python-constraint/intro.html

Ressources Prolog : 
- https://fr.wikipedia.org/wiki/Prolog
