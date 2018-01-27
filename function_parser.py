from expressions import *


class Operator:
    def __init__(self, character, operation):
        self.character = character
        self.operation = operation


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
        if string[0] == "(" and string[-1] == ")":
            string = string[1:-1]

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
            operators_by_character = {o.character: o for o in current_operators}

            operator_position = len(string) - 1
            braces = 0

            for s in string[::-1]:
                if s == "(":
                    braces -= 1
                elif s == ")":
                    braces += 1

                if braces == 0:
                    operator = operators_by_character.get(s)
                    if operator is not None:
                        break

                operator_position -= 1
            else:
                continue

            arg1 = self._parse(string[:operator_position])
            arg2 = self._parse(string[operator_position + 1:])

            return Function(
                operator.operation(arg1.expression, arg2.expression),
                arg1.variables + arg2.variables)

        raise Exception()


default_parser = Parser([
    {
        Operator("+", Addition),
        Operator("-", Deduction),
    },
    {
        Operator("*", Multiplication),
        Operator("/", Division),
    },
])
