#   numth/factorization/two_squares.py
#===========================================================
from functools import reduce

from ..modular import mod_sqrt
from ..types import GaussianInteger
from .main import factor, square_part, square_free_part
#===========================================================

def gaussian_divisor(prime):
    """
    Find a Gaussian Integer divisor of a prime number.

    Computes a Gaussian Integer whose norm is equal to the given prime.

    params
    + prime : int

    return
    GaussianInteger
    """
    if prime % 4 == 3:
        raise ValueError('{} does not split over Z[i]'.format(prime))

    s = min(mod_sqrt(-1, prime))
    return GaussianInteger(prime, 0).gcd(GaussianInteger(s, 1))

#-----------------------------

def is_sum_of_two_squares(factorization):
    """
    Determine whether a number can be written as a sum of two squares.

    params
    + factorization : dict
        corresponding to the number in question

    return
    bool
    """
    return 3 not in map(lambda x: x % 4, square_free_part(factorization).keys())

#-----------------------------

def two_squares_from_factorization(factorization):
    """
    Find two numbers whose squares sum to corresponding number.

    params
    + factorization : dict
        corresponding to the number in question

    return
    tuple
    """
    square = square_part(factorization)
    square_free = square_free_part(factorization)
    if is_sum_of_two_squares(square_free):
        return _square_and_square_free_to_pair(square, square_free)

#-----------------------------

def two_squares(number):
    """
    Find two numbers whose squares sum to the number.

    params
    + number : int

    return
    tuple
    """
    return two_squares_from_factorization(factor(number))

#===========================================================

def _square_to_quadratic(square_factorization):
    """Convert square_part of factorization to quadratic integer."""
    return GaussianInteger(
        reduce(
            lambda x, y: x * y,
            map(lambda z: z[0] ** (z[1] // 2), square_factorization.items()),
            1
        ), 0)

#-----------------------------

def _square_free_to_quadratic(square_free_factorization):
    """Convert square_free_part of factorization to quadratic integer."""
    return reduce(
        lambda x, y: x * y,
        map(gaussian_divisor, square_free_factorization.keys()),
        1
    )

#-----------------------------

def _quadratic_to_pair(quadratic_element):
    """Convert quadratic integer to tuple."""
    return tuple(sorted(map(abs, quadratic_element.components), reverse=True))

#-----------------------------

def _square_and_square_free_to_pair(square, square_free):
    """Convert square and square_free parts to tuple."""
    return _quadratic_to_pair(
        _square_to_quadratic(square) * _square_free_to_quadratic(square_free)
    )

