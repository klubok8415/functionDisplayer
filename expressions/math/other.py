import math

from expressions.core import Operation
from expressions.math.simple import Deduction


class Modulus(Operation):
    def calculate(self):
        return abs(self.args[0].calculate())


class Floor(Operation):
    def calculate(self):
        return math.floor(self.args[0].calculate())


class Truncate(Deduction):
    def __init__(self, *args):
        super(Truncate, self).__init__(args[0], Floor([args[0]]))
