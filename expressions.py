import math

import numpy


class Value:
    def __init__(self, value):
        self.value = value

    def calculate(self):
        return self.value


class Operation:
    def __init__(self, args):
        self.args = args


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


class Power(Operation):
    def calculate(self):
        x = self.args[0].calculate()
        power = self.args[1].calculate()

        return numpy.nan if (x == 0 and power < 0) or (x < 0 and math.modf(power)[0] != 0) else x**power


class Modulus(Operation):
    def calculate(self):
        return abs(self.args[0].calculate())


class Sinus(Operation):
    def calculate(self):
        return math.sin(self.args[0].calculate())


class Logarithm(Operation):
    def calculate(self):
        x = self.args[0].calculate()
        base = self.args[1].calculate()

        return math.log(x, base) if base > 0 and base != 1 and x > 0 else numpy.nan


class Function:
    def __init__(self, expression, variables):
        self.expression = expression
        self.variables = variables

    @staticmethod
    def concat(functions, operation):
        return Function(operation([f.expression for f in functions]), sum([f.variables for f in functions], []))

    def calculate(self, x):
        for var in self.variables:
            var.value = x

        return self.expression.calculate()
