#   numth/types/gaussian_integer.py
#===========================================================
from .quadratic import Quadratic
from .quadratic_integer import QuadraticInteger
#===========================================================

class GaussianInteger(QuadraticInteger):

    def __init__(self, real, imag):
        self._real = int(real)
        self._imag = int(imag)
        self._root = -1

    @property
    def is_complex(self):
        return True

    #=========================

    @property
    def _root_display(self):
        return '\u2139'

    #=========================

    def is_same_type(self, other):
        return type(self) is type(other) \
            or type(other) is QuadraticInteger and other.root == -1

    #=========================

    @classmethod
    def from_signature(self, *signature):
        return GaussianInteger(*signature[:2])

    @property
    def to_quadratic_integer(self):
        return QuadraticInteger(*self.signature)

    @property
    def to_quadratic(self):
        return Quadratic(*self.signature)

    #=========================

    @property
    def canonical(self):
        if abs(self.real) < abs(self.imag):
            canonical = self * GaussianInteger(0, 1)
        elif self.real == -self.imag:
            canonical = self * GaussianInteger(0, -1)
        else:
            canonical = self

        return -canonical if canonical.real < 0 else canonical

    #=========================

    def gcd(self, other):
        if isinstance(other, int):
            return self.gcd(GaussianInteger(other, 0))

        if type(other) is QuadraticInteger and other.root == -1:
            return self.gcd(GaussianInteger(*other.components))

        if type(other) is GaussianInteger:
            a, b = self, other
            while b.components != (0, 0):
                a, b = b, a % b

            return a.canonical

        return NotImplemented

