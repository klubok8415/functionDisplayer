class Function:
    def __init__(self, expression, variables):
        self.expression = expression
        self.variables = variables

    @staticmethod
    def concat(functions, operation, new_variables=None):
        if new_variables is None:
            new_variables = []

        return Function(
            operation(*[f.expression for f in functions]),
            sum([f.variables for f in functions], new_variables))

    def calculate(self, x):
        for var in self.variables:
            var.value = x

        return self.expression.calculate()

    def differentiate(self):
        return Function(self.expression.differentiate(self.variables), self.variables)


class Operation:
    def __init__(self, *args):
        self.args = args

    def calculate(self):
        raise NotImplementedError()

    def differentiate(self, variables):
        raise NotImplementedError()


class Value:
    def __init__(self, value):
        self.value = value

    def calculate(self):
        return self.value

    def differentiate(self, variables):
        return Value(1 if self in variables else 0)

    def __call__(self, *args):
        return self
