# Planning Solver
Planning Solver est un outil de résolution de contraintes pour établir un planning.

Il a été codé sous Windows, la plupart des commandes conseillées sont donc adaptées à PowerShell ou Cmd mais sont largement adaptables à un environnement Linux.

> Ce projet est en cours d'exploration en Python et en Prolog pour trouver la solution le plus appropriée.

## Sommaire
1. [Objectifs du projet](#objectifs-du-projet)
1. [Prérequis](#prérequis)
1. [Initialiser le projet](#initialiser-le-projet)
1. [Problèmes connus](#problèmes-connus)
1. [Documentation](#documentation)

## Objectifs du projet
L'objectif théorique de ce projet est de proposer une plate-forme de résolution de contraintes pour établir un planning en fonction des souhaits des différentes personnes impliquées, des activités proposées et des horaires possibles. 

L'objectif appliqué de ce projet est la résolution des problématiques de planning pour répartir des parties de jeux de rôles en fonction des joueureuses, des MJs, des parties proposées et des souhaits exprimés (parties désirées et moments de repos à inclure).

### Définition du problème et contraintes à résoudre
Le planning est à constitué à l'occasion de la tenue d'un festival de jeu de rôle.

Définition de l'évènement : 
- Ce festival se déroule sur une succession de créneaux horaires de deux types : après-midi et soir.
- Plusieurs personnes y participent et peuvent prendre les rôles de joueureuse et/ou de MJ.
- Ces personnes ne sont pas forcément présentes sur l'intégralité des créneaux du festival. 
- Les MJ proposent des parties en indiquant notamment le nombre de joueureuses minimum et maximum pour que la partie soit jouable, et éventuellement un type de créneau préférentiel pour son jeu (après-midi ou soir). Toutes les parties proposées ne seront pas nécessairement toutes jouées.
- Les joueureuses expriment leurs préférences en classant les parties qu'iels voudraient jouer. Iels peuvent indiquer des parties qu'iels ne veulent au contraire pas du tout jouer (car déjà jouées antérieurement par exemple). 
- Les joueureuses expriment également leurs préférences concernant le nombre de moments de pause (c'est à dire des moments sans jouer) qu'iels souhaitent durant le festival.

Voici les différentes contraintes à appliquer au planning : 
1. Contraintes dures : 
    - Un.e joueureuse (ou un.e MJ) ne peut pas participer à deux parties en même temps.
    - Un.e joueureuse (ou un.e MJ) ne peut pas participer à une partie se déroulant sur un créneau horaire où iel n'est pas présent.
    - Un.e joueureuse ne peut pas participer deux fois à la même partie.
    - Un.e joueureuse ne peut pas participer à une partie qu'iel ne veut pas jouer.
    - Une partie ne peut pas être jouée sans son.a MJ pour la mener.
    - Une partie ne peut pas être jouée si elle n'obtient pas un nombre de joueureuses compris entre le minimum et le maximum exprimé par le.a MJ.
2. Contraintes faibles : 
    - Un.e joueureuse doit jouer les parties qu'iel préfère selon ses souhaits exprimés, dans la mesure du possible.
    - Un.e joueureuse doit obtenir des moments de pause selon ses souhaits exprimés, dans la mesure du possible.
    - Une partie de jeu de rôle doit se dérouler sur le type de créneau préférentiel exprimé (après-midi ou soir), dans la mesure du possible.
    - Si une partie est particulièrement demandée et que le.a MJ est d'accord, elle peut être proposée plusieurs fois pour satisfaire tout.es les joueureuses intéressé.es.

## Prérequis
- Une version de [Git](https://git-scm.com/downloads) installée.

### Pour l'implémentation en Prolog
[TODO]

### Pour l'implémentation en Python 
- Une version de [Python 3](https://www.python.org/downloads/) installée (préférentiellement 3.9).
Les autres dépendances sont listées dans "pyproject.toml", le fichier utilisé par [Poetry](https://python-poetry.org/docs/) pour gérer les bibliothèques.

## Initialiser le projet
1. Télécharger les fichiers sources avec `git clone https://github.com/Teazane/PlanningSolver.git`

### Pour l'implémentation en Prolog
[TODO]

### Pour l'implémentation en Python 
1. Installer [Poetry](https://python-poetry.org/docs/) avec la commande : `pip install poetry`
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
- https://pcaboche.developpez.com/article/prolog/presentation/

Ressources algorithme génétique : 
- https://www.alliot.fr/fgenetic.html.fr
- Appliqués à des problèmes de planning :
    - https://github.com/rayjasson98/Hybrid-Genetic-Algorithm-Simulated-Annealing-for-Presentation-Scheduling
    - https://www.codeproject.com/Articles/23111/Making-a-Class-Schedule-Using-a-Genetic-Algorithm
    - https://ichi.pro/fr/utilisation-d-algorithmes-genetiques-pour-planifier-les-horaires-43916892693120
