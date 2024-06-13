#   lib/factorization/quaternion_divisor.py
#   - module for finding quaternion divisor of a prime number

# ===========================================================
from ..basic import jacobi
from ..primality import is_prime
from ..types import QuaternionInteger
from .gaussian_divisor import _get_gaussian_divisor

# ===========================================================
__all__ = [
    "get_quaternion_divisor",
]
# ===========================================================


def get_quaternion_divisor(prime: int) -> QuaternionInteger:
    """
    Get a quaternion integer whose norm is equal to `prime`.

    + prime: int
    ~> QuaternionInteger
    """

    if not is_prime(prime):
        raise ValueError(f"{prime} is not prime")

    return _get_quaternion_divisor(prime)


# -----------------------------


def _get_quaternion_divisor(prime: int) -> QuaternionInteger:
    """
    Find quaternion integer whose norm is equal to `prime`.

    + prime: int --assumed prime
    ~> QuaternionInteger
    """
    if prime == 2 or prime % 4 == 1:
        return QuaternionInteger.from_gaussian_integer(
            _get_gaussian_divisor(prime),
        )

    if prime % 8 == 3:
        s = pow(2, (prime + 1) // 4, prime)
        t = 1
    else:
        t, a = 2, 5
        while jacobi(a, prime) == 1:
            t += 1
            a = pow(t, 2, prime) + 1
        s = pow(a, (prime + 1) // 4, prime)

    if 2 * s > prime:
        s = prime - s
    return _quaternion_descent(QuaternionInteger(s, t, 1, 0), prime)


# -----------------------------


def _quaternion_descent(quaternion: QuaternionInteger, prime: int) -> QuaternionInteger:
    """
    Given a quaternion integer whose norm is divisible by a prime, find a quaternion
    integer whose norm is equal to the prime.

    + quaternion: QuaternionInteger
    + prime: int --assumed prime
    ~> QuaternionInteger
    """

    modulus = quaternion.norm // prime

    if modulus == 1:
        return quaternion

    quaternion_modulus = QuaternionInteger(modulus, 0, 0, 0)
    return _quaternion_descent(
        (quaternion.conjugate * (quaternion % quaternion_modulus)) // quaternion_modulus,
        prime,
    )
