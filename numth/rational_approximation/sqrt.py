#   numth/rational_approximation/sqrt.py
#===========================================================
from ..basic import integer_sqrt
from ..types import frac, Rational 
#===========================================================

def first_approximation(number, initial=None):
    """Returns integer square root or initial value as a Rational."""
    if initial is None:
        return frac(integer_sqrt(number))
    return frac(initial)

#=============================

def babylonian_gen(number, initial=None):
    """
    Babylonian method for approximating the square root of number.

    This is equivalent to Newton's method applied to `x^2 - number`.

    params
    + number : int, float, Rational
    + initial : int, float, Rational
        initial guess

    return
    generator -> Rational
    """
    approx = first_approximation(number, initial)

    while True:
        yield approx
        approx = (approx + number / approx) / 2

#=============================

def halley_sqrt_gen(number, initial=None):
    """
    Halleys's method for approximating the square root of number.

    This is equivalent to Halley's method applied to `x^2 - number`.

    params
    + number : int, float, Rational
    + initial : int, float, Rational
        initial guess

    return
    generator -> Rational
    """
    approx = first_approximation(number, initial)

    while True:
        yield approx
        approx = (approx + 8 * number * approx / (3 * approx**2 + number)) / 3

#=============================

def bakhshali_gen(number, initial=None):
    """
    Bakhshali's method for approximating the square root of number.

    This is equivalent to two iterations of the Babylonian method.

    params
    + number : int, float, Rational
    + initial : int, float, Rational
        initial guess

    return
    generator -> Rational
    """
    approx = first_approximation(number, initial)

    while True:
        yield approx
        a = (number / approx - approx) / 2
        b = approx + a
        approx = b - a**2 / (2 * b)

#=============================

def goldschmidt_gen(number, initial=None):
    """
    Goldschmidt's method for approximating the square root of number.

    This simultaneously approimates sqrt(number) and sqrt(1 / number).

    params
    + number : int, float, Rational
    + initial : int, float, Rational
        initial guess

    return
    generator -> (Rational, Rational)
    """
    b = number
    Y = first_approximation(number, initial).inverse()
    y = Y
    x = number * y

    while True:
        yield x, y
        b = b * Y**2
        Y = (3 - b) / 2
        x = x * Y
        y = y * Y

#=============================

def ladder_arithmetic_gen(number, initial=None):
    """
    Ladder arithmetic method for approximating the square root of number.

    Similar to a continued fraction method, likely known to the Babylonians.

    params
    + number : int, float, Rational
    + initial : int, float, Rational
        initial guess

    return
    generator -> Rational
    """
    m = first_approximation(number, initial)
    m2 = m**2
    s0, s1 = 0, 1
    s = frac(0)
    
    while True:
        yield m + (number - m2) * s
        s = s.denom / ((number - m2) * s.numer + 2 * m * s.denom)

#=============================

def linear_fractional_transformation_gen(number, initial=None):
    """
    Linear frational transformation method for approximating 
    the square root of number.

    For a decent initial guess `x = a / c`, the linear functional transformation
    `f(x) = (a * x + number * c) / (c * x + a)` produces a better approximation.

    params
    + number : int, float, Rational
    + initial : int, float, Rational
        initial guess

    return
    generator -> Rational
    """
    approx = first_approximation(number, initial)
    a = approx.numer
    c = approx.denom
    b = number * c

    while True:
        yield approx
        approx = (a * approx + b) / (c * approx + a)

