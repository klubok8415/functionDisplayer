import math

import numpy

from expressions.core import Operation, Value
from expressions.math.simple import Division, MultiplicativeInversion, Addition, Multiplication, Deduction, Sqrt, Power


class Sinus(Operation):
    def calculate(self):
        return math.sin(self.args[0].calculate())

    def differentiate(self, variables):
        return Multiplication(
            self.args[0].differentiate(variables),
            Sinus(Addition(self.args[0], Value(math.pi / 2)))
        )


class Cosine(Sinus):
    def __init__(self, *args):
        super(Cosine, self).__init__(Addition(args[0], Value(math.pi / 2)))


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

    def differentiate(self, variables):
        return Multiplication(
            self.args[0].differentiate(variables),
            Sqrt(Deduction(Value(1), Power(self.args[0], Value(2))))
        )


class Arccosine(Deduction):
    def __init__(self, *args):
        super(Arccosine, self).__init__(Arcsine(args[0]), Value(math.pi / 2))


class Arctangent(Operation):
    def calculate(self):
        try:
            return math.atan(self.args[0].calculate())
        except ValueError:
            return numpy.nan

    def differentiate(self, variables):
        return Division(
            self.args[0].differentiate(variables),
            Addition(Value(1), Power(self.args[0], Value(2)))
        )


class Arccotangent(Arctangent):
    def __init__(self, *args):
        super(Arccotangent, self).__init__(MultiplicativeInversion(args[0]))
