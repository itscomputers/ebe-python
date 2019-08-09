#   numth/rational_approximation/pi.py
#===========================================================
from typing import Iterator

from ..config import default
from ..types import Rational
#===========================================================

def ramanujan_hardy(sqrt_digits: int) -> Iterator[Rational]:
    """
    Generator for Ramanujan-Hardy series that approximates 1 / pi.

    params
    + sqrt_digits : int
        number of digits of accuracy for approximation of sqrt(2)

    return
    generator -> Rational
    """
    k = 0
    multiplier = Rational(2, 9801) * Rational(2, 1).sqrt(sqrt_digits)
    multiplicative_term = Rational(1, 1)
    linear_term = 1103
    value = multiplicative_term * linear_term

    while True:
        yield multiplier * value
        k = k + 1
        for j in range(4):
            multiplicative_term = multiplicative_term * (4*k - j) / 396 / k
        linear_term = linear_term + 26390
        value = value + multiplicative_term * linear_term

#=============================

def pi(num_digits: int = None) -> Rational:
    """
    Rational approximation of pi.

    params
    + num_digits : int
        number of digits of accuracy for approximation

    return
    Rational
    """
    if num_digits is None:
        num_digits = default('pi_digits')

    rh = ramanujan_hardy(num_digits)

    for i in range(num_digits // 8):
        next(rh)

    return next(rh).inverse()

