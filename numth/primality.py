#   numth/primality.py
#===========================================================
from functools import reduce

from .basic import prime_to 
from .primality_miller_rabin import miller_rabin_test, miller_rabin_cutoffs
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

    if number < miller_rabin_cutoffs()[-1][0]:
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
    return [next(next_prime_gen(number, sieve_primes)) for _ in range(k)]

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

def next_twin_primes_gen(number, sieve_primes=None):
    gen = next_prime_gen(number - 2, sieve_primes)
    
    p, q = next(gen), next(gen)
    while True:
        while q != p + 2:
            p, q = q, next(gen)
        yield p, q
        p, q =q, next(gen)

#-----------------------------

def next_twin_primes(number, sieve_primes=None):
    return next(next_twin_primes_gen(number, sieve_primes))

