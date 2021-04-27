from argparse import ArgumentParser, Namespace

from analysers.genetic_algorithm_analysis import GeneticAlgorithmAnalyser
from analysers.a_star_analysis import AStarAnalyser


def main(args: Namespace):
    if args.a_star:
        analyser = AStarAnalyser()
    elif args.genetic:
        analyser = GeneticAlgorithmAnalyser()
    else:
        raise ValueError("Must specify an analyser")

    analyser.run()


def parse_args():
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-a", "--a_star", action="store_true", help="Flag for performing analysis on a star")
    group.add_argument('-g', "--genetic", action='store_true',
                       help="Flag for performing analysis on genetic algorithms")
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
