#   lib/factorization/gaussian_divisor.py
#   - module for finding gaussian divisor of a prime number

# ===========================================================
from ..modular import mod_sqrt
from ..primality import is_prime
from ..types import GaussianInteger

# ===========================================================
__all__ = [
    "get_gaussian_divisor",
]
# ===========================================================


def get_gaussian_divisor(prime: int) -> GaussianInteger:
    """
    Get a Gaussian integer whose norm is equal to `prime`, if possible.

    + prime: int
    ~> GaussianInteger
    """

    if not is_prime(prime):
        raise ValueError(f"{prime} is not prime")
    if prime % 4 == 3:
        raise ValueError(f"{prime} does not split over Z[i]")

    return _get_gaussian_divisor(prime)


# -----------------------------


def _get_gaussian_divisor(prime: int) -> GaussianInteger:
    """
    Get a Gaussian integer divisor of a prime that is not 3 mod 4.

    + prime: int --assumed prime and prime % 4 != 3
    ~> GaussianInteger
    """

    s = min(mod_sqrt(-1, prime))
    return GaussianInteger(prime, 0).gcd(GaussianInteger(s, 1))
