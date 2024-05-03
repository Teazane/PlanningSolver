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

from model import *

# --- Définition des créneaux horaires --- #
samedi_am = TimeSlot("samedi", "am")
samedi_soir = TimeSlot("samedi", "soir")

# --- Définition des joueurs --- #
alice = Player("Alice", 0, [samedi_am, samedi_soir])
bob = Player("Bob", 0, [samedi_am, samedi_soir])
clement = Player("Clément", 0, [samedi_am, samedi_soir])
david = Player("David", 0, [samedi_am, samedi_soir])
emilie = Player("Emilie", 0, [samedi_am, samedi_soir])
fanny = Player("Fanny", 0, [samedi_am, samedi_soir])
godric = Player("Godric", 0, [samedi_am, samedi_soir])
hermione = Player("Hermione", 1, [samedi_am, samedi_soir])
ingrid = Player("Ingrid", 1, [samedi_am, samedi_soir])
joe = Player("Joe", 1, [samedi_am, samedi_soir])

# --- Définition des contraintes de MJ/parties --- #
# Parties proposées
alien = ProposedRPG(alice, 4, "Alien RPG", "soir")
ryuutama = ProposedRPG(david, 5, "Ryuutama")
dnd = ProposedRPG(david, 6, "D&D")
scion = ProposedRPG(fanny, 5, "Scion")

# --- Définition des contraintes de joueurs --- #
# Parties demandées (choix exprimés)
alice_wish_1 = Wish(alice, dnd, 0)
alice_wish_2 = Wish(alice, scion, 0)
bob_wish_1 = Wish(bob, alien, 0)
bob_wish_2 = Wish(bob, scion, 0)
clement_wish_1 = Wish(clement, scion, 0)
clement_wish_2 = Wish(clement, alien, 0)
david_wish_1 = Wish(david, alien, 0)
david_wish_2 = Wish(david, scion, 0)
emilie_wish_1 = Wish(emilie, ryuutama, 0)
emilie_wish_2 = Wish(emilie, dnd, 0)
fanny_wish_1 = Wish(fanny, ryuutama, 0)
fanny_wish_2 = Wish(fanny, scion, 0)
godric_wish_1 = Wish(godric, scion, 0)
godric_wish_2 = Wish(godric, dnd, 0)
hermione_wish_1 = Wish(hermione, ryuutama, 0)
ingrid_wish_1 = Wish(ingrid, alien, 0)
joe_wish_2 = Wish(joe, dnd, 0)

# --- Définition du système complet --- #
festanche = Festival(
                [samedi_am, samedi_soir], 
                [alice, bob, clement, david, emilie, fanny, godric, hermione, ingrid, joe],
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
                ],
                [alien, ryuutama, dnd, scion]
            )
