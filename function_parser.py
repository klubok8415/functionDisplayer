import itertools

from expressions import *


class Brace:
    def __init__(self, opening_character, closing_character, operation=None):
        self.opening_character = opening_character
        self.closing_character = closing_character
        self.operation = operation

    def parse(self, string, parsing_function):
        if len(string) > 1 \
                and string[0] == self.opening_character \
                and string[-1] == self.closing_character:

            return parsing_function(string[1:-1]) \
                if self.operation is None \
                else Function.concat([parsing_function(string[1:-1])], self.operation)
        else:
            return None


class VariableOperator:
    @staticmethod
    def parse(string, parsing_function):
        if string == "x":
            v = Value(0)
            return Function(v, [v])
        return None


class ConstantOperator:
    @staticmethod
    def parse(string, parsing_function):
        try:
            value = float(string)
        except ValueError:
            return None
        else:
            return Function(Value(value), [])


class Operator:
    def __init__(self, character, operation):
        self.character = character
        self.operation = operation

    def parse(self, string, parsing_function):
        """Returns None, if parsing is not possible, else new function"""

        braces = 0
        operator_position = len(string) - 1

        for s in string[::-1]:
            if s == "(":
                braces -= 1
            elif s == ")":
                braces += 1

            if braces == 0 and s == self.character:
                args = [parsing_function(a) for a in [string[:operator_position], string[operator_position + 1:]]]
                if any(a is None for a in args):
                    return None
                return Function.concat(args, self.operation)

            operator_position -= 1
        else:
            return None


class Parser:
    def __init__(self, operators, braces):
        self.operators = braces + operators
        self.braces = braces

    def parse(self, string):
        string = string.replace(" ", "")
        try:
            string = string.split("=")[1]
        except IndexError:
            raise Exception("Wrong format: '<function_name>=' is required")
        return self._parse(string)

    def _parse(self, string):
        for current_operators in self.operators:
            for o in current_operators:
                result = o.parse(string, self._parse)

                if result is not None:
                    break
            else:
                continue

            return result

        return None


default_parser = Parser(
    [
        [
            Operator("+", Addition),
            Operator("-", Deduction),
        ],
        [
            Operator("*", Multiplication),
            Operator("/", Division),
        ],
        [
            Operator("^", Power),
        ],
        [
            VariableOperator,
            ConstantOperator,
        ]
    ],
    [
        [
            Brace("(", ")")
        ]
    ])
