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


class Operation:
    def __init__(self, args):
        self.args = args