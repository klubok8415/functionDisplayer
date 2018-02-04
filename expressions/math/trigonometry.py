import math

from expressions.core import Operation
from expressions.math.simple import Division


class Sinus(Operation):
    def calculate(self):
        return math.sin(self.args[0].calculate())


class Cosine(Operation):
    def calculate(self):
        return math.cos(self.args[0].calculate())


class Tangent(Division):
    def __init__(self, args):
        super(Tangent, self).__init__([Sinus([args[0]]), Cosine([args[0]])])


class Cotangent(Division):
    def __init__(self, args):
        super(Cotangent, self).__init__([Cosine([args[0]]), Sinus([args[0]])])
