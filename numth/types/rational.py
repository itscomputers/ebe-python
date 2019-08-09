#   numth/types/rational.py
#===========================================================
from fractions import Fraction
from typing import Any, Union
import re

from ..config import default
from ..basic import div, gcd, integer_sqrt, is_square, mod_inverse
#===========================================================

def frac(*inputs: Any) -> 'Rational':
    """Shortcut to create a Rational object."""
    if len(inputs) == 1:
        number = inputs[0]

        if type(number) not in [int, float, str, list, tuple, Fraction, Rational]:
            raise ValueError('incompatible type: {}'.format(type(number)))

        type_name = type(number).__name__
        function_name = 'Rational.from_{}'.format(type_name)
        return eval(function_name)(number)

    return Rational(*inputs)

#===========================================================

class Rational:
    """
    Rational number class.

    params
    + numer : int
    + denom : int
        nonzero

    represents
    numer / denom
    """
    def __init__(self, numer: int, denom: int):
        """Inits Rational number with numer and denom."""
        if denom == 0:
            raise ValueError('Attempted division by zero')

        if numer * denom < 0:
            sgn = -1
        else:
            sgn = 1

        d = gcd(numer, denom)
        self.numer = sgn * abs(numer) // d
        self.denom = abs(denom) // d
        self.sign = sgn

    #-------------------------

    def __repr__(self) -> str:
        """Represents Rational number as string."""
        if self.denom == 1:
            return '{}'.format(self.numer)
        return '{}/{}'.format(self.numer, self.denom)

    #-------------------------

    def display(self) -> str:
        """Pretty-print Rational number."""
        minus = self.sign == -1
        numer = abs(self.numer)
        denom = self.denom
        numer_length = len(str(numer))
        denom_length = len(str(denom))
        length = max(numer_length, denom_length)
        numer_offset = (length - numer_length + 1) // 2
        denom_offset = (length - denom_length + 1) // 2
        numer_s = ' '*(minus + numer_offset + 1) + str(numer)
        denom_s = ' '*(minus + denom_offset + 1) + str(denom)
        line = '-'*minus + ' ' + '\u2500'*length
        return '{}\n{}\n{}'.format(numer_s, line, denom_s)

    #-------------------------

    def decimal(self, num_digits: int = None) -> str:
        """
        Express rational number as a string in decimal form.

        params
        + num_digits : int

        return
        str
            decimal representation of self
        """
        if num_digits == 0:
            return str(int(self + Rational(1, 2)))

        num_digits = num_digits or default('decimal_digits')

        quotient, remainder = div(self.numer, self.denom)
        if num_digits == 0:
            return format(quotient)
        shifted_remainder = Rational(remainder * 10**num_digits, self.denom)
        digits = format(int(shifted_remainder + Rational(1, 2)))
        num_zeros = num_digits - len(digits)

        return '{}.{}{}'.format(quotient, '0'*num_zeros, digits)

    #=========================

    def compare(self, other: Union[int, float, Fraction, 'Rational']) -> int:
        other_ = frac(other)
        return self.numer * other_.denom - self.denom * other_.numer

    def __eq__(self, other: Any) -> bool:
        if type(other) in [int, float, Fraction, Rational]:
            return self.compare(other) == 0
        return other == self

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def __lt__(self, other: Any) -> bool:
        if type(other) in [int, float, Fraction, Rational]:
            return self.compare(other) < 0
        return other > self

    def __gt__(self, other: Any) -> bool:
        if type(other) in [int, float, Fraction, Rational]:
            return self.compare(other) > 0
        return other < self

    def __le__(self, other: Any) -> bool:
        return not (self > other)

    def __ge__(self, other: Any) -> bool:
        return not (self < other)

    #=========================

    def __int__(self) -> int:
        return self.numer // self.denom

    def __float__(self) -> float:
        return self.numer / self.denom

    def __round__(self) -> int:
        return int(self + Rational(1, 2))

    def __neg__(self) -> 'Rational':
        return Rational(-self.numer, self.denom)

    def __abs__(self) -> 'Rational':
        return Rational(abs(self.numer), self.denom)

    def inverse(self) -> 'Rational':
        return Rational(self.denom, self.numer)

    #=========================

    def __add__(self, other: Any) -> 'Rational':
        if type(other) in [int, float, Rational]:
            other_ = frac(other)
            d = gcd(self.denom, other_.denom)
            self_scalar = other_.denom // d
            other_scalar = self.denom // d
            numer = (self.numer * self_scalar) + (other_.numer * other_scalar)
            denom = self_scalar * self.denom
            return Rational(numer, denom)
        return other + self

    def __radd__(self, other: Any) -> 'Rational':
        return self + other

    #-------------------------

    def __sub__(self, other: Any) -> 'Rational':
        return self + (-other)

    def __rsub__(self, other: Any) -> 'Rational':
        return -self + other

    #-------------------------

    def __mul__(self, other: Any) -> 'Rational':
        if type(other) in [int, float, Rational]:
            other_ = frac(other)
            return Rational(
                self.numer * other_.numer,
                self.denom * other_.denom
            )
        return other * self

    def __rmul__(self, other: Any) -> 'Rational':
        return self * other

    #-------------------------

    def __truediv__(self, other: Any) -> 'Rational':
        if type(other) in [int, float, Rational]:
            return self * frac(other).inverse()
        return self * other.inverse()

    def __rtruediv__(self, other: Any) -> 'Rational':
        return self.inverse() * other

    #-------------------------

    def __pow__(self, other: int) -> 'Rational':
        if type(other) is not int:
            raise ValueError('Exponent must be an integer')

        if other == 0:
            return Rational(1, 1)
        elif other < 0:
            return (self**(-other)).inverse()
        else:
            return Rational(pow(self.numer, other), pow(self.denom, other))

    #-------------------------

    def __mod__(self, other: int) -> int:
        if type(other) is not int or other < 2:
            raise ValueError('Modulus must an integer greater than 1')

        inv_denom = mod_inverse(self.denom, other)
        return (self.numer * inv_denom) % other

    #=========================

    def approx_equal(self, other: Any, num_digits: int = None) -> bool:
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
        ad = self.numer * other_.denom
        bc = self.denom * other_.numer
        bd = self.denom * other_.denom

        return 10**num_digits * abs(ad - bc) < abs(bd)

    #=========================

    def sqrt(self, num_digits: int = None) -> 'Rational':
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

        numer_integer_sqrt = integer_sqrt(self.numer)
        denom_integer_sqrt = integer_sqrt(self.denom)
        guess = Rational(numer_integer_sqrt, denom_integer_sqrt)

        if numer_integer_sqrt**2 == self.numer \
                and denom_integer_sqrt**2 == self.denom:
            return guess

        num_digits = num_digits or default('sqrt_digits')

        if self.numer > self.denom:
            other_guess = self / guess

            while not guess.approx_equal(other_guess, num_digits):
                guess = (guess + other_guess) / 2
                other_guess = self / guess

            return guess

        else:
            return self.inverse().inverse_sqrt()

    #-------------------------

    def inverse_sqrt(self, num_digits: int = None) -> 'Rational':
        """
        Inverse square root (or approximation) of a rational number greater than 1.

        Computes sqrt such that ``sqrt**2 == self.inverse()``,
        or up to desired accuracy if not a perfect square.

        params
        + num_digits : int

        return
        Rational
        """
        if self.numer <= self.denom:
            raise ValueError('Inverse square root only if greater than 1')

        guess = self.sqrt(2).inverse()
        other_guess = guess * (2 - self * guess**2)

        while not guess.approx_equal(other_guess, num_digits):
            guess = (guess + other_guess) / 2
            other_guess = guess * (2 - self * guess**2)

        return guess

    #-------------------------

    def is_square(self) -> bool:
        return is_square(self.numer) and is_square(self.denom)

    #=========================

    def from_int(int_):
        return Rational(int_, 1)

    #-------------------------

    def from_float(float_):
        exponent_pattern = re.fullmatch(r'(.+)e([\+\-]?\d+)', str(float_))
        if exponent_pattern is None:
            number, exponent = str(float_), None
        else:
            number, exponent = exponent_pattern.group(1, 2)

        decimal_pattern = re.fullmatch(r'([\+\-]?\d+)\.(\d+)', str(number))
        if decimal_pattern is None:
            numer, denom = int(number), 1
        else:
            whole, decimal = decimal_pattern.group(1, 2)
            numer = int(whole + decimal)
            denom = 10**len(decimal)

        if exponent is None:
            return Rational(numer, denom)

        exp = int(exponent)
        if exp < 0:
            return Rational(numer, denom * 10**(-exp))
        return Rational(numer * 10**exp, denom)

    #-------------------------

    def from_str(string_):
        try:
            int_ = int(string_)
            return Rational.from_int(int_)
        except:
            pass

        try:
            float_ = float(string_)
            return Rational.from_float(float_)
        except:
            pass

        pattern = re.match(r'([\+\-]?\d+)\/(\d+)', ''.join(string_.split()))
        if pattern is not None:
            return Rational(*map(int, pattern.group(1, 2)))

    #-------------------------

    def from_list(list_):
        return Rational(*list_)

    #-------------------------

    def from_tuple(tuple_):
        return Rational(*tuple_)

    #-------------------------

    def from_Fraction(Fraction_):
        return Rational(Fraction_.numerator, Fraction_.denominator)

    #-------------------------

    def from_Rational(Rational_):
        return Rational_

