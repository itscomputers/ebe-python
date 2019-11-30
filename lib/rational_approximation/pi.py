#   lib/rational_approximation/pi.py
#   - module for rational approximation of pi

#===========================================================
from ..config import default
from ..types import Rational
#===========================================================
__all__ = [
    'ramanujan_hardy',
    'pi',
]
#===========================================================

def ramanujan_hardy(sqrt_digits):
    """
    Generate Ramanujan-Hardy sequence that approximates 1 / pi.

    + sqrt_digits: int --number of digits for approximation of sqrt(2)
    ~> Iterator[Rational]
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

def pi(num_digits=None):
    """
    Compute rational approximation of pi.

    + num_digits: int
    ~> Rational
    """
    if num_digits is None:
        num_digits = default('pi_digits')

    rh = ramanujan_hardy(num_digits)

    for i in range(num_digits // 8):
        next(rh)

    return next(rh).inverse

