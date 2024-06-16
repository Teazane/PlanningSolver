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
        # TODO
        pass

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