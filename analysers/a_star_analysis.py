import csv

import matplotlib.pyplot as plt

from game.game import Game
from game.helpers.constants import Constants
from game.models.domain_specific.a_star_solver import AStarSolver
from .analysis_parent import Analysis
from pathlib import Path
import os


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
                 special_boost=self.boost)


        self._save_test_png(path, test_name, "screen size", "score")

    def fruit_boost_test(self):
        test_name = "Fruit_Boost"

        path = f"scores/{self.analysis_name_str}_" + test_name + ".csv"
        if Path(path).exists():
            os.remove(path)

        for fruit in [1, 2, 4, 8]:
            for boost in [1, 2, 4, 8]:
                game_model = AStarSolver(test_name, boost)
                Game(game_model=game_model,
                     fps=Constants.FPS,
                     pixel_size=Constants.PIXEL_SIZE,
                     screen_width=self.width,
                     screen_height=self.height,
                     navigation_bar_height=Constants.NAVIGATION_BAR_HEIGHT,
                     number_of_fruit=fruit,
                     special_chance=1,
                     special_boost=boost)


        self._save_test_png2(path, test_name, "fruit boost", "score")

    def fruit_chance_test(self):
        test_name = "Fruit_Chance"

        path = f"scores/{self.analysis_name_str}_" + test_name + ".csv"
        if Path(path).exists():
            os.remove(path)

        for fruit in [1, 2, 4, 8]:
            for chance in [0, 0.2, 0.5, 0.8, 1]:
                game_model = AStarSolver(test_name, chance)
                Game(game_model=game_model,
                     fps=Constants.FPS,
                     pixel_size=Constants.PIXEL_SIZE,
                     screen_width=self.width,
                     screen_height=self.height,
                     navigation_bar_height=Constants.NAVIGATION_BAR_HEIGHT,
                     number_of_fruit=fruit,
                     special_chance=chance,
                     special_boost=2)


        self._save_test_png2(path, test_name, "fruit chance", "score")

    def _save_test_png2(self, input_path, test_name, x_label, y_label):
        x = []
        count_1_list = []
        count_2_list = []
        count_3_list = []
        count_4_list = []

        with open(input_path, "r") as scores:
            reader = csv.reader(scores)
            data = list(reader)
            for boost, score in data:
                if str(boost) not in x:
                    x.append(str(boost))
                    x.sort()
                if x.index(str(boost)) == 0:
                    count_1_list.append(float(score))
                elif x.index(str(boost)) == 1:
                    count_2_list.append(float(score))
                elif x.index(str(boost)) == 2:
                    count_3_list.append(float(score))
                elif x.index(str(boost)) == 3:
                    count_4_list.append(float(score))

        plt.plot(x, count_1_list, label="count: 1")
        plt.plot(x, count_2_list, label="count: 2")
        plt.plot(x, count_3_list, label="count: 4")
        plt.plot(x, count_4_list, label="count: 8")

        plt.title(test_name)
        plt.xlabel(x_label)
        plt.ylabel(y_label)

        plt.legend(loc="upper left")
        plt.savefig(f"scores/{self.analysis_name_str}_" + test_name + ".png", bbox_inches="tight")
        plt.close()
