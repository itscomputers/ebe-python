#   numth/tests/primality_test.py
#===========================================================
from hypothesis import given, assume, strategies as st
from random import sample

from ..basic import gcd, is_prime__naive, prime_sieve
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

#=============================

@given(st.integers(min_value=-1))
def test_next_prime(number):
    p = next_prime(number)
    assert( is_prime(p) )
    for x in range(number+1, p):
        assert( not is_prime(x) )

#-----------------------------

@given(
    st.integers(min_value=-1, max_value=10**5),
    st.integers(min_value=1, max_value=30)
)
def test_next_primes(number, number_of_primes):
    primes = next_primes(number, number_of_primes) 
    assert( len(primes) == number_of_primes )
    for i in range(len(primes) - 1):
        assert( is_prime(primes[i]) )
        for x in range(primes[i] + 1, primes[i+1]):
            assert( not is_prime(x) )

#-----------------------------

@given(
    st.integers(min_value=-1, max_value=10**4),
    st.integers(min_value=1, max_value=10**4)
)
def test_primes_in_range(lower_bound, difference):
    upper_bound = lower_bound + difference
    primes = primes_in_range(lower_bound, upper_bound)
    if primes != []:
        assert( primes[0] >= lower_bound )
        assert( primes[-1] < upper_bound )
    for p in primes:
        assert( is_prime(p) )

#=============================

@given(st.integers(min_value=-1, max_value=10**4))
def test_prev_primes_gen(number):
    g = prev_prime_gen(number)
    primes = []
    while True:
        try:
            primes = primes + [next(g)]
        except StopIteration:
            break
    assert( list(reversed(primes)) == primes_in_range(1, number) )

#-----------------------------

def test_prev_prime_small():
    assert( prev_prime(5) == prev_prime(4) == 3 )
    assert( prev_prime(3) == 2 )
    assert( prev_prime(2) == prev_prime(1) == prev_prime(0) == None )

#-----------------------------

@given(st.integers(max_value=-1))
def test_prev_prime_neg(number):
    assert( prev_prime(number) is None )

#-----------------------------

@given(st.integers(min_value=6, max_value=10**4))
def test_prev_prime(number):
    p = prev_prime(number)
    assert( is_prime(p) )
    for x in range(p+1, number):
        assert( not is_prime(x) )

#=============================

@given(st.integers(min_value=-1, max_value=10**10))
def test_next_twin_primes(number):
    p, q = next_twin_primes(number)
    assert( is_prime(p) )
    assert( is_prime(q) )
    assert( q == p + 2 )
    for i in range(number + 1 - number % 2, p, 2):
        assert( not is_prime(i) or not is_prime(i+2) )

#=============================

@given(st.integers(min_value=6, max_value=10**10))
def test_goldbach_conjecture(number):
    partition = weak_goldbach_partition(number)
    assert( list(partition) == sorted(partition, reverse=True) )
    for p in partition:
        assert( is_prime(p) )
    assert( sum(partition) == number )
    if number % 2 == 0:
        assert( len(partition) == 2 )
    else:
        assert( len(partition) == 3 )

#-----------------------------

def test_goldbach_conjecture_small():
    assert( weak_goldbach_partition(4) == (2, 2) )
    assert( weak_goldbach_partition(5) == (3, 2) )

    
