# Résolution du problème avec algorithme génétique

from model import *
from pandas import DataFrame
import numpy as np

class Planning():
    def __init__(self, festival):
        self.festival = festival
        self.matrix = None 
        self.generate_matrix()
        
    def generate_matrix(self):
        """
        Generate a matrix where columns are players and time slots, and lines are proposed RPG.
        
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
        
    def planning_evaluation(self):
        # TODO
        pass
    
    def conversion_planning_to_matrix(self):
        # TODO
        pass
    
    def conversion_matrix_to_planning(self):
        # TODO
        pass