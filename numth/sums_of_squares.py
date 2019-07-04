#   numth/sums_of_squares.py
#===========================================================
from functools import reduce

from .basic import jacobi
from .factorization import factor, square_part, square_free_part
from .modular import mod_sqrt
from .quadratic import Quadratic
from .quaternion import Quaternion
#===========================================================

def gaussian_divisor(prime):
    if prime % 4 == 3:
        raise ValueError('{} does not split over Z[i]'.format(prime))

    s = min(mod_sqrt(-1, prime))
    return Quadratic(prime, 0, -1).gcd(Quadratic(s, 1, -1))

#-----------------------------

def is_sum_of_two_squares(factorization):
    return 3 not in map(lambda x: x % 4, square_free_part(factorization).keys())

#-----------------------------

def two_squares_from_factorization(factorization):
    square = square_part(factorization)
    square_free = square_free_part(factorization)
    if is_sum_of_two_squares(square_free):
        return _square_and_square_free_to_pair(square, square_free)

#-----------------------------

def two_squares(number):
    return two_squares_from_factorization(factor(number))

#=============================

def quaternion_descent(quaternion, prime):
    m = quaternion.norm() // prime
    if m == 1:
        return quaternion
    return quaternion_descent(
        (quaternion.conjugate() * (quaternion % m)) // m,
        prime
    )

def quaternion_divisor(prime):
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

def four_squares_from_factorization(factorization):
    square = square_part(factorization)
    square_free = square_free_part(factorization)
    return _square_and_square_free_to_quadruple(square, square_free)

def four_squares(number):
    return four_squares_from_factorization(factor(number))

def _quaternion_to_quadruple(quaternion_element):
    return tuple(sorted(map(abs, quaternion_element.components), reverse=True))

def _square_and_square_free_to_quadruple(square, square_free):
    return _quaternion_to_quadruple(
        _square_to_quaternion(square) * _square_free_to_quaternion(square_free)
    )

def _square_free_to_quaternion(square_free_factorization):
    return reduce(
        lambda x, y: x * y,
        map(quaternion_divisor, square_free_factorization.keys()),
        1
    )

def _square_to_quaternion(square_factorization):
    return _quadratic_to_quaternion(_square_to_quadratic(square_factorization))

def _quadratic_to_quaternion(quadratic_element):
    return Quaternion(quadratic_element.real, quadratic_element.imag, 0, 0)

#===========================================================

def _square_to_quadratic(square_factorization):
    return Quadratic(
        reduce(
            lambda x, y: x * y,
            map(lambda z: z[0] ** (z[1] // 2), square_factorization.items()),
            1
        ), 0, -1)

#-----------------------------

def _square_free_to_quadratic(square_free_factorization):
    return reduce(
        lambda x, y: x * y,
        map(gaussian_divisor, square_free_factorization.keys()),
        1
    )

#-----------------------------

def _quadratic_to_pair(quadratic_element):
    canonical = quadratic_element.canonical()
    return (canonical.real, abs(canonical.imag))

#-----------------------------

def _square_and_square_free_to_pair(square, square_free):
    return _quadratic_to_pair(
        _square_to_quadratic(square) * _square_free_to_quadratic(square_free)
    )

#-----------------------------

