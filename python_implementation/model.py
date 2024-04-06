# Définition des objets du problème

# Créneau horaire
class TimeSlot():
    def __init__(day, moment):
        self.day = day # Ex : Lundi
        self.moment = moment # Ex : Après-midi
        
class ProposedRPG():
    def __init__(best_moment, mj, player_nb, game_title):
        self.best_moment = best_moment # Ex : Après-midi
        self.mj = mj # Player
        self.player_nb = player_nb # Ex : 4
        self.game_title = game_title # Ex : Alien - Hadley's Hope
        
class Wish():
    def __init__(player, proposed_rpg, wish_rank):
        self.player = player # Player
        self.proposed_rpg = proposed_rpg # ProposedRPG
        self.wish_rank = wish_rank # Ex : 10
        
class Player():
    def __init__(name, pause_nb, availabilities):
        self.name = name # Ex : Bob
        self.pause_nb = pause_nb # Ex : 2
        self.availabilities = availabilities # TimeSlot list
        
class Festival():
    def __init__(time_slots, players, wishes, proposed_rpg):
        self.time_slots = time_slots # TimeSlot list
        self.players = players # Player list
        self.wishes = wishes # Wish list
        self.proposed_rpg = proposed_rpg # ProposedRPG list

