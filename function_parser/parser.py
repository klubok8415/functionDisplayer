import re

from expressions.core import Function
from function_parser.lexis.lexis_analyzer import LexisAnalyzer


class ParsingData:
    def __init__(self, operation, arguments, new_variables=None):
        self.operation = operation
        self.arguments = arguments
        self.new_variables = [] if new_variables is None else new_variables


class Parser:
    def __init__(self, operators, braces):
        self.lexis_analyzer = LexisAnalyzer(sum([o.get_determinants() for o in operators], []))

        self.operators = braces + operators
        self.braces_pairs = [(b.opening_name, b.closing_name) for b in braces]

    def parse(self, string):
        return self._parse(self.lexis_analyzer.analyze(string))

    def _parse(self, lexis_string, forbidden_operators=None):
        if forbidden_operators is None:
            forbidden_operators = []

        if len(lexis_string) == 0 or len(lexis_string[0]) == 0:
            return None

        for o in (o for o in self.operators if o not in forbidden_operators):
            result = o.parse(lexis_string, self.braces_pairs)

            for data in result:
                args = [self._parse(a) for a in data.arguments]

                if any(a is None for a in args):
                    continue

                return args[0] \
                    if data.operation is None \
                    else Function.concat(args, data.operation, data.new_variables)
        return None
