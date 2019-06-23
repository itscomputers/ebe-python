#   numth/tests/factorization.py
#===========================================================
from functools import reduce
from hypothesis import assume, example, given, strategies as st

from ..primality import is_prime, next_prime
from ..factorization import *
#===========================================================

def build_composite(*numbers):
    return reduce(lambda x, y: x * next_prime(y), numbers, 1)

def build_strategy(min_digits, max_digits):
    return st.integers(min_value=10**min_digits, max_value=10**max_digits)

def coordinates(num_args, min_digits, max_digits):
    return [build_strategy(min_digits, max_digits) for _ in range(num_args)]

#=============================

@given(*coordinates(4, 2, 5))
def test_find_divisor(a, b, c, d):
    number = build_composite(a, b, c, d)
    divisors = find_divisor(number)
    for d in divisors:
        assert( 1 < d < number )
        assert( number % d == 0 )

#-----------------------------

@given(*coordinates(4, 0, 5))
def test_factor_trivial(a, b, c, d):
    number = build_composite(a, b, c, d)
    remaining, divisors = factor_trivial(number)
    for d in divisors.keys():
        assert( is_prime(d) )
    product = reduce(lambda x, y: x * y[0]**y[1], divisors.items(), remaining)
    assert( product == number )

#-----------------------------

@given(*coordinates(4, 2, 5))
def test_factor_nontrivial(a, b, c, d):
    number = build_composite(a, b, c, d)
    divisors = factor_nontrivial(number)
    for d in divisors.keys():
        assert( is_prime(d) )
    product = reduce(lambda x, y: x * y[0]**y[1], divisors.items(), 1)
    assert( product == number )

#-----------------------------

@given(st.integers(min_value=2, max_value=10**15))
def test_factor(number):
    divisors = factor(number)
    for d in divisors.keys():
        assert( is_prime(d) )
    product = reduce(lambda x, y: x * y[0]**y[1], divisors.items(), 1)
    assert( product == number )

