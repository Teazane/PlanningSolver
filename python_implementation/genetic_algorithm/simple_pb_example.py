"""
Example pour simplfier le pb : 

Nous disposons d'une journée pour jouer, un samedi.
Il y a donc deux créneaux de jeux : 
- samedi après-midi
- samedi soir

Il y a 10 joueurs : 
- Alice : voudrait jouer à D&D ou Scion.
- Bob : voudrait jouer à Alien ou Scion.
- Clément : voudrait jouer à Scion ou Alien.
- David : voudrait jouer à Alien ou Scion.
- Emilie : Voudrait jouer à Ryuutama ou D&D.
- Fanny : Voudrait jouer à Ryuutama ou Scion.
- Godric : Voudrait jouer à Scion ou D&D.
- Hermione : Voudrait jouer à Ryuutama et avoir une pause.
- Ingrid : Voudrait jouer à Alien et avoir une pause.
- Joe : Voudrait jouer à D&D et avoir une pause. 

Il y a quatre parties de proposées : 
- Alice en propose une, à 4 joueurs, le soir : Alien RPG.
- David en propose deux, une de 4 à 5 joueurs, une de 4 à 6 joueurs, peu importe quand : Ryuutama et D&D.
- Fanny en propose une de 4 à 5 joueurs, peu importe quand : Scion.
"""

from model import *
from genetic_algorithm import *

# --- Définition des créneaux horaires --- #
samedi_am = TimeSlot("samedi", "am")
samedi_soir = TimeSlot("samedi", "soir")

# --- Définition des joueurs --- #
alice = Player("Alice", [], [samedi_am, samedi_soir])
bob = Player("Bob", [], [samedi_am, samedi_soir])
clement = Player("Clément", [], [samedi_am, samedi_soir])
david = Player("David", [], [samedi_am, samedi_soir])
emilie = Player("Emilie", [], [samedi_am, samedi_soir])
fanny = Player("Fanny", [], [samedi_am, samedi_soir])
godric = Player("Godric", [], [samedi_am, samedi_soir])
hermione = Player("Hermione", [2], [samedi_am, samedi_soir])
ingrid = Player("Ingrid", [1], [samedi_am, samedi_soir])
joe = Player("Joe", [2], [samedi_am, samedi_soir])

# --- Définition des contraintes de MJ/parties --- #
# Parties proposées
alien = ProposedRPG(alice, "Alien RPG", 4, 4, "soir")
ryuutama = ProposedRPG(david, "Ryuutama", 4, 5)
dnd = ProposedRPG(david, "D&D", 4, 6)
scion = ProposedRPG(fanny, "Scion", 4, 5)

# --- Définition des contraintes de joueurs --- #
# Parties demandées (choix exprimés)
alice_wish_1 = Wish(alice, dnd, 1)
alice_wish_2 = Wish(alice, scion, 2)
bob_wish_1 = Wish(bob, alien, 1)
bob_wish_2 = Wish(bob, scion, 2)
clement_wish_1 = Wish(clement, scion, 1)
clement_wish_2 = Wish(clement, alien, 2)
david_wish_1 = Wish(david, alien, 1)
david_wish_2 = Wish(david, scion, 2)
emilie_wish_1 = Wish(emilie, ryuutama, 1)
emilie_wish_2 = Wish(emilie, dnd, 2)
fanny_wish_1 = Wish(fanny, ryuutama, 1)
fanny_wish_2 = Wish(fanny, scion, 2)
godric_wish_1 = Wish(godric, scion, 1)
godric_wish_2 = Wish(godric, dnd, 2)
hermione_wish_1 = Wish(hermione, ryuutama, 1)
ingrid_wish_1 = Wish(ingrid, alien, 2)
joe_wish_2 = Wish(joe, dnd, 1)

# --- Définition du système complet --- #
festanche = Festival(
                [samedi_am, samedi_soir], 
                [alice, bob, clement, david, emilie, fanny, godric, hermione, ingrid, joe],
                [alien, ryuutama, dnd, scion],
                [
                    alice_wish_1, 
                    alice_wish_2, 
                    bob_wish_1, 
                    bob_wish_2, 
                    clement_wish_1, 
                    clement_wish_2, 
                    david_wish_1, 
                    david_wish_2, 
                    emilie_wish_1, 
                    emilie_wish_2, 
                    fanny_wish_1, 
                    fanny_wish_2, 
                    godric_wish_1, 
                    godric_wish_2, 
                    hermione_wish_1, 
                    ingrid_wish_1, 
                    joe_wish_2 
                ]
            )

# # Tests d'affichage
# print(festanche) # <model.Festival object at 0x0000021A0FD56760>
# print(repr(alice)) # Player(Alice, [], [TimeSlot(samedi, am), TimeSlot(samedi, soir)])
# print(str(alice)) # Alice
# print(samedi_am) # samedi am

planning = Planning(festanche)
print(planning.matrix)