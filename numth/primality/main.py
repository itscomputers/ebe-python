#   numth/primality/main.py
#===========================================================
from functools import reduce
from typing import Iterator, List, Tuple

from ..config import default
from ..basic import prime_to 
from .lucas import lucas_test
from .miller_rabin import miller_rabin_test, miller_rabin_max_cutoff
#===========================================================

def is_prime(
        number: int,
        mr_wit: int = None,
        l_wit: int = None
    ) -> bool:
    """
    Primality test.

    params
    + number : int
    + mr_wit : int
        number of Miller-Rabin witnesses
    + l_wit : int
        number of Lucas witness pairs

    return
    bool
        * if number < 341_550_071_728_321, only pre-determined Miller-Rabin
        witnesses are used and result is deterministic
        * otherwise, the result is probabalistic
        incorrect with probability < (1/4) ** mr_wit * (4/15) ** l_wit
    """
    if number < 2:
        return False

    if number < miller_rabin_max_cutoff():
        return miller_rabin_test(number, 1) == 'prime'

    mr_wit = mr_wit or default('miller_rabin_witness_count')
    if miller_rabin_test(number, mr_wit) == 'composite':
        return False

    l_wit = l_wit or default('lucas_witness_pair_count')
    if lucas_test(number, l_wit) == 'composite':
        return False

    return True

#=============================

def next_prime_gen(
        number: int,
        sieve_primes: List[int] = None
    ) -> Iterator[int]:
    """
    Generator that yields primes after given number.

    params
    number : int
    sieve_primes : list(int)
        list of primes used to make a sieving block

    return
    generator -> int
        yields next prime number
    """
    sieve_primes = sieve_primes or default('sieve_primes')

    start = max(number, 1)
    diameter = reduce(lambda x, y: x * y, sieve_primes, 1)
    block = [
        start - start % diameter + x \
            for x in prime_to({p : 1 for p in sieve_primes})
    ]

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

#-----------------------------

def next_prime(
        number: int,
        sieve_primes: List[int] = None
    ) -> int:
    """
    Next prime after given number.

    params
    number : int
    sieve_primes : list(int)
    
    return
    int
    """
    return next(next_prime_gen(number, sieve_primes))

#-----------------------------

def next_primes(
        number: int,
        k: int,
        sieve_primes: List[int] = None
    ) -> List[int]:
    """
    List of next k primes after given number.

    params
    + number : int
    + k : int
        number of primes to generate
    + sieve_primes : list(int)

    return
    list(int)
    """
    gen = next_prime_gen(number, sieve_primes)
    return [next(gen) for _ in range(k)]

#-----------------------------

def primes_in_range(
        lower_bound: int,
        upper_bound: int,
        sieve_primes: List[int] = None
    ) -> List[int]:
    """
    Primes in a range.

    Finds prime numbers in range(lower_bound, upper_bound).

    params
    + lower_bound : int
    + upper_bound : int
    + sieve_primes : list(int)

    return
    list(int)
    """
    gen = next_prime_gen(lower_bound - 1, sieve_primes)
    
    primes = []         # type: List[int]
    while True:
        p = next(gen)
        if p < upper_bound:
            primes = primes + [p]
        else:
            break

    return primes

#=============================

def prev_prime_gen(
        number: int,
        sieve_primes: List[int] = None
    ) -> Iterator[int]:
    """
    Generator that yields primes before given number.

    params
    number : int
    sieve_primes : list(int)
        list of primes used to make a sieving block

    return
    generator -> int
        yields previous prime number
    """
    sieve_primes = sieve_primes or default('sieve_primes')

    diameter = reduce(lambda x, y: x * y, sieve_primes, 1)
    block = [
        number - number % diameter + x \
            for x in reversed(prime_to({p : 1 for p in sieve_primes}))
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

#-----------------------------

def prev_prime(
        number: int,
        sieve_primes: List[int] = None
    ) -> int:
    """
    Prev prime before given number.

    params
    + number : int
    + sieve_primes : list(int)

    return
    int
    """
    try:
        return next(prev_prime_gen(number, sieve_primes))
    except StopIteration:
        return None

#=============================

def next_twin_primes_gen(
        number: int,
        sieve_primes: List[int] = None
    ) -> Iterator[Tuple[int, int]]:
    """
    Generator that yields twin primes after given number.

    Produce twin primes (primes that differ by two)

    params
    + number : int
    + sieve_primes : list(int)

    return
    generator -> (int, int)
        yields next pair of twin primes
    """
    gen = next_prime_gen(number - 2, sieve_primes)
    
    p, q = next(gen), next(gen)
    while True:
        while q != p + 2:
            p, q = q, next(gen)
        yield p, q
        p, q =q, next(gen)

#-----------------------------

def next_twin_primes(
        number: int,
        sieve_primes: List[int] = None
    ) -> Tuple[int, int]:
    """
    Next pair of twin primes after given number.

    params
    + number : int
    + sieve_primes : list(int)

    return
    (int, int)
    """
    return next(next_twin_primes_gen(number, sieve_primes))

#=============================

def goldbach_partition(
        number: int,
        sieve_primes: List[int] = None
    ) -> Tuple[int, ...]:
    """
    Goldbach partition of a number.

    Compute pair or triple of primes that sum to number.

    params
    + number : int
    + sieve_primes : list(int)

    return
    tuple(int)
        * tuple has two primes if number is 5 or even
        * otherwise, tuple has three primes
    """
    if number < 4:
        raise ValueError('Must be at least 4')

    if number % 2 == 1 and number > 6:
        p = prev_prime(number - 4)
        return tuple(sorted(
            [p, *goldbach_partition(number - p, sieve_primes)],
            reverse=True))

    start = number // 2 - 1
    prime_gen = next_prime_gen(start, sieve_primes)
    p = next(prime_gen)
    
    while not is_prime(number - p):
        p = next(prime_gen)

    return tuple(sorted([p, number - p], reverse=True))

