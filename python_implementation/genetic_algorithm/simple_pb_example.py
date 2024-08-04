"""
Exemple pour simplifier le pb : 

Nous disposons d'une journée pour jouer, un samedi.
Il y a donc deux créneaux de jeux : 
- samedi après-midi
- samedi soir

Il y a 10 joueurs ayant classé leurs voeux de 0 à 5 (dont les pauses) : 
Alice, Bob, Clément, David, Emilie, Fanny, Godric, Hermione, Ingrid, Joe.
Parmi ces joueurs, Hermione, Ingrid et Joe ont exprimé un ou deux choix de pauses.

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
emilie = Player("Emilie", [], [samedi_am])
fanny = Player("Fanny", [], [samedi_soir])
godric = Player("Godric", [], [samedi_am, samedi_soir])
hermione = Player("Hermione", [4], [samedi_am, samedi_soir])
ingrid = Player("Ingrid", [3], [samedi_am, samedi_soir])
joe = Player("Joe", [5, 2], [samedi_am, samedi_soir])

# --- Définition des contraintes de MJ/parties --- #
# Parties proposées
alien = ProposedRPG(alice, "Alien RPG", 4, 4, "soir")
ryuutama = ProposedRPG(david, "Ryuutama", 4, 5)
dnd = ProposedRPG(david, "D&D", 4, 6)
scion = ProposedRPG(fanny, "Scion", 4, 5)

# --- Définition des contraintes de joueurs --- #
# Parties demandées (choix exprimés)
alice_wish_1 = Wish(alice, dnd, 1)
alice_wish_2 = Wish(alice, ryuutama, 3)
alice_wish_3 = Wish(alice, scion, 5)
bob_wish_1 = Wish(bob, alien, 5)
bob_wish_2 = Wish(bob, ryuutama, 4)
bob_wish_3 = Wish(bob, dnd, 3)
bob_wish_4 = Wish(bob, scion, 0)
clement_wish_1 = Wish(clement, alien, -1)
clement_wish_2 = Wish(clement, ryuutama, 5)
clement_wish_3 = Wish(clement, dnd, 0)
clement_wish_4 = Wish(clement, scion, 4)
david_wish_1 = Wish(david, alien, 5)
david_wish_4 = Wish(david, scion, 3)
emilie_wish_1 = Wish(emilie, alien, 2)
emilie_wish_2 = Wish(emilie, ryuutama, -1)
emilie_wish_3 = Wish(emilie, dnd, 5)
emilie_wish_4 = Wish(emilie, scion, 3)
fanny_wish_1 = Wish(fanny, alien, 1)
fanny_wish_2 = Wish(fanny, ryuutama, 4)
fanny_wish_3 = Wish(fanny, dnd, 0)
godric_wish_1 = Wish(godric, alien, 3)
godric_wish_2 = Wish(godric, ryuutama, 1)
godric_wish_3 = Wish(godric, dnd, 5)
godric_wish_4 = Wish(godric, scion, 2)
hermione_wish_1 = Wish(hermione, alien, 5)
hermione_wish_2 = Wish(hermione, ryuutama, 3)
hermione_wish_3 = Wish(hermione, dnd, 1)
hermione_wish_4 = Wish(hermione, scion, 0)
ingrid_wish_1 = Wish(ingrid, alien, 0)
ingrid_wish_2 = Wish(ingrid, ryuutama, 2)
ingrid_wish_3 = Wish(ingrid, dnd, 5)
ingrid_wish_4 = Wish(ingrid, scion, 4)
joe_wish_1 = Wish(joe, alien, -1)
joe_wish_2 = Wish(joe, ryuutama, 4)
joe_wish_3 = Wish(joe, dnd, 3)
joe_wish_4 = Wish(joe, scion, 0)

# --- Définition du système complet --- #
festanche = Festival(
                [samedi_am, samedi_soir], 
                [alice, bob, clement, david, emilie, fanny, godric, hermione, ingrid, joe],
                [alien, ryuutama, dnd, scion],
                [
                    alice_wish_1, alice_wish_2, alice_wish_3, 
                    bob_wish_1, bob_wish_2, bob_wish_3, bob_wish_4, 
                    clement_wish_1, clement_wish_2, clement_wish_3, clement_wish_4, 
                    david_wish_1, david_wish_4, 
                    emilie_wish_1, emilie_wish_2, emilie_wish_3, emilie_wish_4, 
                    fanny_wish_1, fanny_wish_2, fanny_wish_3, 
                    godric_wish_1, godric_wish_2, godric_wish_3, godric_wish_4, 
                    hermione_wish_1, hermione_wish_2, hermione_wish_3, hermione_wish_4, 
                    ingrid_wish_1, ingrid_wish_2, ingrid_wish_3, ingrid_wish_4, 
                    joe_wish_1, joe_wish_2, joe_wish_3, joe_wish_4
                ]
            )

# # Tests d'affichage
# print(festanche) # <model.Festival object at 0x0000021A0FD56760>
# print(repr(alice)) # Player(Alice, [], [TimeSlot(samedi, am), TimeSlot(samedi, soir)])
# print(str(alice)) # Alice
# print(samedi_am) # samedi am

# # Test de l'objet Planning
# planning = Planning(festanche)
# print(planning.schedule)
# print(planning.evaluation_score)

# Test de l'algorithme
gen_a = GeneticAlgorithm()
gen_a.complete_process_run(festanche, 1000, 10)