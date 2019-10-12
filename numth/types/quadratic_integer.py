#   numth/types/quadratic_integer.py
#===========================================================
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
        if self.root == -1:
            return '\u2139'
        return '\u221a{}'.format(self.root)

    #=========================

    def is_similar_type(self, other):
        return type(other) is Quadratic and self.root == other.root

    #=========================

    @property
    def to_quadratic(self):
        return Quadratic(self._real, self._imag, self._root)

    #-------------------------

    @classmethod
    def from_signature(self, *signature):
        return QuadraticInteger(*signature)

    @classmethod
    def from_quadratic(self, quadratic):
        return self.from_signature(*quadratic.round.signature)

    #=========================

    @property
    def inverse(self):
        norm = self.norm
        if norm not in (1, -1):
            return self.conjugate / norm
        return self.conjugate * norm

    @property
    def round(self):
        return self

    #=========================

    def _add_rational(self, other):
        return self.to_quadratic + other

    def _add_similar_type(self, other):
        return self.to_quadratic + other

    #=========================

    def _mul_rational(self, other):
        return self.to_quadratic * other

    def _mul_similar_type(self, other):
        return self.to_quadratic * other

    #=========================

    def _div_int(self, other):
        return self.to_quadratic / other

    def _div_same_type(self, other):
        return self.to_quadratic / other

    def _floor_div_same_type(self, other):
        return self.from_components(*((self / other).round).components)

    #=========================

    def __rtruediv__(self, other):
        return self.to_quadratic.inverse * other

    def __rfloordiv__(self, other):
        if isinstance(other, (int, Rational)):
            return Quadratic(other, 0, self.root) // self

        if self.is_similar_type(other) or self.is_same_type(other):
            return self.from_quadratic((other / self).round)

