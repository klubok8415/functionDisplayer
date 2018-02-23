from expressions.math.other import *
from expressions.math.simple import *
from expressions.math.trigonometry import *
from function_parser.operators import *
from function_parser.parser import Parser

default_parser = Parser(
    [
        InfixOperator("+", Addition),
        InfixOperator("-", Deduction),

        Prefix("-", AdditiveInversion),

        InfixOperator("*", Multiplication),
        InfixOperator("", Multiplication),
        InfixOperator("/", Division),

        InfixOperator("**", Power),
        InfixOperator("ˆ", Power),

        FunctionOperator("sin", Sinus, 1),
        FunctionOperator("cos", Cosine, 1),
        FunctionOperator("tan", Tangent, 1),
        FunctionOperator("cot", Cotangent, 1),

        FunctionOperator("arcsin", Arcsine, 1),
        FunctionOperator("arccos", Arccosine, 1),
        FunctionOperator("arctan", Arctangent, 1),
        FunctionOperator("arccot", Arccotangent, 1),

        FunctionOperator("log", Logarithm, 2),
        FunctionOperator("ln", NaturalLogarithm, 1),

        FunctionOperator("sqrt", Sqrt, 1),

        VariableOperator(),
        ConstantOperator(),
    ],
    [
        Brace("(", ")"),
        Brace("|", "|", operation=Modulus),
        Brace("[", "]", operation=Floor),
        Brace("{", "}", operation=Truncate),
    ])