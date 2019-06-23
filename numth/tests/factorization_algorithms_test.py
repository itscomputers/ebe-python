#   numth/tests/factorization_algorithms_test.py
#===========================================================
from random import randint
from hypothesis import assume, example, given, strategies as st

from ..quadratic import Quadratic
from ..primality import is_prime
from ..factorization_algorithms import *
#===========================================================

@given(st.integers(min_value=2, max_value=10**12))
def test_pollard_rho(number):
    if not is_prime(number):
        d = pollard_rho(number, 2, lambda x: x**2 + 1)
        assert( d > 1 and number % d == 0 )

#=============================

@given(st.integers(min_value=2, max_value=10**12))
def test_pollard_p_minus_one(number):
    if not is_prime(number):
        d = pollard_p_minus_one(number, 2)
        assert( d > 1 and number % d == 0 )
        
#=============================

@given(st.integers(min_value=2, max_value=10**12))
def test_williams_p_plus_one(number):
    if not is_prime(number):
        d = williams_p_plus_one(number, Quadratic(1, 1, -1))
        assert( d > 1 and number % d == 0 )

