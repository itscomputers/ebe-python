#   numth/types/rational.py
#===========================================================
from fractions import Fraction
import math
import numbers
import re

from ..config import default
from ..basic import div, gcd, integer_sqrt, is_square, mod_inverse
#===========================================================

def frac(*inputs):
    """Shortcut to create Rational"""
    if len(inputs) == 1:
        first = inputs[0]

        if not isinstance(first, (numbers.Real, str, list, tuple)):
            raise TypeError('incompatible type for rational number')

        type_name = type(first).__name__
        function_name = 'Rational.from_{}'.format(type_name)
        return eval(function_name)(first)

    return Rational(*inputs)

#===========================================================

class Rational(Fraction):
    """
    Rational number class.

    Primarily inherits from fractions.Fraction
    """
    def __new__(cls, numer, denom, _normalize=True):
        self = super(Rational, cls).__new__(cls)

        if denom == 0:
            raise ZeroDivisionError('Rational(_, 0)')

        if _normalize:
            d = math.gcd(numer, denom)
            if denom < 0:
                d = -d
            numer = numer // d
            denom = denom // d

        self._numerator = numer
        self._denominator = denom
        return self

    #-------------------------

    @property
    def numer(self):
        return self._numerator

    @property
    def denom(self):
        return self._denominator

    @classmethod
    def from_int(self, integer):
        return Rational(integer, 1, _normalize=False)

    @classmethod
    def from_Rational(self, rational):
        return rational

    @classmethod
    def from_Fraction(self, fraction):
        return Rational(
            fraction._numerator,
            fraction._denominator,
            _normalize=False
        )

    @classmethod
    def from_float(self, fl):
        return Rational.from_str(str(fl))

    @classmethod
    def from_str(self, string):
        return Rational.from_Fraction(Fraction(string.replace(' ', '')))

    @classmethod
    def from_list(self, li):
        return Rational(*li)

    @classmethod
    def from_tuple(self, tu):
        return Rational(*tu)

    #-------------------------

    def __repr__(self):
        if self._denominator == 1:
            return '{}'.format(self._numerator)
        return '{}/{}'.format(self._numerator, self._denominator)

    #-------------------------

    def display(self):
        """Pretty-print rational number."""
        minus = self.sign == -1
        numer = str(abs(self._numerator))
        denom = str(self._denominator)
        length = max(len(numer), len(denom))
        numer_offset = (length - len(numer) + 1) // 2
        denom_offset = (length - len(denom) + 1) // 2
        numer = ' '*(minus + numer_offset + 1) + numer
        denom = ' '*(minus + denom_offset + 1) + denom
        line = '-'*minus + ' ' + '\u2500'*length
        return '{}\n{}\n{}'.format(numer, line, denom)

    #-------------------------

    def decimal(self, num_digits=None):
        """
        Express rational number as a string in decimal form.

        params
        + num_digits : int

        return
        str
            decimal representation of self
        """
        if num_digits == 0:
            return str(self.round_to_nearest_int())

        sign = '-' if self._numerator < 0 else ''

        num_digits = num_digits or default('decimal_digits')

        quotient, remainder = divmod(abs(self._numerator), self._denominator)
        if num_digits == 0:
            return str(quotient)
        shifted_rem = Rational(remainder * 10**num_digits, self._denominator)
        digits = str(shifted_rem.round_to_nearest_int())
        num_zeros = num_digits - len(digits)

        return '{}{}.{}{}'.format(sign, quotient, '0'*num_zeros, digits)

    #=========================

    def inverse(self):
        if self._numerator < 0:
            return Rational(-self._denominator, -self._numerator, _normalize=False)
        return Rational(self._denominator, self._numerator, _normalize=False)

    #-------------------------

    def round_to_nearest_int(self):
        return math.floor(self + Rational(1, 2))

    #-------------------------

    def is_square(self):
        return is_square(self._numerator) and is_square(self._denominator)

    #=========================

    def approx_equal(self, other, num_digits=None):
        """
        Approximate equality of two rational numbers.

        Determines if ``abs(self - other) < 10**(-num_digits)``.

        params
        + other : Rational
            or type that can be converted to Rational using frac
        + num_digits : int

        return
        bool
        """
        if num_digits == 0:
            return abs(self - other) < 1

        num_digits = num_digits or default('decimal_digits')

        other_ = frac(other)
        ad = self._numerator * other_._denominator
        bc = self._denominator * other_._numerator
        bd = self._denominator * other_._denominator

        return 10**num_digits * abs(ad - bc) < abs(bd)

    #=========================

    def sqrt(self, num_digits=None):
        """
        Square root (or approximation of square root) of a rational number.

        Computes sqrt such that ``sqrt**2 == self``,
        or up to desired accuracy if not a perfect square.

        params
        + num_digits : int

        return
        Rational
        """
        if self < 0:
            raise ValueError('Cannot take square root of negative number')

        numer_integer_sqrt = integer_sqrt(self._numerator)
        denom_integer_sqrt = integer_sqrt(self._denominator)
        guess = Rational(numer_integer_sqrt, denom_integer_sqrt)

        if numer_integer_sqrt**2 == self._numerator \
                and denom_integer_sqrt**2 == self._denominator:
            return guess

        num_digits = num_digits or default('sqrt_digits')

        if self._numerator > self._denominator:
            other_guess = self / guess

            while not guess.approx_equal(other_guess, num_digits):
                guess = (guess + other_guess) / 2
                other_guess = self / guess

            return guess

        else:
            return self.inverse().inverse_sqrt()

    #-------------------------

    def inverse_sqrt(self, num_digits=None):
        """
        Inverse square root (or approximation) of a rational number greater than 1.

        Computes sqrt such that ``sqrt**2 == self.inverse()``,
        or up to desired accuracy if not a perfect square.

        params
        + num_digits : int

        return
        Rational
        """
        if self._numerator <= self._denominator:
            raise ValueError('Inverse square root only if greater than 1')

        guess = self.sqrt(2).inverse()
        other_guess = guess * (2 - self * guess**2)

        while not guess.approx_equal(other_guess, num_digits):
            guess = (guess + other_guess) / 2
            other_guess = guess * (2 - self * guess**2)

        return guess

    #=========================

    def __pos__(self):
        return self

    def __neg__(self):
        return Rational(
            -self._numerator,
            self._denominator,
            _normalize=False
        )

    def __abs__(self):
        return Rational(
            abs(self._numerator),
            self._denominator,
            _normalize=False
        )

    #=========================

    def __add__(self, other):
        if type(other) is int:
            return Rational(
                self._numerator + other * self._denominator,
                self._denominator
            )
        if isinstance(other, numbers.Rational):
            return Rational(
                self._numerator * other._denominator + self._denominator * other._numerator,
                self._denominator * other._denominator
            )
        return NotImplemented

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if type(other) is int:
            return Rational(
                self._numerator * other,
                self._denominator
            )
        if isinstance(other, numbers.Rational):
            return Rational(
                self._numerator * other._numerator,
                self._denominator * other._denominator
            )
        return NotImplemented

    def __truediv__(self, other):
        if type(other) is int:
            return Rational(
                self._numerator,
                self._denominator * other
            )
        if isinstance(other, numbers.Rational):
            return Rational(
                self._numerator * other._denominator,
                self._denominator * other._numerator
            )
        return NotImplemented

    def __pow__(self, other):
        if isinstance(other, numbers.Rational) and other.denominator == 1:
            if other == 0:
                return Rational(1, 1)
            elif other < 0:
                return (self**(-other)).inverse()
            return Rational(
                self._numerator ** other,
                self._denominator ** other,
                _normalize=False
            )
        return NotImplemented

    #-------------------------

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return -self + other

    def __rmul__(self, other):
        return self * other

    def __rtruediv__(self, other):
        return self.inverse() * other

    def __rpow__(self, other):
        if self.denom == 1:
            return other ** self.numer
        return NotImplemented
