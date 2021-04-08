import argparse
import random
import csv
import os
import matplotlib.pyplot as plt

from game.helpers.constants import Constants
from game.models.domain_specific.dnn_genetic_evolution_ai_solver import DNNGeneticEvolutionSolver, DNNGeneticEvolutionTrainer
from game.game import Game



def selection_rate_test():

    test_name = "Selection_Rate"

    # for selection_rate in [0.01, 0.1, 0.5, 1.0]:

        # ga_trainer = DNNGeneticEvolutionTrainer()
        # ga_trainer.population_size = 100
        # ga_trainer.selection_rate = selection_rate
        # ga_trainer.mutation_rate = 0.01
        # ga_trainer.move(ga_trainer.prepare_training_environment())

        # game_model=DNNGeneticEvolutionSolver(test_name, selection_rate)
        # Game(game_model,
        #     fps=Constants.FPS,
        #     pixel_size=Constants.PIXEL_SIZE,
        #     screen_width=Constants.SCREEN_WIDTH,
        #     screen_height=Constants.SCREEN_HEIGHT + Constants.NAVIGATION_BAR_HEIGHT,
        #     navigation_bar_height=Constants.NAVIGATION_BAR_HEIGHT)

    path = "scores/deep_neural_net_genetic_evolution_" + test_name + ".csv"
    _save_test_png(path, test_name, "selection rate", "score")



def mutation_rate_test():

    test_name = "Mutation_Rate"

    # for mutation_rate in [0.01, 0.1, 0.5, 1]:

        # ga_trainer = DNNGeneticEvolutionTrainer()
        # ga_trainer.population_size = 100
        # ga_trainer.selection_rate = 0.01
        # ga_trainer.mutation_rate = mutation_rate
        # ga_trainer.move(ga_trainer.prepare_training_environment())

        # game_model=DNNGeneticEvolutionSolver(test_name, mutation_rate)
        # Game(game_model,
        #     fps=Constants.FPS,
        #     pixel_size=Constants.PIXEL_SIZE,
        #     screen_width=Constants.SCREEN_WIDTH,
        #     screen_height=Constants.SCREEN_HEIGHT + Constants.NAVIGATION_BAR_HEIGHT,
        #     navigation_bar_height=Constants.NAVIGATION_BAR_HEIGHT)

    path = "scores/deep_neural_net_genetic_evolution_" + test_name + ".csv"
    _save_test_png(path, test_name, "mutation rate", "score")



def population_size_test():

    test_name = "Population_Size"

    # for population_size in [10, 100, 500, 1000]:

    #     ga_trainer = DNNGeneticEvolutionTrainer()
    #     ga_trainer.population_size = population_size
    #     ga_trainer.selection_rate = 0.01
    #     ga_trainer.mutation_rate = 0.01
    #     ga_trainer.move(ga_trainer.prepare_training_environment())

        # game_model=DNNGeneticEvolutionSolver(test_name, selection_rate)
        # Game(game_model,
        #     fps=Constants.FPS,
        #     pixel_size=Constants.PIXEL_SIZE,
        #     screen_width=Constants.SCREEN_WIDTH,
        #     screen_height=Constants.SCREEN_HEIGHT + Constants.NAVIGATION_BAR_HEIGHT,
        #     navigation_bar_height=Constants.NAVIGATION_BAR_HEIGHT)

    path = "scores/deep_neural_net_genetic_evolution_" + test_name + ".csv"
    _save_test_png(path, test_name, "population size", "score")



def _save_test_png(input_path, test_name, x_label, y_label):
    x = []
    y = []
    with open(input_path, "r") as scores:
        reader = csv.reader(scores)
        data = list(reader)
        for i in range(0, len(data)):
            x.append(str(data[i][0]))
            y.append(float(data[i][1]))

    plt.subplots()
    plt.plot(x, y, label="score")

    plt.title(test_name)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.legend(loc="upper left")
    plt.savefig("scores/deep_neural_net_genetic_evolution_" + test_name + ".png", bbox_inches="tight")
    plt.close()


if __name__ == '__main__':

    # selection_rate_test()
    # mutation_rate_test() 
    population_size_test()