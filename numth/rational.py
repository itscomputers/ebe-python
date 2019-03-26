#   numth/rational.py
#===========================================================
from fractions import Fraction
import re

from numth.basic import gcd, mod_inverse, integer_sqrt
#===========================================================

def _default_values(category):
    if category == 'decimal':
        return 20

#=============================

def frac(number):
    """Shortcut to create Rational"""
    if isinstance(number, Rational):
        return number
    if isinstance(number, int):
        return _int_to_rational(number)
    if isinstance(number, Fraction):
        return _fraction_to_rational(number)
    if isinstance(number, float):
        return _float_to_rational(number)
    if isinstance(number, str):
        return _str_to_rational(number)

#===========================================================

class Rational:
    """
    Class for arithmetic of rational numbers.

    Args:   numer:  int
            denom:  int
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
        denom = ' '*(minus + denom_offset + 1) * str(denom)
        line = '-'*minus + ' ' + '\u2500'*length
        return '{}\n{}\n{}'.format(numer, line, denom)

    #-------------------------

    def decimal(self, num_digits=None):
        """
        Express rational number as a decimal.

        Args:   num_digits: int

        Return: expression: str
        """
        whole = int(self)
        
        if num_digits is None:
            num_digits = _default_values('decimal')

        remainder = self.numer % self.denom

        digits = []
        while len(digits) <= num_digits:
            remainder *= 10
            digits.append(remainder // self.denom)
            remainder %= self.denom

        if digits[-1] >= 5:
            try:
                digits[-2] += 1
            except IndexError:
                whole += 1
        for i in range(num_digits):
            if digits[-i-2] == 10:
                digits[-i-2] = 0
                try:
                    digits[-i-3] += 1
                except IndexError:
                    whole += 1
            else:
                break

        return '{}{}{}'.format(
                whole,
                '.'*(num_digits > 0),
                ''.join(str(d) for d in digits[:-1])
        )

    #=========================

    def __eq__(self, other):
        other = frac(other)
        return self.numer * other.denom == other.numer * self.denom

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        other = frac(other)
        return self.numer * other.denom < other.numer * self.denom

    def __gt__(self, other):
        other = frac(other)
        return self.numer * other.denom > other.numer * self.denom

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
        other = frac(other)
        d = gcd(self.denom, other.denom)
        self_scalar = other.denom // d
        other_scalar = self.denom // d
        numer = (self.numer * self_scalar) + (other.numer * other_scalar)
        denom = self_scalar * self.denom
        return Rational(numer, denom)

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        return self + other

    #-------------------------

    def __sub__(self, other):
        other = frac(other)
        return self + (-other)

    def __rsub__(self, other):
        return -self + other

    def __isub__(self, other):
        return self - other

    #-------------------------
        
    def __mul__(self, other):
        other = frac(other)
        return Rational(self.numer*other.numer, self.denom*other.denom)

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        return self * other

    #-------------------------

    def __truediv__(self, other):
        other = frac(other)
        return self * other.inverse()

    def __rtruediv__(self, other):
        return self.inverse() * other

    def __itruediv__(self, other):
        return self / other

    #=========================

    def __pow__(self, other):
        if not isinstance(other, int):
            raise ValueError('Exponent must be an integer')

        if other == 0:
            return Rational(1, 1)
        elif other < 0:
            return (self**(-other)).inverse()
        else:
            return Rational(pow(self.numer, other), pow(self.denom, other))

    def __ipow__(self, other):
        return self**other

    #=========================

    def __mod__(self, other):
        if not isinstance(other, int) or other < 2:
            raise ValueError('Modulus must an integer greater than 1')

        inv_denom = mod_inverse(self.denom, other)
        return (self.numer * inv_denom) % other

    def __imod__(self, other):
        return self % other

    #=========================

    def approx_equal(self, other, num_digits=None):
        """
        Determine approximate equality of two rational numbers.

        Args:   other:      Rational
                num_digits: int             number of digits of accuracy

        Return: bool                        abs(self - other) < 10**(-num_digits)
        """
        if num_digits is None:
            num_digits = _default_values('decimal')

        other = frac(other)
        ad = self.numer * other.denom
        bc = self.denom * other.numer
        bd = self.denom * other.denom

        return 10**num_digits * abs(ad - bc) < abs(bd)

    #=========================

    def sqrt(self, num_digits=None):
        """
        Calculate or approximate the square root of a rational number.
        
        Args:   num_digits: int             number of digits of accuracy

        Return: val:        Rational        val**2 == self or 
                                            self.approx_equal(val**2)
        """
        if self == 0:
            return self

        if num_digits is None:
            num_digits = _default_values('decimal')

        val = Rational(integer_sqrt(self.numer), integer_sqrt(self.denom))
        next_val = (val + self / val) * Rational(1, 2)

        while not val.approx_equal(next_val, num_digits):
            val, next_val = next_val, (next_val + self / next_val) * Rational(1, 2)

        return next_val

    #-------------------------

    def is_square(self):
        return self.sqrt()**2 == self

#===========================================================

def _int_to_rational(number):
    return Rational(number, 1)

#-----------------------------

def _split_float_with_decimal_point(number):
    pattern = re.fullmatch(r'(-?\d+)\.(\d+)', str(number))
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
    pattern = re.match(r'(-?\d+) *\/ *(\d+)', str(number))
    if pattern is not None:
        return Rational(*map(int, pattern.group(1, 2)))

#-----------------------------

def _str_to_rational(number):
    try:
        return _frac_string_to_rational(number)
    except:
        pass
    
    try:
        return _float_to_rational(float(number))
    except:
        pass

    try:
        return _int_to_rational(int(number))
    except Exception as e:
        raise TypeError(e)

