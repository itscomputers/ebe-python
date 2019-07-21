#   numth/types/rational.py
#===========================================================
from fractions import Fraction
import re

from ..config import default
from ..basic import div, gcd, integer_sqrt, is_square, mod_inverse
#===========================================================

def frac(number):
    """Shortcut to create Rational"""
    if type(number) is Rational:
        return number
    if type(number) is int:
        return _int_to_rational(number)
    if type(number) is Fraction:
        return _fraction_to_rational(number)
    if type(number) is float:
        return _float_to_rational(number)
    if type(number) is str:
        return _str_to_rational(number)

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
    def __init__(self, numer, denom):
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

    def __repr__(self):
        if self.denom == 1:
            return '{}'.format(self.numer)
        return '{}/{}'.format(self.numer, self.denom)

    #-------------------------

    def display(self):
        """Pretty-print rational number."""
        minus = self.sign == -1
        numer = abs(self.numer)
        denom = self.denom
        numer_length = len(str(numer))
        denom_length = len(str(denom))
        length = max(numer_length, denom_length)
        numer_offset = (length - numer_length + 1) // 2
        denom_offset = (length - denom_length + 1) // 2
        numer = ' '*(minus + numer_offset + 1) + str(numer)
        denom = ' '*(minus + denom_offset + 1) + str(denom)
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
            return str(round(self))

        num_digits = num_digits or default('decimal_digits')
        
        quotient, remainder = div(self.numer, self.denom)
        if num_digits == 0:
            return format(quotient)
        digits = format(round(Rational(remainder*10**num_digits, self.denom)))
        num_zeros = num_digits - len(digits)

        return '{}.{}{}'.format(quotient, '0'*num_zeros, digits)

    #=========================

    def compare(self, other):
        other_ = frac(other)
        return self.numer * other_.denom - self.denom * other_.numer

    def __eq__(self, other):
        if type(other) in [int, float, Fraction, Rational]:
            return self.compare(other) == 0
        return other == self

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        if type(other) in [int, float, Fraction, Rational]:
            return self.compare(other) < 0
        return other > self

    def __gt__(self, other):
        if type(other) in [int, float, Fraction, Rational]:
            return self.compare(other) > 0
        return other < self

    def __le__(self, other):
        return not (self > other)

    def __ge__(self, other):
        return not (self < other)

    #=========================

    def __int__(self):
        return self.numer // self.denom

    def __float__(self):
        return self.numer / self.denom

    def __round__(self):
        return int(Rational(2*self.numer + self.denom, 2*self.denom))

    def __neg__(self):
        return Rational(-self.numer, self.denom)

    def __abs__(self):
        return Rational(abs(self.numer), self.denom)

    def inverse(self):
        return Rational(self.denom, self.numer)

    #=========================
    
    def __add__(self, other):
        if type(other) in [int, float, Rational]:
            other_ = frac(other)
            d = gcd(self.denom, other_.denom)
            self_scalar = other_.denom // d
            other_scalar = self.denom // d
            numer = (self.numer * self_scalar) + (other_.numer * other_scalar)
            denom = self_scalar * self.denom
            return Rational(numer, denom)
        return other + self

    def __radd__(self, other):
        return self + other

    #-------------------------

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return -self + other

    #-------------------------
        
    def __mul__(self, other):
        if type(other) in [int, float, Rational]:
            return Rational(self.numer*frac(other).numer, self.denom*frac(other).denom)
        return other * self

    def __rmul__(self, other):
        return self * other

    #-------------------------

    def __truediv__(self, other):
        if type(other) in [int, float, Rational]:
            return self * frac(other).inverse()
        return self * other.inverse()

    def __rtruediv__(self, other):
        return self.inverse() * other

    #-------------------------

    def __pow__(self, other):
        if type(other) is not int:
            raise ValueError('Exponent must be an integer')

        if other == 0:
            return Rational(1, 1)
        elif other < 0:
            return (self**(-other)).inverse()
        else:
            return Rational(pow(self.numer, other), pow(self.denom, other))

    #-------------------------

    def __mod__(self, other):
        if type(other) is not int or other < 2:
            raise ValueError('Modulus must an integer greater than 1')

        inv_denom = mod_inverse(self.denom, other)
        return (self.numer * inv_denom) % other

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
        ad = self.numer * other_.denom
        bc = self.denom * other_.numer
        bd = self.denom * other_.denom

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
        if self.numer <= self.denom:
            raise ValueError('Inverse square root only if greater than 1')

        guess = self.sqrt(2).inverse()
        other_guess = guess * (2 - self * guess**2)

        while not guess.approx_equal(other_guess, num_digits):
            guess = (guess + other_guess) / 2
            other_guess = guess * (2 - self * guess**2)

        return guess

    #-------------------------

    def is_square(self):
        return is_square(self.numer) and is_square(self.denom)

#===========================================================

def _int_to_rational(number):
    return Rational(number, 1)

#-----------------------------

def _split_float_with_decimal_point(number):
    pattern = re.fullmatch(r'([\+\-]?\d+)\.(\d+)', str(number))
    if pattern is not None:
        whole, decimal = pattern.group(1, 2)
        numer = int(whole + decimal)
        denom = 10**len(decimal)
        return numer, denom
        
#-----------------------------

def _split_float_with_exponent(number):
    pattern = re.fullmatch(r'(.+)e([+-]?\d+)', str(number))
    if pattern is not None:
        num, exponent = pattern.group(1, 2)
        return num, int(exponent)

#-----------------------------

def _float_to_rational(number):
    with_exponent = _split_float_with_exponent(number)
    
    if with_exponent is None:
        numer, denom = _split_float_with_decimal_point(number)

    else:
        number_, exponent = with_exponent
        with_decimal = _split_float_with_decimal_point(number_)
        if with_decimal:
            numer, denom = with_decimal
        else:
            numer = int(number_)
            denom = 1
        if exponent >= 0:
            numer *= 10**exponent
        else:
            denom *= 10**(-exponent)

    return Rational(numer, denom)

#-----------------------------

def _fraction_to_rational(number):
    return Rational(number.numerator, number.denominator)

#-----------------------------

def _frac_string_to_rational(number):
    """Convert string of form 'a/b' to Rational."""
    pattern = re.match(r'([\+\-]?\d+)\/(\d+)', ''.join(number.split()))
    if pattern is not None:
        return Rational(*map(int, pattern.group(1, 2)))

#-----------------------------

def _str_to_rational(number):
    try:
        return _int_to_rational(int(number))
    except:
        pass

    try:
        return _frac_string_to_rational(number)
    except:
        pass
    
    try:
        return _float_to_rational(float(number))
    except Exception as e:
        raise TypeError(e)

