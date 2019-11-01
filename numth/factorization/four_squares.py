#   numth/factorization/four_squares.py
#===========================================================
from functools import reduce

from ..basic import jacobi
from ..types import QuaternionInteger
from .main import factor, square_part, square_free_part
from .two_squares import gaussian_divisor
#===========================================================

def quaternion_descent(quaternion_integer, prime):
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
    m = quaternion_integer.norm // prime
    if m == 1:
        return quaternion_integer
    m_q = QuaternionInteger(m, 0, 0, 0)
    return quaternion_descent(
        (quaternion_integer.conjugate * (quaternion_integer % m_q)) // m_q,
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
        return QuaternionInteger.from_gaussian_integer(gaussian_divisor(prime))

    if prime % 8 == 3:
        s = pow(2, (prime + 1) // 4, prime)
        if 2 * s > prime:
            s = prime - s
        return quaternion_descent(QuaternionInteger(s, 1, 1, 0), prime)

    t, a = 2, 5
    while jacobi(a, prime) == 1:
        t = t + 1
        a = pow(t, 2, prime) + 1

    s = pow(a, (prime + 1) // 4, prime)
    if 2 * s > prime:
        s = prime - s

    return quaternion_descent(QuaternionInteger(s, t, 1, 0), prime)

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
    quaternion_square_free = reduce(
        lambda x, y: x * y,
        map(quaternion_divisor, square_free_part(factorization).keys()),
        1
    )

    square_root = reduce(
        lambda x, y: x * y,
        map(lambda z: z[0] ** (z[1] // 2), square_part(factorization).items()),
        1
    )
    quaternion_square = QuaternionInteger(square_root, 0, 0, 0)

    return tuple(sorted(
        map(abs, (quaternion_square * quaternion_square_free).components),
        reverse=True
    ))

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

