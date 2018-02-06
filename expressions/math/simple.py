import math
import numpy
from expressions.core import Operation, Value


class Addition(Operation):
    def calculate(self):
        return sum(a.calculate() for a in self.args)

    def differentiate(self):
        return Value(0)


class Multiplication(Operation):
    def calculate(self):
        return self.args[0].calculate() * self.args[1].calculate()

    def differentiate(self):
        return Addition(
            Multiplication(self.args[0], self.args[1].differentiate()),
            Multiplication(self.args[0].differentiate(), self.args[1]),
        )


class AdditiveInversion(Multiplication):
    def __init__(self, *args):
        super(AdditiveInversion, self).__init__(Value(-1), args[0])


class Deduction(Addition):
    def __init__(self, *args):
        super(Deduction, self).__init__(args[0], AdditiveInversion(args[1]))


class Power(Operation):
    def calculate(self):
        x = self.args[0].calculate()
        power = self.args[1].calculate()

        return numpy.nan if (x == 0 and power < 0) or (x < 0 and math.modf(power)[0] != 0) else x**power

    def differentiate(self):
        return Multiplication()


class MultiplicativeInversion(Power):
    def __init__(self, *args):
        super(MultiplicativeInversion, self).__init__(args[0], Value(-1))


class Division(Multiplication):
    def __init__(self, *args):
        super(Division, self).__init__(args[0], MultiplicativeInversion(args[1]))


class Logarithm(Operation):
    def calculate(self):
        x = self.args[0].calculate()
        base = self.args[1].calculate()

        return math.log(x, base) if base > 0 and base != 1 and x > 0 else numpy.nan


class Sqrt(Power):
    def __init__(self, *args):
        super(Sqrt, self).__init__(args[0], Value(0.5))
