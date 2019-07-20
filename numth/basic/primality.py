#   numth/basic/primality.py
#===========================================================
from .sqrt import integer_sqrt
#===========================================================

def prime_sieve(max_value, primes=None, numbers_left=None):
    """
    Sieve of Eratosthenes.

    Computes primes up to max_value.

    params
    + max_value : int
    + primes : list(int)
        primes so far
    + numbers_left : list(int)
        numbers left to check

    return
    list(int)
    """
    if primes is None and numbers_left is None:
        primes = []
        numbers_left = (x for x in range(2, max_value + 1))
    try:
        min_value = next(numbers_left)
    except StopIteration:
        return primes

    if min_value**2 >= max_value:
        return primes + [min_value] + list(numbers_left)

    return prime_sieve(
        max_value,
        primes + [min_value],
        (x for x in numbers_left if x % min_value != 0)
    )

#=============================

def is_prime__naive(number, numbers_left=None):
    """
    Primality testing using Sieve of Eratosthenes.

    Determines if a number is prime by computing all primes up to its square root.

    params:
    + number : int
    + numbers_left : list(int)
        numbers left to check

    return
    bool
    """
    if number < 2:
        return False

    if numbers_left is None:
        numbers_left = (x for x in range(2, integer_sqrt(number) + 1))
    
    try:
        min_value = next(numbers_left)
    except StopIteration:
        return True

    if number % min_value == 0:
        return False

    return is_prime__naive(
        number,
        (x for x in numbers_left if x % min_value != 0)
    )

