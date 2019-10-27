#   numth/types/quadratic.py
#===========================================================
import math
import operator as op

from .arithmetic_type import ArithmeticType
from .rational import frac, Rational
#===========================================================


class Quadratic(ArithmeticType):
    """
    Arithmetic class that represents `real + imag * sqrt(root)`.
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

    #=========================

    @property
    def _root_display(self):
        if self.is_complex:
            return '\u2139'
        elif self.root.denom == 1:
            return '\u221a{}'.format(self.root)
        else:
            return '\u221a({})'.format(self.root)

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
            return '-{}'.format(self._root_display)
        return '{} {}'.format(self.imag, self._root_display)

    def __repr__(self):
        real = self._real_display
        imag = self._imag_display

        if real is None:
            return imag

        if imag is None:
            return real

        return '{} + {}'.format(real, imag).replace(' + -', ' - ')

    #=========================

    def from_components(self, *components):
        return Quadratic(*components, self.root)

    #=========================

    def _eq_int(self, other):
        return self.imag == 0 and self.real == other

    def _eq_Rational(self, other):
        return self.imag == 0 and self.real == other

    def _eq_Quadratic(self, other):
        return self.signature == other.signature

    #=========================

    def __neg__(self):
        return self.from_components(*map(op.__neg__, self.components))

    def __abs__(self):
        return abs(self.norm)

    @property
    def conjugate(self):
        return self.from_components(self.real, -self.imag)

    @property
    def norm(self):
        return self.real**2 - self.root * self.imag**2

    @property
    def inverse(self):
        norm = frac(self.norm)
        return Quadratic(
            *map(lambda x: x / norm, (self.real, -self.imag)),
            self.root
        )

    @property
    def round(self):
        return Quadratic(
            *map(lambda x: x.round_prefer_toward_zero, self.components),
            self.root
        )

    #=========================

    def _add_int(self, other):
        return self.from_components(self.real + other, self.imag)

    def _add_Rational(self, other):
        return Quadratic(self.real + other, self.imag, self.root)

    def _add_Quadratic(self, other):
        if self.root != other.root:
            return NotImplemented
        return Quadratic(
            *map(op.__add__, self.components, other.components),
            self.root
        )

    #-------------------------

    def _mul_int(self, other):
        return self.from_components(
            *map(lambda x: x * other, self.components)
        )

    def _mul_Rational(self, other):
        return Quadratic(
            *map(lambda x: x * other, self.components),
            self.root
        )

    def _mul_Quadratic(self, other):
        if self.root != other.root:
            return NotImplemented
        return Quadratic(
            self.real * other.real + self.imag * other.imag * self.root,
            self.real * other.imag + self.imag * other.real,
            self.root
        )

    def _rmul_int(self, other):
        return self * other

    def _rmul_Rational(self, other):
        return self * other

    #-------------------------

    def _truediv_int(self, other):
        return Quadratic(
            *map(lambda x: x / frac(other), self.components),
            self.root
        )

    def _truediv_Rational(self, other):
        return Quadratic(
            *map(lambda x: x / other, self.components),
            self.root
        )

    def _truediv_Quadratic(self, other):
        if self.root != other.root:
            return NotImplemented
        return self * other.inverse

    def _rtruediv_int(self, other):
        return self.inverse * other

    def _rtruediv_Rational(self, other):
        return self.inverse * other

    #-------------------------

    def _floordiv_int(self, other):
        return self.from_components(
            *map(lambda x: x // other, self.components)
        )

    def _floordiv_Rational(self, other):
        return self.from_components(
            *map(lambda x: x // other, self.components)
        )

    def _floordiv_Quadratic(self, other):
        if self.root != other.root:
            return NotImplemented
        return (self * other.inverse).round

    def _rfloordiv_int(self, other):
        return (self.inverse * other).round

    def _rfloordiv_Rational(self, other):
        return (self.inverse * other).round

    #-------------------------

    def _mod_int(self, other):
        return self.from_components(
            *map(lambda x: x % other, self.components)
        )

    def _mod_Rational(self, other):
        return Quadratic(
            *map(lambda x: x % other, self.components),
            self.root
        )

    def _mod_Quadratic(self, other):
        if self.root != other.root:
            return NotImplemented
        return self - (self // other) * other

    def _rmod_int(self, other):
        return other - (other // self) * self

    def _rmod_Rational(self, other):
        return other - (other // self) * self

    #-------------------------

    def _inv_pow_int(self, other):
        return self.__pow__(-other).inverse

    def _zero_pow_int(self, _other):
        return self.from_components(1, 0)

    #=========================

    def rational_approx(self, num_digits=None):
        if self.imag == 0:
            return self.real

        if not self.is_real:
            raise ValueError('No rational approximation possible for non-real number')

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

