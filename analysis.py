from argparse import ArgumentParser, Namespace

from analysers.genetic_algorithm_analysis import GeneticAlgorithmAnalyser
from analysers.a_star_analysis import AStarAnalyser


def main(args: Namespace):
    switcher = {
        "GeneticAlgorithmAnalyser": GeneticAlgorithmAnalyser,
        "AStarAnalyser": AStarAnalyser
    }
    analyser = switcher[args.analyser]()
    if args.analyser == "GeneticAlgorithmAnalyser":
        analyser.selection_rate_test()
        analyser.mutation_rate_test()
        analyser.population_size_test()

    analyser.screen_size_test()
    analyser.fruit_boost_test()
    # analyser.fruit_chance_test()


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-a", "--analyser", type=str,
                        help="The name of the analyser class to use (i.e. GeneticAlgorithmAnalyser)", required=True)
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
