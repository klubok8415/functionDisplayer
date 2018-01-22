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
    
    def parse(string):
        string = string.replace(" ", "")
        try:
            string = string.split("=")[1]
        except IndexError:
            raise Exception("Wrong format: '<function_name>=' is required")
        return Function._parse(string)

    def _parse(string):
        if string == "x":
            v = Value(0)
            return Function(v, [v])
        
        is_float = True
        try:
            value = float(string)
        except ValueError:
            is_float = False

        if is_float:
            return Function(Value(value), [])

        operators = [
            {
                "+": Addition,
                "-": Deduction,
            },
            {
                "*": Multiplication,
                "/": Division,
            },
        ]

        for current_operators in operators:
            operators_indices = [string.rfind(o) for o in current_operators if string.rfind(o) != -1]
            if len(operators_indices) <= 0:
                continue
            operator_position = max(operators_indices)
            
            operator_class = current_operators[string[operator_position]]
            arg1 = Function._parse(string[:operator_position])
            arg2 = Function._parse(string[operator_position + 1:])

            return Function(
                operator_class(arg1.expression, arg2.expression),
                arg1.variables + arg2.variables)

        raise Exception()
