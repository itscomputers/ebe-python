
#   numth/rational.py

import numth.numth as numth
import numth.polynomial as polynomial
import math

##############################

def _default_values(cat):
    if cat == 'frac_to_dec':
        return 20
    if cat == 'sqrt_digits':
        return 20
    if cat == 'pi_digits':
        return 20

############################################################
############################################################
#       Rational class
############################################################
############################################################

class Rational:
    """Class for arithmetic of rational numbers."""
    def __init__(self, numer: int, denom: int) -> None:
        if denom == 0:
            raise ValueError('Attempt to divide by zero')
        
        if numer * denom < 0:
            sgn = -1
        else:
            sgn = 1
        d = numth.gcd(numer, denom)
        self.numer = sgn * abs(numer) // d
        self.denom = abs(denom) // d

    def __repr__(self):
        if self.numer * self.denom < 0:
            sgn = -1
        else:
            sgn = 1
        if self.denom == 1:
            return '{}'.format(self.numer)
        else:
            return '{}/{}'.format(self.numer, self.denom)

    ##########################
    
    def inverse(self):
        return Rational(self.denom, self.numer)

    ##########################

    def __add__(self, other):
        other = frac(other)
        d = numth.gcd(self.denom, other.denom)
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
        """Write a rational number as a decimal."""
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
        """Determine if a rational number is approximately equal
        to another rational number, up to a given number of digits."""
        other = frac(other)
        return self.decimal(num_digits) == other.decimal(num_digits)

    ##########################

    def sqrt(self, num_digits=None):
        """Approximate square root with arbitrary precision."""
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

def int_to_rational(a: int) -> Rational:
    """Convert an integer to a rational number."""
    return Rational(a, 1)

##############################

def float_to_rational(a: float) -> Rational:
    """Convert a float to a rational number."""
    if 'e-' in str(a):
        num, exp = str(a).split('e-')
        whole = '0'
        frac = '0'*(int(exp) - 1) + num.replace('.', '')
    else:
        whole, frac = str(a).split('.')
    return Rational( int(whole + frac), 10**len(frac) )

##############################

def frac_to_rational(frac: str) -> Rational:
    """Convert a string 'a/b' to a rational number."""
    numer, denom = frac.split('/')
    numer.strip(' ', '')
    denom.replace(' ', '')
    return Rational( int(numer), int(denom) )

##############################

def repeating_dec_to_rational(initial, repeat: int) -> Rational:
    """
    Convert a repeating decimal to a rational number.

    Comment:
    To convert 3.24178178178178... to a fraction, use input (3.24, 178)
    """
    period = len(str(repeat))
    if '.' not in str(initial):
        displace = 0
    else:
        displace = len(str(initial).split('.')[-1])
    first = Rational(repeat, 10**(displace + period))
    one_minus_r = Rational(1) - Rational(1, 10**period)
    return float_to_rational(initial) + (first / one_minus_r)

##############################

def str_to_rational(s: str) -> Rational:
    """Convert a string to a rational number."""
    try:
        return frac_to_rational(s)
    except:
        pass
    try:
        return repeating_dec_to_rational(s)
    except:
        pass
    try:
        return frac( float(s) )
    except:
        pass
    try:
        return frac( int(s) )
    except Exception as e:
        raise TypeError(e)

##############################

def frac(a, b=None) -> Rational:
    """A shortcut function for creating an instance of the Rational class."""
    if isinstance(b, int):
        return Rational(a, b)
    elif isinstance(b, Rational):
        return a / b
    elif b is None:
        if isinstance(a, Rational):
            return a
        elif isinstance(a, int):
            return int_to_rational(a)
        elif isinstance(a, float):
            return float_to_rational(a)
        elif isinstance(a, str):
            return str_to_rational(a)    
    raise ValueError('Cannot convert to rational number')

############################################################
############################################################
#       Rational approximation
############################################################
############################################################

def newton_gen(init, coeffs):
    """
    Newton's method for approximating a zero of a polynomial.
    
    Example:
    For the polynomial -10 + x^3, which has coeffs = (-10, 0, 0, 1),
    and an initial guess near 2, this will approximate cube root of 10.
    """
    x = frac(init)
    p = polynomial.polyn(coeffs)
    dp = p.deriv()
    while True:
        yield x
        x = x - p.eval(x) / dp.eval(x)

##############################

def halley_gen(init, coeffs):
    """Halley's method for approximating a zero of a polynomial."""
    x = frac(init)
    p = polynomial.polyn(coeffs)
    dp = p.deriv()
    d2p = dp.deriv()
    while True:
        yield x
        p_div_dp = p.eval(x) / dp.eval(x)
        x = x - p_div_dp / (1 - p_div_dp * d2p.eval(x) / dp.eval(x) / 2)

##############################

def sqrt(num, num_digits=None, FLOAT=False):
    """Square root approximation with arbitrary precision."""
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

def Pi(num_digits=None):
    """Rational approximation of pi."""
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
    """Rough estimate of square root to be used in other approximations."""
    if num in [0, 1]:
        return num
    elif num < 1:
        return 1 / rough_sqrt(int(1 / num))
    else:
        return num >> (len(bin(num)) // 2 - 1)

##############################

def babylonian_sqrt_gen(num, init=None):
    """
    Generator for Babylonian square root approximation.

    Comments:
    An initial value may be supplied for faster convergence.
    This is equivalent to Newton's method.
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
    """Computer integer part of square root of a number."""
    bab = babylonian_sqrt_gen(num)
    m = int(next(bab))
    m2 = m**2
    while m2 > num or m2 + 2*m + 1 <= num:
        m = int(next(bab))
        m2 = m**2
    return m

##############################

def halley_sqrt_gen(num):
    """Generator for Halley's square root approximation."""
    x = frac(integer_sqrt(num))
    while True:
        yield x
        x = (x + (8 * num * x) / (3 * x**2 + num) ) * frac(1,3)

##############################

def bakhshali_sqrt_gen(num):
    """Generator for Bakhshali's square root approximation."""
    x = frac(integer_sqrt(num))
    while True:
        yield x
        a = (num / x - x) * frac(1,2)
        b = x + a
        x = b - a**2 / (2*b)

##############################

def goldschmidt_sqrt_gen(num):
    """
    Generator for Goldschmidt's square root approximation.

    Comment:
    This simultaneously approximates sqrt(num) and sqrt(1/num)
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
    """Generator for the continued fraction convergents 
    of the square root of a number."""
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
        g = numth.gcd(c, d)
        alpha = (x * c // g, b * c // g, d // g)
        yield frac(n1, d1)

##############################

def generalized_continued_fraction_sqrt_gen(num):
    """Generator for the generalized continued fraction convergents."""
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
    """Generator for the generalized continued fraction convergents,
    sped up by collapsing each pair of fractions into a single."""
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
    """Generator for square root approximation using ladder arithmetic."""
    m = integer_sqrt(num)
    m2 = m**2
    s0, s1 = 0, 1
    while True:
        yield m + (num - m2) * frac(s0, s1)
        s0, s1 = s1, (num - m2)*s0 + 2*m*s1

##############################
        
def linear_fractional_transformation_sqrt_gen(num, a, c):
    """Generator for square root approximation 
    using linear fractional transformations."""
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
    Ramanujan's original approximmation of pi.
    
    Comment:
    num_digits refers to the decimal accuracy of the
    approximation of sqrt(1/2).
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
############################################################
############################################################
############################################################

##  testing

#############################

if __name__ == '__main__':

    ##########################
    #   test Rational class
    a = frac(3,4)
    b = frac(.4)
    c = frac(3)
    assert( a + b == frac(23,20) and a + b == 1.15 )
    assert( a + c == frac(15,4) and a + c == 3.75 )
    assert( b + c == frac(17,5) and b + c == 3.4 )
    assert( a + 3 == a + c and 3 + a == a + c )
    assert( a + b == b + a and a + c == c + a and b + c == c + b )
    assert( a - b == frac(7,20) and a - b == .35 )
    assert( a - c == frac(-9,4) and a - c == -2.25 )
    assert( b - c == frac(-13,5) and b - c == -2.6 )
    assert( a - b == -b + a and a - c == -c + a and b - c == -c + b )
    assert( b - a == -a + b and c - a == -a + c and c - b == -b + c )
    assert( a - 3 == a - c and 3 - a == c - a )
    assert( a * b == frac(3,10) and a * b == .3 )
    assert( a * c == frac(9,4) and a * c == 2.25 )
    assert( b * c == frac(6,5) and b * c == 1.2 )
    assert( a * b == b * a and a * c == c * a and b * c == b * c )
    assert( a * 3 == a * c and 3 * a == c * a )
    assert( a / b == frac(15,8) and a / b == 1.875 )
    assert( a / c == frac(1,4) and a / c == .25 )
    assert( c / b == frac(15,2) and c / b == 7.5 )
    assert( a / b == 1 / (b / a)\
            and a / c == 1 / (c / a)\
            and b / c == 1 / (c / b) )
    assert( a / 3 == a / c and 3 / a == c / a )
    assert( a + a == 2 * a and a - a == 0 )
    assert( b * b == b**2 and b / b == 1 )
    assert( a.inverse() * a == 1 )
    assert( b.inverse() * b == 1 )
    assert( c.inverse() * c == 1 )
    assert( int(a) == 0 and int(b) == 0 )
    assert( round(a) == 1 and round(b) == 0 )
    assert( float(a) == .75  and float(b) == .4 )
    assert( -a == frac(-3,4) and -b == frac(-.4) )
    assert( abs(-a) == a and abs(-b) == b )
    assert( b < a and a < c and b < c )
    assert( -b > -a and -a > -c and -b > -c )
    assert( a % 13 == 4 and b % 13 == 3 )
    assert( frac(.599).decimal(2) == '0.60' )
    assert( frac(100,49).sqrt() == frac(10,7) )
