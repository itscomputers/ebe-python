#   lib/primality/__init__.py
#   - module for primality testing and its applications

# ===========================================================
from .algorithms import (  # noqa: 401
    is_prime,
    lucas_test,
    miller_rabin_test,
    LucasWitness,
    MillerRabinWitness,
    Observation,
    PrimalityWitness,
)
from .prime_search import (  # noqa: 401
    is_prime,
    next_prime,
    next_primes,
    primes_in_range,
    prev_prime,
    prev_primes,
    goldbach_partition,
    PrimeSearch,
)

# ===========================================================
__all__ = [
    "is_prime",
    "next_prime",
    "next_primes",
    "primes_in_range",
    "prev_prime",
    "prev_primes",
    "goldbach_partition",
]
