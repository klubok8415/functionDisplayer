import math

import re

from expressions.core import Value
from function_parser.lexis.lexis_element import LexisElement
from function_parser.lexis_helper import startswith, endswith, split
from function_parser.parser import ParsingData


class Operator:
    def parse(self, lexis_string, braces_pairs):
        raise NotImplementedError()

    def get_determinants(self):
        raise NotImplementedError()


class Prefix(Operator):
    TYPE_NAME = "prefix"

    def __init__(self, name, operation):
        self.name = name
        self.operation = operation

    def parse(self, lexis_string, braces_pairs):
        if not startswith(lexis_string, [LexisElement(self.name, Prefix.TYPE_NAME)]):
            return []

        return [ParsingData(
            self.operation,
            [lexis_string[1:]]
        )]

    def get_determinants(self):
        return [
            lambda s: [LexisElement(self.name, Prefix.TYPE_NAME)] if s.startswith(self.name) else []
        ]


class FunctionOperator(Operator):
    FUNCTION_NAME_TYPE = "function name"
    OPENING_BRACE_TYPE = "function opening brace"
    CLOSING_BRACE_TYPE = "function closing brace"
    SEPARATOR_TYPE = "function separator"

    def __init__(self, name, operation, args_number, opening_brace="(", closing_brace=")", separator=","):
        self.operation = operation
        self.args_number = args_number

        self.name = LexisElement(name, FunctionOperator.FUNCTION_NAME_TYPE)
        self.opening_brace = LexisElement(opening_brace, FunctionOperator.OPENING_BRACE_TYPE)
        self.closing_brace = LexisElement(closing_brace, FunctionOperator.CLOSING_BRACE_TYPE)
        self.separator = LexisElement(separator, FunctionOperator.SEPARATOR_TYPE)

    def parse(self, lexis_string, braces_pairs):
        if startswith(lexis_string, [self.name, self.opening_brace]) \
                and endswith(lexis_string, [self.closing_brace]):
            args = split(
                lexis_string[len(self.name.string) + len(self.opening_brace.string):-len(self.closing_brace.string)],
                self.separator)

            if len(args) == self.args_number:
                return [ParsingData(self.operation, args, [])]
        return []

    def get_determinants(self):
        return [
            lambda s: [self.name] if s.startswith(self.name.string) else [],
            lambda s: [self.opening_brace] if s.startswith(self.opening_brace.string) else [],
            lambda s: [self.closing_brace] if s.startswith(self.closing_brace.string) else [],
            lambda s: [self.separator] if s.startswith(self.separator.string) else [],
        ]


class Brace(Operator):
    OPENING_BRACE_TYPE = "opening brace"
    CLOSING_BRACE_TYPE = "closing brace"

    def __init__(self, opening_brace, closing_brace, operation=None):
        self.opening_brace = LexisElement(opening_brace, Brace.OPENING_BRACE_TYPE)
        self.closing_brace = LexisElement(closing_brace, Brace.CLOSING_BRACE_TYPE)

        self.operation = operation

    def parse(self, lexis_string, braces_pairs):
        if startswith(lexis_string, [self.opening_brace]) and endswith(lexis_string, [self.closing_brace]):
            lexis_string = lexis_string[len(self.opening_brace.string):-len(self.closing_brace.string)]
        return []

        converted_opening_name = element_pattern.findall(self.opening_name)
        converted_closing_name = element_pattern.findall(self.closing_name)

        if startswith(lexis_string, converted_opening_name) and endswith(lexis_string, converted_closing_name):
            lexis_string = lexis_string[len(converted_opening_name):-len(converted_closing_name)]

            braces_counter = 0
            if converted_opening_name != converted_closing_name:
                for i in range(len(lexis_string)):
                    if startswith(lexis_string[i:], converted_opening_name):
                        braces_counter += 1
                    elif startswith(lexis_string[i:], converted_closing_name):
                        braces_counter -= 1

                        if braces_counter < 0:
                            return []

            return [ParsingData(
                self.operation,
                [lexis_string]
            )]
        return []

    def get_determinants(self):
        return [
            lambda s: [self.opening_brace] if s.startswith(self.opening_brace.string) else [],
            lambda s: [self.closing_brace] if s.startswith(self.closing_brace.string) else [],
        ]


class VariableOperator(Operator):
    TYPE_NAME = "variable"

    def parse(self, lexis_string, braces_pairs):
        if len(lexis_string) == 1 and LexisElement("x", VariableOperator.TYPE_NAME) in lexis_string[0]:
            v = Value(0)
            return [ParsingData(v, [], [v])]
        return []

    def get_determinants(self):
        return [
            lambda s: [LexisElement("x", VariableOperator.TYPE_NAME)] if s.startswith("x") else []
        ]


class ConstantOperator(Operator):
    TYPE_NAME = "constant"
    E = "e"
    PI = "pi"

    def parse(self, lexis_string, braces_pairs):
        first_element = lexis_string[0][0]

        if first_element.type != ConstantOperator.TYPE_NAME or len(lexis_string) != len(first_element.string):
            return []

        if first_element.string == ConstantOperator.E:
            value = math.e
        elif first_element.string == ConstantOperator.PI:
            value = math.pi
        else:
            try:
                value = float(first_element.string)
            except ValueError:
                return []
        return [ParsingData(Value(value), [])]

    @staticmethod
    def constant_determinant(string):
        m = re.match(r'^([\d.]+|' + ConstantOperator.E + r'|' + ConstantOperator.PI + r')', string)

        return [] if m is None else [LexisElement(m.group(0), ConstantOperator.TYPE_NAME)]

    def get_determinants(self):
        return [self.constant_determinant]


class InfixOperator(Operator):
    INFIX_TYPE = "infix operator"

    def __init__(self, infix, operation):
        self.infix = LexisElement(infix, InfixOperator.INFIX_TYPE)

        self.operation = operation

    def parse(self, lexis_string, braces_pairs):
        result = []
        for i in range(len(lexis_string)):
            if self.infix in lexis_string[i]:
                current_data = ParsingData(
                    self.operation,
                    [
                        lexis_string[:i],
                        lexis_string[i + len(self.infix.string):]
                    ]
                )

                if len(lexis_string[i]) == 1:
                    return [current_data]
                result.append(current_data)

        return result

        # opening_braces = [element_pattern.findall(pair[0]) for pair in braces_pairs]
        # closing_braces = [element_pattern.findall(pair[1]) for pair in braces_pairs]
        # braces_counters = [0] * len(braces_pairs)
        # result = []
        # converted_name = element_pattern.findall(self.name)
        #
        # for i in range(len(lexis_string) - 1, -1, -1):
        #     for b in opening_braces:
        #         if startswith(lexis_string[i:], b):
        #             braces_counters[opening_braces.index(b)] += 1
        #
        #     for b in closing_braces:
        #         if startswith(lexis_string[i:], b):
        #             braces_counters[closing_braces.index(b)] -= 1
        #
        #     if all(b == 0 for b in braces_counters) \
        #             and startswith(lexis_string[i:], converted_name) \
        #             and (len(converted_name) > 0 or i != 0):
        #         result += [ParsingData(
        #             self.operation,
        #             [
        #                 lexis_string[:i],
        #                 lexis_string[i + len(converted_name):],
        #             ]
        #         )]
        # return result

    def get_determinants(self):
        return [
            lambda s: [self.infix] if s.startswith(self.infix.string) else []
        ]
