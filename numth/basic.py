#   numth/basic.py
#===========================================================
import math
#===========================================================

def div(number, divisor):
    """
    Division with remainder.

    Args:   number:     int
            divisor:    int != 0

    Return: quotient:   int
            remainder:  int

    Notes:  0 <= remainder < abs(divisor)
            number = quotient * divisor + remainder
    """
    if divisor == 0:
        raise ValueError('Attempted division by zero')

    quotient = number // divisor
    remainder = number % divisor
    if divisor < 0 and remainder != 0:
        quotient += 1
        remainder -= divisor

    return quotient, remainder

#-----------------------------

def div_with_small_remainder(number, divisor):
    """
    Division with (smaller) remainder, similar to `div`.

    Note:  -abs(divisor) / 2 < remainder <= abs(divisor) / 2
    """
    quotient, remainder = div(number, divisor)
    
    if 2 * remainder > abs(divisor):
        remainder -= abs(divisor)
        quotient = (number - remainder) // divisor

    return quotient, remainder 

#-----------------------------

def euclidean_algorithm(a, b, division=div):
    """
    Euclidean algorithm.

    Args:   a:          int
            b:          int != 0
            [division:  function (either `div` or `div_with_small_remainder)]

    Return: None

    Note: prints a = q * b + r, using division with remainder until r == 0
    """
    q, r = division(a, b)
    print('{} = {} * {} + {}'.format(a, q, b, r))
    if r != 0:
        euclidean_algorithm(b, r, division)

#-----------------------------

def gcd(a, b):
    """
    Greatest common divisor.

    Args:   a:  int
            b:  int     (a, b) != (0, 0)

    Return: d:  int     d is the largest positive integer dividing both a and b
    """
    if (a, b) == (0, 0):
        raise VAlueError('gcd(0, 0) is undefined')

    if b == 0:
        return abs(a)
    else:
        return gcd(b, a % b)

#-----------------------------

def lcm(a, b):
    """
    Least common multiple.

    Args:   a:  int
            b:  int     a * b != 0

    Return: m:  int     m is the smallest positive integer divisible by both a and b
    """
    if a * b == 0:
        raise ValueError('lcm(_, 0) is undefined')

    return abs(a // gcd(a, b) * b)

#-----------------------------

def bezout(a, b):
    """
    Bezout's Lemma: integer solution (x, y) to a*x + b*y = gcd(a, b)

    Args:   a:  int
            b:  int     (a, b) != (0, 0)

    Return: x:  int
            y:  int     a*x + b*y == gcd(a, b)
    """
    if (a, b) == (0, 0):
        raise ValueError('gcd(0, 0) is undefined')

    if b == 0:
        return a // abs(a), 0

    nums = (a, b)
    q, r = div(*nums)
    X = (0, 1)
    Y = (1, -q)

    def advance(u, v, q):
        return v, u - q*v

    while r != 0:
        nums = nums[1], r
        q, r = div(*nums)
        X = advance(*X, q)
        Y = advance(*Y, q)
        
    if a*X[0] + b*Y[0] > 0:
        sign = 1
    else:
        sign = -1
    return sign * X[0], sign * Y[0]

#-----------------------------

def padic(number, base):
    """
    p-adic representation.

    Args:   number: int     number != 0
            base:   int     base > 1

    Return: exp:    int     num == (base**exp) * rest
            rest:   int     rest % base != 0
    """
    if number == 0:
        raise ValueError('number must be nonzero')

    if base < 2:
        raise ValueError('base must be at least 2')

    exp = 0
    rest = number
    while rest % base == 0:
        exp += 1
        rest //= base
    
    return exp, rest

#-----------------------------

def integer_sqrt(number):
    """
    Integer part of the square root of a number.

    Args:   number: int     number >= 0

    Return: val:    int     val <= sqrt(num) < val + 1
    """
    val = int(math.sqrt(number))

    while val**2 > number or (val+1)**2 <= number:
        val = (val + number // val) // 2

    return val

#-----------------------------

def is_square(number):
    """
    Args:   number:     int

    Return: is_square:  bool
    """
    return integer_sqrt(number)**2 == number

#-----------------------------

def mod_inverse(number, modulus):
    """
    Args:   number:     int
            modulus:    int     modulus > 1

    Return: inverse:    int     (number * inverse) % modulus == 1
    """
    if modulus < 2:
        raise ValueError('Modulus must be at least 2')

    x, y = bezout(number, modulus) 
    
    if number*x + modulus*y not in [1, -1]:
        raise ValueError(
                '{} is not invertible modulo {}'
                .format(number, modulus))

    if x < 0:
        x += modulus

    return x

#-----------------------------

def mod_power(number, exponent, modulus):
    """
    Power of a number relative to a modulus.

    Args:   number:     int
            exponent:   int     (could be negative)
            modulus:    int     modulus > 1

    Return: val:        int     val == (num**exp) % mod
    """
    if modulus < 2:
        raise ValueError('Modulus must be at least 2')

    if exponent < 0:
        return pow(mod_inverse(number, modulus), -exponent, modulus)
    else:
        return pow(number, exponent, modulus)

#-----------------------------

def jacobi(a, b):
    """
    Jacobi symbol (a | b).

    Args:   a:      int
            b:      int         b odd

    Return: val:    int         val in [1, 0, -1]
    """
    if b % 2 == 0:
        raise ValueError(
                'Jacobi symbol is undefined when second argument is even')

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
        return sgn * jacob(b, a_)

