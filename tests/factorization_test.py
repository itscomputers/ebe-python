#   tests/factorization_test.py
#===========================================================
import env
from functools import reduce
from hypothesis import assume, given, strategies as st

from numth.basic import is_square
from numth.primality import is_prime, next_prime
from numth.types import GaussianInteger, Quaternion
from numth.factorization import *
from numth.factorization.main import _combine_counters
#===========================================================

def build_composite(*numbers):
    return reduce(lambda x, y: x * next_prime(y), numbers, 1)

def build_strategy(min_digits, max_digits):
    return st.integers(min_value=10**min_digits, max_value=10**max_digits)

def coordinates(num_args, min_digits, max_digits):
    return [build_strategy(min_digits, max_digits) for _ in range(num_args)]

#===========================================================
#   algorithms
#===========================================================

@given(st.integers(min_value=2, max_value=10**12))
def test_pollard_rho(number):
    if not is_prime(number):
        d = pollard_rho(number, 2, lambda x: x**2 + 1)
        assert( d > 1 and number % d == 0 )

#-----------------------------

@given(st.integers(min_value=2, max_value=10**10))
def test_pollard_p_minus_one(number):
    if not is_prime(number):
        d = pollard_p_minus_one(number, 2)
        assert( d > 1 and number % d == 0 )
        
#-----------------------------

@given(st.integers(min_value=2, max_value=10**12))
def test_williams_p_plus_one(number):
    if not is_prime(number):
        d = williams_p_plus_one(number, GaussianInteger(1, 1))
        assert( d > 1 and number % d == 0 )

#===========================================================
#   four_squares
#===========================================================

@given(st.integers(min_value=2))
def test_quaternion_divisor(number):
    prime = next_prime(number)
    q = quaternion_divisor(prime)
    assert( q.norm() == prime )
    assert( Quaternion(prime, 0, 0, 0) % q == Quaternion(0, 0, 0, 0) )

#-----------------------------

@given(st.integers(min_value=2, max_value=10**4))
def test_four_squares(number):
    factorization = factor(number)
    squares = four_squares_from_factorization(factorization)
    assert( sorted(squares, reverse=True) == list(squares) )
    assert(
        sum(map(
            lambda x: x**2,
            squares
        )) == number
    )

#===========================================================
#   main
#===========================================================

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
    remaining, factorization = factor_trivial(number)
    for d in factorization.keys():
        assert( is_prime(d) )
    assert( number_from_factorization(factorization) == number // remaining )

#-----------------------------

@given(*coordinates(4, 2, 5))
def test_factor_nontrivial(a, b, c, d):
    number = build_composite(a, b, c, d)
    factorization = factor_nontrivial(number)
    for d in factorization.keys():
        assert( is_prime(d) )
    assert( number_from_factorization(factorization) == number )

#-----------------------------

@given(st.integers(min_value=2, max_value=10**15))
def test_factor(number):
    factorization = factor(number)
    for d in factorization.keys():
        assert( is_prime(d) )
    assert( number_from_factorization(factorization) == number )

#-----------------------------

@given(st.integers(min_value=2, max_value=10**12))
def test_square_and_square_free_parts(number):
    factorization = factor(number)
    square = square_part(factorization)
    square_free = square_free_part(factorization)
    square_number = number_from_factorization(square)
    square_free_number = number_from_factorization(square_free)
    if square != dict():
        assert( set(map(lambda v: v % 2, square.values())) == set([0]) )
    if square_free != dict():
        assert( set(square_free.values()) == set([1]) )
    assert( _combine_counters(square, square_free) == factorization )
    assert( is_square(square_number) )
    assert( square_number * square_free_number == number )

#-----------------------------

@given(st.integers(min_value=2, max_value=10**12))
def test_divisors(number):
    all_divisors = divisors(number)
    for i in range(len(all_divisors) // 2):
        assert( all_divisors[i] * all_divisors[-i-1] == number )

#===========================================================
#   two_squares
#===========================================================

@given(st.integers(min_value=5))
def test_gaussian_divisor(number):
    prime = next_prime(number)
    if prime % 4 == 1:
        g = gaussian_divisor(prime)
        assert( g.norm == prime )
        assert( GaussianInteger(prime, 0) % g == GaussianInteger(0, 0) )

#-----------------------------

@given(st.integers(min_value=2, max_value=10**4))
def test_two_squares(number):
    factorization = factor(number)
    squares = two_squares_from_factorization(factorization)
    if is_sum_of_two_squares(factorization):
        assert( sorted(squares, reverse=True) == list(squares) )
        assert(
            sum(map(
                lambda x: x**2,
                squares
            )) == number
        )
    else:
        assert( squares is None )

