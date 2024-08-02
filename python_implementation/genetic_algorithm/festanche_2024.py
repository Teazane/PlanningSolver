"""
2e édition du Festanche, 2024
"""

from model import *
from genetic_algorithm import *

# --- Définition des créneaux horaires --- #
mercredi_soir = TimeSlot("mercredi", "soir")
jeudi_am = TimeSlot("jeudi", "am")
jeudi_soir = TimeSlot("jeudi", "soir")
vendredi_am = TimeSlot("vendredi", "am")
vendredi_soir = TimeSlot("vendredi", "soir")
samedi_am = TimeSlot("samedi", "am")
samedi_soir = TimeSlot("samedi", "soir")

# --- Définition des joueurs --- #
claire_le = Player("Claire Le.", [13, 10, 9, 6], [mercredi_soir, jeudi_am, jeudi_soir, vendredi_am, vendredi_soir, samedi_am, samedi_soir])
claire_li = Player("Claire Li.", [15, 14], [mercredi_soir, jeudi_am, jeudi_soir, vendredi_am, vendredi_soir, samedi_am, samedi_soir])
dimitri = Player("Dimitri", [], [])
julien = Player("Julien", [13, 9, 4], [mercredi_soir, jeudi_am, jeudi_soir, vendredi_am, vendredi_soir, samedi_am, samedi_soir])
lorraine = Player("Lorraine", [13, 8, 5, 4], [mercredi_soir, jeudi_am, jeudi_soir, vendredi_am, vendredi_soir, samedi_am, samedi_soir])
lucile = Player("Lucile", [], [mercredi_soir, jeudi_am, jeudi_soir, vendredi_am, vendredi_soir, samedi_am, samedi_soir])
marion = Player("Marion", [11, 7, 2], [mercredi_soir, jeudi_am, jeudi_soir, vendredi_am, vendredi_soir, samedi_am, samedi_soir])
morgane = Player("Morgane", [], [mercredi_soir, jeudi_am, jeudi_soir, vendredi_am, vendredi_soir, samedi_am, samedi_soir])
pierre = Player("Pierre", [], [mercredi_soir, jeudi_am, jeudi_soir, vendredi_am, vendredi_soir, samedi_am, samedi_soir])
remi = Player("Rémi", [], [mercredi_soir, jeudi_am, jeudi_soir, vendredi_am, vendredi_soir, samedi_am, samedi_soir])
sean = Player("Sean", [9, 8, 7, 6], [jeudi_am, jeudi_soir, vendredi_am, vendredi_soir, samedi_am, samedi_soir])
thomas = Player("Thomas", [10, 9, 7], [mercredi_soir, jeudi_am, jeudi_soir, vendredi_am, vendredi_soir, samedi_am, samedi_soir])
tom = Player("Tom", [10, 9], [mercredi_soir, jeudi_am, jeudi_soir, vendredi_am, vendredi_soir, samedi_am, samedi_soir])
yohan = Player("Yohan", [6, 1, 0], [mercredi_soir, jeudi_am, jeudi_soir, vendredi_am, vendredi_soir, samedi_am, samedi_soir])

# --- Définition des contraintes de MJ/parties --- #
# Parties proposées
stonebelow = ProposedRPG(claire_li, "Stonebelow", 3, 4, "soir")
vaesen = ProposedRPG(claire_li, "Le manoir aux curiosités", 4, 4)
veggie_patch = ProposedRPG(claire_li, "Panique au potager", 4, 6, "am")
ten_candles = ProposedRPG(lucile, "Ten Candles", 3, 6, "soir")
tftl = ProposedRPG(lucile, "Vacances d'été", 4, 5)
zombie = ProposedRPG(claire_le, "Chasse foraine", 4, 4)
bebop = ProposedRPG(yohan, "Smoke on the water", 4, 5)
lalaland = ProposedRPG(yohan, "Lalaland of the dead", 2, 5)
magical_girl = ProposedRPG(remi, "Magical date", 4, 6)
ryuutama = ProposedRPG(morgane, "Le dragon des merveilles", 3, 4, "am")
root = ProposedRPG(morgane, "De résine et de croc", 3, 4)
scion = ProposedRPG(tom, "Pour la ruine du panthéon", 4, 4)

# --- Définition des contraintes de joueurs --- #
# Parties demandées (choix exprimés)
# Voeux de Claire Le.
claire_le_wish_1 = Wish(claire_le, stonebelow, 2)
claire_le_wish_2 = Wish(claire_le, vaesen, 8)
claire_le_wish_3 = Wish(claire_le, veggie_patch, 15)
claire_le_wish_4 = Wish(claire_le, ten_candles, 3)
claire_le_wish_5 = Wish(claire_le, bebop, 4)
claire_le_wish_6 = Wish(claire_le, lalaland, 14)
claire_le_wish_7 = Wish(claire_le, tftl, 12)
claire_le_wish_8 = Wish(claire_le, magical_girl, 11)
claire_le_wish_9 = Wish(claire_le, ryuutama, 5)
claire_le_wish_10 = Wish(claire_le, root, 1)
claire_le_wish_11 = Wish(claire_le, scion, 0)
# Voeux de Claire Li.
claire_li_wish_1 = Wish(claire_li, ten_candles, -1)
claire_li_wish_2 = Wish(claire_li, zombie, 5)
claire_li_wish_3 = Wish(claire_li, bebop, 6)
claire_li_wish_4 = Wish(claire_li, lalaland, 8)
claire_li_wish_5 = Wish(claire_li, tftl, 11)
claire_li_wish_6 = Wish(claire_li, magical_girl, 7)
claire_li_wish_7 = Wish(claire_li, ryuutama, 12)
claire_li_wish_8 = Wish(claire_li, root, 9)
claire_li_wish_9 = Wish(claire_li, scion, 13)
# Voeux de Dimitri
# TODO
# Voeux de Julien
julien_wish_1 = Wish(julien, stonebelow, 15)
julien_wish_2 = Wish(julien, vaesen, 7)
julien_wish_3 = Wish(julien, veggie_patch, 2)
julien_wish_4 = Wish(julien, ten_candles, 6)
julien_wish_5 = Wish(julien, zombie, 5)
julien_wish_6 = Wish(julien, bebop, 12)
julien_wish_7 = Wish(julien, lalaland, 3)
julien_wish_8 = Wish(julien, tftl, 14)
julien_wish_9 = Wish(julien, magical_girl, 10)
julien_wish_10 = Wish(julien, ryuutama, 1)
julien_wish_11 = Wish(julien, root, 8)
julien_wish_12 = Wish(julien, scion, 11)
# Voeux de Lorraine
lorraine_wish_1 = Wish(lorraine, stonebelow, 14)
lorraine_wish_2 = Wish(lorraine, vaesen, 12)
lorraine_wish_3 = Wish(lorraine, veggie_patch, 11)
lorraine_wish_4 = Wish(lorraine, ten_candles, -1)
lorraine_wish_5 = Wish(lorraine, zombie, 2)
lorraine_wish_6 = Wish(lorraine, bebop, 7)
lorraine_wish_7 = Wish(lorraine, lalaland, 3)
lorraine_wish_8 = Wish(lorraine, tftl, 15)
lorraine_wish_9 = Wish(lorraine, magical_girl, 1)
lorraine_wish_10 = Wish(lorraine, ryuutama, 10)
lorraine_wish_11 = Wish(lorraine, root, 6)
lorraine_wish_12 = Wish(lorraine, scion, 9)
# Voeux de Lucile 
lucile_wish_1 = Wish(lucile, stonebelow, 15)
lucile_wish_2 = Wish(lucile, vaesen, 14)
lucile_wish_3 = Wish(lucile, veggie_patch, 12)
lucile_wish_4 = Wish(lucile, zombie, 11)
lucile_wish_5 = Wish(lucile, bebop, 10)
lucile_wish_6 = Wish(lucile, lalaland, 13)
lucile_wish_7 = Wish(lucile, magical_girl, 4)
lucile_wish_8 = Wish(lucile, ryuutama, 6)
lucile_wish_9 = Wish(lucile, root, 1)
lucile_wish_10 = Wish(lucile, scion, 7)
# Voeux de Marion
marion_wish_1 = Wish(marion, stonebelow, 9)
marion_wish_2 = Wish(marion, vaesen, 4)
marion_wish_3 = Wish(marion, veggie_patch, 15)
marion_wish_4 = Wish(marion, ten_candles, 13)
marion_wish_5 = Wish(marion, zombie, 8)
marion_wish_6 = Wish(marion, bebop, 5)
marion_wish_7 = Wish(marion, lalaland, 14)
marion_wish_8 = Wish(marion, tftl, 6)
marion_wish_9 = Wish(marion, magical_girl, 0)
marion_wish_10 = Wish(marion, ryuutama, 3)
marion_wish_11 = Wish(marion, root, 10)
marion_wish_12 = Wish(marion, scion, 12)
# Voeux de Morgane
# TODO
# Voeux de Pierre
pierre_wish_1 = Wish(pierre, stonebelow, 10)
pierre_wish_2 = Wish(pierre, vaesen, 11)
pierre_wish_3 = Wish(pierre, veggie_patch, 8)
pierre_wish_4 = Wish(pierre, ten_candles, 15)
pierre_wish_5 = Wish(pierre, zombie, 7)
pierre_wish_6 = Wish(pierre, bebop, 9)
pierre_wish_7 = Wish(pierre, lalaland, 6)
pierre_wish_8 = Wish(pierre, tftl, 14)
pierre_wish_9 = Wish(pierre, magical_girl, 5)
pierre_wish_10 = Wish(pierre, ryuutama, 4)
pierre_wish_11 = Wish(pierre, root, 13)
pierre_wish_12 = Wish(pierre, scion, 12)
# Voeux de Rémi
# TODO
# Voeux de Scean
sean_wish_1 = Wish(sean, stonebelow, 11)
sean_wish_2 = Wish(sean, vaesen, 10)
sean_wish_3 = Wish(sean, veggie_patch, -1)
sean_wish_4 = Wish(sean, ten_candles, -1)
sean_wish_5 = Wish(sean, zombie, 15)
sean_wish_6 = Wish(sean, bebop, 13)
sean_wish_7 = Wish(sean, lalaland, -1)
sean_wish_8 = Wish(sean, tftl, 14)
sean_wish_9 = Wish(sean, magical_girl, 12)
sean_wish_10 = Wish(sean, ryuutama, -1)
sean_wish_11 = Wish(sean, root, -1)
sean_wish_12 = Wish(sean, scion, -1)
# Voeux de Thomas
thomas_wish_1 = Wish(thomas, stonebelow, 13)
thomas_wish_2 = Wish(thomas, vaesen, 15)
thomas_wish_3 = Wish(thomas, veggie_patch, 3)
thomas_wish_4 = Wish(thomas, ten_candles, 12)
thomas_wish_5 = Wish(thomas, zombie, 5)
thomas_wish_6 = Wish(thomas, bebop, 8)
thomas_wish_7 = Wish(thomas, lalaland, 6)
thomas_wish_8 = Wish(thomas, tftl, 14)
thomas_wish_9 = Wish(thomas, magical_girl, 2)
thomas_wish_10 = Wish(thomas, ryuutama, 1)
thomas_wish_11 = Wish(thomas, root, 4)
thomas_wish_12 = Wish(thomas, scion, 11)
# Voeux de Tom
tom_wish_1 = Wish(tom, stonebelow, 3)
tom_wish_2 = Wish(tom, vaesen, 6)
tom_wish_3 = Wish(tom, veggie_patch, 14)
tom_wish_4 = Wish(tom, ten_candles, 12)
tom_wish_5 = Wish(tom, zombie, 2)
tom_wish_6 = Wish(tom, bebop, 13)
tom_wish_7 = Wish(tom, lalaland, 5)
tom_wish_8 = Wish(tom, tftl, 8)
tom_wish_9 = Wish(tom, magical_girl, 1)
tom_wish_10 = Wish(tom, ryuutama, 11)
tom_wish_11 = Wish(tom, root, 15)
# Voeux de Yohan
yohan_wish_1 = Wish(yohan, stonebelow, 9)
yohan_wish_2 = Wish(yohan, vaesen, 8)
yohan_wish_3 = Wish(yohan, veggie_patch, 10)
yohan_wish_4 = Wish(yohan, ten_candles, 7)
yohan_wish_5 = Wish(yohan, zombie, 15)
yohan_wish_6 = Wish(yohan, tftl, 14)
yohan_wish_7 = Wish(yohan, magical_girl, -1)
yohan_wish_8 = Wish(yohan, ryuutama, 11)
yohan_wish_9 = Wish(yohan, root, 13)
yohan_wish_10 = Wish(yohan, scion, 12)


# --- Définition du système complet --- #
festanche = Festival(
                [mercredi_soir, jeudi_am, jeudi_soir, vendredi_am, vendredi_soir, samedi_am, samedi_soir], 
                [claire_le, claire_li, dimitri, julien, lorraine, lucile, marion, morgane, pierre, remi, sean, thomas, tom, yohan],
                [stonebelow, vaesen, veggie_patch, ten_candles, zombie, bebop, lalaland, tftl, magical_girl, ryuutama, root, scion],
                [
                    claire_le_wish_1, claire_le_wish_2, claire_le_wish_3, claire_le_wish_4, claire_le_wish_5, claire_le_wish_6, claire_le_wish_7, claire_le_wish_8, claire_le_wish_9, claire_le_wish_10, claire_le_wish_11, 
                    claire_li_wish_1, claire_li_wish_2, claire_li_wish_3, claire_li_wish_4, claire_li_wish_5, claire_li_wish_6, claire_li_wish_7, claire_li_wish_8, claire_li_wish_9, 
                    julien_wish_1, julien_wish_2, julien_wish_3, julien_wish_4, julien_wish_5, julien_wish_6, julien_wish_7, julien_wish_8, julien_wish_9, julien_wish_10, julien_wish_11, julien_wish_12, 
                    lorraine_wish_1, lorraine_wish_2, lorraine_wish_3, lorraine_wish_4, lorraine_wish_5, lorraine_wish_6, lorraine_wish_7, lorraine_wish_8, lorraine_wish_9, lorraine_wish_10, lorraine_wish_11, lorraine_wish_12, 
                    lucile_wish_1, lucile_wish_2, lucile_wish_3, lucile_wish_4, lucile_wish_5, lucile_wish_6, lucile_wish_7, lucile_wish_8, lucile_wish_9, lucile_wish_10, 
                    marion_wish_1, marion_wish_2, marion_wish_3, marion_wish_4, marion_wish_5, marion_wish_6, marion_wish_7, marion_wish_8, marion_wish_9, marion_wish_10, marion_wish_11, marion_wish_12, 
                    pierre_wish_1, pierre_wish_2, pierre_wish_3, pierre_wish_4, pierre_wish_5, pierre_wish_6, pierre_wish_7, pierre_wish_8, pierre_wish_9, pierre_wish_10, pierre_wish_11, pierre_wish_12, 
                    sean_wish_1, sean_wish_2, sean_wish_3, sean_wish_4, sean_wish_5, sean_wish_6, sean_wish_7, sean_wish_8, sean_wish_9, sean_wish_10, sean_wish_11, sean_wish_12, 
                    thomas_wish_1, thomas_wish_2, thomas_wish_3, thomas_wish_4, thomas_wish_5, thomas_wish_6, thomas_wish_7, thomas_wish_8, thomas_wish_9, thomas_wish_10, thomas_wish_11, thomas_wish_12, 
                    tom_wish_1, tom_wish_2, tom_wish_3, tom_wish_4, tom_wish_5, tom_wish_6, tom_wish_7, tom_wish_8, tom_wish_9, tom_wish_10, tom_wish_11, 
                    yohan_wish_1, yohan_wish_2, yohan_wish_3, yohan_wish_4, yohan_wish_5, yohan_wish_6, yohan_wish_7, yohan_wish_8, yohan_wish_9, yohan_wish_10
                ]
            )

# Test de l'objet Planning
planning = Planning(festanche)
print(planning.schedule)
planning.schedule_evaluation()
print(planning.evaluation_score)