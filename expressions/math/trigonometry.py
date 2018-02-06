import math

import numpy

from expressions.core import Operation
from expressions.math.simple import Division, MultiplicativeInversion


class Sinus(Operation):
    def calculate(self):
        return math.sin(self.args[0].calculate())


class Cosine(Operation):
    def calculate(self):
        return math.cos(self.args[0].calculate())


class Tangent(Division):
    def __init__(self, *args):
        super(Tangent, self).__init__(Sinus(args[0]), Cosine(args[0]))


class Cotangent(Division):
    def __init__(self, *args):
        super(Cotangent, self).__init__(Cosine(args[0]), Sinus(args[0]))


class Arcsine(Operation):
    def calculate(self):
        try:
            return math.asin(self.args[0].calculate())
        except ValueError:
            return numpy.nan


class Arccosine(Operation):
    def calculate(self):
        try:
            return math.acos(self.args[0].calculate())
        except ValueError:
            return numpy.nan


class Arctangent(Operation):
    def calculate(self):
        try:
            return math.atan(self.args[0].calculate())
        except ValueError:
            return numpy.nan


class Arccotangent(Arctangent):
    def __init__(self, *args):
        super(Arccotangent, self).__init__(MultiplicativeInversion(args[0]))
