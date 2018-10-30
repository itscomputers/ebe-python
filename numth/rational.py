
#   numth/rational.py

from numth.main import gcd, mod_inverse 
from numth.polynomial import polyn

import math
import tabulate

##############################

def _default_values(cat):
    if cat == 'frac_to_dec':
        return 20
    if cat == 'sqrt_digits':
        return 20
    if cat == 'pi_digits':
        return 20
    if cat == 'continued fraction':
        return 10

############################################################
############################################################
#       Rational class
############################################################
############################################################

class Rational:
    """
    Class for arithmetic of rational numbers.
    
    Args:   int:    numer, denom
    """
    ##########################

    def __init__(self, numer, denom):
        """Initialize rational number."""
        if denom == 0:
            raise ValueError('Attempt to divide by zero')
        
        if numer * denom < 0:
            sgn = -1
        else:
            sgn = 1
        d = gcd(numer, denom)
        self.numer = sgn * abs(numer) // d
        self.denom = abs(denom) // d
        self.sign = sgn

    ##########################

    def __repr__(self):
        """Print rational number."""
        if self.denom == 1:
            return '{}'.format(self.numer)
        else:
            return '{}/{}'.format(self.numer, self.denom)

    ##########################

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
        numer = ' ' * (minus + numer_offset + 1) + str(numer)
        denom = ' ' * (minus + denom_offset + 1) + str(denom)
        line = '-' * minus + ' ' + '\u2500'*length
        return '{}\n{}\n{}'.format(numer, line, denom)

    ##########################
    
    def inverse(self):
        """Reciprocal of rational number."""
        return Rational(self.denom, self.numer)

    ##########################

    def __add__(self, other):
        other = frac(other)
        d = gcd(self.denom, other.denom)
        self_sc = other.denom // d
        other_sc = self.denom // d
        new_numer = (self.numer * self_sc) + (other.numer * other_sc)
        new_denom = (self.denom // d) * other.denom
        return Rational(new_numer, new_denom)

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        return self + other

    ##########################

    def __sub__(self, other):
        other = frac(other)
        return self + Rational(-other.numer, other.denom)

    def __rsub__(self, other):
        return -self + other

    def __isub__(self, other):
        return self - other

    ##########################

    def __mul__(self, other):
        other = frac(other)
        return Rational( self.numer * other.numer, self.denom * other.denom )

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        return self * other

    ##########################

    def __truediv__(self, other):
        other = frac(other)
        return self * other.inverse()

    def __rtruediv__(self, other):
        return self.inverse() * other

    def __itruediv__(self, other):
        return self / other

    ##########################

    def __pow__(self, other):
        return Rational( pow(self.numer, other), pow(self.denom, other) )

    def __ipow__(self, other):
        return self**other

    ##########################

    def __mod__(self, other):
        inv_denom = mod_inverse(self.denom, other)
        return (self.numer * inv_denom) % other

    def __imod__(self, other):
        return self % other

    ##########################

    def __neg__(self):
        return Rational(-self.numer, self.denom)

    def __abs__(self):
        return Rational(abs(self.numer), self.denom)

    def __int__(self):
        return self.numer // self.denom

    def __float__(self):
        return self.numer / self.denom

    def __round__(self):
        if int(self.decimal(1)[-1]) > 4:
            shift = 1
        else:
            shift = 0
        return int(self.decimal(0)) + shift

    ##########################

    def __eq__(self, other):
        other = frac(other)
        return (self.numer * other.denom) == (other.numer * self.denom)

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        other = frac(other)
        return (self.numer * other.denom) < (other.numer * self.denom)

    def __ge__(self, other):
        return not (self < other)

    def __gt__(self, other):
        other = frac(other)
        return (self.numer * other.denom) > (other.numer * self.denom)

    def __le__(self, other):
        return not (self > other)

    ##########################

    def decimal(self, num_digits=None):
        """
        Write rational number as a decimal.
        
        Args:   int:    num_digits

        Return: str:    represented by num_digits digits
        """
        whole = int(self)
        if num_digits is None:
            num_digits = _default_values('frac_to_dec')
        if num_digits == 0:
            return whole
        remainder = self.numer % self.denom
        frac_digits = []
        while len(frac_digits) <= num_digits:
            remainder *= 10
            next_digit = remainder // self.denom
            frac_digits.append(next_digit)
            remainder %= self.denom
        if frac_digits[-1] >= 5:
            frac_digits[-2] += 1
        for i in range(len(frac_digits)-1):
            if frac_digits[-i-2] == 10:
                frac_digits[-i-2] = 0
                frac_digits[-i-3] += 1
            else:
                break
        frac_digits = [ str(d) for d in frac_digits[:-1] ]
        return str(whole) + '.' + ''.join(frac_digits)

    ##########################

    def approx_equal(self, other, num_digits=None):
        """
        If rational number is approximately equal to another rational number.
        
        Args:   Rational:   other
                int:        num_digits

        Return: bool
        """
        other = frac(other)
        return self.decimal(num_digits) == other.decimal(num_digits)

    ##########################

    def sqrt(self, num_digits=None):
        """
        Approximate square root of rational number with arbitrary precision.
        
        Args:   int:        num_digits

        Return: Rational
        """
        if num_digits is None:
            num_digits = _default_values('sqrt_digits')
        size_n = len(str(self.numer))
        size_d = len(str(self.denom))
        n_sqrt = sqrt(self.numer, num_digits + size_d + 1)
        d_sqrt = sqrt(self.denom, num_digits + size_n + 1)

        return frac(n_sqrt) / frac(d_sqrt)

############################################################
############################################################
#       Shortcuts for converting to Rational
############################################################
############################################################

def _int_to_rational(i):
    """
    Convert an integer to a rational number.
    
    Args:   int:        i
    
    Return: Rational
    """
    return Rational(i, 1)

##############################

def _float_to_rational(f):
    """
    Convert a float to a rational number.
    
    Args:   float:      f
    Return: Rational
    """
    if 'e-' in str(f):
        num, exp = str(f).split('e-')
        whole = '0'
        frac = '0'*(int(exp) - 1) + num.replace('.', '')
    else:
        whole, frac = str(f).split('.')
    return Rational( int(whole + frac), 10**len(frac) )

##############################

def _frac_to_rational(frac):
    """
    Convert a fraction string to a rational number.
    
    Args:   str:        frac
                        eg frac = 'a/b'

    Return: Rational
    """
    numer, denom = frac.split('/')
    numer.strip(' ', '')
    denom.replace(' ', '')
    return Rational( int(numer), int(denom) )

##############################

def repeating_dec_to_rational(init, repeat):
    """
    Convert a repeating decimal to a rational number.

    Args:   int/float:  init
            int:        repeat

    Return: Rational
    
    Example:    to convert 3.24178178178178... to a rational, use
                    init = 3.24,    repeat = 178
    """
    period = len(str(repeat))
    if '.' not in str(init):
        displace = 0
    else:
        displace = len(str(init).split('.')[-1])
    first = Rational(repeat, 10**(displace + period))
    one_minus_r = Rational(1,1) - Rational(1, 10**period)
    return _float_to_rational(float(init)) + (first / one_minus_r)

##############################

def _str_to_rational(s):
    """
    Convert a string to a rational number.
    
    Args:   str:        s

    Return: Rational
    """
    try:
        return _frac_to_rational(s)
    except:
        pass
    try:
        return repeating_dec_to_rational(s)
    except:
        pass
    try:
        return _float_to_rational( float(s) )
    except:
        pass
    try:
        return _int_to_rational( int(s) )
    except Exception as e:
        raise TypeError(e)

##############################

def frac(a, b=None):
    """
    A shortcut for creating an instance of the Rational class.
    
    Args:   int/float/str/Rational:     a
            int/Rational:               b

    Return: Rational
    """
    if isinstance(b, int):
        return Rational(a, b)
    elif isinstance(b, Rational):
        return a / b
    elif b is None:
        if isinstance(a, Rational):
            return a
        elif isinstance(a, int):
            return _int_to_rational(a)
        elif isinstance(a, float):
            return _float_to_rational(a)
        elif isinstance(a, str):
            return _str_to_rational(a)    
    raise ValueError('Cannot convert to rational number')

############################################################
############################################################
#       Rational approximation
############################################################
############################################################

def newton_gen(init, coeffs):
    """
    Newton's method for approximating a zero of a polynomial.

    Args:   int/float/Rational:     init        initial guess
            tuple                   coeffs      coefficients of polynomial
                                                eg use (-10, 0, 0, 1)
                                                for polynomial -10 + x^3
                                                to approximate cube root of 10

    Return: generator:  Rational
    """
    x = frac(init)
    p = polyn(coeffs)
    dp = p.deriv()
    while True:
        yield x
        x = x - p.eval(x) / dp.eval(x)

##############################

def halley_gen(init, coeffs):
    """
    Halley's method for approximating a zero of a polynomial.
    
    Args:   int/float/Rational:     init        initial guess
            tuple:                  coeffs      coefficients of polynomial

    Return: generator:  Rational
    """
    x = frac(init)
    p = polyn(coeffs)
    dp = p.deriv()
    d2p = dp.deriv()
    while True:
        yield x
        p_div_dp = p.eval(x) / dp.eval(x)
        x = x - p_div_dp / (1 - p_div_dp * d2p.eval(x) / dp.eval(x) / 2)

##############################

def sqrt(num, num_digits=None, FLOAT=False):
    """
    Square root approximation with arbitrary precision.
    
    Args:   int/float/Rational:     num
            int:                    num_digits
            bool:                   FLOAT           return a float

    Return: Rational/float

    Note:   this uses math.sqrt() for initial approximation, 
            then Babylonian method and Rational class for arbitrary precision
    """
    if num_digits is None:
        num_digits = _default_values('sqrt_digits')
   
    if isinstance(num, Rational):
        return num.sqrt()

    flx = math.sqrt(num)
    ix = int(flx)
    frx = frac(flx)
    if ix**2 == num:
        return ix
    if FLOAT == True:
        return flx
    if frx**2 == num:
        return frx

    if num >= 1:
        x = frac(ix)
    else:
        x = frx
    y = num / x

    while not x.approx_equal(y, num_digits):
        x = (x + y) * frac(1,2)
        y = num / x
 
    return x

##############################

def is_square(num):
    """
    Determine if a number is a perfect square.

    Args:   int:    num

    Return: bool
    """
    return integer_sqrt(num)**2 == num

##############################

def shape_number_nth(sides, num):
    return num * (num * (sides - 2) - sides + 4) // 2

##############################

def which_shape_number(num, sides):
    """
    Determine if a number is a shape (polygonal) number.

    Args:   int:    num, sides      sides: number of sides of polygon
    Return: bool
    """
    denom = 2 * (sides - 2)
    root = 8 * (sides - 2) * num + (sides - 4)**2
    x = frac(sides - 4 + integer_sqrt(root), denom)
    if is_square(root) and int(x) == x:
        return x

##############################

def pi(num_digits=None):
    """
    Rational approximation of pi.
    
    Args:   int:        num_digits

    Return: Rational

    Note:   this uses Ramanujan-Hardy series to approximate 1 / pi
    """
    if num_digits is None:
        num_digits = _default_values('pi_digits')
    rh = ramanujan_hardy(num_digits)
    for i in range(num_digits//7):
        next(rh)
    return next(rh).inverse()

############################################################
############################################################
#       Generators for square root approximation
############################################################
############################################################

def rough_sqrt(num):
    """
    Rough estimate of square root.
    
    Args:   int:    num

    Return: int:    half as many bits as num
    """
    if num in [0, 1]:
        return num
    elif num < 1:
        return 1 / rough_sqrt(int(1 / num))
    else:
        return num >> (len(bin(num)) // 2 - 1)

##############################

def babylonian_sqrt_gen(num, init=None):
    """
    Babylonian method to approximate square root.

    Args:   int:        num
            int:        init        initial guess

    Return: generator:  Rational
    
    Note:   this is equivalent to Newton's method
    """
    if init is None:
        x = frac(rough_sqrt(num))
    else:
        x = frac(init)
    while True:
        yield x
        x = (x + num / x) * frac(1,2)

##############################

def integer_sqrt(num):
    """Integer part of square root of a number."""
    bab = babylonian_sqrt_gen(num)
    m = int(next(bab))
    m2 = m**2
    while m2 > num or m2 + 2*m + 1 <= num:
        m = int(next(bab))
        m2 = m**2
    return m

##############################

def halley_sqrt_gen(num):
    """
    Halley's method to approximate square root.
    
    Args:   int:        num

    Return: generator:  Rational
    """
    x = frac(integer_sqrt(num))
    while True:
        yield x
        x = (x + (8 * num * x) / (3 * x**2 + num) ) * frac(1,3)

##############################

def bakhshali_sqrt_gen(num):
    """
    Bakhshali's method to approximate square root.
    
    Args:   int:        num

    Return: generator:  Rational
    """
    x = frac(integer_sqrt(num))
    while True:
        yield x
        a = (num / x - x) * frac(1,2)
        b = x + a
        x = b - a**2 / (2*b)

##############################

def goldschmidt_sqrt_gen(num):
    """
    Goldschmidt's method to approximate square root.
    
    Args:   int:        num

    Return: generator:  tuple(Rational, Rational)
    
    Note: this simultaneously approximates sqrt(num) and sqrt(1/num)
    """
    b = num
    Y = integer_sqrt(num)
    Y = 1 / Y
    y = frac(Y)
    x = num*y
    while True:
        yield x, y
        b = b * Y**2
        Y = (3 - b) * frac(1,2)
        x = x*Y
        y = y*Y

##############################

def continued_fraction_sqrt_gen(num):
    """
    Continued fraction method to approximate square root.
    
    Args:   int:        num

    Return: generator:  Rational
    """
    m = integer_sqrt(num)
    n0, n1 = 0, 1
    d0, d1 = 1, 0
    alpha = (0, 1, 1)
    while True:
        a, b, c = alpha
        q = (a + b*m) // c
        n0, n1 = n1, q*n1 + n0
        d0, d1 = d1, q*d1 + d0
        x = q * c - a
        d = num * b**2 - x**2
        g = gcd(c, d)
        alpha = (x * c // g, b * c // g, d // g)
        yield frac(n1, d1)

##############################

def generalized_continued_fraction_sqrt_gen(num):
    """
    Generalized continued fraction method to approximate square root.
    
    Args:   int:        num

    Return: generator:  Rational
    """
    m = integer_sqrt(num)
    a = num - m**2
    b = 2*m
    n0, n1 = 1, m
    d0, d1 = 0, 1
    yield frac(n1, d1)

    while True:
        n0, n1 = n1, a*n0 + b*n1
        d0, d1 = d1, a*d0 + b*d1
        yield frac(n1, d1)

##############################

def generalized_continued_fraction_sqrt_gen_2(num):
    """
    Alternate generalized continued fraction method to approximate square root.
    
    Args:   int:        num

    Return: generator: Rational

    Note:   sped up from original by collapsing 
            each pair of fractions into a single fraction.
    """
    m = integer_sqrt(num)
    r = num - m**2
    a0 = 2*m*r
    b0 = 4*num - 3*r
    a = -r**2
    b = 4*num - 2*r
    n0, n1 = m, a0 + b0*m
    d0, d1 = 1, b0
    yield frac(n0, d0)
    
    while True:
        n0, n1 = n1, a*n0 + b*n1
        d0, d1 = d1, a*d0 + b*d1
        yield frac(n1, d1)
        

##############################

def ladder_arithmetic_sqrt_gen(num):
    """
    Ladder arithmetic method to approximate square root.
    
    Args:   int:        num

    Return: generator:  Rational
    """
    m = integer_sqrt(num)
    m2 = m**2
    s0, s1 = 0, 1
    while True:
        yield m + (num - m2) * frac(s0, s1)
        s0, s1 = s1, (num - m2)*s0 + 2*m*s1

##############################
        
def linear_fractional_transformation_sqrt_gen(num, a, c):
    """
    Linear fractional transformation method to approximate square root.
    
    Args:   int:        num, a, c       a, c: parameters

    Return: generator:  Rational
    """
    b = num * c
    x = frac(a, c)
    while True:
        yield x
        x = (a*x + b) / (c*x + a)

############################################################
############################################################
#       Generators for rational approximations of pi
############################################################
############################################################

def ramanujan_hardy(num_digits):
    """
    Ramanujan-Hardy approximmation of 1/pi.

    Args:   int:        num_digits
   
    Return: generator:  Rational

    Note:   the num_digits argument is NOT in reference to 1/pi, but
            in reference to the accuracy of the approximation of sqrt(1/2)
    """
    k = 0
    multiplier = frac(2, 9801) / sqrt(.5, num_digits)
    mult_term = frac(1)
    lin_term = 1103
    value = mult_term * lin_term
    while True:
        yield multiplier * value
        k += 1
        for j in range(4):
            mult_term = mult_term * (4*k - j) / 396 / k
        lin_term = lin_term + 26390
        value += mult_term * lin_term

############################################################
############################################################
#       End
############################################################
############################################################
