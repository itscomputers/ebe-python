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
    square_free = square_free_part(factorization)
    if not is_sum_of_two_squares(square_free):
        return None

    gaussian_square_free = reduce(
        lambda x, y: x * y,
        map(gaussian_divisor, square_free.keys()),
        1
    )

    square_root = reduce(
        lambda x, y: x * y,
        map(lambda z: z[0] ** (z[1] // 2), square_part(factorization).items()),
        1
    )
    gaussian_square = GaussianInteger(square_root, 0)

    return tuple(sorted(
        map(abs, (gaussian_square * gaussian_square_free).components),
        reverse=True
    ))

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

