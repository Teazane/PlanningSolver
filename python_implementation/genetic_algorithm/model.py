# Définition des objets du problème

# Créneau horaire
class TimeSlot():
    def __init__(self, day, moment):
        self.day = day # Ex : Lundi
        self.moment = moment # Ex : Après-midi
        
    def __repr__(self):
        return f'TimeSlot({self.day}, {self.moment})'
    
    def __str__(self):
        return self.day + " " + self.moment
        
class ProposedRPG():
    def __init__(self, mj, game_title, player_nb, best_moment=None):
        self.mj = mj # Player
        self.game_title = game_title # Ex : Alien - Hadley's Hope
        self.player_nb = player_nb # Ex : 4
        self.best_moment = best_moment # Ex : Après-midi
        
    def __repr__(self):
        return f'ProposedRPG({self.mj}, {self.game_title}, {self.player_nb}, {self.best_moment})'
    
    def __str__(self):
        return self.game_title
        
class Wish():
    def __init__(self, player, proposed_rpg, wish_rank):
        self.player = player # Player
        self.proposed_rpg = proposed_rpg # ProposedRPG
        self.wish_rank = wish_rank # Ex : 10
        
    def __repr__(self):
        return f'Wish({self.player}, {self.proposed_rpg}, {self.wish_rank})'
        
class Player():
    def __init__(self, name, pause_nb, availabilities=[]):
        self.name = name # Ex : Bob
        self.pause_nb = pause_nb # Liste de ranks pour avoir des pauses. Ex : [8, 2]
        self.availabilities = availabilities # TimeSlot list
        
    def __repr__(self):
        return f'Player({self.name}, {self.pause_nb}, {self.availabilities})'
    
    def __str__(self):
        return self.name
        
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
        if (wish.player in self.players):
            if (wish.proposed_rpg in self.proposed_rpgs):
                self.wishes.append(wish) # TODO: check rank
            else:
                raise NotExistingError("RPG does not exist.")
        else:
            raise NotExistingError("Player does not exist.")
        
    def add_proposed_rpg(self, proposed_rpg):
        self.proposed_rpgs.append(proposed_rpg)
        
    def add_wished_pause(self, player, rank):
        if player in self.players:
            player.pause_nb.append(rank)
        else:
            raise NotExistingError("Player does not exist.")
