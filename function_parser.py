from expressions import *


class Parser:
    def __init__(self, operators):
        self.operators = operators

    def parse(self, string):
        string = string.replace(" ", "")
        try:
            string = string.split("=")[1]
        except IndexError:
            raise Exception("Wrong format: '<function_name>=' is required")
        return self._parse(string)

    def _parse(self, string):
        if string == "x":
            v = Value(0)
            return Function(v, [v])

        try:
            value = float(string)
        except ValueError:
            pass
        else:
            return Function(Value(value), [])

        for current_operators in self.operators:
            operators_indices = [string.rfind(o) for o in current_operators if string.rfind(o) != -1]
            if len(operators_indices) <= 0:
                continue
            operator_position = max(operators_indices)

            operator_class = current_operators[string[operator_position]]
            arg1 = self._parse(string[:operator_position])
            arg2 = self._parse(string[operator_position + 1:])

            return Function(
                operator_class(arg1.expression, arg2.expression),
                arg1.variables + arg2.variables)

        raise Exception()


default_parser = Parser([
    {
        "+": Addition,
        "-": Deduction,
    },
    {
        "*": Multiplication,
        "/": Division,
    },
])
