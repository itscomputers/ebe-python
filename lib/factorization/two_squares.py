#   lib/factorization/two_squares.py
#   - module to express integer as sum of two squares

#===========================================================
from functools import reduce

from ..modular import mod_sqrt
from ..types import GaussianInteger
from .main import factor, square_and_square_free
#===========================================================
__all__ = [
    'gaussian_divisor',
    'is_sum_of_two_squares',
    'two_squares',
]
#===========================================================

def gaussian_divisor(prime):
    """
    Find Gaussian integer with norm equal to `prime`.

    example: `gaussian_divisor(13) ~> 3 - 2 i`
        with `(3 - 2 i).norm == 13`

    + prime: int --prime
    ~> GaussianInteger
    """
    if prime % 4 == 3:
        raise ValueError('{} does not split over Z[i]'.format(prime))

    s = min(mod_sqrt(-1, prime))
    return GaussianInteger(prime, 0).gcd(GaussianInteger(s, 1))

#-----------------------------

def is_sum_of_two_squares(factorization):
    """
    Determine if corresponding `number` can be written as a sum of two squares,
    whether all primes that are 3 mod 4 occur with even multiplicity.

    example: `is_sum_of_two_squares({5: 1, 19: 1}) ~> False`
             `is_sum_of_two_squares({5: 1, 17: 1}) ~> True`

    + factorization: Dict[int, int] --with shape {prime: multiplicity}
    ~> bool
    """
    square, square_free = square_and_square_free(factorization)
    return 3 not in map(lambda x: x % 4, square_free.keys())

#-----------------------------

def two_squares_from_factorization(factorization):
    """
    Find two integers whose squares sum to corresponding `number`.

    example: `two_squares_from_factorization({5: 1, 17: 1}) ~> (7, 6)`
        with `7**2 + 6**2 == 85 == 5 * 17`

    + factorization: Dict[int, int] --with shape {prime: multiplicity}
    ~> Tuple[int, int]
    """
    square, square_free = square_and_square_free(factorization)
    if not is_sum_of_two_squares(square_free):
        return None

    gaussian_square_free = reduce(
        lambda x, y: x * y,
        map(gaussian_divisor, square_free.keys()),
        1
    )

    square_root = reduce(
        lambda x, y: x * y,
        map(lambda z: z[0] ** (z[1] // 2), square.items()),
        1
    )
    gaussian_square = GaussianInteger(square_root, 0)

    return tuple(sorted(
        map(abs, (gaussian_square * gaussian_square_free).components),
        reverse=True
    ))

#-----------------------------

def two_squares(number_or_factorization):
    """
    Find two integers whose squares sum to `number`.

    example: `two_squares(85) = (7, 6)`
             `two_squares({5: 1, 17: 1}) ~> (7, 6)`

    + number_or_factorization: Union[int, Dict[int, int]]
    ~> Tuple[int, int]
    """
    if isinstance(number_or_factorization, int):
        factorization = factor(number_or_factorization)
    else:
        factorization = number_or_factorization

    return two_squares_from_factorization(factorization)

