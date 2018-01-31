from expressions import *


class Operator:
    def __init__(self, character, operation):
        self.character = character
        self.operation = operation

    def parse(self, string):
        """Returns None, if parsing is not possible, else (operation, arguments strings)"""

        braces = 0
        operator_position = len(string) - 1

        for s in string[::-1]:
            if s == "(":
                braces -= 1
            elif s == ")":
                braces += 1

            if braces == 0 and s == self.character:
                return self.operation, [string[:operator_position], string[operator_position + 1:]]

            operator_position -= 1
        else:
            return None


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

        # variable

        if string == "x":
            v = Value(0)
            return Function(v, [v])

        # constant value

        try:
            value = float(string)
        except ValueError:
            pass
        else:
            return Function(Value(value), [])

        # operator

        for current_operators in self.operators:
            for o in current_operators:
                parsing_result = o.parse(string)

                if parsing_result is not None:
                    operation, args = parsing_result
                    break
            else:
                continue

            args = [self._parse(a) for a in args]
            try:
                return Function(operation(*[a.expression for a in args]), sum(a.variables for a in args))
            except TypeError:
                print([a.variables for a in args])

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
