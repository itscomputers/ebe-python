#   numth/types/quadratic_integer.py
#===========================================================
import operator as op

from ..basic import mod_inverse
from .quadratic import Quadratic
from .rational import Rational
#===========================================================

class QuadraticInteger(Quadratic):

    def __init__(self, real, imag, root):
        self._real = int(real)
        self._imag = int(imag)
        self._root = int(root)

    #=========================

    @property
    def _root_display(self):
        if self.is_complex:
            return '\u2139'
        return '\u221a{}'.format(self.root)

    #=========================

    def from_components(self, *components):
        return QuadraticInteger(*components, self.root)

    @property
    def to_quadratic(self):
        return Quadratic(self._real, self._imag, self._root)

    #=========================

    def _eq_QuadraticInteger(self, other):
        return self.signature == other.signature

    #=========================

    @property
    def round(self):
        return self

    def mod_inverse(self, modulus):
        norm_inverse = mod_inverse(self.norm, modulus)
        return self.from_components(
            *map(lambda x: (x * norm_inverse) % modulus, (self.real, -self.imag)),
        )

    #=========================

    def _add_QuadraticInteger(self, other):
        if self.root != other.root:
            return NotImplemented
        return QuadraticInteger(
            *map(op.__add__, self.components, other.components),
            self.root
        )

    #=========================

    def _mul_QuadraticInteger(self, other):
        if self.root != other.root:
            return NotImplemented
        return QuadraticInteger(
            self.real * other.real + self.imag * other.imag * self.root,
            self.real * other.imag + self.imag * other.real,
            self.root
        )

    def _rmul_Quadratic(self, other):
        return self * other

    #=========================

    def _truediv_QuadraticInteger(self, other):
        if self.root != other.root:
            return NotImplemented
        return self * other.inverse

    def _rtruediv_Quadratic(self, other):
        if self.root != other.root:
            return NotImplemented
        return self.inverse * other

    #=========================

    def _floordiv(self, other):
        return QuadraticInteger(*(self / other).round.signature)

    def _floordiv_Quadratic(self, other):
        if self.root != other.root:
            return NotImplemented
        return self._floordiv(other)

    def _floordiv_QuadraticInteger(self, other):
        if self.root != other.root:
            return NotImplemented
        return self._floordiv(other)

    def _rfloordiv(self, other):
        return QuadraticInteger(*(self.inverse * other).round.signature)

    def _rfloordiv_int(self, other):
        return self._rfloordiv(other)

    def _rfloordiv_Rational(self, other):
        return self._rfloordiv(other)

    def _rfloordiv_Quadratic(self, other):
        return self._rfloordiv(other)

    #=========================

    def _mod_QuadraticInteger(self, other):
        if self.root != other.root:
            return NotImplemented
        return self - (self // other) * other

    def _rmod_Quadratic(self, other):
        if self.root != other.root:
            return NotImplemented
        return other - (other // self) * self

    #=========================

    def _inv_pow_mod_int(self, other, modulus):
        return self.__pow__(-other, modulus).mod_inverse(modulus)

