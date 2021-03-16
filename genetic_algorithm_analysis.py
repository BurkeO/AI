import argparse
import random

from game.helpers.constants import Constants
from game.models.domain_specific.dnn_genetic_evolution_ai_solver import DNNGeneticEvolutionSolver, DNNGeneticEvolutionTrainer
from game.game import Game

def selection_rate():
    ga_trainier = DNNGeneticEvolutionTrainer()        
    ga_trainier.population_size = 1000
    ga_trainier.mutation_rate = 0.01
    selection_rates = [0.01, 0.1, 0.5, 1]
    
    for selection_rate in selection_rates:
        ga_trainier.selection_rate = selection_rate
        ga_trainier.move(ga_trainier.prepare_training_environment())


if __name__ == '__main__':

    # ga_trainer = DNNGeneticEvolutionTrainer()
    # ga_trainer.population_size = 100
    # ga_trainer.selection_rate = 0.1
    # ga_trainer.mutation_rate = 0.01
    # ga_trainer.move(ga_trainer.prepare_training_environment())

    for i in range(3):
        Game(game_model=DNNGeneticEvolutionSolver("test", i),
                fps=Constants.FPS,
                pixel_size=Constants.PIXEL_SIZE,
                screen_width=Constants.SCREEN_WIDTH,
                screen_height=Constants.SCREEN_HEIGHT + Constants.NAVIGATION_BAR_HEIGHT,
                navigation_bar_height=Constants.NAVIGATION_BAR_HEIGHT)