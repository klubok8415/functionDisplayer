from expressions.core import Function


class ParsingData:
    def __init__(self, operation, arguments, new_variables):
        self.operation = operation
        self.arguments = arguments
        self.new_variables = new_variables


class Parser:
    def __init__(self, operators, braces):
        self.operators = braces + operators
        self.braces_pairs = [(b.opening_character, b.closing_character) for b in braces]

    def parse(self, string):
        string = string.replace(" ", "")
        return self._parse(string)

    def _parse(self, string):
        if string == "":
            return None

        for o in self.operators:
            result = o.parse(string, self.braces_pairs)

            if result is not None:
                args = [self._parse(a) for a in result.arguments]

                if any(a is None for a in args):
                    continue

                return args[0] \
                    if result.operation is None \
                    else Function.concat(args, result.operation, result.new_variables)
        return None
