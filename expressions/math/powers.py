import math

import numpy

from expressions.core import Operation
from expressions.math.simple import Division, Value


class Power(Operation):
    def calculate(self):
        x = self.args[0].calculate()
        power = self.args[1].calculate()

        return numpy.nan if (x == 0 and power < 0) or (x < 0 and math.modf(power)[0] != 0) else x**power


class Logarithm(Operation):
    def calculate(self):
        x = self.args[0].calculate()
        base = self.args[1].calculate()

        return math.log(x, base) if base > 0 and base != 1 and x > 0 else numpy.nan


class Sqrt(Power):
    def __init__(self, args):
        super(Sqrt, self).__init__([args[0], Value(0.5)])
