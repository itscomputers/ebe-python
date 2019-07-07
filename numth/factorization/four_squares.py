#   numth/sum_of_four_squares.py
#===========================================================
from functools import reduce

from ..basic import jacobi
from .main import factor, square_part, square_free_part
from ..types import Quaternion
from .two_squares import gaussian_divisor, _square_to_quadratic
#===========================================================

def quaternion_descent(quaternion, prime):
    """
    Method of descent for quaternions.

    Given a quaternion and a prime dividing its norm, compute a quaternion
    whose norm is equal to the prime.

    params
    + quaternion : Quaternion
    + prime : int

    return
    Quaternion
    """
    m = quaternion.norm() // prime
    if m == 1:
        return quaternion
    return quaternion_descent(
        (quaternion.conjugate() * (quaternion % m)) // m,
        prime
    )

#-----------------------------

def quaternion_divisor(prime):
    """
    Find a quaternion divisor of a prime.

    Given a prime, compute a quaternion whose norm is equal to the prime.

    params
    + prime : int

    return
    Quaternion
    """
    if prime == 2 or prime % 4 == 1:
        return _quadratic_to_quaternion(gaussian_divisor(prime))

    if prime % 8 == 3:
        s = pow(2, (prime + 1) // 4, prime)
        if 2 * s > prime:
            s = prime - s
        return quaternion_descent(Quaternion(s, 1, 1, 0), prime)
    
    t, a = 2, 5
    while jacobi(a, prime) == 1:
        t = t + 1
        a = pow(t, 2, prime) + 1

    s = pow(a, (prime + 1) // 4, prime)
    if 2 * s > prime:
        s = prime - s

    return quaternion_descent(Quaternion(s, t, 1, 0), prime)

#-----------------------------

def four_squares_from_factorization(factorization):
    """
    Find four numbers whose squares sum to a given number.

    params
    + factorization : dict
        corresponding to the number in question

    return
    tuple
    """
    square = square_part(factorization)
    square_free = square_free_part(factorization)
    return _square_and_square_free_to_quadruple(square, square_free)

#-----------------------------

def four_squares(number):
    """
    Find four numbers whose squares sum to a number.

    params
    + number : int

    return
    tuple
    """
    return four_squares_from_factorization(factor(number))

#===========================================================

def _quaternion_to_quadruple(quaternion_element):
    """Convert quaternion to tuple."""
    return tuple(sorted(map(abs, quaternion_element.components), reverse=True))

#-----------------------------

def _square_and_square_free_to_quadruple(square, square_free):
    """Convert square and square_free parts to tuple."""
    return _quaternion_to_quadruple(
        _square_to_quaternion(square) * _square_free_to_quaternion(square_free)
    )

#-----------------------------

def _square_free_to_quaternion(square_free_factorization):
    """Convert square_free_part to Quaternion."""
    return reduce(
        lambda x, y: x * y,
        map(quaternion_divisor, square_free_factorization.keys()),
        1
    )

#-----------------------------

def _square_to_quaternion(square_factorization):
    """Convert square_part to Quaternion."""
    return _quadratic_to_quaternion(_square_to_quadratic(square_factorization))

#-----------------------------

def _quadratic_to_quaternion(quadratic_element):
    """Convert Quadratic to Quaternion."""
    return Quaternion(quadratic_element.real, quadratic_element.imag, 0, 0)

