#   numth/rational_approximation/pi.py
#===========================================================
from ..types import Rational
#===========================================================

def _default_values(category):
    return {
        'pi'    :   20,
    }[category]

#=============================

def ramanujan_hardy(sqrt_digits):
    k = 0
    multiplier = Rational(2, 9801) / Rational(1, 2).sqrt(sqrt_digits)
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
    if num_digits is None:
        num_digits = _default_values('pi')

    rh = ramanujan_hardy(num_digits)

    for i in range(num_digits // 7):
        next(rh)

    return next(rh).inverse()

