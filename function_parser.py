import itertools

from expressions import *


class FunctionOperator:
    def __init__(self, name, operation, args_number):
        self.name = name
        self.operation = operation
        self.args_number = args_number

    def parse(self, string, parsing_function, braces_pairs):
        if len(string) < len(self.name) + 2 or not string.endswith(")"):
            return None

        for i in range(len(string)):
            if string[i:].startswith(self.name) \
                    and len(self.name) + i < len(string) \
                    and string[len(self.name) + i] == "(":
                string = string[i + len(self.name) + 1:-1]
                args = [parsing_function(a) for a in string.split(',')]

                if len(args) != self.args_number or any(a is None for a in args):
                    return None
                return Function.concat(args, self.operation)


class Brace:
    def __init__(self, opening_character, closing_character, operation=None):
        self.opening_character = opening_character
        self.closing_character = closing_character
        self.operation = operation

    def parse(self, string, parsing_function, braces_pairs):
        if len(string) > 1 \
                and string[0] == self.opening_character \
                and string[-1] == self.closing_character:

            argument = parsing_function(string[1:-1])

            if argument is None:
                return None

            return argument \
                if self.operation is None \
                else Function.concat([argument], self.operation)
        else:
            return None


class VariableOperator:
    @staticmethod
    def parse(string, parsing_function, braces_pairs):
        if string == "x":
            v = Value(0)
            return Function(v, [v])
        return None


class ConstantOperator:
    @staticmethod
    def parse(string, parsing_function, braces_pairs):
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

    def parse(self, string, parsing_function, braces_pairs):
        """Returns None, if parsing is not possible, else new function"""

        opening_braces = [pair[0] for pair in braces_pairs]
        closing_braces = [pair[1] for pair in braces_pairs]
        braces_counters = [0] * len(braces_pairs)

        operator_position = len(string) - 1

        for s in string[::-1]:
            try:
                brace_index = opening_braces.index(s)
            except ValueError:
                pass
            else:
                braces_counters[brace_index] += 1

            try:
                brace_index = closing_braces.index(s)
            except ValueError:
                pass
            else:
                braces_counters[brace_index] -= 1

            if all(b == 0 for b in braces_counters) and s == self.character:
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
        self.braces_pairs = [(b.opening_character, b.closing_character) for b in braces]

    def parse(self, string):
        string = string.replace(" ", "")
        try:
            string = string.split("=")[1]
        except IndexError:
            raise Exception("Wrong format: '<function_name>=' is required")
        return self._parse(string)

    def _parse(self, string):
        for o in self.operators:
            result = o.parse(string, self._parse, self.braces_pairs)

            if result is not None:
                return result
        return None


default_parser = Parser(
    [
        Operator("+", Addition),
        Operator("-", Deduction),
        Operator("*", Multiplication),
        Operator("/", Division),

        Operator("^", Power),

        FunctionOperator("sin", Sinus, 1),
        FunctionOperator("log", Logarithm, 2),

        VariableOperator,
        ConstantOperator,
    ],
    [
        Brace("(", ")"),
        Brace("|", "|", operation=Modulus),
    ])
