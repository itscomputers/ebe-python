#   numth/types/quadratic_integer.py
#===========================================================
import operator as op

from ..basic import mod_inverse
from .quadratic import *
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
        return (self.conjugate * mod_inverse(self.norm, modulus)) % modulus

    #=========================

    def _add_QuadraticInteger(self, other):
        if self.root == other.root:
            return QuadraticInteger(*add_(self, other), self.root)

    #=========================

    def _mul_QuadraticInteger(self, other):
        if self.root == other.root:
            return QuadraticInteger(*mul_(self, other), self.root)

    #=========================

    def _truediv_QuadraticInteger(self, other):
        if self.root == other.root:
            return Quadratic(*truediv_(self, other), self.root)
        return NotImplemented

    #=========================

    def _floordiv_Quadratic(self, other):
        if self.root == other.root:
            return QuadraticInteger(*(self / other).round.signature)
        return NotImplemented

    def _floordiv_QuadraticInteger(self, other):
        if self.root == other.root:
            return QuadraticInteger(*(self / other).round.signature)
        return NotImplemented

    #=========================

    def _mod_QuadraticInteger(self, other):
        if self.root == other.root:
            return self - (self // other) * other
        return NotImplemented

    #=========================

    def _inv_pow_mod_int(self, other, modulus):
        return self.__pow__(-other, modulus).mod_inverse(modulus)

