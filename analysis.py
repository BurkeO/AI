from argparse import ArgumentParser, Namespace

from analysers.genetic_algorithm_analysis import GeneticAlgorithmAnalysis


def main(args: Namespace):
    switcher = {
        "GeneticAlgorithmAnalysis": GeneticAlgorithmAnalysis
    }
    analyser = switcher[args.analyser]()
    analyser.selection_rate_test()
    analyser.mutation_rate_test()
    analyser.population_size_test()
    analyser.screen_size_test()
    analyser.fruit_boost_test()
    analyser.fruit_chance_test()


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-a", "--analyser", type=str,
                        help="The name of the analyser class to use (i.e. GeneticAlgorithmAnalysis)", required=True)
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
