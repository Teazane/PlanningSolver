# Résolution du problème avec algorithme génétique

from model import *
from pandas import DataFrame

class Planning():
    
    def __init__(self, festival):
        self.festival = festival
        self.matrix = None 
        self.generate_initial_matrix()
        
    def generate_initial_matrix(self):
        # Initialisation
        # On met les players et time_slots en guise de colonnes (en string pour une liste homogène)
        columns = []
        for player in self.festival.players:
            columns.append(str(player))
        for time_slot in self.festival.time_slots:
            columns.append(str(time_slot))
        # On crée le dataframe avec en index les noms de parties
        self.matrix = DataFrame(data=None, index=self.festival.proposed_rpgs, columns=columns)
        
    def planning_evaluation(self):
        # TODO
        pass
    
    def conversion_planning_to_matrix(self):
        # TODO
        pass
    
    def conversion_matrix_to_planning(self):
        # TODO
        pass