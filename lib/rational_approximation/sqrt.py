#   lib/rational_approximation/sqrt.py
#   - module for rational approximation of square roots

# ===========================================================
from ..basic import integer_sqrt
from ..continued_fraction import continued_fraction_convergents
from ..types import frac, QuadraticInteger

# ===========================================================
__all__ = [
    "babylonian_gen",
    "halley_sqrt_gen",
    "bakhshali_gen",
    "continued_fraction_convergent_gen",
    "goldschmidt_gen",
    "ladder_arithmetic_gen",
    "linear_fractional_transformation_gen",
]
# ===========================================================


def babylonian_gen(number, initial=None):
    """
    Generate approximations of `sqrt(number)` using Babylonian method.
    This is equivalent to Newton's method applied to `x^2 - number`.

    + number: Union[int, float, Rational]
    + initial: Union[int, float, Rational]
    ~> Iterator[Rational]
    """
    approx = _first_approximation(number, initial)

    while True:
        yield approx
        approx = (approx + number / approx) / 2


# =============================


def halley_sqrt_gen(number, initial=None):
    """
    Generate approximations of `sqrt(number)` using Halley's method.

    + number: Union[int, float, Rational]
    + initial: Union[int, float, Rational]
    ~> Iterator[Rational]
    """
    approx = _first_approximation(number, initial)

    while True:
        yield approx
        approx = (approx + 8 * number * approx / (3 * approx ** 2 + number)) / 3


# =============================


def bakhshali_gen(number, initial=None):
    """
    Generate approximations of `sqrt(number)` using Bakhshali's method.
    This is equivalent to two iterations of the Babylonian method.

    + number: Union[int, float, Rational]
    + initial: Union[int, float, Rational]
    ~> Iterator[Rational]
    """
    approx = _first_approximation(number, initial)

    while True:
        yield approx
        a = (number / approx - approx) / 2
        b = approx + a
        approx = b - a ** 2 / (2 * b)


# =============================


def continued_fraction_convergent_gen(number):
    """
    Generate approximations of `sqrt(number)` using continued fractions.

    + number: int
    ~> Iterator[Rational]
    """

    def to_quadratic_integer(pair):
        return QuadraticInteger(pair[0], pair[1], number)

    def to_rational(quadratic_integer):
        return frac(quadratic_integer.real, quadratic_integer.imag)

    convergents = continued_fraction_convergents(number)
    quadratics = list(map(to_quadratic_integer, convergents))
    last = quadratics[-1]

    while True:
        for quadratic_integer in quadratics:
            yield to_rational(quadratic_integer)

        quadratics = list(map(lambda q: q * last, quadratics))


# =============================


def goldschmidt_gen(number, initial=None):
    """
    Generate approximations of `sqrt(number)` using Goldschmidt's method.
    This simultaneously approximates `sqrt(number)` and `sqrt(1 / number)`.

    + number: Union[int, float, Rational]
    + initial: Union[int, float, Rational]
    ~> Iterator[Tuple[Rational, Rational]]
    """
    b = number
    Y = _first_approximation(number, initial).inverse
    y = Y
    x = number * y

    while True:
        yield x, y
        b = b * Y ** 2
        Y = (3 - b) / 2
        x = x * Y
        y = y * Y


# =============================


def ladder_arithmetic_gen(number, initial=None):
    """
    Generate approximations of `sqrt(number)` using ladder arithmetic.
    Similar to a continued fraction method, likely known to the Babylonians.

    + number: Union[int, float, Rational]
    + initial: Union[int, float, Rational]
    ~> Iterator[Rational]
    """
    m = _first_approximation(number, initial)
    m2 = m ** 2
    s0, s1 = 0, 1
    s = frac(0)

    while True:
        yield m + (number - m2) * s
        s = s.denom / ((number - m2) * s.numer + 2 * m * s.denom)


# =============================


def linear_fractional_transformation_gen(number, initial=None):
    """
    Generate approximations of `sqrt(number)` using linear fractional
    transformations.  For a decent initial guess `x = a / c`, the linear
    fractional transformation `f(x) = (a * x + number * c) / (c * x + a)`
    produces a good approximation.

    + number: Union[int, float, Rational]
    + initial: Union[int, float, Rational]
    ~> Iterator[Rational]
    """
    approx = _first_approximation(number, initial)
    a = approx.numer
    c = approx.denom
    b = number * c

    while True:
        yield approx
        approx = (a * approx + b) / (c * approx + a)


# =============================


def _first_approximation(number, initial=None):
    """Returns integer square root or initial value as a Rational."""
    if initial is None:
        return frac(integer_sqrt(number))
    return frac(initial)
