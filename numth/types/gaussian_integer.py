#   numth/types/gaussian_integer.py
#===========================================================
import operator as op

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

    def from_components(self, *components):
        return GaussianInteger(*components)

    @property
    def to_quadratic_integer(self):
        return QuadraticInteger(*self.signature)

    @property
    def to_quadratic(self):
        return Quadratic(*self.signature)

    #=========================

    def _eq_GaussianInteger(self, other):
        return self.components == other.components

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

    def gcd(self, other):
        if isinstance(other, GaussianInteger):
            a, b = self, other
            while b.components != (0, 0):
                a, b = b, a % b
            return a.canonical

        if isinstance(other, int):
            return self.gcd(GaussianInteger(other, 0))

        if isinstance(other, QuadraticInteger) and other.is_complex:
            return self.gcd(GaussianInteger(*other.components))

        return NotImplemented

    #=========================

    def _add_GaussianInteger(self, other):
        return GaussianInteger(
            *map(op.__add__, self.components, other.components)
        )

    def _add_QuadraticInteger(self, other):
        if not other.is_complex:
            return NotImplemented
        return self._add_GaussianInteger(other)

    #=========================

    def _mul_GaussianInteger(self, other):
        return GaussianInteger(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real
        )

    def _mul_QuadraticInteger(self, other):
        if not other.is_complex:
            return NotImplemented
        return self._mul_GaussianInteger(other)

    #=========================

    def _truediv_GaussianInteger(self, other):
        return self * other.inverse

    def _rtruediv_QuadraticInteger(self, other):
        if not other.is_complex:
            return NotImplemented
        return self.inverse * other

    #=========================

    def _floordiv(self, other):
        return GaussianInteger(*(self / other).round.components)

    def _floordiv_GaussianInteger(self, other):
        return self._floordiv(other)

    def _floordiv_QuadraticInteger(self, other):
        if not other.is_complex:
            return NotImplemented
        return self._floordiv(other)

    def _rfloordiv(self, other):
        return GaussianInteger(*(self.inverse * other).round.components)

    def _rfloordiv_QuadraticInteger(self, other):
        if not other.is_complex:
            return NotImplemented
        return self._rfloordiv(other)

    #=========================

    def _mod_GaussianInteger(self, other):
        return self - (self // other) * other

    def _rmod_QuadraticInteger(self, other):
        if not other.is_complex:
            return NotImplemented
        return other - (other // self) * self

