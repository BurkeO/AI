import argparse
import random

from game.helpers.constants import Constants
from game.models.domain_specific.a_star_solver import AStarSolver
from game.models.domain_specific.dnn_ai_solver import DNNSolver, DNNTrainer
from game.models.domain_specific.dnn_genetic_evolution_ai_solver import DNNGeneticEvolutionSolver, \
    DNNGeneticEvolutionTrainer
from game.models.domain_specific.dnn_monte_carlo_ai_solver import DNNMonteCarloSolver
from game.models.domain_specific.hamilton_ai_solver import HamiltonSolver
from game.models.domain_specific.longest_path_ai_solver import LongestPathSolver
from game.models.domain_specific.shortest_path_bfs_ai_solver import ShortestPathBFSSolver
from game.models.domain_specific.shortest_path_dfs_ai_solver import ShortestPathDFSSolver
from game.models.general_purpose.ddqn_ai_solver import DDQNSolver, DDQNTrainer
from game.models.general_purpose.human_solver import HumanSolver
from game.models.general_purpose.monte_carlo_ai_solver import MonteCarloSolver
from game.models.general_purpose.random_ai_solver import RandomSolver

solvers = [RandomSolver(),
           HumanSolver(),
           MonteCarloSolver(),
           ShortestPathBFSSolver(),
           ShortestPathDFSSolver(),
           AStarSolver(),
           LongestPathSolver(),
           HamiltonSolver(),
           DNNSolver(),
           DNNMonteCarloSolver(),
           DNNGeneticEvolutionSolver(),
           DDQNSolver()]

trainers = [DNNTrainer(),
            DNNGeneticEvolutionTrainer(),
            DDQNTrainer()]

game_models = solvers + trainers


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fruit", help="number of normal fruit on screen", default=1, type=int)
    parser.add_argument("-w", "--width", help="The width of the screen (default 300)", type=int)
    parser.add_argument("-t", "--height", help="The height of the screen (default 300)", type=int)
    parser.add_argument("-c", "--chance", help="The chance of every new fruit spawning as a special fruit (0 - 1)",
                        type=float, default=0)
    parser.add_argument("-b", "--boost", help="The number of blocks that snake grows by on a special fruit", type=int,
                        default=1)
    for game_model in game_models:
        parser.add_argument("-" + game_model.abbreviation, "--" + game_model.short_name,
                            help=game_model.long_name,
                            action="store_true")
    return parser.parse_args()


if __name__ == '__main__':
    selected_game_model = random.choice(solvers)
    args = args()
    for game_model in game_models:
        if game_model.short_name in args and vars(args)[game_model.short_name]:
            selected_game_model = game_model
    if selected_game_model in trainers:
        selected_game_model.move(selected_game_model.prepare_training_environment())
    else:
        from game.game import Game
        if args.chance > 1 or args.chance < 0:
            raise ValueError("Invalid value for chance argument")
        Game(game_model=selected_game_model,
             fps=Constants.FPS,
             pixel_size=Constants.PIXEL_SIZE,
             screen_width=args.width if args.width is not None else Constants.SCREEN_WIDTH,
             screen_height=(args.height if args.height is not None else Constants.SCREEN_HEIGHT) + Constants.NAVIGATION_BAR_HEIGHT,
             navigation_bar_height=Constants.NAVIGATION_BAR_HEIGHT,
             number_of_fruit=args.fruit,
             special_chance=args.chance,
             special_boost=args.boost)
