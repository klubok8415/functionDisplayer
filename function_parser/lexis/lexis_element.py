class LexisElement:
    def __init__(self, string, type_):
        self.string = string
        self.type = type_

    def __eq__(self, other):
        return self.string == other.string

    def __str__(self):
        return str.format('<{type}: "{string}"', type=self.type, string=self.string)
