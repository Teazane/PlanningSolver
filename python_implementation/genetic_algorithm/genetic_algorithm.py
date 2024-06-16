# Résolution du problème avec algorithme génétique

import json
from model import *
from pandas import DataFrame, Series
import numpy as np

class Planning():
    def __init__(self, festival, matrix=None, schedule=None):
        self.festival = festival
        self.matrix = matrix
        self.schedule = schedule
        self.evaluation_score = 0
        if not matrix and not schedule:
            self.generate_matrix()
            self.conversion_matrix_to_schedule()
        elif not matrix and schedule:
            self.conversion_schedule_to_matrix()
            self.schedule_evaluation()
        elif matrix and not schedule:
            self.conversion_matrix_to_schedule()
        else:
            raise Exception("Only one of matrix or schedule should be provided.")
        
    def generate_matrix(self):
        """
        Generate a pandas.DataFrame matrix where columns are players and time slots, and lines are proposed RPG.
        
        For example:
            - Players are: Alice, Bob and Chris.
            - Time slots are: saturday afternoon, saturday night and sunday afternoon.
            - Proposed RPG are: D&D, Alien and MYZ.
        
        So the generated matrix will look like : 
                | Alice | Bob   | Chris | sat. a. | sat. n. | sun. a. |
        D&D     | NaN   | NaN   | NaN   | NaN     | NaN     | NaN     |
        Alien   | Nan   | NaN   | NaN   | NaN     | NaN     | NaN     |
        MYZ     | Nan   | NaN   | NaN   | NaN     | NaN     | NaN     |
        
        Then, random boolean values are generated to fill the matrix.
        
        For example, in the previous matrix, it could give: 
                | Alice | Bob   | Chris | sat. a. | sat. n. | sun. a. |
        D&D     | 1     | 0     | 0     | 1       | 0       | 1       |
        Alien   | 1     | 1     | 0     | 0       | 1       | 0       |
        MYZ     | 1     | 0     | 1     | 1       | 0       | 0       |
        """
        # Initialisation
        # On met les players et time_slots en guise de colonnes (en string pour une liste homogène)
        columns = []
        for player in self.festival.players:
            columns.append(str(player))
        for time_slot in self.festival.time_slots:
            columns.append(str(time_slot))
        # On génère des données aléatoires
        data = np.random.choice(a=[0, 1], size=(len(self.festival.proposed_rpgs), len(columns)))
        # On crée le dataframe avec en index les noms de parties
        self.matrix = DataFrame(data=data, index=self.festival.proposed_rpgs, columns=columns)
        
    def schedule_evaluation(self):
        """
        Evaluation of a generated (or submitted) schedule based on hard and soft constraints fulfillment. 

        Exemple d'utilisation:
        # Construire le festival et les objets associés
        time_slots = [TimeSlot("saturday", "afternoon"), TimeSlot("saturday", "night"), TimeSlot("sunday", "afternoon")]
        players = [Player("Alice", [2], [TimeSlot("saturday", "afternoon"), TimeSlot("saturday", "night")]), 
                Player("Bob", [2], [TimeSlot("saturday", "afternoon"), TimeSlot("saturday", "night")]), 
                Player("Chris", [1], [TimeSlot("sunday", "afternoon")])]
        proposed_rpgs = [ProposedRPG(players[0], "D&D", 2, 5, "afternoon"), 
                        ProposedRPG(players[1], "Alien", 2, 4, "night")]
        wishes = [Wish(players[0], proposed_rpgs[0], 10), Wish(players[1], proposed_rpgs[1], 8)]

        festival = Festival(time_slots, players, proposed_rpgs, wishes)

        # Construire un planning
        data = {
            "name": ["D&D", "Alien"],
            "Alice": [1, 1],
            "Bob": [1, 1],
            "Chris": [1, 0],
            "saturday afternoon": [0, 0],
            "saturday night": [0, 1],
            "sunday afternoon": [1, 0]
        }
        schedule = pd.DataFrame(data).set_index("name")

        # Évaluer le planning
        score = evaluate_schedule(schedule, festival)
        print("Score du planning:", score)
        """
        score = 0
        hard_constraints_violations = 0
        soft_constraints_score = 0
        
        # --- Contraintes dures
        for index, row in self.schedule.iterrows():
            game = index
            # On retrouve la partie parmis les parties proposées
            try:
                game_rpg = next(rpg for rpg in self.festival.proposed_rpgs if rpg.game_title == game)
            except StopIteration:
                continue # Si la partie n'est pas censée exister, on passe à la ligne suivante de la matrice
            players = [player for player in self.festival.players if row[player.name] == 1]

            # Vérifier que le MJ est présent
            if row[game_rpg.dm.name] != 1:
                hard_constraints_violations += 1

            # Vérifier le nombre de joueurs (sans compter le MJ)
            if not (game_rpg.player_nb_min <= len(players) - 1 <= game_rpg.player_nb_max):
                hard_constraints_violations += 1
            
            # Vérifier les disponibilités des joueurs et MJ
            for player in players:
                if not any(row[ts.__str__()] == 1 for ts in player.availabilities):
                    hard_constraints_violations += 1
            
            # Vérifier que chaque joueur n'a pas plusieurs parties en même temps
            for ts in self.festival.time_slots:
                ts_str = ts.__str__()
                if row[ts_str] == 1:
                    for player in players:
                        if self.schedule.loc[:, ts_str].sum() > 1:
                            hard_constraints_violations += 1

            # Vérifier qu'une partie ne se déroule que sur un seul créneau
            num_timeslots = sum(row[ts.__str__()] for ts in self.festival.time_slots)
            if num_timeslots != 1:
                hard_constraints_violations += 1
        
        # --- Contraintes faibles
        for player in self.festival.players:
            # Calcul du contentement des joueurs de leurs parties attribuées
            player_wishes = [wish for wish in self.festival.wishes if wish.player == player]
            for wish in player_wishes:
                game = wish.proposed_rpg.game_title
                if self.schedule.loc[game, player.name] == 1:
                    soft_constraints_score += wish.wish_rank
            
            # Moments de pause
            obtained_pauses = 0
            for ts in self.festival.time_slots:
                ts_str = ts.__str__()
                if self.schedule.loc[:, (player.name, ts_str)].sum() == 0:
                    obtained_pauses += 1
        
            sorted_pause_wishes = sorted(player.pause_wishes, reverse=True)
            for i in range(obtained_pauses):
                if i < len(sorted_pause_wishes):
                    soft_constraints_score += sorted_pause_wishes[i]
                else:
                    # Pénaliser les pauses supplémentaires non souhaitées
                    soft_constraints_score -= 1 # TODO: voir si 1 est assez pénalisant
        
        # TODO ----------- arrêt de la relecture ChatGPT, lire la fin de la méthode
        # Respect des créneaux préférentiels
        for index, row in self.schedule.iterrows():
            game = index
            game_rpg = next(rpg for rpg in self.festival.proposed_rpgs if rpg.game_title == game)
            if game_rpg.best_moment:
                preferred_ts = [ts for ts in self.festival.time_slots if ts.moment == game_rpg.best_moment]
                if not any(row[ts.__str__()] == 1 for ts in preferred_ts):
                    soft_constraints_score -= 1
        
        # Calcul final du score
        score = -hard_constraints_violations * 1000 + soft_constraints_score
        return score

    def conversion_matrix_to_schedule(self):
        """
        Convert a pandas.DataFrame matrix format schedule into a more readable JSON format.
        The schedule should be realistic (without any unsatisfied hard constraint) to be generated.
        If the schedule is not realistic, the generated JSON is empty.

        For example, if the matrix schedule is: 
                | Alice | Bob   | Chris | sat. a. | sat. n. | sun. a. |
        D&D     | 1     | 0     | 0     | 1       | 0       | 1       |
        Alien   | 1     | 1     | 0     | 0       | 1       | 0       |
        MYZ     | 1     | 0     | 1     | 1       | 0       | 0       |

        This matrix schedule is no realistic because D&D should not be played on saturday AND sunday afternoons.
        The JSON format will be: {"games":[]}

        But if the matrix schedule is: 
                | Alice | Bob   | Chris | sat. a. | sat. n. | sun. a. |
        D&D     | 1     | 1     | 1     | 0       | 0       | 1       |
        Alien   | 1     | 1     | 0     | 0       | 1       | 0       |
        MYZ     | 1     | 0     | 1     | 1       | 0       | 0       |

        The JSON format will be:
        {"games":[
            { "name": "D&D", "players":["Alice", "Bob", "Chris"], "timeslot":"sun. a."},
            { "name": "Alien", "players":["Alice", "Bob"], "timeslot":"sat. n."},
            { "name": "MYZ", "players":["Alice", "Chris"], "timeslot":"sat. a."}
        ]}
        """
        if self.schedule_evaluation() > 0:
            games = []
            for game_name, row in self.matrix.iterrows():
                game_info = {"name": game_name, "players": [], "timeslot": None}
                for col in self.matrix.columns:
                    if col.startswith(('sat.', 'sun.')): # TODO: vérifier de manière moins empirique
                        if row[col] == 1:
                            game_info["timeslot"] = col
                    else:
                        if row[col] == 1:
                            game_info["players"].append(col)
                games.append(game_info)
            self.schedule = json.dumps({"games": games})
        else:
            self.schedule = json.dumps({"games":[]})

    def conversion_schedule_to_matrix(self):
        """
        Convert a JSON format schedule into a pandas.DataFrame matrix format.
        The schedule should not be empty to be generated.
        If the schedule is empty, the generated matrix is None.

        For example, if the JSON format is:
        {"games":[
            { "name": "D&D", "players":["Alice", "Bob", "Chris"], "timeslot":"sun. a."},
            { "name": "Alien", "players":["Alice", "Bob"], "timeslot":"sat. n."},
            { "name": "MYZ", "players":["Alice", "Chris"], "timeslot":"sat. a."}
        ]}

        The matrix schedule will be: 
                | Alice | Bob   | Chris | sat. a. | sat. n. | sun. a. |
        D&D     | 1     | 1     | 1     | 0       | 0       | 1       |
        Alien   | 1     | 1     | 0     | 0       | 1       | 0       |
        MYZ     | 1     | 0     | 1     | 1       | 0       | 0       |
        """
        games = self.schedule["games"]
        if len(games) > 0:
            # Extraction des joueurs et créneaux horaires sans doublons
            players = set()
            timeslots = set()
            for game in games:
                players.update(game["players"])
                timeslots.add(game["timeslot"])
            # On met les players et time_slots en guise de colonnes
            columns = list(players) + list(timeslots)
            df = DataFrame(columns=columns)
            # On ajoute les données au DataFrame
            for game in games:
                row = {player: 0 for player in players}
                row.update({timeslot: 0 for timeslot in timeslots})
                for player in game["players"]:
                    row[player] = 1
                if game["timeslot"]:
                    row[game["timeslot"]] = 1
                df = df.append(Series(row, name=game["name"]))
            self.matrix = df
        else:
            self.matrix = None