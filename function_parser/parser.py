from expressions.core import Function


class Argument:
    def __init__(self, string, forbidden_operators=None):
        self.string = string
        self.forbidden_operations = [] if forbidden_operators is None else forbidden_operators


class ParsingData:
    def __init__(self, operation, arguments, new_variables=None):
        self.operation = operation
        self.arguments = arguments
        self.new_variables = [] if new_variables is None else new_variables


class Parser:
    def __init__(self, operators, braces):
        self.operators = braces + operators
        self.braces_pairs = [(b.opening_character, b.closing_character) for b in braces]

    def parse(self, string):
        return self._parse(string.replace(" ", ""))

    def _parse(self, string, forbidden_operators=None):
        if forbidden_operators is None:
            forbidden_operators = []

        if string == "":
            return None

        for o in (o for o in self.operators if o not in forbidden_operators):
            result = o.parse(string, self.braces_pairs)

            for data in result:
                args = [self._parse(a.string, a.forbidden_operations) for a in data.arguments]

                if any(a is None for a in args):
                    continue

                return args[0] \
                    if data.operation is None \
                    else Function.concat(args, data.operation, data.new_variables)
        return None
