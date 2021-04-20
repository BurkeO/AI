import csv
from abc import ABC

import matplotlib.pyplot as plt


class Analysis(ABC):
    def __init__(self, analysis_name_str) -> None:
        self.analysis_name_str = analysis_name_str

    def screen_size_test(self):
        raise NotImplementedError

    def fruit_boost_test(self):
        raise NotImplementedError

    def fruit_chance_test(self):
        raise NotImplementedError

    def _save_test_png(self, input_path, test_name, x_label, y_label):
        x = []
        y = []
        with open(input_path, "r") as scores:
            reader = csv.reader(scores)
            data = list(reader)
            for x_value, y_value in data:
                x.append(x_value)
                y.append(float(y_value))

        plt.subplots()
        plt.plot(x, y, label="score")

        plt.title(test_name)
        plt.xlabel(x_label)
        plt.ylabel(y_label)

        plt.legend(loc="upper left")
        plt.savefig(f"scores/{self.analysis_name_str}_" + test_name + ".png", bbox_inches="tight")
        plt.close()

    def _save_test_png2(self, input_path, test_name, x_label, y_label):
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
        plt.savefig(f"scores/{self.analysis_name_str}_" + test_name + ".png", bbox_inches="tight")
        plt.close()
