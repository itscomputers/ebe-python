#   numth/basic/division.py
#===========================================================
import math
#===========================================================

def div(a, b):
    """
    Division with remainder of `a` by `b`.
    Computes `quotient` and `remainder` such that
        `0 <= remainder < abs(b)` and
        `a == b * quotient + remainder`.

    example:
        `div(55, 21) => (2, 13)`
        since `55 == 21 * 2 + 13`

    params:
        `a : int`,
        `b : int --nonzero`

    returns:
        `(quotient : int, remainder : int)`
    """
    quotient = a // b
    remainder = a % b
    if b < 0 and remainder != 0:
        quotient += 1
        remainder -= b

    return quotient, remainder

#-----------------------------

def div_with_small_remainder(a, b):
    """
    Like `numth.basic.division.div`.  Computes `quotient` and `remainder` such
    that
        `-abs(b) / 2 < remainder <= abs(b) / 2` and
        `a == b * quotient + remainder`.

    example:
        `div_with_small_remainder(55, 21) => (3, -8)`
        since `55 == 21 * 3 - 8`

    params:
        `a : int`,
        `b : int --nonzero`

    returns:
        `(quotient : int, remainder : int)`
    """
    quotient, remainder = div(a, b)

    if 2 * remainder > abs(b):
        remainder -= abs(b)
        quotient = (a - remainder) // b

    return quotient, remainder

#=============================

def gcd(*numbers):
    """
    Greatest common divisor.  Computes largest positive integer that divides
    each of given `numbers`.

    examples:
        `gcd(12, 8) => 4`,
        `gcd(12, 8, 10) => 2`

    params:
        `numbers : list of int --not all zero`

    returns:
        `int`
    """
    if 0 in numbers:
        return gcd(*filter(lambda x: x != 0, numbers))

    if len(numbers) == 0:
        raise ValueError('gcd(0, 0) is undefined')

    if len(numbers) == 1:
        return abs(*numbers)

    if len(numbers) > 2:
        first, *rest = numbers
        return gcd(first, gcd(*rest))

    return math.gcd(*numbers)

#=============================

def lcm(*numbers):
    """
    Least common multiple.  Computes smallest positive integer that is divisible
    by each of given `numbers`.

    examples:
        `lcm(12, 8) => 24`,
        `lcm(12, 8, 10) => 120`

    params:
        `numbers : list of int --not all zero`

    returns:
        `int`
    """
    if len(numbers) == 1:
        return abs(*numbers)

    if len(numbers) > 2:
        first, *rest = numbers
        return lcm(first, lcm(*rest))

    a, b = numbers
    return abs(a // gcd(a, b) * b)

#=============================

def bezout(a, b):
    """
    Finds a solution `(x, y)` to Bezout's identity:
        `a*x + b*y == gcd(a, b)`.

    example:
        `bezout(5, 7) => (3, -2)`
        since `5*3 - 7*2 == 1 == gcd(5, 7)`

    params:
        `a : int`,
        `b : int`
        `--not both zero`

    returns:
        `(x : int, y : int)`
    """
    if (a, b) == (0, 0):
        raise ValueError('bezout(0, 0) is undefined')
    if b == 0:
        return (1, 0) if a > 0 else (-1, 0)
    if b < 0:
        x, y = bezout(a, -b)
        return x, -y

    def advance(u, v, q):
        return v, u - q * v

    q, r = div(a, b)
    X = (0, 1)
    Y = (1, -q)
    while r != 0:
        a, b, = b, r
        q, r = div(a, b)
        X, Y = advance(*X, q), advance(*Y, q)

    return X[0], Y[0]

#=============================

def padic(number, base):
    """
    Computes p-adic `exponent` and `unit` part of `number` relative to `base`,
    ie satisfying
        `number == (base ** exponent) * unit`,
        `gcd(number, unit) == 1`.

    example:
        `padic(48, 2) == (4, 3)`
        since `48 == (2**4) * 3`.

    params:
        `number : int --nonzero`,
        `base : int --at least 2`

    returns:
        `(exp : int, unit : int)`
    """
    if number == 0:
        raise ValueError('number must be nonzero')

    if base < 2:
        raise ValueError('base must be at least 2')

    exp = 0
    unit = number
    while unit % base == 0:
        unit //= base
        exp += 1

    return exp, unit

