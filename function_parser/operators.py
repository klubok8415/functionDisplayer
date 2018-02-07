from expressions.core import Value
from function_parser.parser import ParsingData


class Operator:
    def parse(self, string, braces_pairs):
        raise NotImplementedError()


class Prefix(Operator):
    def __init__(self, name, operation):
        self.name = name
        self.operation = operation

    def parse(self, string, braces_pairs):
        if not string.startswith(self.name):
            return []

        return [ParsingData(self.operation, [string[len(self.name):]], [])]


class FunctionOperator(Operator):
    def __init__(self, name, operation, args_number):
        self.name = name
        self.operation = operation
        self.args_number = args_number

    def parse(self, string, braces_pairs):
        if len(string) > len(self.name) + 2 \
                and string.endswith(")") \
                and string.startswith(self.name) \
                and len(self.name) < len(string) \
                and string[len(self.name)] == "(":

            args = string[len(self.name) + 1:-1].split(',')

            if len(args) == self.args_number:
                return [ParsingData(self.operation, args, [])]
        return []


class Brace(Operator):
    def __init__(self, opening_character, closing_character, operation=None):
        self.opening_character = opening_character
        self.closing_character = closing_character
        self.operation = operation

    def parse(self, string, braces_pairs):
        if string.startswith(self.opening_character) and string.endswith(self.closing_character):
            return [ParsingData(self.operation, [string[len(self.opening_character):-len(self.closing_character)]], [])]
        return []


class VariableOperator(Operator):
    def parse(self, string, braces_pairs):
        if string == "x":
            v = Value(0)
            return [ParsingData(v, [], [v])]
        return []


class ConstantOperator(Operator):
    def parse(self, string, braces_pairs):
        try:
            value = float(string)
        except ValueError:
            return []
        else:
            return [ParsingData(Value(value), [], [])]


class InfixOperator(Operator):
    def __init__(self, name, operation):
        self.name = name
        self.operation = operation

    def parse(self, string, braces_pairs):
        opening_braces = [pair[0] for pair in braces_pairs]
        closing_braces = [pair[1] for pair in braces_pairs]
        braces_counters = [0] * len(braces_pairs)
        result = []

        for i in range(len(string) - 1, -1, -1):
            for b in opening_braces:
                if string[i:].startswith(b):
                    braces_counters[opening_braces.index(b)] += 1

            for b in closing_braces:
                if string[i:].startswith(b):
                    braces_counters[closing_braces.index(b)] -= 1

            if all(b == 0 for b in braces_counters) \
                    and string[i:].startswith(self.name) \
                    and (len(self.name) > 0 or i != 0):
                result += [ParsingData(self.operation, [string[:i], string[i + len(self.name):]], [])]
        return result
