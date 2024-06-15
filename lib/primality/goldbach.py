#   lib/primality/goldbach.py
#   - module for goldbach partitions

# ===========================================================
from .algorithms import is_prime
from .prime_search import prev_prime, PrimeSearch

# ===========================================================
__all__ = [
    "goldbach_partition",
]
# ===========================================================


def goldbach_partition(number: int) -> tuple[int, int] | tuple[int, int, int]:
    """
    Get Goldbach partition of 2 or 3 primes that sum to `number`.

    If `number` is even, the unproven conjecture is that it is the sum of two primes. This
    has been proven for `number < 4 * 10**18`, so this function is not guaranteed to
    terminate beyond that.

    If a `number` is odd, the weak Goldbach conjecture is that it is the sum of at most 3
    primes. The same bound applies to to this as well.

    + number: int
    ~> tuple[int, int] | tuple[int, int, int]
    """

    if number < 4:
        raise ValueError("Must be at least 4")

    if number % 2 == 1:
        if is_prime(number - 2):
            return (number - 2, 2)

        prime = prev_prime(number - 4)
        assert prime is not None
        p, q, r = sorted(
            [prime, *goldbach_partition(number - prime)],
            reverse=True,
        )
        return p, q, r

    prime_search = PrimeSearch(number // 2 - 1)
    prime = prime_search.next().value

    while not is_prime(number - prime):
        prime = prime_search.next().value

    p, q = sorted([number - prime, prime], reverse=True)
    return p, q
