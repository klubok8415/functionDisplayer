import math
from expressions.core import Operation


class Sinus(Operation):
    def calculate(self):
        return math.sin(self.args[0].calculate())
