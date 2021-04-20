from .analysis_parent import Analysis
from game.game import Game
from game.helpers.constants import Constants
from game.models.domain_specific.dnn_genetic_evolution_ai_solver import (DNNGeneticEvolutionSolver,
                                                                         DNNGeneticEvolutionTrainer)


class GeneticAlgorithmAnalysis(Analysis):

    def __init__(self):
        super(GeneticAlgorithmAnalysis, self).__init__(analysis_name_str="deep_neural_net_genetic_evolution")
        self.width = 300
        self.height = 300
        self.fruit = 1
        self.chance = 0
        self.boost = 1

    def selection_rate_test(self):
        test_name = "Selection_Rate"

        for selection_rate in [0.01, 0.1, 0.5, 1.0]:
            ga_trainer = DNNGeneticEvolutionTrainer()
            ga_trainer.population_size = 100
            ga_trainer.selection_rate = selection_rate
            ga_trainer.mutation_rate = 0.01
            ga_trainer.move(ga_trainer.prepare_training_environment())

            game_model = DNNGeneticEvolutionSolver(test_name, selection_rate)
            Game(game_model,
                 fps=Constants.FPS,
                 pixel_size=Constants.PIXEL_SIZE,
                 screen_width=self.width,
                 screen_height=self.height,
                 navigation_bar_height=Constants.NAVIGATION_BAR_HEIGHT,
                 number_of_fruit=self.fruit,
                 special_chance=self.chance,
                 special_boost=self.boost)

        path = f"scores/{self.analysis_name_str}_" + test_name + ".csv"
        self._save_test_png(path, test_name, "selection rate", "score")

    def mutation_rate_test(self):
        test_name = "Mutation_Rate"

        for mutation_rate in [0.01, 0.1, 0.5, 1]:
            ga_trainer = DNNGeneticEvolutionTrainer()
            ga_trainer.population_size = 100
            ga_trainer.selection_rate = 0.01
            ga_trainer.mutation_rate = mutation_rate
            ga_trainer.move(ga_trainer.prepare_training_environment())

            game_model = DNNGeneticEvolutionSolver(test_name, mutation_rate)
            Game(game_model=game_model,
                 fps=Constants.FPS,
                 pixel_size=Constants.PIXEL_SIZE,
                 screen_width=self.width,
                 screen_height=self.height,
                 navigation_bar_height=Constants.NAVIGATION_BAR_HEIGHT,
                 number_of_fruit=self.fruit,
                 special_chance=self.chance,
                 special_boost=self.boost)

        path = f"scores/{self.analysis_name_str}_" + test_name + ".csv"
        self._save_test_png(path, test_name, "mutation rate", "score")

    def population_size_test(self):
        test_name = "Population_Size"

        for population_size in [10, 100, 500, 1000]:
            ga_trainer = DNNGeneticEvolutionTrainer()
            ga_trainer.population_size = population_size
            ga_trainer.selection_rate = 0.01
            ga_trainer.mutation_rate = 0.01
            ga_trainer.move(ga_trainer.prepare_training_environment())

            game_model = DNNGeneticEvolutionSolver(test_name, population_size)
            Game(game_model=game_model,
                 fps=Constants.FPS,
                 pixel_size=Constants.PIXEL_SIZE,
                 screen_width=self.width,
                 screen_height=self.height,
                 navigation_bar_height=Constants.NAVIGATION_BAR_HEIGHT,
                 number_of_fruit=self.fruit,
                 special_chance=self.chance,
                 special_boost=self.boost)

        path = f"scores/{self.analysis_name_str}_" + test_name + ".csv"
        self._save_test_png(path, test_name, "population size", "score")

    def screen_size_test(self):
        test_name = "Screen_Size"

        ga_trainer = DNNGeneticEvolutionTrainer()
        ga_trainer.population_size = 500
        ga_trainer.selection_rate = 0.01
        ga_trainer.mutation_rate = 0.01
        ga_trainer.move(ga_trainer.prepare_training_environment())

        for size in [300, 400, 500, 600]:
            game_model = DNNGeneticEvolutionSolver(test_name, size)
            Game(game_model=game_model,
                 fps=Constants.FPS,
                 pixel_size=Constants.PIXEL_SIZE,
                 screen_width=size,
                 screen_height=size,
                 navigation_bar_height=Constants.NAVIGATION_BAR_HEIGHT,
                 number_of_fruit=self.fruit,
                 special_chance=self.chance,
                 special_boost=self.boost)

        path = f"scores/{self.analysis_name_str}_" + test_name + ".csv"
        self._save_test_png(path, test_name, "screen size", "score")

    def fruit_boost_test(self):
        test_name = "Fruit_Boost"

        ga_trainer = DNNGeneticEvolutionTrainer()
        ga_trainer.population_size = 500
        ga_trainer.selection_rate = 0.01
        ga_trainer.mutation_rate = 0.01
        ga_trainer.move(ga_trainer.prepare_training_environment())

        for fruit in [8]:
            for boost in [1, 2, 4, 8]:
                game_model = DNNGeneticEvolutionSolver(test_name, boost)
                Game(game_model=game_model,
                     fps=Constants.FPS,
                     pixel_size=Constants.PIXEL_SIZE,
                     screen_width=self.width,
                     screen_height=self.height,
                     navigation_bar_height=Constants.NAVIGATION_BAR_HEIGHT,
                     number_of_fruit=fruit,
                     special_chance=1,
                     special_boost=boost)

        path = f"scores/{self.analysis_name_str}_" + test_name + ".csv"
        self._save_test_png2(path, test_name, "fruit boost", "score")

    def fruit_chance_test(self):
        test_name = "Fruit_Chance"

        ga_trainer = DNNGeneticEvolutionTrainer()
        ga_trainer.population_size = 500
        ga_trainer.selection_rate = 0.01
        ga_trainer.mutation_rate = 0.01
        ga_trainer.move(ga_trainer.prepare_training_environment())

        for fruit in [1]:
            for chance in [0, 0.2, 0.5, 0.8, 1]:
                game_model = DNNGeneticEvolutionSolver(test_name, chance)
                Game(game_model=game_model,
                     fps=Constants.FPS,
                     pixel_size=Constants.PIXEL_SIZE,
                     screen_width=self.width,
                     screen_height=self.height,
                     navigation_bar_height=Constants.NAVIGATION_BAR_HEIGHT,
                     number_of_fruit=fruit,
                     special_chance=chance,
                     special_boost=2)

        path = f"scores/{self.analysis_name_str}_" + test_name + ".csv"
        self._save_test_png2(path, test_name, "fruit chance", "score")
