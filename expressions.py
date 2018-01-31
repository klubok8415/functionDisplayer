class Value:
    def __init__(self, value):
        self.value = value

    def calculate(self):
        return self.value


class Addition:
    def __init__(self, *args):
        self.args = args

    def calculate(self):
        return sum(a.calculate for a in self.args)


class Deduction(Addition):
    def calculate(self):
        return self.args[0].calculate() - self.args[1].calculate()


class Multiplication(Addition):
    def calculate(self):
        return self.args[0].calculate() * self.args[1].calculate()


class Division(Addition):
    def calculate(self):
        return self.args[0].calculate() / self.args[1].calculate()


class Function:
    def __init__(self, expression, variables):
        self.expression = expression
        self.variables = variables

    def calculate(self, x):
        for var in self.variables:
            var.value = x

        return self.expression.calculate()
