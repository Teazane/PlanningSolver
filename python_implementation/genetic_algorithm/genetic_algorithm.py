# Résolution du problème avec algorithme génétique

import json, random
from model import *
from pandas import DataFrame, Series, concat
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
            self.schedule_evaluation()
        elif not matrix and schedule:
            self.conversion_schedule_to_matrix()
            self.schedule_evaluation()
        elif matrix and not schedule:
            self.conversion_matrix_to_schedule()
            self.schedule_evaluation()
        else:
            raise Exception("Only one of matrix or schedule should be provided, or none of them.")
        
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
        return self.matrix
        
    def schedule_evaluation(self):
        """
        Evaluation of a generated (or submitted) schedule based on hard and soft constraints fulfillment. 
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

            # Vérifier les parties incompatibles
            for conflicting_game in game_rpg.conflicting_rpg:
                if conflicting_game in self.schedule.index:
                    conflicting_game_rpg = next(rpg for rpg in self.festival.proposed_rpgs if rpg.game_title == conflicting_game)
                    for player in players:
                        if self.schedule.loc[conflicting_game, player.name] == 1:
                            if player != game_rpg.dm and player != conflicting_game_rpg.dm:
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
        
        # Respect des créneaux préférentiels
        for index, row in self.schedule.iterrows():
            game = index
            try:
                game_rpg = next(rpg for rpg in self.festival.proposed_rpgs if rpg.game_title == game)
            except StopIteration:
                continue # Si la partie n'est pas censée exister, on passe à la ligne suivante de la matrice
            if game_rpg.best_moment:
                preferred_ts = [ts for ts in self.festival.time_slots if ts.moment == game_rpg.best_moment]
                if not any(row[ts.__str__()] == 1 for ts in preferred_ts):
                    soft_constraints_score -= 1 # TODO: voir si 1 est assez pénalisant
        
        # Calcul final du score
        score = -hard_constraints_violations * 1000 + soft_constraints_score # TODO voir si ce calcul final est assez souple
        self.evaluation_score = score
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
        return self.schedule

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
        games = json.loads(self.schedule)["games"]
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
        return self.matrix


class GeneticAlgorithm():
    """
    Implementation of all genetic algorithm's process.
    """

    def crossover(self, planning_1, planning_2):
        """
        Crossover between two planning schedules to generate a new schedule child.
        
        :param planning_1: Planning representing the first parent
        :param planning_2: Planning representing the second parent
        :type planning_1: genetic_algorithm.Planning
        :type planning_2: genetic_algorithm.Planning
        :return: DataFrame representing the child's schedule
        :rtype: pandas.Dataframe
        """
        # Assurez-vous que les parents ont la même structure
        assert planning_1.schedule.shape == planning_2.schedule.shape
        # Choisir un point de croisement aléatoire
        crossover_point = random.randint(1, planning_1.schedule.shape[0] - 1)
        # Créer l'enfant en combinant les parents
        child = concat([planning_1.schedule.iloc[:crossover_point], planning_2.schedule.iloc[crossover_point:]], axis=0)
        return child
    
    def mutate(self, schedule, festival, mutation_rate=0.1):
        """
        Create a mutation in a schedule.
        
        :param schedule: DataFrame representing the original schedule
        :param mutation_rate: Mutation rate (probability of mutation for each element)
        :type schedule: pandas.DataFrame
        :type mutation_rate: float
        :return: DataFrame representing the mutated schedule
        :rtype: pandas.DataFrame
        """
        mutated_schedule = schedule.copy()
        for index, row in mutated_schedule.iterrows():
            for col in row.index:
                if col not in festival.players and col not in festival.time_slots:
                    continue
                if random.random() < mutation_rate:
                    # Mutation pour les joueurs : inverser le statut de participation
                    if col in festival.players: # TODO : Vérifier que l'égalité peut se faire (typage)
                        mutated_schedule.at[index, col] = 1 - row[col]
                    # Mutation pour les créneaux horaires : activer ou désactiver la partie à ce créneau
                    if col in festival.time_slots: # TODO : Vérifier que l'égalité peut se faire (typage)
                        mutated_schedule.at[index, col] = 1 - row[col]
        return mutated_schedule
    
    def tournament_selection(self, population, k=3):
        """
        Select a parent by tournament method.
    
        :param population: Planning list
        :param k: Tournament size (default 3)
        :type population: genetic_algorithm.Planning
        :type k: integer
        :return: The best selected Planning
        :rtype: genetic_algorithm.Planning
        """
        random_selection = random.sample(population, k)
        # Tri en ordre décroissant pour que le meilleur score soit en premier
        sorted_selection = sorted(random_selection, key=lambda x: x.evaluation_score, reverse=True)
        return sorted_selection[0]

    def generate_children(self, festival, parents, mutation_rate):
        """
        Crée une nouvelle génération de plannings.
        
        :param festival: Festival information
        :param population: Planning list
        :param mutation_rate: Mutation rate (probability of mutation for each element in the planning schedule)
        :type festival: model.Festival
        :type population: list(genetic_algorithm.Planning)
        :type mutation_rate: integer
        :return: New generation planning list
        :rtype: list(genetic_algorithm.Planning)
        """
        new_population = []
        size = len(parents)
        for _ in range(size // 2):
            # Sélectionner les parents
            parent1 = self.tournament_selection(parents)
            parent2 = self.tournament_selection(parents)
            # Croisement
            child1 = self.crossover(parent1, parent2)
            child2 = self.crossover(parent2, parent1)
            # Mutation
            child1 = self.mutate(child1, mutation_rate)
            child2 = self.mutate(child2, mutation_rate)
            # Ajout des enfants à la nouvelle génération
            new_population.extend([Planning(festival, child1), Planning(festival, child2)])
        return new_population

    def complete_process_run(self, festival, population_number, generations_number, mutation_rate=0.1):
        """
        Run a complete process of genetic algorithm

        :param festival: Festival information
        :param population_number: Initial population size
        :param generations_number: Number of iteration to generate new children with previous ancestors
        :param mutation_rate: Mutation rate (probability of mutation for each element in the planning schedule)
        :type festival: model.Festival
        :type population_number: integer
        :type generations_number: integer
        :type mutation_rate: float
        """
        population = []
        for individual in population_number:
            individual = Planning(festival=festival)
            population.append(individual)
        print("Initial generation :")
        for individual in population:
            print("\t Individual (score" + str(individual.evaluation_score) + ")")
            print("\t" + str(individual.schedule))  
        for round in range(generations_number):
            population = self.generate_children(festival, population, mutation_rate)
            print("Generation " + str(round+1) + " :")
            for individual in population:
                print("\t Individual (score" + str(individual.evaluation_score) + ")")
                print("\t" + str(individual.schedule))
