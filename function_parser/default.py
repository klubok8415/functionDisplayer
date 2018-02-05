from expressions.math.other import *
from expressions.math.powers import *
from expressions.math.simple import *
from expressions.math.trigonometry import *
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
        FunctionOperator("cos", Cosine, 1),
        FunctionOperator("tan", Tangent, 1),
        FunctionOperator("cot", Cotangent, 1),

        FunctionOperator("log", Logarithm, 2),

        VariableOperator,
        ConstantOperator,
    ],
    [
        Brace("(", ")"),
        Brace("|", "|", operation=Modulus),
        Brace("[", "]", operation=Floor),
        Brace("{", "}", operation=Truncate),
    ])