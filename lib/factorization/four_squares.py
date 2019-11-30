#   lib/factorization/four_squares.py
#   - module to express integer as sum of four squares

#===========================================================
from functools import reduce

from ..basic import jacobi
from ..types import QuaternionInteger
from .main import factor, square_and_square_free
from .two_squares import gaussian_divisor
#===========================================================
__all__ = [
    'quaternion_descent',
    'quaternion_divisor',
    'four_squares',
]
#===========================================================

def quaternion_descent(quaternion_integer, prime):
    """
    Given `quaternion_integer` whose norm is divisible by `prime`,
    find quaternion integer whose norm is equal to `prime`.

    example: for `q = QuaternionInteger(1, -2, 3, -4)`,
        `quaternion_descent(q, 5) ~> QuaternionInteger(0, 0, 2, 1)`

    + quaternion_integer: QuaternionInteger
    + prime: int --prime
    ~> QuaternionInteger
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
    Find quaternion integer whose norm is equal to `prime`.

    example: `quaternion_divisor(23) ~> QuaternionInteger(-3, -2, 2, -1)`

    + prime: int
    ~> QuaternionInteger
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
    Find four integers whose squares sum to corresponding `number`.

    example: `four_squares_from_factorization({5: 1, 19: 1}) ~> (7, 6, 3, 1)`

    + factorization: Dict[int, int] --with shape {prime: multiplicity}
    ~> Tuple[int, int, int, int]
    """
    square, square_free = square_and_square_free(factorization)
    quaternion_square_free = reduce(
        lambda x, y: x * y,
        map(quaternion_divisor, square_free.keys()),
        1
    )

    square_root = reduce(
        lambda x, y: x * y,
        map(lambda z: z[0] ** (z[1] // 2), square.items()),
        1
    )
    quaternion_square = QuaternionInteger(square_root, 0, 0, 0)

    return tuple(sorted(
        map(abs, (quaternion_square * quaternion_square_free).components),
        reverse=True
    ))

#-----------------------------

def four_squares(number_or_factorization):
    """
    Find four integers whose squares sum to `number`.

    example: `four_squares(95) ~> (7, 6, 3, 1)`
             `four_squares({5: 1, 19: 1}) ~> (7, 6, 3, 1)`

    + number_or_factorization: Union[int, Dict[int, int]]
    ~> Tuple[int, int, int, int]
    """
    if isinstance(number_or_factorization, int):
        factorization = factor(number_or_factorization)
    else:
        factorization = number_or_factorization

    return four_squares_from_factorization(factorization)

