import re

from expressions.core import Function


class ParsingData:
    def __init__(self, operation, arguments, new_variables=None):
        self.operation = operation
        self.arguments = arguments
        self.new_variables = [] if new_variables is None else new_variables


class Parser:
    def __init__(self, operators, braces, element_pattern=None):
        self.operators = braces + operators
        self.braces_pairs = [(b.opening_name, b.closing_name) for b in braces]
        self.element_pattern = re.compile(r'([\d.]+|\S)') if element_pattern is None else element_pattern

    def parse(self, string):
        return self._parse(self.element_pattern.findall(string))

    def _parse(self, string, forbidden_operators=None):
        if forbidden_operators is None:
            forbidden_operators = []

        if string == "":
            return None

        for o in (o for o in self.operators if o not in forbidden_operators):
            result = o.parse(string, self.braces_pairs, self.element_pattern)

            for data in result:
                args = [self._parse(a) for a in data.arguments]

                if any(a is None for a in args):
                    continue

                return args[0] \
                    if data.operation is None \
                    else Function.concat(args, data.operation, data.new_variables)
        return None
