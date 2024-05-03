# Définition des objets du problème

# Créneau horaire
class TimeSlot():
    def __init__(self, day, moment):
        self.day = day # Ex : Lundi
        self.moment = moment # Ex : Après-midi
        
class ProposedRPG():
    def __init__(self, mj, player_nb, game_title, best_moment=None):
        self.mj = mj # Player
        self.player_nb = player_nb # Ex : 4
        self.game_title = game_title # Ex : Alien - Hadley's Hope
        self.best_moment = best_moment # Ex : Après-midi
        
class Wish():
    def __init__(self, player, proposed_rpg, wish_rank):
        self.player = player # Player
        self.proposed_rpg = proposed_rpg # ProposedRPG
        self.wish_rank = wish_rank # Ex : 10
        
class Player():
    def __init__(self, name, pause_nb, availabilities=[]):
        self.name = name # Ex : Bob
        self.pause_nb = pause_nb # Liste de ranks pour avoir des pauses. Ex : [8, 2]
        self.availabilities = availabilities # TimeSlot list
        
    def add_availability(time_slot):
        self.availabilities.append(time_slot)
        
class Festival():
    def __init__(self, time_slots=[], players=[], wishes=[], proposed_rpg=[]):
        self.time_slots = time_slots # TimeSlot list
        self.players = players # Player list
        self.wishes = wishes # Wish list
        self.proposed_rpgs = proposed_rpg # ProposedRPG list
        
    class NotExistingError(Exception):
        pass
        
    def add_time_slot(self, time_slot):
        self.time_slots.append(time_slot)
        
    def add_player(self, player):
        self.players.append(player)
        
    def add_wish(self, wish):
        self.wishes.append(wish)
        
    def add_proposed_rpg(self, proposed_rpg):
        self.proposed_rpgs.append(proposed_rpg)
        
    def add_wished_pause(self, player, rank):
        if player in self.players:
            player.pause_nb.append(rank)
        else:
            raise NotExistingError("Player does not exist.")
