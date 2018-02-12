import math

from expressions.core import Operation, DifferentiationError
from expressions.math.simple import Deduction, Division, Multiplication


class Modulus(Operation):
    def calculate(self):
        return abs(self.args[0].calculate())

    def differentiate(self, variables):
        return Multiplication(
            self.args[0].differentiate(variables),
            Division(
                self.args[0],
                Modulus(self.args[0])))


class Floor(Operation):
    def calculate(self):
        return math.floor(self.args[0].calculate())

    def differentiate(self, variables):
        raise DifferentiationError()


class Truncate(Deduction):
    def __init__(self, *args):
        super(Truncate, self).__init__(args[0], Floor(args[0]))
