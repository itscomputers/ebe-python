#   numth/tests/primality_test.py
#===========================================================
from hypothesis import given, assume, strategies as st

from ..basic import is_prime__naive, prime_sieve
from ..primality_miller_rabin import miller_rabin_test
from ..primality_lucas import lucas_test
from ..primality import *
#===========================================================

def test_is_prime_on_sieve():
    primes = prime_sieve(10**4)
    for p in primes:
        assert( is_prime(p) )
    
    non_primes = set(range(10**4)) - set(primes)
    for p in non_primes:
        assert( not is_prime(p) )

#-----------------------------

@given(st.integers(min_value=3))
def test_integration_of_miller_rabin_and_lucas(number):
    number += 1 - number % 2
    number_is_prime = is_prime(number)
    mr_primality = miller_rabin_test(number, 20)
    l_primality = lucas_test(number, 20)
    if 'composite' in [mr_primality, l_primality]:
        assert( not number_is_prime )
    else:
        assert( number_is_prime )

#-----------------------------

@given(st.integers(min_value=2, max_value=10**7))
def test_is_prime(number):
    assert( is_prime(number) == is_prime__naive(number) )

