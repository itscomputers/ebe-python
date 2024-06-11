#   lib/types/quadratic.py
#   - class for arithmetic of quadratic numbers

# ===========================================================
import math
import operator as op

from .arithmetic_type import ArithmeticType
from .rational import frac, Rational

# ===========================================================
__all__ = [
    "add_",
    "add_constant",
    "mul_",
    "mul_constant",
    "truediv_",
    "truediv_constant",
    "floordiv_",
    "floordiv_constant",
    "mod_constant",
    "Quadratic",
]
# ===========================================================


def add_(a, b):
    """Shortcut to add other quadratic numbers."""
    return map(op.__add__, a.components, b.components)


def add_constant(a, b):
    """Shortcut to add rational numbers and integers."""
    return (a.real + b, a.imag)


def mul_(a, b):
    """Shortcut to multiply by other quadratic numbers."""
    return (a.real * b.real + a.imag * b.imag * a.root, a.real * b.imag + a.imag * b.real)


def mul_constant(a, b):
    """Shortcut to multiply by rational numbers and integers."""
    return map(lambda x: x * b, a.components)


def truediv_(a, b):
    """Shortcut to divide by other quadratic numbers."""
    norm = frac(b.norm)
    return (
        (a.real * b.real - a.imag * b.imag * a.root) / norm,
        (-a.real * b.imag + a.imag * b.real) / norm,
    )


def truediv_constant(a, b):
    """Shortcut to divide by rational numbers and integers."""
    return map(lambda x: x / frac(b), a.components)


def floordiv_(a, b):
    """Shortcut to floor divide by other quadratic numbers."""
    return (a / b).round.components


def floordiv_constant(a, b):
    """Shortcut to floor divide by rational numbers and integers."""
    return map(lambda x: x // b, a.components)


def mod_constant(a, b):
    """Shortcut to mod by rational numbers and integers."""
    return map(lambda x: x % b, a.components)


# ===========================================================


class Quadratic(ArithmeticType):
    """
    Class that represents `real + imag * sqrt(root)`,
    where `real`, `imag`, and `root` are rational numbers.

    The class implements arithmetic operations with members of itself,
    integers, and rational numbers.

    + real: Union[int, float, Rational]
    + imag: Union[int, float, Rational]
    + root: Union[int, float, Rational]
    """

    def __init__(self, real, imag, root):
        self._real = frac(real)
        self._imag = frac(imag)
        self._root = frac(root)

    @property
    def real(self):
        return self._real

    @property
    def imag(self):
        return self._imag

    @property
    def root(self):
        return self._root

    @property
    def components(self):
        return (self.real, self.imag)

    @property
    def signature(self):
        return (*self.components, self.root)

    @property
    def is_real(self):
        return self.root >= 0

    @property
    def is_complex(self):
        return self.root == -1

    # =========================

    @property
    def _root_display(self):
        if self.is_complex:
            return "\u2139"
        elif self.root.denom == 1:
            return "\u221a{}".format(self.root)
        else:
            return "\u221a({})".format(self.root)

    @property
    def _real_display(self):
        if self.real == 0 and self.imag != 0:
            return None
        return format(self.real)

    @property
    def _imag_display(self):
        if self.imag == 0:
            return None
        if self.imag == 1:
            return self._root_display
        elif self.imag == -1:
            return "-{}".format(self._root_display)
        return "{} {}".format(self.imag, self._root_display)

    def __repr__(self):
        real = self._real_display
        imag = self._imag_display

        if real is None:
            return imag

        if imag is None:
            return real

        return "{} + {}".format(real, imag).replace(" + -", " - ")

    # =========================

    def _eq_int(self, other):
        return self.imag == 0 and self.real == other

    def _eq_Rational(self, other):
        return self.imag == 0 and self.real == other

    def _eq_Quadratic(self, other):
        return self.signature == other.signature

    # =========================

    def __neg__(self):
        return self.__class__(*map(op.__neg__, self.components), self.root)

    def __abs__(self):
        return abs(self.norm)

    @property
    def conjugate(self):
        return self.__class__(self.real, -self.imag, self.root)

    @property
    def norm(self):
        return self.real**2 - self.root * self.imag**2

    @property
    def inverse(self):
        return self.conjugate / frac(self.norm)

    @property
    def round(self):
        return self.__class__(
            *map(lambda x: x.round_prefer_toward_zero, self.components), self.root
        )

    # =========================

    def _add_int(self, other):
        return self.__class__(*add_constant(self, other), self.root)

    def _add_Rational(self, other):
        return Quadratic(*add_constant(self, other), self.root)

    def _add_Quadratic(self, other):
        if self.root == other.root:
            return Quadratic(*add_(self, other), self.root)
        return NotImplemented

    # -------------------------

    def _mul_int(self, other):
        return self.__class__(*mul_constant(self, other), self.root)

    def _mul_Rational(self, other):
        return Quadratic(*mul_constant(self, other), self.root)

    def _mul_Quadratic(self, other):
        if self.root == other.root:
            return Quadratic(*mul_(self, other), self.root)
        return NotImplemented

    def __rmul__(self, other):
        return self * other

    # -------------------------

    def _truediv_int(self, other):
        return Quadratic(*truediv_constant(self, other), self.root)

    def _truediv_Rational(self, other):
        return Quadratic(*truediv_constant(self, other), self.root)

    def _truediv_Quadratic(self, other):
        if self.root == other.root:
            return Quadratic(*truediv_(self, other), self.root)
        return NotImplemented

    def __rtruediv__(self, other):
        return self.inverse * other

    # -------------------------

    def _floordiv_int(self, other):
        return self.__class__(*floordiv_constant(self, other), self.root)

    def _floordiv_Rational(self, other):
        return self.__class__(*floordiv_constant(self, other), self.root)

    def _floordiv_Quadratic(self, other):
        if self.root == other.root:
            return self.__class__(*floordiv_(self, other), self.root)
        return NotImplemented

    def __rfloordiv__(self, other):
        return self.__class__(*floordiv_(other, self), self.root)

    # -------------------------

    def _mod_int(self, other):
        return self.__class__(*mod_constant(self, other), self.root)

    def _mod_Rational(self, other):
        return Quadratic(*mod_constant(self, other), self.root)

    def _mod_Quadratic(self, other):
        if self.root == other.root:
            return self - (self // other) * other
        return NotImplemented

    def __rmod__(self, other):
        return other - (other // self) * self

    # -------------------------

    def _inv_pow_int(self, other):
        return self.__pow__(-other).inverse

    def _zero_pow_int(self, _other):
        return self.__class__(1, 0, self.root)

    # =========================

    def rational_approx(self, num_digits=None):
        """Compute rational approximation if `root` is positive."""
        if self.imag == 0:
            return self.real

        if not self.is_real:
            raise ValueError("No rational approximation possible for non-real number")

        abs_imag = frac(self.imag)

        if abs_imag.numer >= abs_imag.denom:
            log_ten = len(str(int(abs_imag)))
        else:
            log_ten = len(str(int(abs_imag.inverse)))

        approx_sqrt = frac(self.root).sqrt(num_digits + log_ten + 1)

        return self.real + self.imag * approx_sqrt

    def decimal(self, num_digits=None):
        return self.rational_approx(num_digits).decimal(num_digits)

    def __int__(self):
        return int(self.rational_approx(1))

    def __floor__(self):
        return math.floor(self.rational_approx(1))

    def __round__(self):
        return round(self.rational_approx(1))

    def __float__(self):
        return float(self.rational_approx(20))
