#   numth/types/quadratic.py
#===========================================================
import math
import numbers
import operator as op

from .rational import frac, Rational
#===========================================================

class Quadratic(numbers.Number):
    """
    Numeric class that represents `real + imag * sqrt(root)`.
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

    #=========================

    @property
    def _root_display(self):
        if self.root == -1:
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

    def is_same_type(self, other):
        return type(self) is type(other) and self.root == other.root

    def is_similar_type(self, other):
        return self.is_same_type(other)

    #-------------------------

    @classmethod
    def from_signature(self, *signature):
        return Quadratic(*signature)

    @classmethod
    def from_complex(self, cmplx):
        return self.from_signature(cmplx.real, cmplx.imag, -1)

    def from_components(self, *components):
        return self.from_signature(*components, self.root)

    #=========================

    def __pos__(self):
        return self

    def __neg__(self):
        return self.from_components(*map(op.__neg__, self.components))

    @property
    def conjugate(self):
        return self.from_components(self.real, -self.imag)

    @property
    def norm(self):
        return self.real**2 - self.root * self.imag**2

    @property
    def inverse(self):
        norm = self.norm
        return self.from_components(
            *map(lambda x: x / norm, (self.real, -self.imag))
        )

    @property
    def round(self):
        return self.from_components(*map(_round_prefer_down, self.components))

    #=========================

    def __eq__(self, other):
        if isinstance(other, Quadratic):
            return self.signature == other.signature

        if isinstance(other, numbers.Rational):
            return self.imag == 0 and self.real == other

        return NotImplemented

    def __lt__(self, other):
        if self.is_similar_type(other):
            return self.norm < other.norm

        return NotImplemented

    def __gt__(self, other):
        if self.is_similar_type(other):
            return self.norm > other.norm

    def __le__(self, other):
        return not (self > other)

    def __ge__(self, other):
        return not (self < other)

    #=========================

    def _add_int(self, other):
        return self.from_components(self.real + other, self.imag)

    def _add_rational(self, other):
        return self._add_int(other)

    def _add_same_type(self, other):
        return self.from_components(
            *map(op.__add__, self.components, other.components)
        )

    def _add_similar_type(self, other):
        return self._add_same_type(other)

    def __add__(self, other):
        if isinstance(other, int):
            return self._add_int(other)

        if isinstance(other, Rational):
            return self._add_rational(other)

        if self.is_same_type(other):
            return self._add_same_type(other)

        if self.is_similar_type(other):
            return self._add_similar_type(other)

        return NotImplemented

    #-------------------------

    def __sub__(self, other):
        return self + -other

    #-------------------------

    def _mul_int(self, other):
        return self.from_components(
            *map(lambda x: x * other, self.components)
        )

    def _mul_rational(self, other):
        return self._mul_int(other)

    def _mul_same_type(self, other):
        return self.from_components(
            self.real * other.real + self.imag * other.imag * self.root,
            self.real * other.imag + self.imag * other.real
        )

    def _mul_similar_type(self, other):
        return self._mul_same_type(other)

    def __mul__(self, other):
        if isinstance(other, int):
            return self._mul_int(other)

        if isinstance(other, Rational):
            return self._mul_rational(other)

        if self.is_same_type(other):
            return self._mul_same_type(other)

        if self.is_similar_type(other):
            return self._mul_similar_type(other)

        return NotImplemented

    #-------------------------

    def _div_int(self, other):
        return self.from_components(
            *map(lambda x: x / other, self.components)
        )

    def _div_rational(self, other):
        return self._div_int(other)

    def _div_same_type(self, other):
        return self * other.inverse

    def _div_similar_type(self, other):
        return self._div_same_type(other)

    def __truediv__(self, other):
        if isinstance(other, int):
            return self._div_int(other)

        if isinstance(other, Rational):
            return self._div_rational(other)

        if self.is_same_type(other):
            return self._div_same_type(other)

        if self.is_similar_type(other):
            return self._div_similar_type(other)

        return NotImplemented

    #-------------------------

    def _floor_div_int(self, other):
        return self.from_components(
            *map(lambda x: x // other, self.components)
        )

    def _floor_div_rational(self, other):
        return self._floor_div_int(other)

    def _floor_div_same_type(self, other):
        return (self / other).round

    def _floor_div_similar_type(self, other):
        return self._floor_div_same_type(other)

    def __floordiv__(self, other):
        if isinstance(other, int):
            return self._floor_div_int(other)

        if isinstance(other, Rational):
            return self._floor_div_rational(other)

        if self.is_same_type(other):
            return self._floor_div_same_type(other)

        if self.is_similar_type(other):
            return self._floor_div_similar_type(other)

        return NotImplemented

    #-------------------------

    def _mod_int(self, other):
        return self.from_components(
            *map(lambda x: x % other, self.components)
        )

    def _mod_rational(self, other):
        return self._mod_int(other)

    def _mod_same_type(self, other):
        return self - (self // other) * other

    def _mod_similar_type(self, other):
        return self._mod_same_type(other)

    def __mod__(self, other):
        if isinstance(other, int):
            return self._mod_int(other)

        if isinstance(other, Rational):
            return self._mod_rational(other)

        if self.is_same_type(other):
            return self._mod_same_type(other)

        if self.is_similar_type(other):
            return self._mod_similar_type(other)

        return NotImplemented

    #-------------------------

    def __pow__(self, other, modulus=None):
        if not isinstance(other, int):
            raise TypeError('Integer exponent is required')

        if other < 0:
            result = pow(self, -other).inverse
            return result if modulus is None else result % modulus

        if other == 0:
            return self.from_components(1, 0)

        if other == 1:
            return self if modulus is None else self % modulus

        if other % 2 == 0:
            return pow(self * self, other // 2, modulus)

        result = self * pow(self * self, other // 2, modulus)
        return result if modulus is None else result % modulus

    #=========================

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return -self + other

    def __rmul__(self, other):
        return self * other

    def __rtruediv__(self, other):
        return self.inverse * other

    def __rfloordiv__(self, other):
        return (self.inverse * other).round

    def __rmod__(self, other):
        return other - (other // self) * self

    #=========================

    def rational_approx(self, num_digits=None):
        if self.imag == 0:
            return self.real

        if not self.is_real:
            raise ValueError('No rational approximation possible for non-real number')

        if self.imag.numer >= self.imag.denom:
            log_ten = len(str(int(self.imag)))
        else:
            log_ten = len(str(int(self.imag.inverse)))

        approx_sqrt = self.root.sqrt(num_digits + log_ten + 1)

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

#===========================================================

def _round_prefer_down(number):
    """Rounds toward zero if fractional part is less than or equal to half."""
    if number < 0:
        return - _round_prefer_down(-number)

    if 2 * (number - int(number)) > 1:
        return int(number) + 1

    return int(number)

