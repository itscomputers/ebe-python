#   tests/sums_of_squares_test.py
#===========================================================
from hypothesis import given, assume, strategies as st

from ..factorization import factor
from ..primality import next_prime
from ..quadratic import Quadratic
from ..sums_of_squares import *
#===========================================================

@given(st.integers(min_value=5))
def test_gaussian_divisor(number):
    prime = next_prime(number)
    if prime % 4 == 1:
        g = gaussian_divisor(prime)
        assert( g.norm() == prime )
        assert( Quadratic(prime, 0, -1) % g == Quadratic(0, 0, -1) )

#=============================

@given(st.integers(min_value=2, max_value=10**4))
def test_two_squares(number):
    factorization = factor(number)
    if is_sum_of_two_squares(factorization):
        assert(
            sum(map(
                lambda x: x**2,
                two_squares_from_factorization(factorization)
            )) == number
        )
    else:
        assert( two_squares_from_factorization(factorization) is None )

#=============================

@given(st.integers(min_value=2))
def test_quaternion_divisor(number):
    prime = next_prime(number)
    q = quaternion_divisor(prime)
    assert( q.norm() == prime )
    assert( Quaternion(prime, 0, 0, 0) % q == Quaternion(0, 0, 0, 0) )
