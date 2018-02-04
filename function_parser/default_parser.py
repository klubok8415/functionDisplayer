from expressions.simple_math import *
from expressions.trigonometry import *
from function_parser.operators import *
from function_parser.parser import Parser

default_parser = Parser(
    [
        Operator("+", Addition),
        Operator("-", Deduction),

        Prefix("-", Inversion),

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