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
from .goldbach import goldbach_partition
from .prime_search import (  # noqa: 401
    is_prime,
    next_prime,
    next_primes,
    primes_in_range,
    prev_prime,
    prev_primes,
    PrimeSearch,
)
from .twin_prime_search import (  # noqa: 401
    next_twin_prime,
    prev_twin_prime,
    TwinPrimeSearch,
)

# ===========================================================
__all__ = [
    "goldbach_partition",
    "is_prime",
    "next_prime",
    "next_primes",
    "primes_in_range",
    "prev_prime",
    "prev_primes",
    "next_twin_prime",
    "prev_twin_prime",
]
