#   numth/basic/primality.py
#===========================================================
import itertools as it

from .sqrt import integer_sqrt
#===========================================================

def prime_gen():
    primes = it.count(2)
    while True:
        prime = next(primes)
        primes = filter(prime.__rmod__, primes)
        yield prime

#-----------------------------

def iter_primes_up_to(number):
    return it.takewhile(lambda x: x <= number, prime_gen())

#-----------------------------

def primes_up_to(max_value, primes=None, numbers_left=None):
    """
    Uses the sieve of Eratosthenes to find all prime numbers up to `max_value`.

    example:
        `prime_sieve(19) => [2, 3, 5, 7, 11, 13, 17, 19]`

    params:
        `max_value : int`

    returns:
        `list of int`
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
    Uses the sieve of Eratosthenes to determine if `number` is prime.

    example:
        `is_prime__naive(19) => True` and
        `is_prime__naive(20) => False`
        since 19 is not divisible by 2 or 3 but 20 is

    params:
        `number : int`

    returns:
        `bool`
    of whether `number` is prime.
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

