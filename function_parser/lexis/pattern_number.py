class PatternNumber:
    ANY = lambda v0, v1, it: True
    MORE = lambda v0, v1, it: it > v0
    MORE_OR_EQUAL = lambda v0, v1, it: it >= v0
    LESS = lambda v0, v1, it: it < v0
    LESS_OR_EQUAL = lambda v0, v1, it: it <= v0
    BETWEEN = lambda v0, v1, it: v0 < it < v1
    EXACTLY = lambda v0, v1, it: it == v0

    def __init__(self, _type, value0=0, value1=0):
        self.type = _type
        self.value0 = value0
        self.value1 = value1

    def match(self, integer):
        return self.type(self.value0, self.value1, integer)

    def __eq__(self, item):
        if isinstance(item, PatternNumber):
            return self.type == item.type and self.value0 == item.value0 and self.value1 == item.value1

        return self.match(item)

    def __str__(self):
        result = "Number pattern: "

        if self.type == PatternNumber.ANY:
            result += "Any number"
        elif self.type == PatternNumber.MORE:
            result += str.format("number > {0}", self.value0)
        elif self.type == PatternNumber.MORE_OR_EQUAL:
            result += str.format("number >= {0}", self.value0)
        elif self.type == PatternNumber.LESS:
            result += str.format("number < {0}", self.value0)
        elif self.type == PatternNumber.LESS_OR_EQUAL:
            result += str.format("number <= {0}", self.value0)
        elif self.type == PatternNumber.BETWEEN:
            result += str.format("{0} < number < {1}", self.value0, self.value1)
        elif self.type == PatternNumber.EXACTLY:
            result += str.format("number == {0}", self.value0)
        else:
            result += str(self.type)

        return result

    @staticmethod
    def any():
        return PatternNumber(PatternNumber.ANY)

    @staticmethod
    def more(value):
        return PatternNumber(PatternNumber.MORE, value)

    @staticmethod
    def more_or_equal(value):
        return PatternNumber(PatternNumber.MORE_OR_EQUAL, value)

    @staticmethod
    def less(value):
        return PatternNumber(PatternNumber.LESS, value)

    @staticmethod
    def less_or_equal(value):
        return PatternNumber(PatternNumber.LESS_OR_EQUAL, value)

    @staticmethod
    def between(lower_value, greater_value):
        return PatternNumber(PatternNumber.BETWEEN, lower_value, greater_value)

    @staticmethod
    def exactly(value):
        return PatternNumber(PatternNumber.EXACTLY, value)
