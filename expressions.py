import math


class Value:
    def __init__(self, value):
        self.value = value

    def calculate(self):
        return self.value


class Operation:
    def __init__(self, args):
        self.args = args

    def calculate(self):
        raise NotImplementedError()


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
        return self.args[0].calculate() / self.args[1].calculate()


class Power(Operation):
    def calculate(self):
        return self.args[0].calculate() ** self.args[1].calculate()


class Modulus(Operation):
    def calculate(self):
        return abs(self.args[0].calculate())


class Sinus(Operation):
    def calculate(self):
        return math.sin(self.args[0].calculate())


class Logarithm(Operation):
    def calculate(self):
        return math.log(self.args[0].calculate(), self.args[1].calculate())


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
