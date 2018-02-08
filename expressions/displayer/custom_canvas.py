from tkinter import *

import math

from expressions.displayer.exceptions import TooBigNumbersError, WrongFunctionStringError
from function_parser.default import default_parser


class Displayer(Canvas):
    def __init__(self, root, x_min=-25, x_max=25, y_min=-25, y_max=25, size_x=500, size_y=500, border=50):
        self.root = root
        self.size_x = size_x
        self.size_y = size_y
        self.border = border
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.functions_list = []
        self.parser = default_parser
        super(Displayer, self).__init__(self.root, width=self.size_x + self.border, height=self.size_y + self.border,
                                        bg='white')
        self.default_colors = [
            '#0A62A5',
            '#181CB3',
            '#6D0AF7',
            '#F600F6',
            '#FC004C',
            '#FF4900',
            '#FF9000',
            '#FFBF00',
            '#FFE800',
            '#9BED00',
            '#00C80D']

    def update_graph(self):
        self.delete(ALL)
        x_axis_position = self.size_y // 2 + (self.y_max + self.y_min) / 2 * self.size_y / (
            self.y_max - self.y_min) + self.border // 2
        y_axis_position = self.size_x // 2 - (self.x_max + self.x_min) / 2 * self.size_x / (
            self.x_max - self.x_min) + self.border // 2

        if x_axis_position < self.border / 2:
            x_axis_position = self.border / 2
        if y_axis_position < self.border / 2:
            y_axis_position = self.border / 2
        if x_axis_position > self.size_x + self.border / 2:
            x_axis_position = self.size_x + self.border / 2
        if y_axis_position > self.size_y + self.border / 2:
            y_axis_position = self.size_y + self.border / 2

        if self.functions_list:
            for i, f in enumerate(self.functions_list):
                pp = []

                for x in range(self.size_x + 1):
                    try:
                        current_f_value = f.calculate((self.x_max - self.x_min) / self.size_x * x + self.x_min)
                    except OverflowError:
                        index = self.functions_list.index(f)
                        self.functions_list.remove(f)
                        raise TooBigNumbersError(index)

                    point = (
                        x + self.border // 2,
                        self.size_y
                        - (self.size_y * (current_f_value - self.y_min) / (self.y_max - self.y_min))
                        + self.border // 2)

                    if math.isnan(point[1]):
                        if len(pp) > 0:
                            self.create_line(pp, fill=self.default_colors[i % len(self.default_colors)], width=2)
                        pp = []
                        continue

                    if point[1] > self.size_y + self.border + 10:
                        point = (point[0], self.size_y + self.border + 10)

                    if point[1] < self.border / 2 or point[1] > self.size_y + self.border / 2:
                        continue

                    pp.append(point)

                if len(pp) > 1:
                    self.create_line(pp, fill=self.default_colors[i % len(self.default_colors)], width=2)

        self.create_line(y_axis_position, self.size_y + self.border // 2,
                         y_axis_position, self.border // 2,
                         width=1, arrow=LAST, fill="gray")

        self.create_line(self.border // 2, x_axis_position,
                         self.size_x + self.border // 2, x_axis_position,
                         width=1, arrow=LAST, fill="gray")
        # marking x_axis
        i = 0
        while True:
            n = 0

            while (self.x_max - self.x_min) * (10 ** n) < self.size_x // 50:
                n += 1

            k = (self.x_max - self.x_min) * (10 ** n) // (self.size_x // 50)

            a = k * (i + self.x_min * (10 ** n) // k)

            i += 1

            x = self.size_x * (
                1 - (1 - 1 / ((self.x_max - self.x_min) * (10 ** n)) * (a - self.x_min * (10 ** n))))

            if x > self.size_x:
                break

            self.create_line(x + self.border // 2, -2 + x_axis_position, x + self.border // 2, 2 + x_axis_position,
                             width=0.25, fill='gray')

            self.create_text(x + self.border // 2, 15 + x_axis_position,
                             text=str(a / (10 ** n)), fill='black',
                             font=('Helvectica', '10'))

        # marking y_axis
        i = 0
        while True:
            n = 0

            while (self.y_max - self.y_min) * (10 ** n) < self.size_y // 50:
                n += 1

            k = (self.y_max - self.y_min) * (10 ** n) // (self.size_y // 50)

            a = k * (i + self.y_min * (10 ** n) // k)

            i += 1

            if a == 0:
                continue

            y = self.size_y * (1 - 1 / ((self.y_max - self.y_min) * (10 ** n)) * (a - self.y_min * (10 ** n)))

            if y < 0:
                break

            self.create_line(-2 + y_axis_position, y + self.border // 2, 2 + y_axis_position, y + self.border // 2,
                             width=0.25, fill='gray')

            self.create_text(15 + y_axis_position, y + self.border // 2,
                             text=str(a / (10 ** n)), fill='black',
                             font=('Helvectica', '10'))

    def add_point(self, x, y, color="black"):
        self.create_oval(
            x - 1,
            self.size_y * y + 1,
            x + 1,
            self.size_y * y - 1,
            fill=color)

    def rescale(self, x_min, x_max, y_min, y_max):
        self.x_max = x_max
        self.x_min = x_min
        self.y_min = y_min
        self.y_max = y_max

    def add_function(self, func):
        f = self.parser.parse(func)

        if f is None:
            raise WrongFunctionStringError()

        self.functions_list.append(f)

    def add_derivative(self, index):
        self.functions_list.append(self.functions_list[index].differentiate())

    def delete_function(self, index):
        self.functions_list.pop(index)
        self.delete(ALL)
        self.update_graph()

    def clear(self):
        self.functions_list = []
        self.delete(ALL)
        self.update_graph()
