# Résolution du problème avec algorithme génétique
import json, random, time, logging, pathlib, sys
import logging.handlers
from model import *
from pandas import DataFrame, Series, concat
import numpy as np

# Define MESSAGE log level
DEBUG_EVAL = 9
logging.DEBUG_EVAL = DEBUG_EVAL
logging.addLevelName(DEBUG_EVAL, 'DEBUG EVAL')

class MyLogger(logging.Logger):
    def debug_eval(self, msg, *args, **kwargs):
        self.log(DEBUG_EVAL, msg, *args, **kwargs) 

logging.setLoggerClass(MyLogger)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
cmd_output = logging.StreamHandler(sys.stdout) # Log en console
cmd_output.setLevel(logging.DEBUG)
cmd_output.setFormatter(formatter)
logger.addHandler(cmd_output)
log_filepath = pathlib.Path(__file__).parent.parent.parent / 'log' / "genetic_algorithm.log"
file_output = logging.handlers.TimedRotatingFileHandler(filename=log_filepath.resolve(), encoding="utf-8")
file_output.setLevel(logging.DEBUG)
file_output.setFormatter(formatter)
logger.addHandler(file_output)

class Planning():
    hard_constraints_time = 0
    soft_constraints_time = 0
    temp1 = 0
    temp2 = 0

    def __init__(self, festival, schedule=None, json_string_schedule=None):
        """
        Initialization of the Planning object.

        It takes a model.Festival object then build the rest of the attributes.
        If the schedule is not supplied, from pandas.DataFrame or JSON string object, a new one is generated.
        The supplied or generated schedule is then evaluated.
        """
        self.festival = festival
        self.schedule = schedule
        self.json_string_schedule = json_string_schedule
        self.evaluation_score = 0
        if schedule is None and json_string_schedule is None:
            # self.generate_schedule()
            self.generate_heuristic_schedule()
            self.schedule_evaluation()
            # self.conversion_df_schedule_to_json_string_schedule()
        elif schedule is None and json_string_schedule is not None:
            self.conversion_json_string_schedule_to_df_schedule()
            self.schedule_evaluation()
        elif schedule is not None and json_string_schedule is None:
            self.schedule_evaluation()
            # self.conversion_df_schedule_to_json_string_schedule()
        else:
            raise Exception("Only one of DataFrame schedule or JSON string schedule should be provided, or none of them.")
        
    def generate_schedule(self):
        """
        Generate a pandas.DataFrame format schedule where columns are players and time slots, and lines are proposed RPG.
        
        For example:
            - Players are: Alice, Bob and Chris.
            - Time slots are: saturday afternoon, saturday night and sunday afternoon.
            - Proposed RPG are: D&D, Alien and MYZ.
        
        So the generated schedule will look like: 
                | Alice | Bob   | Chris | sat. a. | sat. n. | sun. a. |
        D&D     | NaN   | NaN   | NaN   | NaN     | NaN     | NaN     |
        Alien   | Nan   | NaN   | NaN   | NaN     | NaN     | NaN     |
        MYZ     | Nan   | NaN   | NaN   | NaN     | NaN     | NaN     |
        
        Then, random boolean values are generated to fill the schedule.
        
        For example, in the previous schedule, it could give: 
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
        self.schedule = DataFrame(data=data, index=self.festival.proposed_rpgs, columns=columns)
        return self.schedule
    
    def generate_heuristic_schedule(self):
        """
        Generate a pandas.DataFrame format schedule where columns are players and time slots, and lines are proposed RPG.
        
        For example:
            - Players are: Alice, Bob and Chris.
            - Time slots are: saturday afternoon, saturday night and sunday afternoon.
            - Proposed RPG are: D&D, Alien and MYZ.
        
        So the generated schedule will look like: 
                | Alice | Bob   | Chris | sat. a. | sat. n. | sun. a. |
        D&D     | NaN   | NaN   | NaN   | NaN     | NaN     | NaN     |
        Alien   | Nan   | NaN   | NaN   | NaN     | NaN     | NaN     |
        MYZ     | Nan   | NaN   | NaN   | NaN     | NaN     | NaN     |
        
        Then, random boolean values are generated to fill the schedule.
        
        For example, in the previous schedule, it could give: 
                | Alice | Bob   | Chris | sat. a. | sat. n. | sun. a. |
        D&D     | 1     | 0     | 0     | 1       | 0       | 1       |
        Alien   | 1     | 1     | 0     | 0       | 1       | 0       |
        MYZ     | 1     | 0     | 1     | 1       | 0       | 0       |

        The generation is pseudo random as we try to fill some priority constraints:
            - Players and MJ availabilities
            - MJ presence
            - Unique time_slot for a single game
            - Only one game at a time for each player
        """
        # Initialisation
        # On met les players et time_slots en guise de colonnes (en string pour une liste homogène)
        columns = []
        for player in self.festival.players:
            columns.append(str(player))
        for time_slot in self.festival.time_slots:
            columns.append(str(time_slot))
        # On génère des données = 0
        data = np.zeros((len(self.festival.proposed_rpgs), len(columns)), dtype=int)
        # On crée le dataframe avec en index les noms de parties
        self.schedule = DataFrame(data=data, index=self.festival.proposed_rpgs, columns=columns)

        # Remplissage pseudo-aléatoire
        for rpg in self.festival.proposed_rpgs:
            # Sélection aléatoire d'un créneau horaire où le MJ est disponible
            available_timeslots = [ts for ts in self.festival.time_slots if ts in rpg.dm.availabilities]
            if not available_timeslots:
                logger.error(rpg.dm.name + " is never available")
                continue  # Si aucun créneau disponible pour le MJ, ignorer cette partie
            timeslot = random.choice(available_timeslots)
            # On met un 1 dans la colonne du time_slot sélectionné au hasard et dans la colonne du MJ
            self.schedule.loc[rpg, str(timeslot)] = 1
            self.schedule.loc[rpg, str(rpg.dm)] = 1
            
            # On mélange la liste de souhaits pour ajouter de l'aléatoire
            random.shuffle(self.festival.wishes) 
            # On choisit un nombre cohérent mais aléatoire de joueurs
            nb_of_players = random.randint(rpg.player_nb_min, rpg.player_nb_max)
            assigned_players = 0
            # Assigner les joueurs disponibles
            for wish in self.festival.wishes:
                # Vérifier si le joueur ne veut pas participer à cette partie (wish_rank == -1)
                if wish.wish_rank == -1:
                    continue  # Ignorer ce joueur pour cette partie
                if wish.player != rpg.dm and timeslot in wish.player.availabilities:
                    # Vérifier si le joueur est déjà assigné à une autre partie à ce créneau
                    if not self._is_player_assigned(wish.player, timeslot):
                        self.schedule.loc[rpg, str(wish.player)] = 1
                        assigned_players += 1
                        if assigned_players >= nb_of_players:
                            break

            # Vérifier si le nombre minimal de joueurs est atteint
            if assigned_players < rpg.player_nb_min:
                self.schedule.loc[rpg] = 0  # Annuler la partie si le minimum de joueurs n'est pas atteint

        return self.schedule

    def _is_player_assigned(self, player, timeslot):
        """
        Check if the player is already assigned to another game at the same timeslot.
        """
        player_col = str(player)
        timeslot_col = str(timeslot)
        
        # Création d'un masque pour trouver les lignes où le joueur et le créneau horaire sont tous les deux assignés
        player_assigned_mask = self.schedule[player_col] == 1
        timeslot_assigned_mask = self.schedule[timeslot_col] == 1
        
        # Application des masques pour compter les lignes correspondantes
        assigned_count = self.schedule[player_assigned_mask & timeslot_assigned_mask].shape[0]
        
        return assigned_count > 0
        
    def schedule_evaluation(self):
        """
        Evaluation of a generated (or submitted) schedule based on hard and soft constraints fulfillment. 
        """
        score = 0
        hard_constraints_violations = 0
        soft_constraints_score = 0
        # --- Contraintes dures
        hard_constraints_start = time.perf_counter()
        for index, row in self.schedule.iterrows():
            game = index
            # Si toutes les colonnes sont égales à 0
            if (self.schedule.loc[game] == 0).all():
                # La partie n'est pas jouée, pas de violation de contrainte forte 
                logger.debug_eval("Game " + str(game) + " is not played")
                continue
            else:
                # On retrouve la partie parmi les parties proposées
                try:
                    game_rpg = next(rpg for rpg in self.festival.proposed_rpgs if rpg.game_title == game.game_title)
                except StopIteration:
                    logger.error("Game not found: " + game.game_title)
                    continue # Si la partie n'est pas censée exister, on passe à la ligne suivante de la matrice
                players = [player for player in self.festival.players if row[player.name] == 1]
                timeslots = [timeslot for timeslot in self.festival.time_slots if row[str(timeslot)] == 1]

                logger.debug_eval("Hard constraints : game : " + str(game))
                # Vérifier que le MJ est présent
                if row[game_rpg.dm.name] != 1:
                    hard_constraints_violations += 1
                    logger.debug_eval("- Absent MJ " + str(game_rpg.dm))

                # Vérifier le nombre de joueurs (sans compter le MJ)
                if not (game_rpg.player_nb_min <= len(players) - 1 <= game_rpg.player_nb_max):
                    hard_constraints_violations += 1
                    logger.debug_eval("- Bad player count " + str(len(players)))

                for player in players:
                    # Vérifier les disponibilités des joueurs et MJ
                    if not any(row[ts.__str__()] == 1 for ts in player.availabilities):
                        hard_constraints_violations += 1
                        logger.debug_eval("- Player not present " + str(player))

                    # Vérifier que chaque joueur n'a pas plusieurs parties en même temps
                    for timeslot in timeslots:
                        for game2 in self.schedule.index:
                            if(game2.game_title != game.game_title and self.schedule.loc[game2, str(timeslot)] == 1 and self.schedule.loc[game2, player.name] == 1):
                                hard_constraints_violations += 1
                                logger.debug_eval("- Player play something else " + str(player) + " " + str(game2))


                    # Vérifier les parties incompatibles
                    for conflicting_game in game_rpg.conflicting_rpg:
                        conflicting_game_rpg = next(rpg for rpg in self.festival.proposed_rpgs if rpg.game_title == conflicting_game.game_title)
                        if self.schedule.loc[conflicting_game.game_title, player.name] == 1:
                            if player != game_rpg.dm and player != conflicting_game_rpg.dm:
                                hard_constraints_violations += 1
                                logger.debug_eval("- Conflicting game " + str(player) + " " + str(conflicting_game))

                    # Vérifier qu'aucun joueur n'est dans une partie notée à -1
                    player_wishes = [wish for wish in self.festival.wishes if (wish.player == player and wish.proposed_rpg == game)]
                    for wish in player_wishes:
                        if wish.wish_rank == -1:
                            hard_constraints_violations += 1
                            logger.debug_eval("- Player " + str(player) + " would rather run naked in the woods than play " + str(game))

                # Vérifier qu'une partie ne se déroule que sur un seul créneau
                num_timeslots = len(timeslots)
                if num_timeslots != 1:
                    hard_constraints_violations += 1
                    logger.debug_eval("- Bad number of timeslot " + str(num_timeslots))

        Planning.hard_constraints_time += time.perf_counter() - hard_constraints_start

        soft_constraints_start = time.perf_counter()
        # --- Contraintes faibles
        for player in self.festival.players:
            logger.debug_eval("Soft constraints : player : " + str(player))
            # Calcul du contentement des joueurs de leurs parties attribuées
            player_wishes = [wish for wish in self.festival.wishes if wish.player == player]
            total_wish = 0
            for wish in player_wishes:
                wished_game = wish.proposed_rpg
                if self.schedule.loc[wished_game, player.name] == 1:
                    soft_constraints_score += wish.wish_rank
                    total_wish += wish.wish_rank
            logger.debug_eval("- Total game score " + str(total_wish))

            # Moments de pause
            played_games = self.schedule.loc[:, player.name]
            obtained_pauses = len(player.availabilities) - sum(played_games)
            sorted_pause_wishes = sorted(player.pause_wishes, reverse=True)
            total_pauses = 0
            for i in range(obtained_pauses):
                if i < len(sorted_pause_wishes):
                    soft_constraints_score += sorted_pause_wishes[i]
                    total_pauses += sorted_pause_wishes[i]
                else:
                    # Pénaliser les pauses supplémentaires non souhaitées
                    soft_constraints_score -= 1 # TODO: voir si 1 est assez pénalisant
                    total_pauses -= 1
            logger.debug_eval("- Total pause score " + str(total_pauses) + " (" + str(obtained_pauses) + ")")
        
        # Respect des créneaux préférentiels
        for index, row in self.schedule.iterrows():
            game = index
            try:
                game_rpg = next(rpg for rpg in self.festival.proposed_rpgs if rpg.game_title == game.game_title)
            except StopIteration:
                logger.debug_eval("Game not found: " + game.game_title)
                continue # Si la partie n'est pas censée exister, on passe à la ligne suivante de la matrice
            logger.debug_eval("Soft constraints : game : " + str(game))
            total_game = 0
            if game_rpg.best_moment:
                preferred_ts = [ts for ts in self.festival.time_slots if ts.moment == game_rpg.best_moment]
                if not any(row[ts.__str__()] == 1 for ts in preferred_ts):
                    soft_constraints_score -= 1 # TODO: voir si 1 est assez pénalisant
                    total_game -= 1
            logger.debug_eval("- Total game timeslot score " + str(total_game))
        Planning.soft_constraints_time += time.perf_counter() - soft_constraints_start

        # Calcul final du score
        score = -hard_constraints_violations * 1000 + soft_constraints_score # TODO: voir si ce calcul final est assez souple
        self.evaluation_score = score
        return score

    def conversion_df_schedule_to_json_string_schedule(self):
        """
        Convert a pandas.DataFrame format schedule into a more readable JSON format.
        The schedule should be realistic (without any unsatisfied hard constraint) to be generated.
        If the schedule is not realistic, the generated JSON is empty.

        For example, if the DataFrame schedule is: 
                | Alice | Bob   | Chris | sat. a. | sat. n. | sun. a. |
        D&D     | 1     | 0     | 0     | 1       | 0       | 1       |
        Alien   | 1     | 1     | 0     | 0       | 1       | 0       |
        MYZ     | 1     | 0     | 1     | 1       | 0       | 0       |

        This DataFrame schedule is no realistic because D&D should not be played on saturday AND sunday afternoons.
        The JSON format will be: {"games":[]}

        But if the DataFrame schedule is: 
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
        if self.evaluation_score > 0: # TODO: vérifier qu'un planning non-cohérent a forcément un score de 0 ou moins
            games = []
            for game_name, row in self.schedule.iterrows():
                game_info = {"name": game_name, "players": [], "timeslot": None}
                for col in self.schedule.columns:
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

    def conversion_json_string_schedule_to_df_schedule(self):
        """
        Convert a JSON format schedule into a pandas.DataFrame format.
        The schedule should not be empty to be generated.
        If the JSON schedule is empty, the generated DataFrame schedule is None.

        For example, if the JSON format is:
        {"games":[
            { "name": "D&D", "players":["Alice", "Bob", "Chris"], "timeslot":"sun. a."},
            { "name": "Alien", "players":["Alice", "Bob"], "timeslot":"sat. n."},
            { "name": "MYZ", "players":["Alice", "Chris"], "timeslot":"sat. a."}
        ]}

        The DataFrame schedule will be: 
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
            self.schedule = df
        else:
            self.schedule = None
        return self.schedule


class GeneticAlgorithm():
    """
    Implementation of all genetic algorithm's process.
    """
    def __init__(self):
        self.initial_gen_time = 0
        self.selection_time = 0
        self.crosserover_time = 0
        self.mutatione_time = 0
        self.evaluation_time = 0
    
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
        crossover_point = random.randint(1, planning_1.schedule.shape[1] - 1)
        # Créer l'enfant en combinant les parents
        child = concat([planning_1.schedule.iloc[:, :crossover_point], planning_2.schedule.iloc[:, crossover_point:]], axis=1)
        return child
    
    def mutate(self, schedule, mutation_rate=0.1):
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
                rand = random.random()
                if rand < mutation_rate:
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
            start = time.perf_counter()
            parent1 = self.tournament_selection(parents)
            parent2 = self.tournament_selection(parents)
            self.selection_time += time.perf_counter() - start
            # Croisement
            start = time.perf_counter()
            child1 = self.crossover(parent1, parent2)
            child2 = self.crossover(parent2, parent1)
            self.crosserover_time +=  time.perf_counter() - start
            # Mutation
            start = time.perf_counter()
            child1 = self.mutate(child1, mutation_rate)
            child2 = self.mutate(child2, mutation_rate)
            self.mutatione_time += time.perf_counter() - start
            # Ajout des enfants à la nouvelle génération
            start = time.perf_counter()
            new_population.extend([Planning(festival, child1), Planning(festival, child2)])
            self.evaluation_time += time.perf_counter() - start
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
        logger.info('-------- Start --------')
        start_time = time.perf_counter()
        for _ in range(population_number):
            individual = Planning(festival=festival)
            population.append(individual)
        self.initial_gen_time = time.perf_counter() - start_time
        logger.info('Initial population generation over')
        for gen in range(generations_number):
            logger.debug('Generation: ' + str(gen))
            population = self.generate_children(festival, population, mutation_rate)
        population_sorted = sorted(population, key=lambda x: x.evaluation_score, reverse=True)
        logger.info('Best final planning:\n' + str(population_sorted[0].schedule))
        logger.info('Best final score: ' + str(population_sorted[0].evaluation_score))
        logger.info('Total execution time: ' + str(time.perf_counter() - start_time))
        logger.info('Initial gen time: ' + str(self.initial_gen_time))
        logger.info('Total selection time: ' + str(self.selection_time))
        logger.info('Total crossover time: ' + str(self.crosserover_time))
        logger.info('Total mutation time: ' + str(self.mutatione_time))
        logger.info('Total child evaluation time: ' + str(self.evaluation_time))
        logger.info('Total hard constraints time : ' + str(Planning.hard_constraints_time))
        logger.info('Total soft constraints time : ' + str(Planning.soft_constraints_time))
        logger.info('Temp 1 : ' + str(Planning.temp1))
        logger.info('Temp 2 : ' + str(Planning.temp2))
        logger.info('-------- End --------')


