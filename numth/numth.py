
#   numth/numth.py

##############################

def default_values(kind):
    if kind == 'frac_to_dec':
        return 20

##############################

def div(num: int, div: int, METHOD=None) -> (int, int):
    """
    Performs division and returns the quotient and remainder.

    Keyword arguments:
    METHOD -- None (default) or SMALL (for small remainders)
    """
    if div == 0:
        raise ValueError('Attempted division by zero')
    
    if div > 0 or num == 0:
        q, r = num//div, num%div
    else:
        q, r = num//div + 1, (num%div) + abs(div)

    if (METHOD == 'SMALL') and (r > abs(div)//2):
        q += div // abs(div)
        r -= abs(div)

    return q, r

##############################

def euclidean_algorithm(a: int, b: int, METHOD=None) -> None:
    """
    Prints the Euclidean algorithm on two integers.

    Keyword arguments:
    METHOD -- None (default) or SMALL (for small remainders)
    """
    q, r = div(a, b, METHOD)
    print('{} = {} * {} + {}'.format(a, q, b, r))
    if r != 0:
        euclidean_algorithm(b, r, METHOD)

##############################

def gcd(a: int, b: int) -> int:
    """Computes the greatest common divisor of two integers."""
    if (a, b) == (0, 0):
        raise ValueError('gcd(0, 0) is undefined')
    
    a_, b_ = a, b
    while b_ != 0:
        a_, b_ = b_, div(a_, b_, METHOD='SMALL')[1]
    return abs(a_)

##############################

def lcm(a: int, b: int) -> int:
    """Computes the least common multiple of two integers."""
    if a*b == 0:
        raise ValueError('lcm(_,0) is undefined')
    
    return a // gcd(a, b) * b

##############################

def bezout(a: int, b: int) -> (int, int):
    """
    Computes an integer solution to Bezout's lemma.

    Return:
    x, y -- satisfying a*x + b*y == gcd(a, b)
    """
    if (a, b) == (0, 0):
        raise ValueError('gcd(0, 0) is undefined')

    if b == 0:
        if a > 0:
            return 1, 0
        else:
            return -1, 0

    a_, b_ = a, b
    q, r = div(a_, b_, METHOD='SMALL')
    xx, x = 0, 1
    yy, y = 1, -q

    while r != 0:
        a_, b_ = b_, r
        q, r = div(a_, b_, METHOD='SMALL')
        xx, x = x, -q*x + xx
        yy, y = y, -q*y + yy

    if a*xx + b*yy > 0:
        return xx, yy
    else:
        return -xx, -yy
        
##############################

def padic(num: int, base: int) -> (int, int):
    """
    Computes p-adic representation of a number.

    Return:
    exp, rest -- satisfying num == (base**exp) * rest and rest % base != 0
    """
    if base < 2:
        raise ValueError('p-adic base must be at least 2')

    exp = 0
    rest = num
    while rest % base == 0:
        exp += 1
        rest //= base
    return exp, rest

##############################

def mod_inverse(num: int, mod: int) -> int:
    """
    Computes the inverse of a number relative to a modulus.

    Returns:
    inv -- satisfying (num * inv) % mod == 1
    """
    if mod < 1:
        raise ValueError('Modulus must be at least 2')
    if gcd(num, mod) != 1:
        raise ValueError('{} is not invertible modulo {}'.format(num, mod))

    return bezout(num, mod)[0] % mod

##############################

def mod_power(num: int, exp: int, mod: int) -> int:
    """
    Computes power of a number relative to a modulus.

    Returns:
    (num**exp) % mod -- even for negative exp
    """
    if mod < 2:
        raise ValueError('Modulus must be at least 2')

    if exp < 0:
        return pow(mod_inverse(num, mod), -exp, mod)
    else:
        return pow(num, exp, mod) 

##############################

def jacobi(a: int, b: int) -> int:
    """
    Computes Jacobi symbol for two integers.

    Returns:
    the Jacobi symbol ( a | b ) == 1, 0, or -1
    """
    if b % 2 == 0:
        raise ValueError(
                'Jacobi symbol ( {} | {} ) is undefined'.format(num, mod))

    if b == 1:
        return 1
    if gcd(a, b) != 1:
        return 0

    exp, a_ = padic(a % b, 2)
    if (exp % 2 == 1) and (b % 8 in [3, 5]):
        sgn = -1
    else:
        sgn = 1
    if a_ == 1:
        return sgn
    else:
        if (b % 4 != 1) and (a_ % 4 != 1):
            sgn *= -1
        return sgn * jacobi(b, a_)

##############################



############################################################
############################################################
#       Rational class
############################################################
############################################################

class Rational:
    """Class for arithmetic in rational numbers."""
    def __init__(self, numer: int, denom: int) -> None:
        if denom == 0:
            raise ValueError('Attempt to divide by zero')
        
        if numer * denom < 0:
            sgn = -1
        else:
            sgn = 1
        d = gcd(numer, denom)
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
        return round(float(self))

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
            num_digits = default_values('frac_to_dec')
        if num_digits == 0:
            return whole
        remainder = self.numer % self.denom
        frac = '.'
        while len(frac) < num_digits:
            remainder *= 10
            next_digit = remainder // self.denom
            frac += str(next_digit)
            remainder %= self.denom
        remainder *= 10
        next_digit = remainder // self.denom
        remainder %= self.denom
        if 2 * remainder >= self.denom:
            next_digit += 1
        frac += str(next_digit)
        return str(whole) + frac

############################################################

def int_to_rational(a: int) -> Rational:
    """Convert an integer to a rational number."""
    return Rational(a, 1)

def float_to_rational(a: float) -> Rational:
    """Convert a float to a rational number."""
    whole, frac = str(a).split('.')
    return Rational( int(whole + frac), 10**len(frac) )

def frac_to_rational(frac: str) -> Rational:
    """Convert a string 'a/b' to a rational number."""
    numer, denom = frac.split('/')
    numer.strip(' ', '')
    denom.replace(' ', '')
    return Rational( int(numer), int(denom) )

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

def frac(a, b=None) -> Rational:
    """A shortcut function for creating an instance of the Rational class."""
    if b:
        return Rational(a, b)
    elif isinstance(a, Rational):
        return a
    elif isinstance(a, int):
        return int_to_rational(a)
    elif isinstance(a, float):
        return float_to_rational(a)
    elif isinstance(a, str):
        return str_to_rational(a)
    else:
        raise ValueError('Cannot convert to rational number')

############################################################
############################################################







############################################################
############################################################
############################################################
############################################################
############################################################

##  testing

#############################

if __name__ == '__main__':
    from random import randint, choice
    
    ##########################
    #   test div
    for j in range(10):
        a, b = (choice([-1,1]) * randint(1,10**6) for i in range(2))
        q, r = div(a, b)
        assert( a == q*b + r )
        assert( r < abs(b) )
        q, r = div(a, b, 'SMALL')
        assert( a == q*b + r )
        assert( (r <= abs(b)//2) and (r > -abs(b)//2) )

    #########################
    #   test gcd
    for j in range(10):
        a, b = (choice([-1,1]) * randint(1,10**6) for i in range(2))
        d = gcd(a, b)
        assert( (a%d, b%d) == (0, 0) )
        assert( gcd(a//d, b//d) == 1 )

    ##########################
    #   test lcm
    for j in range(10):
        a, b = (choice([-1,1]) * randint(1,10**6) for i in range(2))
        m = lcm(a, b)
        assert( (m%a, m%b) == (0, 0) )
        assert( gcd(m//a, m//b) == 1 )

    ##########################
    #   test bezout
    for j in range(10):
        a, b = (choice([-1,1]) * randint(1,10**6) for i in range(2))
        x, y = bezout(a, b)
        d = gcd(a, b)
        assert( a*x + b*y == d )

    ##########################
    #   test padic
    for j in range(10):
        num, base = choice([-1,1])*randint(1,10**6), randint(2,10**6)
        exp, rest = padic(num, base)
        assert( num == base**exp * rest )
        assert( rest % base != 0 )

    ##########################
    #   test mod_inverse
    for j in range(10):
        num, mod = choice([-1,1])*randint(1,10**6), randint(2,10**6)
        while gcd(num, mod) != 1:
            num += 1
        inv = mod_inverse(num, mod)
        assert( inv > 0 and inv < mod )
        assert( (num * inv) % mod == 1 )

    ##########################
    #   test mod_power
    for j in range(10):
        num, exp, mod = (randint(1,10**4) for i in range(3))
        ans = mod_power(num, exp, mod)
        assert( (num**exp) % mod == ans )
        if gcd(num, mod) == 1:
            inv = mod_power(num, -exp, mod)
            assert( mod_inverse(ans, mod) == inv )

    ##########################
    #   test jacobi
    jacobi_row_15 = [0,1,1,0,1,0,0,-1,1,0,0,-1,0,-1,-1]
    assert( [jacobi(a, 15) for a in range(15)] == jacobi_row_15 )

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
