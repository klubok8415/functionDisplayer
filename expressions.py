class Value:
    def __init__(self, value):
        self.value = value

    def calculate(self):
        return self.value


class Addition:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def calculate(self):
        return self.arg1.calculate() + self.arg2.calculate()


class Deduction(Addition):
    def calculate(self):
        return self.arg1.calculate() - self.arg2.calculate()


class Multiplication(Addition):
    def calculate(self):
        return self.arg1.calculate() * self.arg2.calculate()


class Division(Addition):
    def calculate(self):
        return self.arg1.calculate() / self.arg2.calculate()


class Function:
    def __init__(self, expression, variables):
        self.expression = expression
        self.variables = variables

    def calculate(self, x):
        for var in self.variables:
            var.value = x

        return self.expression.calculate()
