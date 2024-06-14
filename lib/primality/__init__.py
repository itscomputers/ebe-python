#   lib/primality/__init__.py
#   - module for primality testing and its applications

# ===========================================================
from .algorithms import (  # noqa: 401
    lucas_test,
    miller_rabin_test,
    LucasWitness,
    MillerRabinWitness,
    Observation,
    PrimalityWitness,
)
from .main import (
    is_prime,
    next_prime_gen,
    next_prime,
    next_primes,
    primes_in_range,
    prev_prime_gen,
    prev_prime,
    next_twin_primes_gen,
    next_twin_primes,
    goldbach_partition,
)


# ===========================================================
__all__ = [
    "is_prime",
    "next_prime_gen",
    "next_prime",
    "next_primes",
    "primes_in_range",
    "prev_prime_gen",
    "prev_prime",
    "next_twin_primes_gen",
    "next_twin_primes",
    "goldbach_partition",
]
