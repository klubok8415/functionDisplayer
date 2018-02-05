import math
import numpy
from expressions.core import Operation


class Value:
    def __init__(self, value):
        self.value = value

    def calculate(self):
        return self.value


class Inversion(Operation):
    def calculate(self):
        return -self.args[0].calculate()


class Addition(Operation):
    def calculate(self):
        return sum(a.calculate() for a in self.args)


class Deduction(Operation):
    def calculate(self):
        return self.args[0].calculate() - self.args[1].calculate()


class Multiplication(Operation):
    def calculate(self):
        return self.args[0].calculate() * self.args[1].calculate()


class Division(Operation):
    def calculate(self):
        n = self.args[1].calculate()
        return numpy.nan if n == 0 else self.args[0].calculate() / n
