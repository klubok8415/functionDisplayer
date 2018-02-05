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
            result = o.parse(string, self._parse, self.braces_pairs)

            if result is not None:
                return result
        return None
