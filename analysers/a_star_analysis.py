import csv
import os
from pathlib import Path

import matplotlib.pyplot as plt

from game.game import Game
from game.helpers.constants import Constants
from game.models.domain_specific.a_star_solver import AStarSolver
from .analysis_parent import Analysis


class AStarAnalyser(Analysis):

    def __init__(self):
        super(AStarAnalyser, self).__init__(analysis_name_str="a_star")
        self.width = 300
        self.height = 300
        self.fruit = 1
        self.chance = 0
        self.boost = 1

    def screen_size_test(self):
        test_name = "Screen_Size"

        path = f"scores/{self.analysis_name_str}_" + test_name + ".csv"
        if Path(path).exists():
            os.remove(path)

        for size in [300, 400, 500, 600]:
            game_model = AStarSolver(test_name, size)
            Game(game_model=game_model,
                 fps=Constants.FPS,
                 pixel_size=Constants.PIXEL_SIZE,
                 screen_width=size,
                 screen_height=size,
                 navigation_bar_height=Constants.NAVIGATION_BAR_HEIGHT,
                 number_of_fruit=self.fruit,
                 special_chance=self.chance,
                 special_boost=self.boost, is_analysing=True)
            os.remove("scores/" + game_model.short_name + ".csv")

        self._save_test_png(path, test_name, "screen size", "score")

    def fruit_boost_test(self):
        test_name = "Fruit_Boost"

        path = f"scores/{self.analysis_name_str}_" + test_name + ".csv"
        if Path(path).exists():
            os.remove(path)

        x_values = [1, 2, 4, 8]
        legend_values = [1, 2, 4, 8]

        for fruit in legend_values:
            for boost in x_values:
                game_model = AStarSolver(test_name, boost)
                Game(game_model=game_model,
                     fps=Constants.FPS,
                     pixel_size=Constants.PIXEL_SIZE,
                     screen_width=self.width,
                     screen_height=self.height,
                     navigation_bar_height=Constants.NAVIGATION_BAR_HEIGHT,
                     number_of_fruit=fruit,
                     special_chance=1,
                     special_boost=boost, is_analysing=True)
                os.remove("scores/" + game_model.short_name + ".csv")

        self._save_test_png_two(path, test_name, "fruit boost", "score", x_values, legend_values)

    def fruit_chance_test(self):
        test_name = "Fruit_Chance"

        path = f"scores/{self.analysis_name_str}_" + test_name + ".csv"
        if Path(path).exists():
            os.remove(path)

        legend_values = [1, 2, 4, 8]
        x_values = [0, 0.2, 0.5, 0.8, 1]

        for fruit in legend_values:
            for chance in x_values:
                game_model = AStarSolver(test_name, chance)
                Game(game_model=game_model,
                     fps=Constants.FPS,
                     pixel_size=Constants.PIXEL_SIZE,
                     screen_width=self.width,
                     screen_height=self.height,
                     navigation_bar_height=Constants.NAVIGATION_BAR_HEIGHT,
                     number_of_fruit=fruit,
                     special_chance=chance,
                     special_boost=2, is_analysing=True)
                os.remove("scores/" + game_model.short_name + ".csv")

        self._save_test_png_two(path, test_name, "fruit chance", "score", x_values, legend_values)

    def _save_test_png_two(self, input_path, test_name, x_label, y_label, x_values, legend_values):
        x_values.sort()

        x_value_to_list = {}
        for x in x_values:
            x_value_to_list[str(x)] = []

        with open(input_path, "r") as scores:
            reader = csv.reader(scores)
            data = list(reader)
            for boost, score in data:
                x_value_to_list[boost].append(float(score))

        for index, legend in enumerate(legend_values):
            values_list = []
            for y_list in x_value_to_list.values():
                values_list.append(y_list[index])
            plt.plot(x_values, values_list, label=f"count {legend}")

        plt.title(test_name)
        plt.xlabel(x_label)
        plt.ylabel(y_label)

        plt.legend(loc="upper left")
        plt.savefig(f"scores/{self.analysis_name_str}_" + test_name + ".png", bbox_inches="tight")
        plt.close()

    def run(self):
        self.screen_size_test()
        self.fruit_boost_test()
        self.fruit_chance_test()
