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

    for selection_rate in [0.01, 0.1, 0.5, 1.0]:

        ga_trainer = DNNGeneticEvolutionTrainer()
        ga_trainer.population_size = 100
        ga_trainer.selection_rate = selection_rate
        ga_trainer.mutation_rate = 0.01
        ga_trainer.move(ga_trainer.prepare_training_environment())

        game_model=DNNGeneticEvolutionSolver(test_name, selection_rate)
        Game(game_model,
            fps=Constants.FPS,
            pixel_size=Constants.PIXEL_SIZE,
            screen_width=Constants.SCREEN_WIDTH,
            screen_height=Constants.SCREEN_HEIGHT + Constants.NAVIGATION_BAR_HEIGHT,
            navigation_bar_height=Constants.NAVIGATION_BAR_HEIGHT)

    path = "scores/deep_neural_net_genetic_evolution_" + test_name + ".csv"
    _save_test_png(path, test_name, "selection rate", "score")



def mutation_rate_test():

    test_name = "Mutation_Rate"

    width = 300
    height = 300
    fruit = 1
    chance = 0
    boost = 1

    for mutation_rate in [0.01, 0.1, 0.5, 1]:

        ga_trainer = DNNGeneticEvolutionTrainer()
        ga_trainer.population_size = 100
        ga_trainer.selection_rate = 0.01
        ga_trainer.mutation_rate = mutation_rate
        ga_trainer.move(ga_trainer.prepare_training_environment())

        game_model=DNNGeneticEvolutionSolver(test_name, mutation_rate)
        Game(game_model=game_model,
             fps=Constants.FPS,
             pixel_size=Constants.PIXEL_SIZE,
             screen_width=width,
             screen_height=height,
             navigation_bar_height=Constants.NAVIGATION_BAR_HEIGHT,
             number_of_fruit=fruit,
             special_chance=chance,
             special_boost=boost)

    path = "scores/deep_neural_net_genetic_evolution_" + test_name + ".csv"
    _save_test_png(path, test_name, "mutation rate", "score")



def population_size_test():

    test_name = "Population_Size"

    width = 300
    height = 300
    fruit = 1
    chance = 0
    boost = 1

    for population_size in [10, 100, 500, 1000]:

        ga_trainer = DNNGeneticEvolutionTrainer()
        ga_trainer.population_size = population_size
        ga_trainer.selection_rate = 0.01
        ga_trainer.mutation_rate = 0.01
        ga_trainer.move(ga_trainer.prepare_training_environment())

        game_model=DNNGeneticEvolutionSolver(test_name, population_size)
        Game(game_model=game_model,
             fps=Constants.FPS,
             pixel_size=Constants.PIXEL_SIZE,
             screen_width=width,
             screen_height=height,
             navigation_bar_height=Constants.NAVIGATION_BAR_HEIGHT,
             number_of_fruit=fruit,
             special_chance=chance,
             special_boost=boost)

    path = "scores/deep_neural_net_genetic_evolution_" + test_name + ".csv"
    _save_test_png(path, test_name, "population size", "score")



def screen_size_test():

    test_name = "Screen_Size"

    width = 300
    height = 300
    fruit = 1
    chance = 0
    boost = 1

    for size in [300, 400, 500, 600]:

        game_model=DNNGeneticEvolutionSolver(test_name, size)
        Game(game_model=game_model,
             fps=Constants.FPS,
             pixel_size=Constants.PIXEL_SIZE,
             screen_width=size,
             screen_height=size,
             navigation_bar_height=Constants.NAVIGATION_BAR_HEIGHT,
             number_of_fruit=fruit,
             special_chance=chance,
             special_boost=boost)

    path = "scores/deep_neural_net_genetic_evolution_" + test_name + ".csv"
    _save_test_png(path, test_name, "screen size", "score")



def fruit_boost_test():

    test_name = "Fruit_Boost"

    width = 300
    height = 300
    # fruit = 1
    chance = 1
    # boost = 1

    for fruit in [8]:
        for boost in [1, 2, 4, 8]:
            game_model=DNNGeneticEvolutionSolver(test_name, boost)
            Game(game_model=game_model,
                fps=Constants.FPS,
                pixel_size=Constants.PIXEL_SIZE,
                screen_width=width,
                screen_height=height,
                navigation_bar_height=Constants.NAVIGATION_BAR_HEIGHT,
                number_of_fruit=fruit,
                special_chance=chance,
                special_boost=boost)

    path = "scores/deep_neural_net_genetic_evolution_" + test_name + ".csv"
    _save_test_png2(path, test_name, "fruit boost", "score")


def fruit_chance_test():

    test_name = "Fruit_Chance"

    width = 300
    height = 300
    # fruit = 1
    # chance = 0
    boost = 2

    for fruit in [1]:
        for chance in [0, 0.2, 0.5, 0.8, 1]:
            game_model=DNNGeneticEvolutionSolver(test_name, chance)
            Game(game_model=game_model,
                fps=Constants.FPS,
                pixel_size=Constants.PIXEL_SIZE,
                screen_width=width,
                screen_height=height,
                navigation_bar_height=Constants.NAVIGATION_BAR_HEIGHT,
                number_of_fruit=fruit,
                special_chance=chance,
                special_boost=boost)

    path = "scores/deep_neural_net_genetic_evolution_" + test_name + ".csv"
    _save_test_png2(path, test_name, "fruit chance", "score")


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


def _save_test_png2(input_path, test_name, x_label, y_label):
    x = []
    a = []
    b = []
    c = []
    d = []
    with open(input_path, "r") as scores:
        reader = csv.reader(scores)
        data = list(reader)
        for i in range(0, len(data)):
            x.append(str(data[i][0]))
            a.append(float(data[i][1]))            
            b.append(float(data[i][2]))            
            c.append(float(data[i][3]))            
            d.append(float(data[i][4]))

    plt.plot(x, a, label="count: 1")
    plt.plot(x, b, label="count: 2")
    plt.plot(x, c, label="count: 4")
    plt.plot(x, d, label="count: 8")

    plt.title(test_name)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.legend(loc="upper left")
    plt.savefig("scores/deep_neural_net_genetic_evolution_" + test_name + ".png", bbox_inches="tight")
    plt.close()


if __name__ == '__main__':

    selection_rate_test()
    mutation_rate_test() 
    population_size_test()

    ga_trainer = DNNGeneticEvolutionTrainer()
    ga_trainer.population_size = 500
    ga_trainer.selection_rate = 0.01
    ga_trainer.mutation_rate = 0.01
    ga_trainer.move(ga_trainer.prepare_training_environment())

    screen_size_test()

    fruit_boost_test()    
    fruit_chance_test()