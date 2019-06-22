#   numth/primality.py
#===========================================================
from functools import reduce

from .basic import prime_to 
from .primality_miller_rabin import miller_rabin_test, miller_rabin_max_cutoff
from .primality_lucas import lucas_test
#===========================================================

def _default_values(category):
    if category == 'miller_rabin':
        return 40 
    if category == 'lucas':
        return 10
    if category == 'sieve_primes':
        return [2, 3, 5, 7]

#===========================================================

def is_prime(number, mr_wit=None, l_wit=None):
    """
    Primality test.
        (number: int, mr_wit: int, l_wit: int) -> bool
    Notes:  return_val is whether number is prime
            mr_wit is number of witnesses for miller_rabin_test
            l_wit is number of witness pairs for lucas_test
            if number < 341_550_071_728_321:
                a. only pre-designated Miller-Rabin witnesses are used
                b. the result is deterministic
            otherwise, the result is probabilistic
                incorrect with probability < (1/4)**mr_wit * (4/15)**l_wit
    """
    if number < 2:
        return False

    if number < miller_rabin_max_cutoff():
        return miller_rabin_test(number, 1) == 'prime'

    if mr_wit is None:
        mr_wit = _default_values('miller_rabin')
    if miller_rabin_test(number, mr_wit) == 'composite':
        return False

    if l_wit is None:
        l_wit = _default_values('lucas')
    if lucas_test(number, l_wit) == 'composite':
        return False

    return True

#=============================

def next_prime_gen(number, sieve_primes=None):
    """
    Generator that yields primes after given number.
        (number: int, sieve_primes: list) -> generator
    """
    if sieve_primes is None:
        sieve_primes = _default_values('sieve_primes')

    start = max(number, 1)
    diameter = reduce(lambda x, y: x * y, sieve_primes, 1)
    block = [start - start % diameter + x for x in prime_to(*sieve_primes)]

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

def next_prime(number, sieve_primes=None):
    """
    Next prime after given number.
        (number: int, sieve_primes: list) -> int
    """
    return next(next_prime_gen(number, sieve_primes))

#-----------------------------

def next_primes(number, k, sieve_primes=None):
    """
    List of next k primes after given number.
        (number: int, k: int, sieve_primes: list) -> list
    """
    gen = next_prime_gen(number, sieve_primes)
    return [next(gen) for _ in range(k)]

#-----------------------------

def primes_in_range(lower_bound, upper_bound, sieve_primes=None):
    """
    Primes in a range.
        (lower_bound: int, upper_bound: int, sieve_primes: list) -> list
    Notes:  return_val is primes in range(lower_bound, upper_bound)
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

#=============================

def prev_prime_gen(number, sieve_primes=None):
    """
    Generator that yields primes before given number.
        (number: int, sieve_primes: list) -> generator
    """
    if sieve_primes is None:
        sieve_primes = _default_values('sieve_primes')

    diameter = reduce(lambda x, y: x * y, sieve_primes, 1)
    block = [number - number % diameter + x for x in reversed(prime_to(*sieve_primes))]

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

def prev_prime(number, sieve_primes=None):
    """
    Prev prime before given number.
        (number: int, sieve_primes: list) -> int
    """
    try:
        return next(prev_prime_gen(number, sieve_primes))
    except StopIteration:
        return None

#=============================

def next_twin_primes_gen(number, sieve_primes=None):
    """
    Generator that yields twin primes after given number.
        (number: int, sieve_primes: list) -> generator
    """
    gen = next_prime_gen(number - 2, sieve_primes)
    
    p, q = next(gen), next(gen)
    while True:
        while q != p + 2:
            p, q = q, next(gen)
        yield p, q
        p, q =q, next(gen)

#-----------------------------

def next_twin_primes(number, sieve_primes=None):
    """
    Next pair of twin primes after given number.
        (number: int, sieve_primes: list) -> tuple
    Notes:  return_val is pair of primes with difference of 2
    """
    return next(next_twin_primes_gen(number, sieve_primes))

#=============================

def goldbach_partition(number, sieve_primes=None):
    """
    Goldbach partition of a number into a sum of two or three primes.
        (number: int, sieve_primes: list) -> tuple
    Notes:  return_val is a tuple of primes that sum to number
            two primes if number is 5 or even, otherwise three primes
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

