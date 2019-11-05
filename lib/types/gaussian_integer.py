#   numth/types/gaussian_integer.py
#===========================================================
import operator as op

from ..basic import mod_inverse
from .quadratic import *
from .gaussian_rational import GaussianRational
#===========================================================

class GaussianInteger(GaussianRational):

    def __init__(self, real, imag, *args):
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

    @property
    def to_gaussian_rational(self):
        return GaussianRational(*self.components)

    #=========================

    def _eq_GaussianInteger(self, other):
        return self.components == other.components

    #=========================

    def _gcd_GaussianInteger(self, other):
        a, b = self, other
        while b.components != (0, 0):
            a, b = b, a % b
        return a.canonical

    def _gcd_int(self, other):
        return self.gcd_GaussianInteger(GaussianInteger(other, 0))

    def _gcd_QuadraticInteger(self, other):
        return self.gcd_GaussianInteger(GaussianInteger(*other.components))

    def gcd(self, other):
        return self.execute('gcd', other)

    @property
    def round(self):
        return self

    def mod_inverse(self, modulus):
        norm_inverse = mod_inverse(self.norm, modulus)
        return GaussianInteger(
            *map(lambda x: (x * norm_inverse) % modulus, (self.real, -self.imag)),
        )

    #=========================

    def _add_GaussianInteger(self, other):
        return GaussianInteger(*add_(self, other))

    #=========================

    def _mul_GaussianInteger(self, other):
        return GaussianInteger(*mul_(self, other))

    #=========================

    def _truediv_GaussianInteger(self, other):
        return self * other.inverse

    #=========================

    def _floordiv_GaussianInteger(self, other):
        return GaussianInteger(*floordiv_(self, other))

    #=========================

    def _mod_GaussianInteger(self, other):
        return self - (self // other) * other

    #=========================

    def _inv_pow_mod_int(self, other, modulus):
        return self.__pow__(-other, modulus).mod_inverse(modulus)

