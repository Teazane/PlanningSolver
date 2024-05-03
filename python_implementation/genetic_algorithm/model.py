# Définition des objets du problème

# Créneau horaire
class TimeSlot():
    """
    Represents a time slot defined by:
        - A day (such as "monday"), which is a string object
        - A moment of the day (such as "afternoon"), which is a string object
    """
    def __init__(self, day, moment):
        self.day = day # Ex : Lundi
        self.moment = moment # Ex : Après-midi
        
    def __repr__(self):
        return f'TimeSlot({self.day}, {self.moment})'
    
    def __str__(self):
        return self.day + " " + self.moment
    
class Player():
    """
    Represents a player.
    It is defined by:
        - A name, which is a string object
        - A wished ranked pauses list, which is a list of integer objects (can be empty)
        - A availabilities list, which is a list of TimeSlot objects
    """
    def __init__(self, name, pause_wishes, availabilities):
        self.name = name # Ex : Bob
        self.pause_wishes = pause_wishes # Liste de notations pour avoir des pauses. Ex : [8, 2]
        self.availabilities = availabilities # TimeSlot list
        
    def __repr__(self):
        return f'Player({self.name}, {self.pause_wishes}, {self.availabilities})'
    
    def __str__(self):
        return self.name
        
    def add_availability(time_slot):
        self.availabilities.append(time_slot)

class ProposedRPG():
    """
    Represents a role-play game (RPG) proposed by a specific player.
    It is defined by:
        - A dungeon master (DM), which is a Player object
        - A game title, which is a string object
        - A min and a max player number, which are integer objects
        - An optional best moment to play (such as "afternoon"), which is a string object
    """
    def __init__(self, dm, game_title, player_nb_min, player_nb_max, best_moment=None):
        self.dm = dm # Player
        self.game_title = game_title # Ex : Alien - Hadley's Hope
        self.player_nb_min = player_nb_min # Ex : 4
        self.player_nb_max = player_nb_max # Ex : 5
        self.best_moment = best_moment # Ex : Après-midi
        
    def __repr__(self):
        return f'ProposedRPG({self.dm}, {self.game_title}, {player_nb_min}, {self.player_nb_max}, {self.best_moment})'
    
    def __str__(self):
        return self.game_title
        
class Wish():
    """
    Represents a player's wish for a specific proposed RPG.
    It is defined by:
        - A player, which is a Player object
        - A game they would like to play, which is a ProposedRPG object
        - A wish rank, which is a integer object
    """
    def __init__(self, player, proposed_rpg, wish_rank):
        self.player = player # Player
        self.proposed_rpg = proposed_rpg # ProposedRPG
        self.wish_rank = wish_rank # Ex : 10
        
    def __repr__(self):
        return f'Wish({self.player}, {self.proposed_rpg}, {self.wish_rank})'
        
class Festival():
    """
    Represents the festival itself.
    It is defined by:
        - A list of time slots, which is a list of TimeSlot objects
        - A list of players, which is a list of Player objects
        - A list of proposed RPG, which is a list of ProposedRPG objects
        - A list of players' wishes, which is a list of Wish objects
    """
    def __init__(self, time_slots=[], players=[], proposed_rpg=[], wishes=[]):
        self.time_slots = time_slots # TimeSlot list
        self.players = players # Player list
        self.proposed_rpgs = proposed_rpg # ProposedRPG list
        self.wishes = wishes # Wish list
        
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
            player.pause_wishes.append(rank)
        else:
            raise NotExistingError("Player does not exist.")
