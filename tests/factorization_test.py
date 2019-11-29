#   tests/factorization_test.py
#===========================================================
from functools import reduce
from hypothesis import given, strategies as st

import env
from lib.basic import is_square
from lib.primality import is_prime, next_prime
from lib.types import GaussianInteger, Quaternion
from lib.factorization.algorithms import *
from lib.factorization.main import *
from lib.factorization.main import _combine_counters
from lib.factorization.two_squares import *
from lib.factorization.four_squares import *
#===========================================================

@st.composite
def composite(draw, num_factors, min_value, max_value):
    return reduce(
        lambda x, h: x * next_prime(
            draw(st.integers(min_value=min_value, max_value=max_value))
        ),
        range(num_factors),
        1
    )

#===========================================================
#   algorithms
#===========================================================

@given(st.integers(min_value=2, max_value=10**12))
def test_pollard_rho(number):
    if not is_prime(number):
        d = pollard_rho(number, 2, lambda x: x**2 + 1)
        assert d > 1 and number % d == 0

#-----------------------------

@given(st.integers(min_value=2, max_value=10**10))
def test_pollard_p_minus_one(number):
    if not is_prime(number):
        d = pollard_p_minus_one(number, 2)
        assert d > 1 and number % d == 0

#-----------------------------

@given(st.integers(min_value=2, max_value=10**8))
def test_williams_p_plus_one(number):
    if not is_prime(number):
        d = williams_p_plus_one(number, GaussianInteger(1, 2))
        assert d > 1 and number % d == 0

#===========================================================
#   main
#===========================================================

@given(composite(4, 10**2, 10**5))
def test_find_divisor(number):
    divisors = find_divisor(number)
    for d in divisors:
        assert 1 < d < number
        assert number % d == 0

#-----------------------------

@given(composite(4, 1, 10**5))
def test_factor_trivial(number):
    remaining, factorization = factor_trivial(number)
    for d in factorization.keys():
        assert is_prime(d)
    assert number_from_factorization(factorization) == number // remaining

#-----------------------------

@given(composite(4, 10**2, 10**5))
def test_factor_nontrivial(number):
    factorization = factor_nontrivial(number)
    for d in factorization.keys():
        assert is_prime(d)
    assert number_from_factorization(factorization) == number

#-----------------------------

@given(st.integers(min_value=2, max_value=10**15))
def test_factor(number):
    factorization = factor(number)
    for d in factorization.keys():
        assert is_prime(d)
    assert number_from_factorization(factorization) == number

#-----------------------------

@given(st.integers(min_value=2, max_value=10**12))
def test_square_and_square_free(number):
    factorization = factor(number)
    square, square_free = square_and_square_free(factorization)
    square_number = number_from_factorization(square)
    square_free_number = number_from_factorization(square_free)
    if square != dict():
        assert set(map(lambda v: v % 2, square.values())) == set([0])
    if square_free != dict():
        assert set(square_free.values()) == set([1])
    assert _combine_counters(square, square_free) == factorization
    assert is_square(square_number)
    assert square_number * square_free_number == number

#-----------------------------

@given(st.integers(min_value=2, max_value=10**12))
def test_divisors(number):
    all_divisors = divisors(number)
    assert all_divisors == divisors(factor(number))
    for i in range(len(all_divisors) // 2):
        assert all_divisors[i] * all_divisors[-i-1] == number

#===========================================================
#   two_squares
#===========================================================

@given(st.integers(min_value=5))
def test_gaussian_divisor(number):
    prime = next_prime(number)
    if prime % 4 == 1:
        g = gaussian_divisor(prime)
        assert g.norm == prime
        assert GaussianInteger(prime, 0) % g == GaussianInteger(0, 0)

#-----------------------------

@given(st.integers(min_value=2, max_value=10**4))
def test_two_squares(number):
    factorization = factor(number)
    squares = two_squares(factorization)
    assert squares == two_squares(number)
    if is_sum_of_two_squares(factorization):
        assert sorted(squares, reverse=True) == list(squares)
        assert sum(map(lambda x: x**2, squares)) == number
    else:
        assert squares is None

#===========================================================
#   four_squares
#===========================================================

@given(st.integers(min_value=2))
def test_quaternion_divisor(number):
    prime = next_prime(number)
    q = quaternion_divisor(prime)
    assert q.norm == prime
    assert Quaternion(prime, 0, 0, 0) % q == Quaternion(0, 0, 0, 0)

#-----------------------------

@given(st.integers(min_value=2, max_value=10**4))
def test_four_squares(number):
    factorization = factor(number)
    squares = four_squares(factorization)
    assert squares == four_squares(number)
    assert sorted(squares, reverse=True) == list(squares)
    assert sum(map(lambda x: x**2, squares)) == number

