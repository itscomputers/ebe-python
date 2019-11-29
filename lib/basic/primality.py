#   lib/basic/primality.py
#   - module for basic functions related to prime numbers

#===========================================================
import itertools as it

from .sqrt import integer_sqrt
#===========================================================
__all__ = [
    'prime_gen',
    'iter_primes_up_to',
    'primes_up_to',
    'is_prime__naive',
]
#===========================================================

def prime_gen():
    """
    Generator that yields prime numbers using Sieve of Eratosthenes.

    ~> Iterator[int]
    """
    primes = it.count(2)
    while True:
        prime = next(primes)
        primes = filter(prime.__rmod__, primes)
        yield prime

#-----------------------------

def iter_primes_up_to(number):
    """
    Iterator of primes up to `number`.

    example: `list(iter_primes_up_to(10)) ~> [2, 3, 5, 7]`

    + number: int
    ~> Iterator[int]
    """
    return it.takewhile(lambda x: x <= number, prime_gen())

#-----------------------------

def primes_up_to(max_value, primes=None, numbers_left=None):
    """
    Compute primes up to `max_value`.

    example: `primes_up_to(19) ~> [2, 3, 5, 7, 11, 13, 17, 19]`

    + max_value: int
    + primes: List[int] --used for recursive call
    + numbers_left: Iterator[int] --used for recursive call
    ~> List[int]
    """
    if primes is None and numbers_left is None:
        primes = []
        numbers_left = iter(range(2, max_value + 1))

    try:
        min_value = next(numbers_left)
    except StopIteration:
        return primes

    if min_value**2 >= max_value:
        return primes + [min_value] + list(numbers_left)

    return primes_up_to(
        max_value,
        primes + [min_value],
        filter(min_value.__rmod__, numbers_left)
    )

#=============================

def is_prime__naive(number, numbers_left=None):
    """
    Determine if `number` is prime using sieve of Eratosthenes.

    example: `is_prime__naive(19) ~> True`
             `is_prime__naive(20) ~> False`

    + number: int
    + numbers_left: Iterator[int] --used for recursive call
    ~> bool
    """
    if number < 2:
        return False

    if numbers_left is None:
        numbers_left = iter(range(2, integer_sqrt(number) + 1))

    try:
        min_value = next(numbers_left)
    except StopIteration:
        return True

    if number % min_value == 0:
        return False

    return is_prime__naive(
        number,
        filter(min_value.__rmod__, numbers_left)
    )

