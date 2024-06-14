#   lib/primality/main.py
#   - module for primality testing and applications

# ===========================================================
from functools import reduce

from ..config import default
from ..basic import prime_to
from .algorithms import lucas_test, miller_rabin_test, MillerRabinWitness

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
# ===========================================================


def is_prime(number, mr_wit=None, l_wit=None):
    """
    Determine if `number` is prime.
    - a return value of `False` is always correct.
    - if `number < 341_550_071_728_321`, only the pre-determined Miller-Rabin
        witnesses are used and the result is deterministic.
    - otherwise, the result is probabalistic with probability of incorrectness
        less than `(1/4)**mr_wit * (4/15)**l_wit`.

    + number: int
    + mr_wit: int --number of Miller-Rabin witnesses
    + l_wit : int --number of Lucas witness pairs
    ~> bool
    """
    if number < 2:
        return False

    if number == 2:
        return True

    if number % 2 == 0:
        return False

    if number < MillerRabinWitness.MAX_CUTOFF:
        return miller_rabin_test(number, witness_count=1).value == "prime"

    mr_wit = mr_wit or default("miller_rabin_witness_count")
    if miller_rabin_test(number, witness_count=mr_wit).value == "composite":
        return False

    l_wit = l_wit or default("lucas_witness_pair_count")
    if lucas_test(number, witness_count=l_wit).value == "composite":
        return False

    return True


# =============================


def next_prime_gen(number, sieve_primes=None):
    """
    Generate primes after `number`.

    + number: int
    + sieve_primes: List[int] --primes used in sieving block
    ~> Iterator[int]
    """
    sieve_primes = sieve_primes or default("sieve_primes")

    start = max(number, 1)
    diameter = reduce(lambda x, y: x * y, sieve_primes, 1)
    block = [start - start % diameter + x for x in prime_to({p: 1 for p in sieve_primes})]

    for p in sieve_primes:
        if number < p:
            yield p

    shift = 0
    while True:
        for x in block:
            y = x + diameter * shift
            if y > number and is_prime(y):
                yield y
        shift += 1


# -----------------------------


def next_prime(number, sieve_primes=None):
    """
    Compute next prime after `number`.

    + number: int
    + sieve_primes: List[int]
    ~> int
    """
    return next(next_prime_gen(number, sieve_primes))


# -----------------------------


def next_primes(number, k, sieve_primes=None):
    """
    List of next `k` primes after `number`.

    + number: int
    + k: int
    + sieve_primes: List[int]
    ~> List[int]
    """
    gen = next_prime_gen(number, sieve_primes)
    return [next(gen) for _ in range(k)]


# -----------------------------


def primes_in_range(lower_bound, upper_bound, sieve_primes=None):
    """
    Compute prime numbers in `range(lower_bound, upper_bound)`.

    + lower_bound: int
    + upper_bound: int
    + sieve_primes: List[int]
    ~> List[int]
    """
    gen = next_prime_gen(lower_bound - 1, sieve_primes)

    primes = []
    while True:
        p = next(gen)
        if p < upper_bound:
            primes = primes + [p]
        else:
            break

    return primes


# =============================


def prev_prime_gen(number, sieve_primes=None):
    """
    Generate primes before `number`.

    + number: int
    + sieve_primes: List[int] --primes used in sieving block
    ~> Iterator[int]
    """
    sieve_primes = sieve_primes or default("sieve_primes")

    diameter = reduce(lambda x, y: x * y, sieve_primes, 1)
    block = [
        number - number % diameter + x
        for x in reversed(prime_to({p: 1 for p in sieve_primes}))
    ]

    shift = 0
    max_shift = number // diameter
    while shift <= max_shift:
        for x in block:
            y = x - diameter * shift
            if y < number and is_prime(y):
                yield y
        shift += 1

    for p in reversed(sieve_primes):
        if number > p:
            yield p


# -----------------------------


def prev_prime(number, sieve_primes=None):
    """
    Compute previous prime before `number`.

    + number: int
    + sieve_primes: List[int]
    ~> int
    """
    try:
        return next(prev_prime_gen(number, sieve_primes))
    except StopIteration:
        return None


# =============================


def next_twin_primes_gen(number, sieve_primes=None):
    """
    Generate twin primes (two primes that differ by 2) after `number`.

    + number: int
    + sieve_primes: List[int] --primes used in sieving block
    ~> Iterator[Tuple[int, int]]
    """
    gen = next_prime_gen(number - 2, sieve_primes)

    p, q = next(gen), next(gen)
    while True:
        while q != p + 2:
            p, q = q, next(gen)
        yield p, q
        p, q = q, next(gen)


# -----------------------------


def next_twin_primes(number, sieve_primes=None):
    """
    Compute next pair of twin primes after `number`.

    + number: int
    + sieve_primes: List[int]
    ~> Tuple[int, int]
    """
    return next(next_twin_primes_gen(number, sieve_primes))


# =============================


def goldbach_partition(number, sieve_primes=None):
    """
    Compute Goldbach partition of `number`,
    ie, the pair of primes (if `number` is 5 or even)
    or the triple of primes that sum to `number`.

    + number: int
    + sieve_primes: List[int]
    ~> Union[Tuple[int, int], Tuple[int, int, int]]
    """
    if number < 4:
        raise ValueError("Must be at least 4")

    if number % 2 == 1 and number > 6:
        p = prev_prime(number - 4)
        return tuple(
            sorted([p, *goldbach_partition(number - p, sieve_primes)], reverse=True)
        )

    start = number // 2 - 1
    prime_gen = next_prime_gen(start, sieve_primes)
    p = next(prime_gen)

    while not is_prime(number - p):
        p = next(prime_gen)

    return tuple(sorted([p, number - p], reverse=True))
