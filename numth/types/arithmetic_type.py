#   numth/types/arithmetic_type.py
#===========================================================


class ArithmeticType:


    def execute(self, operation, other, *args):
        method_name = '_{}_{}'.format(operation, other.__class__.__name__)
        if hasattr(self, method_name):
            return eval('self.{}'.format(method_name))(other, *args)
        return NotImplemented

    #=========================

    def __eq__(self, other):
        return self.execute('eq', other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.execute('lt', other)

    def __gt__(self, other):
        return self.execute('gt', other)

    def __le__(self, other):
        return not self.__gt__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    #=========================

    def __pos__(self):
        return self

    def __neg__(self):
        return NotImplemented

    #=========================

    def __add__(self, other):
        return self.execute('add', other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        return self.execute('mul', other)

    def __rmul__(self, other):
        return self.execute('rmul', other)

    def __truediv__(self, other):
        return self.execute('truediv', other)

    def __rtruediv__(self, other):
        return self.execute('rtruediv', other)

    def __floordiv__(self, other):
        return self.execute('floordiv', other)

    def __rfloordiv__(self, other):
        return self.execute('rfloordiv', other)

    def __mod__(self, other):
        return self.execute('mod', other)

    def __rmod__(self, other):
        return self.execute('rmod', other)

    #=========================

    def _pow(self, other):
        if other < 0:
            return self.execute('inv_pow', other)

        if other == 0:
            return self.execute('zero_pow', other)

        if other == 1:
            return self

        if other % 2 == 0:
            return (self * self)._pow(other // 2)

        return self * (self * self)._pow(other // 2)

    def _pow_mod(self, other, modulus):
        if other < 0:
            return self.execute('inv_pow_mod', other, modulus)

        if other == 0:
            return self.execute('zero_pow', other)

        if other == 1:
            return self % modulus

        if other % 2 == 0:
            return (self * self)._pow_mod(other // 2, modulus)

        return (self * (self * self)._pow_mod(other // 2, modulus)) % modulus

    def __pow__(self, other, modulus=None):
        if not isinstance(other, int):
            return NotImplemented

        if modulus is None:
            return self._pow(other)

        return self._pow_mod(other, modulus)

