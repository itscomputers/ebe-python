#   numth/rational_approximation/sqrt.py
#===========================================================
from typing import Iterator, Tuple, Union

from ..basic import integer_sqrt
from ..continued_fraction import continued_fraction_convergents
from ..types import frac, Rational, Quadratic

Number = Union[int, float, Rational]
#===========================================================

def first_approximation(
        number: int,
        initial: Number = None
    ) -> Rational:
    """Returns integer square root or initial value as a Rational."""
    if initial is None:
        return frac(integer_sqrt(number))
    return frac(initial)

#=============================

def babylonian_gen(
        number: int,
        initial: Number = None
    ) -> Iterator[Rational]:
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

def halley_sqrt_gen(
        number: int,
        initial: Number = None
    ) -> Iterator[Rational]:
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

def bakhshali_gen(
        number: int,
        initial: Number = None
    ) -> Iterator[Rational]:
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

def continued_fraction_convergent_gen(number: int) -> Iterator[Rational]:
    """
    Continued fraction convergent approximations for square root of number.

    params
    + number : int

    return
    geneartor -> Rational
    """
    def to_quadratic(pair):
        return Quadratic(pair[0], pair[1], number)
    
    def to_rational(quadratic):
        return Rational(quadratic.real, quadratic.imag)

    convergents = continued_fraction_convergents(number)
    quadratics = list(map(to_quadratic, convergents))
    last = quadratics[-1]
    
    while True:
        for quadratic in quadratics:
            yield to_rational(quadratic)
        
        quadratics = list(map(lambda q: q * last, quadratics))

#=============================

def goldschmidt_gen(
        number: int,
        initial: Number = None
    ) -> Iterator[Tuple[Rational, Rational]]:
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
    b = frac(number)
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

def ladder_arithmetic_gen(
        number: int,
        initial: Number = None
    ) -> Iterator[Rational]:
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

def linear_fractional_transformation_gen(
        number: int,
        initial: Number = None
    ) -> Iterator[Rational]:
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

