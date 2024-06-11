#   lib/types/gaussian_rational.py
#   - class for arithmetic of gaussian rational numbers

# ===========================================================
import operator as op

from .rational import frac
from .quadratic import *
from .quadratic_integer import QuadraticInteger

# ===========================================================
__all__ = [
    "GaussianRational",
]
# ===========================================================


class GaussianRational(Quadratic):
    """
    Class that represents `real + imag * sqrt(-1)`,
    where `real` and `imag` are rational numbers.

    The class implements arithmetic operations with members of itself,
    general quadratic numbers and quadratic integers (if `root == -1`),
    integers, and rational numbers.

    Much of the functionality is inherited from `lib.types.Quadratic`
    and any operation with any compatible type returns a gaussian rational.

    + real: Union[int, float, Rational]
    + imag: Union[int, float, Rational]
    """

    def __init__(self, real, imag, *args):
        self._real = frac(real)
        self._imag = frac(imag)
        self._root = -1

    @property
    def is_complex(self):
        return True

    # =========================

    @property
    def _root_display(self):
        return "\u2139"

    # =========================

    @property
    def to_quadratic(self):
        """Cast to Quadratic."""
        return Quadratic(*self.signature)

    # =========================

    def _eq_GaussianRational(self, other):
        return self.components == other.components

    def _eq_QuadraticInteger(self, other):
        return self.components == other.components

    # =========================

    @property
    def canonical(self):
        if abs(self.real) < abs(self.imag):
            canonical = self.__class__(-self.imag, self.real)
        elif self.real == -self.imag:
            canonical = self.__class__(self.imag, -self.real)
        else:
            canonical = self

        return -canonical if canonical.real < 0 else canonical

    # =========================

    def _add_Rational(self, other):
        return GaussianRational(*add_constant(self, other))

    def _add_GaussianRational(self, other):
        return GaussianRational(*add_(self, other))

    def _add_Quadratic(self, other):
        if other.is_complex:
            return GaussianRational(*add_(self, other))
        return NotImplemented

    def _add_QuadraticInteger(self, other):
        if other.is_complex:
            return self.__class__(*add_(self, other))
        return NotImplemented

    # =========================

    def _mul_Rational(self, other):
        return GaussianRational(*mul_constant(self, other))

    def _mul_GaussianRational(self, other):
        return GaussianRational(*mul_(self, other))

    def _mul_Quadratic(self, other):
        if other.is_complex:
            return GaussianRational(*mul_(self, other))
        return NotImplemented

    def _mul_QuadraticInteger(self, other):
        if other.is_complex:
            return self.__class__(*mul_(self, other))
        return NotImplemented

    # =========================

    def _truediv_int(self, other):
        return GaussianRational(*truediv_constant(self, other))

    def _truediv_Rational(self, other):
        return GaussianRational(*truediv_constant(self, other))

    def _truediv_GaussianRational(self, other):
        return GaussianRational(*truediv_(self, other))

    def _truediv_Quadratic(self, other):
        if other.is_complex:
            return GaussianRational(*truediv_(self, other))
        return NotImplemented

    def _truediv_QuadraticInteger(self, other):
        if other.is_complex:
            return GaussianRational(*truediv_(self, other))
        return NotImplemented

    # =========================

    def _floordiv_GaussianRational(self, other):
        return self.__class__(*floordiv_(self, other))

    def _floordiv_Quadratic(self, other):
        if other.is_complex:
            return self.__class__(*floordiv_(self, other))
        return NotImplemented

    def _floordiv_QuadraticInteger(self, other):
        if other.is_complex:
            return self.__class__(*floordiv_(self, other))
        return NotImplemented

    # =========================

    def _mod_Rational(self, other):
        return GaussianRational(*mod_constant(self, other))

    def _mod_GaussianRational(self, other):
        return self - (self // other) * other

    def _mod_Quadratic(self, other):
        return self - (self // other) * other

    def _mod_QuadraticInteger(self, other):
        return self - (self // other) * other
